Module PySense.PySenseElasticube
================================

Classes
-------

`Elasticube(host, token, cube_json)`
:   

    ### Methods

    `add_default_rule(self, server_address, table_name, column_name, data_type, security_values=[])`
    :   Add a rule for the default group
        :param server_address: The server address of the ElastiCube. Use 'Set' for Elasticube Set.
        :param table_name: Table to apply data security to
        :param column_name: Column to apply data security to
        :param data_type: The data type
        :param security_values: Default security values. Leave out for "Nothing." (Recommended)
        :return:

    `add_security_rule(self, server_address, shares, table, column, data_type, members, *, exclusionary=False, all_members=None)`
    :   Defines data security rules for a column on a specific server and elasticube
        
        :param shares: The users or groups to assign the security rule to
        :param server_address: The server address of the ElastiCube. Use 'Set' for Elasticube Set.
        :param table: The table to apply security on
        :param column: The column to apply security on
        :param data_type: The data type of the column
        :param members: An array of values which users should have access to
        :param exclusionary: True if exclusionary rule
        :param all_members: True if all members to be selectable
        :return:

    `delete_rule(self, server_address, table, column)`
    :   Delete data security rule for a column
        :param server_address: The server address of the ElastiCube.
        :param table: The name of the table in the ElastiCube
        :param column: The name of the column in the ElastiCube
        :return: True

    `get_data_source_sql(self, server_address, query, file_type, *, path=None, offset=None, count=None, include_metadata=None, is_masked_response=None)`
    :   Executes elasticube sql. This is a non public API. This functionality is beta
        Seems to only work on localhost
        
        :param path: The location to save the file
        :param server_address: The server address of the ElastiCube.
        :param query: The query to execute
        :param file_type: File format to return
        :param offset: Defines how many items to skip before returning the results.
            For example, to return results from value #101 onward, enter a value of ‘100’.
        :param count: Limits the result set to a defined number of results. Enter 0 (zero) or leave blank not to limit.
        :param include_metadata: Whether to include metadata.
        :param is_masked_response: Whether response should be masked.
        :return: The path of the created file or the content payload if path is None

    `get_elasticube_datasecurity(self, server_address)`
    :   Return data security rules for the elasticube
        :return: The data security rules for the elasticube

    `get_elasticube_datasecurity_by_table_column(self, server_address, table, column)`
    :   Returns ElastiCube data security rules for a column in a table in the ElastiCube
        :param server_address: The server address of the ElastiCube.
        :param table: The name of the table in the ElastiCube
        :param column: The name of the column in the ElastiCube
        :return:

    `get_elasticube_oid(self)`
    :

    `get_model(self)`
    :

    `get_name(self)`
    :