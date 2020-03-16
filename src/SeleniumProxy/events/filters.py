from urllib.parse import urlparse
import logging
import sys
import pdb


domain = 'cardatonce.eftsource.com'

endpoints = [
    '/DropDownLists/AllInstitutions',
    '/DropDownLists/ServiceLocationsForUser'
]


class RequestFilter(logging.Filter):

    @staticmethod
    def parse(r):
        return urlparse(r._data['path'])

    def filter(self, record):
        host = self.parse(record)
        if host.hostname == domain:
            for e in endpoints:
                if host.path == e:
                    pdb.Pdb(stdout=sys.__stdout__).set_trace()
                    return True
                else:
                    del record
