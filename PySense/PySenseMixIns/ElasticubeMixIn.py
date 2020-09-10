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

    """ The end point used here only deletes the build cube and not the actual model. When model deletion is supported,
    these methods will be enabled"""
    # def delete_elasticube_by_name(self, name):
    #     """Deletes the elasticube with given name.
    #
    #     Windows only
    #     """
    #
    #     self._validate_version(SisenseVersion.Version.WINDOWS, 'delete_elasticube_by_name')
    #
    #     elasticube = self.get_elasticube_by_name(name)
    #     if elasticube is not None:
    #         self.delete_elasticube(elasticube)
    #     else:
    #         raise PySenseException.PySenseException('No elasticube with name {} found'.format(name))
    #
    # def delete_elasticube(self, elasticube):
    #     """Deletes the elasticube.
    #
    #     Windows only
    #     """
    #     return self.connector.rest_call('delete', 'api/elasticubes/{}/{}/delete'
    #                                     .format(elasticube.get_address(), elasticube.get_name(url_encoded=True)))

