import datetime as datetime

from PySense import PySenseElasticube


class ElasticubeMixIn:

    elasticubes = None
    last_run_time = datetime.datetime.now()

    def get_elasticubes(self, flush_cache=False):
        """Gets elasticubes

        This method is called frequently so we cache the results to prevent it from being called too often.
        The time we hold the cube is stored in the param dict under 'CUBE_CACHE_TIMEOUT_SECONDS'
        CUBE_CACHE_TIMEOUT_SECONDS is an integer indicating how long before we refresh our list of cubes

        Args:
            flush_cache (bool): (Optional) Ignores cache and pull fresh data from Mongo

        Returns:
            list[Elasticube]: The found elasticubes
        """

        if (datetime.datetime.now() - self.last_run_time).total_seconds() > \
                self.param_dict['CUBE_CACHE_TIMEOUT_SECONDS'] \
                or self.elasticubes is None \
                or flush_cache:

            self.last_run_time = datetime.datetime.now()
            resp_json = self.connector.rest_call('get', 'api/v1/elasticubes/getElasticubes')
            ret_arr = []
            for cube in resp_json:
                ret_arr.append(PySenseElasticube.Elasticube(self, cube))
            self.elasticubes = ret_arr
        return self.elasticubes

    def get_elasticube_by_name(self, name, *, flush_cache=False):
        """Gets elasticube with given name

        Args:
            name (str): The name of the elasticube
            flush_cache (bool): (Optional) Ignores cache and pull fresh data from Mongo

        Returns:
            Elasticube: The Elasticube with the given name
        """

        cubes = self.get_elasticubes(flush_cache=flush_cache)
        for cube in cubes:
            if cube.get_title() == name:
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

