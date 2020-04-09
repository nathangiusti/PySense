import json
import random
import requests
import urllib.parse

from PySense import PySenseGroup
from PySense import PySenseRule
from PySense import PySenseUser
from PySense import PySenseUtils
from PySense import PySenseFormula

class Elasticube:

    def __init__(self, host, token, cube_json):
        self._host = host
        self._token = token
        self._cube_json = cube_json
        metadata = self.get_metadata() 
        if metadata is None:
            print("ERROR")
        self._server_address = metadata['address']

    def get_model(self):
        """
        Returns the ElastiCube model as a json blob  
          
        :return: A json blob    
        """
        
        resp = requests.get('{}/api/v1/elasticubes/{}/datamodel-exports/stream/schema?cachebuster={}'.format(
            self._host, self.get_elasticube_oid(), random.randrange(1000000000000, 9999999999999)), headers=self._token)
        PySenseUtils.parse_response(resp)
        return json.loads(resp.content)

    def get_name(self, url_encoded=False):
        """
        Returns the ElastiCube's name  
          
        Optional  
        :param url_encoded: True to url encode the name  
          
        :return: The name of the ElastiCube  
        """
        
        if url_encoded:
            return urllib.parse.quote(self._cube_json['title'])
        else:
            return self._cube_json['title']

    def run_sql(self, query, file_type, *, path=None, server_address=None,
                offset=None, count=None, include_metadata=None, is_masked_response=None):
        """
        Executes ElastiCube sql. This is a non public API.  
    
        :param query: The query to execute   
        :param file_type: File format to return    
        
        Optional:  
        :param path: The location to save the file   
        :param server_address: The server address of the ElastiCube. 
            Set this to your server ip if this method fails without it set.
        :param offset: Defines how many items to skip before returning the results.  
            For example, to return results from value #101 onward, enter a value of ‘100’.  
        :param count: Limits the result set to a defined number of results. Enter 0 (zero) or leave blank not to limit.  
        :param include_metadata: Whether to include metadata.  
        :param is_masked_response: Whether response should be masked.  
        
        :return: The path of the created file or the content payload if path is None  
        """

        server_address = server_address if server_address else self._server_address
        
        query = urllib.parse.quote(query)

        param_string = PySenseUtils.build_query_string({
            'query': query,
            'format': file_type,
            'offset': offset,
            'count': count,
            'includeMetadata': include_metadata,
            'isMaskedResponse': is_masked_response
        })
        resp = requests.get('{}/api/datasources/{}/{}/sql?{}'.format(
            self._host, server_address, self.get_name(url_encoded=True), param_string), headers=self._token)
        PySenseUtils.parse_response(resp)
        output = resp.content.decode('utf-8-sig').splitlines()
        if path is not None:
            with open(path, "w") as file:
                for line in output:
                    file.write(line + '\n')
            return path
        else:
            return output

    def add_security_rule(self, shares, table, column, data_type, members, *, 
                          server_address=None, exclusionary=False, all_members=None, ):
        """
        Defines data security rules for a column on a specific server and ElastiCube   
  
        :param shares: The users or groups to assign the security rule to  
        :param table: The table to apply security on  
        :param column: The column to apply security on  
        :param data_type: The data type of the column  
        :param members: An array of values which users should have access to  
        
        Optional:  
        :param server_address: The server address of the ElastiCube.  
            Set this to your server ip if this method fails without it set.  
            Use 'Set' for Elasticube Set. Required for elasticube sets.   
        :param exclusionary: True if exclusionary rule    
        :param all_members: True if all members to be selectable   
        
        :return: The new security rule  
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
        for party in shares:
            if isinstance(party, PySenseUser.User):
                shares_json.append({'party': party.get_user_id(), 'type': 'user'})
            elif isinstance(party, PySenseGroup.Group):
                shares_json.append({'party': party.get_group_id(), 'type': 'group'})
        rule_json[0]['shares'] = shares_json

        member_arr = []
        for member in members:
            member_arr.append(str(member))
        rule_json[0]['members'] = member_arr

        resp = requests.post('{}/api/elasticubes/{}/{}/datasecurity'.format(
            self._host, server_address, self.get_name(url_encoded=True)), headers=self._token, json=rule_json)
        PySenseUtils.parse_response(resp)

        return PySenseRule.Rule(self._host, self._token, resp.json()[0])

    def add_default_rule(self, table_name, column_name, data_type, security_values=[], *, server_address=None):
        """  
        Add a rule for the default group  
          
        :param table_name: Table to apply data security to  
        :param column_name: Column to apply data security to  
        :param data_type: The data type  
        :param security_values: Default security values. Leave out for "Nothing." (Recommended)  
        
        Optional:
        :param server_address: The server address of the ElastiCube.  
            Set this to your server ip if this method fails without it set.  
            Use 'Set' for Elasticube Set. Required for elasticube sets.   
        
        :return:  The new security rule
        """
        
        server_address = server_address if server_address else self._server_address
        
        if 'Everything' in security_values:
            return self.add_security_rule([{"type": "default"}], table_name, column_name, data_type, [], 
                                          all_members=True, server_address=server_address)
        else:
            return self.add_security_rule([{"type": "default"}], table_name, column_name, data_type, security_values,
                                          server_address=server_address)

    def get_datasecurity(self, *, server_address=None):
        """
        Return data security rules for the ElastiCube   
          
        Optional:  
        :param server_address: The server address of the ElastiCube.  
            Set this to your server ip if this method fails without it set.  
            Use 'Set' for Elasticube Set. Required for elasticube sets.   
          
        :return: The data security rules for the ElastiCube   
        """
        
        server_address = server_address if server_address else self._server_address
        
        resp = requests.get('{}/api/elasticubes/{}/{}/datasecurity'.format(
            self._host, server_address, self.get_name(url_encoded=True)), headers=self._token)
        PySenseUtils.parse_response(resp)
        ret_arr = []
        for rule in resp.json():
            ret_arr.append(PySenseRule.Rule(self._host, self._token, rule))
        return ret_arr

    def get_datasecurity_by_table_column(self, table, column, *, server_address=None):
        """
        Returns ElastiCube data security rules for a column in a table in the ElastiCube  
        
        :param table: The name of the table in the ElastiCube  
        :param column: The name of the column in the ElastiCube  
        
        Optional:
        :param server_address: The server address of the ElastiCube.  
            Set this to your server ip if this method fails without it set.  
            Use 'Set' for Elasticube Set. Required for elasticube sets.   
            
        :return:
        """

        server_address = server_address if server_address else self._server_address
        
        resp = requests.get('{}/api/elasticubes/{}/{}/datasecurity/{}/{}'.format(
            self._host, server_address, self.get_name(url_encoded=True), table, column), headers=self._token)
        PySenseUtils.parse_response(resp)
        ret_arr = []
        for rule in resp.json():
            ret_arr.append(PySenseRule.Rule(self._host, self._token, rule))
        return ret_arr

    def get_security_for_user(self, user, *, server_address=None):
        """
        Returns an array of rules for the user on this cube
        
        :param user: The user id, username, or user obect  
        
        Optional:
        :param server_address: The server address of the ElastiCube.  
            Set this to your server ip if this method fails without it set.  
             
        :return: An array of PySense Rules  
        """

        server_address = server_address if server_address else self._server_address
        
        if isinstance(user, PySenseUser.User):
            user_id = user.get_user_id()
        else:
            user_id = urllib.parse.quote(user)
        resp = requests.get('{}/api/elasticubes/{}/{}/{}/datasecurity'.format(
            self._host, server_address, self.get_name(url_encoded=True), user_id), headers=self._token)
        PySenseUtils.parse_response(resp)
        ret_arr = []
        for rule in resp.json():
            ret_arr.append(PySenseRule.Rule(self._host, self._token, rule))
        return ret_arr
        
        
    def delete_rule(self, table, column, *, server_address=None):
        """
        Delete data security rule for a column  
          
        :param table: The name of the table in the ElastiCube  
        :param column: The name of the column in the ElastiCube  
          
        Optional:  
        :param server_address: The server address of the ElastiCube.  
            Set this to your server ip if this method fails without it set.  
            Use 'Set' for Elasticube Set. Required for elasticube sets.    
       
        """
        
        server_address = server_address if server_address else self._server_address
        
        param_string = PySenseUtils.build_query_string({
            'table': table,
            'column': column
        })
        resp = requests.delete('{}/api/elasticubes/{}/{}/datasecurity?{}'.format(
            self._host, server_address, self.get_name(url_encoded=True), param_string), headers=self._token)
        PySenseUtils.parse_response(resp)

    def get_elasticube_oid(self):
        """  
        Get's the elasticube's oid  
          
        :return: The elasitcube's oid  
        """
        
        return self._cube_json['oid']

    def get_saved_formulas(self, *, server_address=None):
        """
        Get elasticube formulas 
          
        Optional:  
        :param server_address: The server address of the ElastiCube.  
            Set this to your server ip if this method fails without it set.     
          
        :return: An array of formulas   
        """

        server_address = server_address if server_address else self._server_address
        
        resp = requests.get('{}/api/metadata/measures?datasource={}&server={}'
                            .format(self._host, self.get_name(url_encoded=True), server_address),  headers=self._token)
        PySenseUtils.parse_response(resp)
        ret_arr = []
        for formula in resp.json():
            ret_arr.append(PySenseFormula.Formula(self._host, self._token, formula))
        
        return ret_arr

    def delete_formulas(self, formulas_array):
        """
        Delete given formula from ElastiCube  
  
        :param formulas_array: The array of PySense rules objects to delete  
        """
        
        for formula in formulas_array:
            resp = requests.delete('{}/api/metadata/{}'.format(self._host, formula.get_oid()), headers=self._token)
            PySenseUtils.parse_response(resp)
    
    def get_metadata(self):
        """
        Get ElastiCube metadata  
        
        :return: A json obj of ElastiCube metadata   
        """
        
        resp = requests.get('{}/api/elasticubes/metadata/{}'.format(self._host, self.get_name(url_encoded=True)), 
                            headers=self._token)
        PySenseUtils.parse_response(resp)
        if len(resp.content) == 0:
            # If we don't get a response, it means the cube was never built so we return defaults
            return {
                "title": "",
                "fullname": "",
                "id": "",
                "address": "",
                "database": ""
            }
        return resp.json()
            
    def add_formula_to_cube(self, formula):
        """
        Add formula to cube  
          
        :param formula: The PySense formula to add  
        """
        
        formula.change_datasource(self)
        elements_to_remove = ['_id', 'created', 'lastUpdated', 'oid']

        formula_json = formula.get_json()
        for element in elements_to_remove:
            formula_json.pop(element, None) 

        resp = requests.post('{}/api/metadata'.format(self._host), headers=self._token, json=formula_json)

        PySenseUtils.parse_response(resp)
