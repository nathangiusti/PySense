# ------------------------------------Imports------------------------------------
import csv
from PySense import PySense
# -------------------------------------------------------------------------------

# -----------------------------------Variables-----------------------------------
login_username = 'login@email.com'
login_password = 'password'
server = 'LocalHost:8081'
csv_file_name = 'Security.csv'


if __name__ == '__main__':
    py_client = PySense.PySense(server, login_username, login_password)
    with open(csv_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # skip the headers
        for row in csv_reader:
            security_type = row[0]
            security_name = row[1]  # either the email or the groupName
            elasticube_name = row[2]
            table = row[3]
            column = row[4]
            security_values = row[5].split(',')

            if security_type == 'user':
                user_array = py_client.get_users(email=security_name)
                if len(user_array) == 0:
                    user = py_client.add_user(security_name, security_name, 'Viewer')
                    print('User {} created'.format(user.get_user_user_name()))
                    share_obj = [user]
                else:
                    share_obj = user_array
            elif security_type == 'group':
                groups_array = py_client.get_groups(name=security_name)
                if len(groups_array) == 0:
                    print('Group {} not found'.format(security_name))
                    share_obj = None
                else:
                    share_obj = groups_array
                print('Group ' + security_name + ' was successfully looked up.')
            elasticube = py_client.get_elasticube_by_name(elasticube_name)
            rules_array = elasticube.get_elasticube_datasecurity_by_table_column(table, column)
            if len(rules_array) == 0:
                elasticube.add_default_rule(table, column, 'numeric')
            if share_obj is not None:
                if 'Everything' in security_values:
                    elasticube.add_security_rule(share_obj, table, column, 'numeric', [],
                                                 all_members=True)
                else:
                    elasticube.add_security_rule(share_obj, table, column, 'numeric', security_values)
