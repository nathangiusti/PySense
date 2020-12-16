from PySense import PySenseAuthentication, PySenseException, PySenseRestConnector, SisenseRole, SisenseVersion

from PySense.PySenseMixIns import BrandingMixIn, ConnectionMixIn, DashboardMixIn, DataModelMixIn, ElasticubeMixIn, \
    FolderMixIn, GroupMixIn, RoleMixIn, SettingsMixIn, PluginMixIn, UserMixIn


def authenticate_by_token(host, token, version, debug=False, verify=True):
    """Creates a new PySense client with the token

    Args:
        host (str): The Sisense server address
        token (str): A Sisense user token
        version (str): 'Windows' or 'Linux'
        debug (bool): (Optional) True to enable debugging. False by default.
        verify (bool): (Optional) False to disable SSL certificate verification. True by default.


    Returns:
        PySense: A new PySense client for the given credentials
    """

    return PySenseAuthentication.authenticate_by_token(host, token, version, debug, verify)


def authenticate_by_password(host, username, password, version, debug=False, verify=True):
    """Creates a new PySense client with the username and password

    Args:
        host (str): The Sisense server address
        username (str): Sisense username
        password (str): Sisense password
        version (str): 'Windows' or 'Linux'
        debug (bool): (Optional) True to enable debugging. False by default.
        verify (bool): (Optional) False to disable SSL certificate verification. True by default.


    Returns:
        PySense: A new PySense client for the given credentials
    """

    return PySenseAuthentication.authenticate_by_password(host, username, password, version, debug, verify)


def authenticate_by_file(config_file):
    """Creates a new PySense client with the credentials in the given config file.

    py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')

    See sample config in Snippets/SampleConfig.yaml

    Args:
        config_file (str): Yaml file with credentials

    Returns:
        PySense: A new PySense client for the given credentials
    """

    return PySenseAuthentication.authenticate_by_file(config_file)


def authenticate_custom_connector(version, connector):
    """ Use a custom connector

    Authenticate by setting up your own custom connector.

    Args:
        version (str): 'Windows' or 'Linux'
        connector (RestConnector): The custom connector

    Returns:
        PySense: A new PySense client for the given credentials
    """

    return PySense(None, None, version, connector=connector)


class PySense(BrandingMixIn.BrandingMixIn, ConnectionMixIn.ConnectionMixIn, DashboardMixIn.DashboardMixIn,
              DataModelMixIn.DataModelMixIn, ElasticubeMixIn.ElasticubeMixIn, FolderMixIn.FolderMixIn,
              GroupMixIn.GroupMixIn, PluginMixIn.PluginMixIn, RoleMixIn.RoleMixIn, SettingsMixIn.SettingsMixIn,
              UserMixIn.UserMixIn):

    """The manager of connections to the PySense server

    This class is for sever level changes like getting, adding, and removing dashboards, elasticubes, users, etc

    Attributes:
        connector (RestConnector): The connection to the Sisense Server
        param_dict (dict): Key value store for various configuration options
        version (SisenseVersion): Track whether we are connecting to Windows or Linux Sisense
        roles (dict[SisenseRole,str]): An array of SienseRoles and their role_ids
    """

    def __init__(self, host, token, version, *, debug=False, verify=True, param_dict=None, connector=None):
        """ Initializes a PySense instance

        Args:
            host (str): host address
            token (json): a json bearer token with format
                {'authorization':  "Bearer yourlongaccesstokenstringthatyougotfromapreviouslogin"}
            version (str): version (either 'Windows' or 'Linux')
            debug (bool): (Optional) If true, prints detailed REST API logs to console. False by default.
            verify (bool): (Optional) If false, disables SSL Certification. True by default.
            param_dict (dict): (Optional) For passing in additional parameters
            connector (RestConnector): (Optional) Pass in your own connector (normally used for mock tests)
        """

        if param_dict is None:
            self.param_dict = {}
        else:
            self.param_dict = {}

        default_dict = {
            'CUBE_CACHE_TIMEOUT_SECONDS': 60
        }

        for key, value in default_dict.items():
            if key not in self.param_dict:
                self.param_dict[key] = value

        # Verify version
        if version.lower() == 'windows':
            self.version = SisenseVersion.Version.WINDOWS
        elif version.lower() == 'linux':
            self.version = SisenseVersion.Version.LINUX
        else:
            raise PySenseException.PySenseException('{} not a valid OS. Please select Linux or Windows'.format(version))

        # Initiate PySense Connection
        if connector is not None:
            self.connector = connector
        else:
            self.connector = PySenseRestConnector.RestConnector(host, token, debug, verify)
            # Set up Roles
            roles = self.connector.rest_call('get', 'api/roles')
            self.roles = {}
            for role in roles:
                if role['name'] in ['dataDesigner', 'super', 'dataAdmin', 'admin', 'contributor', 'consumer']:
                    self.roles[SisenseRole.Role.from_str(role['name'])] = role['_id']

    def get_param(self, param):
        """Get the value in the param dictionary for the given parameter. Returns None if not found"""
        if param in self.param_dict:
            return self.param_dict[param]
        else:
            None

    def set_param(self, param, value):
        """Set the key "param" to the value "value". """
        self.param_dict[param] = value
