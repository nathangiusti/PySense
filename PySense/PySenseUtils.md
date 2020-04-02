Module PySense.PySenseUtils
===========================

Functions
---------

    
`build_json_object(dictionary)`
:   

    
`build_query_string(dictionary)`
:   Turns dictionary into param string
    
    :param dictionary: The dictionary of values to transform
    :return: A query string

    
`format_host(host)`
:   Formats host string
    
    :param host: host
    :return: The formatted host string

    
`get_role_id(host, token, role_name)`
:   

    
`get_user_id(host, token, email)`
:   

    
`parse_response(response)`
:   Parses REST response object for errors
    
    :param response: the REST response object
    :return: The response object if no errors

Classes
-------

`RestError(...)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException