from PySense import PySenseElasticube


class ElasticubeMixIn:

    def get_elasticubes(self):
        """Gets elasticubes"""
        resp_json = self.connector.rest_call('get', 'api/v1/elasticubes/getElasticubes')
        ret_arr = []
        for cube in resp_json:
            ret_arr.append(PySenseElasticube.Elasticube(self, cube))
        return ret_arr

    def get_elasticube_by_name(self, name):
        """Gets elasticube with given name"""
        cubes = self.get_elasticubes()
        for cube in cubes:
            if cube.get_name() == name:
                return cube
        return None
