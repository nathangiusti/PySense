class Formula:

    def __init__(self, connector, formula_json):
        self._connector = connector
        self._formula_json = formula_json
        
    def get_oid(self):
        """
        Get's the formula's Oid
        
        :return: The formula's oid 
        """
        
        return self._formula_json['oid']
    
    def change_datasource(self, cube):
        """
        Change the data source of the formula. 
        The formula must be re-added after a data source change for it to take effect  
        
        :param cube: The ElastiCube to set the formula to 
        """
        
        self._formula_json['datasource'] = cube.get_metadata()
        
    def get_json(self):
        """  
        Returns the formula json  
          
        :return: The forumla json   
        """  
        
        return self._formula_json
