"""
This is a rewritten version of the backup dashboards script at https://github.com/nathangiusti/Sisense/tree/master/BackupDashboards that uses the PySense Library. 
"""

from PIL import Image
import yaml
import sys
import PySense

RETRY = 3
ERROR_DASHES = []


def build_path(folder, dashboard_id, file_format, file_num=None):
    """
    Builds the path to save the export to

    :param folder: Folder to save dashboard to
    :param dashboard_id: Id of dashboard
    :param file_format: Format to save dashboard to
    :param file_num: A number to place after the file name in case multiple images from the same dash are taken
    :return: A string in the format <path>/dashboard_id.file_format
    """
    if file_num:
        return "{}\\{}-{}.{}".format(folder, dashboard_id, file_num, file_format)
    else:
        return "{}\\{}.{}".format(folder, dashboard_id, file_format)


def build_query_string(query_parameters):
    """
    Turns a dictionary of query parameters into a query string
    :param query_parameters: a dictionary of query parameters
    :return: The query_parameters dictionary flattened into a string
    """

    query_string = ''
    if not query_parameters:
        return query_string
    for param in query_parameters:
        if isinstance(query_parameters[param], bool):
            val = str(query_parameters[param]).lower()
        else:
            val = query_parameters[param]
        query_string += '{}={}&'.format(param, val)
    if not query_string:
        return ''
    else:
        return query_string[:-1]


def create_cropping_list(cropping_string):
    coord_list = []
    for coord_str in cropping_string:
        if len(coord_str.split(',')) != 5:
            print("Invalid coordinate string {}. Requires 5 integers.".format(cropping_string))
            continue
        for coord in coord_str.split(','):
            coord_list.append(int(coord))
    return coord_list


def export_png(format_vars, dashboard, file_folder, cropping):
    """
    Exports dashboard to png

    :param format_vars: Dictionary from YAML containing format variables
    :param dashboard: The dashboard id
    :param file_folder: Folder to export dashboard to
    :param cropping: The cropping yaml section
    :return: Nothing
    """
    if cropping and dashboard in cropping:
        i = 0
        for coord_str in cropping[dashboard]:
            i += 1
            coord_arr = coord_str.split(',')
            if len(coord_arr) == 5:
                file_path = build_path(file_folder, dashboard, format_vars['file_type'], i)
                png_file = PySense.get_dashboard_export_png(dashboard, file_path, format_vars['query_params'])
                image_obj = Image.open(png_file)
                x1 = int(coord_arr[0])
                y1 = int(coord_arr[1])
                x2 = int(coord_arr[2])
                y2 = int(coord_arr[3])
                width = int(coord_arr[4])
                cropped_image = image_obj.crop((x1, y1, x2, y2))
                scaling_ratio = width / (x2 - x1)
                y_coord = scaling_ratio * (y2 - y1)
                resized_image = cropped_image.resize((width, int(y_coord)))
                file_path = build_path(file_folder, dashboard, format_vars['file_type'], i)
                print('Cropped image to {} by {}'.format(width, int(y_coord)))
                resized_image.save(file_path)
                print("Image saved to {}".format(file_path))
            elif len(coord_arr) == 3:
                width = int(coord_arr[1])
                height = int(coord_arr[2])
                widget_format = {'file_type': 'png', 'query_params': {'width': width, 'height': height}}
                PySense.post_dashboard_widget_export_png(dashboard,
                                                         coord_arr[0],
                                                         build_path(file_folder, dashboard, format_vars['file_type']),
                                                         widget_format['query_params'])
    else:
        return PySense.get_dashboard_export_png(dashboard,
                                                build_path(file_folder, dashboard, format_vars['file_type']),
                                                param_dict=format_vars['query_params'])


def main():
    if sys.argv[1] is None:
        print("No config file supplied")
        exit()

    config = sys.argv[1]

    with open(config, 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    host = data_loaded['host']
    PySense.authenticate(host, data_loaded['authentication']['username'], data_loaded['authentication']['password'])
    global_vars = data_loaded['globals']
    format_vars = global_vars['format']
    file_folder = global_vars['folder']
    cropping = data_loaded['cropping'] if 'cropping' in data_loaded else None

    dashboard_id_list = []
    if 'query_params' in data_loaded['dashboards']:
        dashboard_id_list = PySense.get_dashboards(param_dict=data_loaded['dashboards']['query_params'])

    if 'ids' in data_loaded['dashboards']:
        for dashboard in data_loaded['dashboards']['ids']:
            if dashboard not in dashboard_id_list:
                dashboard_id_list.append(dashboard)

    print('Backing up {} dashboards'.format(len(dashboard_id_list)))
    for dashboard in dashboard_id_list:
        if format_vars['file_type'] == 'png':
            export_png(format_vars, dashboard, file_folder, cropping)
        elif format_vars['file_type'] == 'pdf':
            query_params = format_vars['query_params']
            PySense.get_dashboard_export_pdf(dashboard, file_folder + dashboard + '.pdf', query_params['paperFormat'],
                                             query_params['paperOrientation'], query_params['layout'])
        elif format_vars['file_type'] == 'dash':
            PySense.get_dashboard_export_dash(dashboard, file_folder + dashboard + '.dash')

    print('Backups complete')
    if len(ERROR_DASHES) > 0:
        print("Following calls failed:")
        for dash in ERROR_DASHES:
            print(dash)


main()
