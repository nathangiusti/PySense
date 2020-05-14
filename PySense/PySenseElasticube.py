import random
import urllib.parse

from PySense import SisenseVersion
from PySense import PySenseDataModel
from PySense import PySenseException
from PySense import PySenseGroup
from PySense import PySenseRule
from PySense import PySenseUser
from PySense import PySenseUtils
from PySense import PySenseFormula


class Elasticube:

    def __init__(self, py_client, cube_json):
        self._cube_json = cube_json
        self._py_client = py_client
        self._server_address = 'localhost'
        if py_client.version == SisenseVersion.Version.WINDOWS:
            metadata = self.get_metadata() 
            if metadata is None:
                print('No meta data for cube {}'.format(self.get_name()))
                self._server_address = metadata['address']
        
    def get_oid(self):
        """Returns the datamodel id"""
        return self._cube_json['oid']

    def get_model(self, path=None):
        """Returns the ElastiCube model as a json blob.    
          
        Optional:
            - path: The file location to save the ElastiCube to      
          
        Returns:
            A json blob or the file path if the file path is set.      
        """
        if self._py_client.version == SisenseVersion.Version.WINDOWS:
            return self._get_model_windows(path=path)
        elif self._py_client.version == SisenseVersion.Version.LINUX:
            return self._get_model_linux(path=path)
    
    def _get_model_linux(self, path=None):
        
        query_params = {'datamodelId': self.get_oid(), 'type': 'schema-latest'}
        if path is not None:
            resp_content = self._py_client.connector.rest_call('get', 'api/v2/datamodel-exports/schema', 
                                                               query_params=query_params, raw=True)
            with open(path, 'wb') as out_file:
                out_file.write(resp_content)
            return path
        else:
            data_model_json = self._py_client.connector.rest_call(
                'get', 'api/v2/datamodel-exports/schema', query_params=query_params)
            return PySenseDataModel.DataModel(self._py_client, data_model_json)                                            
        
    def _get_model_windows(self, path=None):
        query_params = {'cachebuster': random.randrange(1000000000000, 9999999999999)}
        if path is not None:
            resp_content = self._py_client.connector.rest_call(
                'get', 'api/v1/elasticubes/{}/datamodel-exports/stream/schema'.format(self.get_elasticube_oid()),
                query_params=query_params, raw=True)

            with open(path, 'wb') as out_file:
                out_file.write(resp_content)
            return path
        else:
            data_model_json = self._py_client.connector.rest_call(
                'get', 'api/v1/elasticubes/{}/datamodel-exports/stream/schema'
                .format(self.get_elasticube_oid()), query_params=query_params)
            return PySenseDataModel.DataModel(self._py_client, data_model_json)    
        
    def get_name(self, url_encoded=False):
        """Returns the ElastiCube's name.    
          
        Optional:
            - url_encoded: True to url encode the name. Use for passing as query parameter.      
          
        Returns:
             The name of the ElastiCube, url encoded if set.     
        """
        if url_encoded:
            return urllib.parse.quote(self._cube_json['title'])
        else:
            return self._cube_json['title']

    def run_sql(self, query, file_type, *, path=None, server_address=None,
                offset=None, count=None, include_metadata=None, is_masked_response=None):
        """Executes ElastiCube sql.   

        Args:
            - query: The query to execute   
            - file_type: File format to return    
        
        Optional:
            - path: The location to save the file   
            - server_address: The server address of the ElastiCube.   
                Set this to your server ip if this method fails without it set.  
            - offset: Defines how many items to skip before returning the results.   
                For example, to return results from value #101 onward, enter a value of ‘100’.  
            - count: Limits the result set to a defined number of results. Enter 0 (zero) or leave blank not to limit.  
            - include_metadata: Whether to include metadata.  
            - is_masked_response: Whether response should be masked.  
        
        Returns:
             The path of the created file or the content payload if path is None  
        """
        server_address = server_address if server_address else self._server_address
        
        query = urllib.parse.quote(query)

        query_params = {
            'query': query,
            'format': file_type,
            'offset': offset,
            'count': count,
            'includeMetadata': include_metadata,
            'isMaskedResponse': is_masked_response
        }
        resp_content = self._py_client.connector.rest_call('get', 'api/datasources/{}/{}/sql'
                                                           .format(server_address, self.get_name(url_encoded=True)),
                                                           query_params=query_params, raw=True)
        output = resp_content.decode('utf-8-sig').splitlines()
        if path is not None:
            with open(path, "w") as file:
                for line in output:
                    file.write(line + '\n')
            return path
        else:
            return resp_content

    def add_security_rule(self, table, column, data_type, *, shares=None, members=[], 
                          server_address=None, exclusionary=False, all_members=None, ):
        """Defines data security rules for a column on a specific server and ElastiCube   
  
        Args:
            - table: The table to apply security on  
            - column: The column to apply security on  
            - data_type: The data type of the column  
        
        Optional:
            - shares: The users or groups to assign the security rule to. If none, will be default rule.  
            - members: An array of values which users should have access to  
                If left blank, user will get none.  
            - server_address: The server address of the ElastiCube.  
                Set this to your server ip if this method fails without it set.  
                Use 'Set' for Elasticube Set. Required for elasticube sets.   
            - exclusionary: True if exclusionary rule    
            - all_members: True if all members to be selectable   
        
        Returns:
             The new security rule    
        """  
        server_address = server_address if server_address else self._server_address
        
        rule_json = [{
                        "column": column,
                        "datatype": data_type,
                        "table": table,
                        "elasticube": self.get_name(),
                        "server": server_address,
                        "exclusionary": exclusionary,
                        "allMembers": all_members
                    }]

        shares_json = []
        if shares is None:
            # Default rule
            rule_json[0]['shares'] = [{"type": "default"}]
        else:
            for party in PySenseUtils.make_iterable(shares):
                if isinstance(party, PySenseUser.User):
                    shares_json.append({'party': party.get_id(), 'type': 'user'})
                elif isinstance(party, PySenseGroup.Group):
                    shares_json.append({'party': party.get_id(), 'type': 'group'})
                else:
                    raise PySenseException.PySenseException('{} is not a user or a group object'.format(party))
            rule_json[0]['shares'] = shares_json

        member_arr = []
        for member in members:
            member_arr.append(str(member))
        rule_json[0]['members'] = member_arr

        resp_json = self._py_client.connector.rest_call('post', 'api/elasticubes/{}/{}/datasecurity'
                                                        .format(server_address, self.get_name(url_encoded=True)),
                                                        json_payload=rule_json)

        return PySenseRule.Rule(self._py_client, resp_json[0])

    def get_datasecurity(self, *, server_address=None):
        """Return data security rules for the ElastiCube.     
          
        Optional:
            - server_address: The server address of the ElastiCube.  
                Set this to your server ip if this method fails without it set.  
                Use 'Set' for Elasticube Set. Required for elasticube sets.   
          
        Returns:
            The data security rules for the ElastiCube   
        """
        server_address = server_address if server_address else self._server_address
        
        resp_json = self._py_client.connector.rest_call('get', 'api/elasticubes/{}/{}/datasecurity'
                                                        .format(server_address, self.get_name(url_encoded=True)))
        ret_arr = []
        for rule in resp_json:
            ret_arr.append(PySenseRule.Rule(self._py_client, rule))
        return ret_arr

    def get_datasecurity_by_table_column(self, table, column, *, server_address=None):
        """Returns ElastiCube data security rules for a column in a table in the ElastiCube.  
          
        Args:
            - table: The name of the table in the ElastiCube  
            - column: The name of the column in the ElastiCube  
          
        Optional:
            - server_address: The server address of the ElastiCube.  
                Set this to your server ip if this method fails without it set.  
                Use 'Set' for Elasticube Set. Required for elasticube sets.   
            
        Returns:
            An array of security rules.    
        """

        server_address = server_address if server_address else self._server_address
        
        table = urllib.parse.quote(table)
        column = urllib.parse.quote(column)
        resp_json = self._py_client.connector.rest_call('get', 'api/elasticubes/{}/{}/datasecurity/{}/{}'
                                                        .format(server_address, self.get_name(url_encoded=True), 
                                                                table, column))
        ret_arr = []
        for rule in resp_json:
            ret_arr.append(PySenseRule.Rule(self._py_client, rule))
        return ret_arr

    def get_security_for_user(self, user, *, server_address=None):
        """Returns an array of rules for the user on this cube
        
        Args:
            - user: The user id, username, or user obect    
        
        Optional:
            - server_address: The server address of the ElastiCube.    
                Set this to your server ip if this method fails without it set.    
             
        Returns:
            An array of PySense Rules      
        """

        server_address = server_address if server_address else self._server_address
        
        if isinstance(user, PySenseUser.User):
            user_id = user.get_id()
        else:
            user_id = urllib.parse.quote(user)
        resp_json = self._py_client.connector.rest_call('get', 'api/elasticubes/{}/{}/{}/datasecurity'
                                                        .format(server_address, self.get_name(url_encoded=True), user_id))
        ret_arr = []
        for rule in resp_json:
            ret_arr.append(PySenseRule.Rule(self._py_client, rule))
        return ret_arr
        
    def delete_rule(self, table, column, *, server_address=None):
        """Delete data security rule for a column.  
          
        Args:
            - table: The name of the table in the ElastiCube  
            - column: The name of the column in the ElastiCube  
            
        Optional:
            - server_address: The server address of the ElastiCube.  
                Set this to your server ip if this method fails without it set.  
                Use 'Set' for Elasticube Set. Required for elasticube sets.    
        """
        server_address = server_address if server_address else self._server_address
        
        query_params = {
            'table': table,
            'column': column
        }
        self._py_client.connector.rest_call('delete', 'api/elasticubes/{}/{}/datasecurity'
                                            .format(server_address, self.get_name(url_encoded=True)),
                                            query_params=query_params)

    def get_elasticube_oid(self):
        """Get's the elasticube's oid"""
        return self._cube_json['oid']

    def get_saved_formulas(self, *, server_address=None):
        """Get elasticube formulas.  
          
        Optional:
            - server_address: The server address of the ElastiCube.  
                Set this to your server ip if this method fails without it set.     
              
        Returns:
             An array of formulas     
        """
        server_address = server_address if server_address else self._server_address
        query_params = {
            'datasource': self.get_name(url_encoded=True),
            'server': server_address
        }
        resp_json = self._py_client.connector.rest_call('get', 'api/metadata/measures', query_params=query_params)
        ret_arr = []
        for formula in resp_json:
            ret_arr.append(PySenseFormula.Formula(self._py_client, formula))
        
        return ret_arr

    def delete_formulas(self, formulas):
        """Delete given formulas from ElastiCube"""
        
        for formula in PySenseUtils.make_iterable(formulas):
            self._py_client.connector.rest_call('delete', 'api/metadata/{}'.format(formula.get_oid()))
    
    def get_metadata(self):
        """Get ElastiCube metadata"""
        resp_json = self._py_client.connector.rest_call('get', 'api/elasticubes/metadata/{}'
                                                        .format(self.get_name(url_encoded=True)))
        if resp_json is None:
            # If we don't get a response, it means the cube was never built so we return defaults
            return {
                "title": "",
                "fullname": "",
                "id": "",
                "address": "",
                "database": ""
            }
        return resp_json
            
    def add_formula_to_cube(self, formulas):
        """Add formulas to cube"""
        for formula in PySenseUtils.make_iterable(formulas):
            formula.change_datasource(self)
            elements_to_remove = ['_id', 'created', 'lastUpdated', 'oid']
            formula_json = formula.get_json()
            for element in elements_to_remove:
                formula_json.pop(element, None) 
            self._py_client.connector.rest_call('post', 'api/metadata', json_payload=formula_json)

