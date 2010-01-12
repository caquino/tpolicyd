# coding: utf-8

import cdb
from twisted.internet import defer

class Tools(object):
    def __init__(self, geoip_cdb):
        self.geoip = GeoIP(geoip_cdb)

    def geoip_lookup(self, addr):
        return self.geoip.lookup(addr)


class GeoIP(object):
    def __init__(self, dbname):
        self.db = cdb.init(dbname)
        self.keys = list(reversed(sorted(self.db.keys())))

    def lookup(self, addr):
        try:
            nbip = self.__convert(addr)
        except:
            return ''

        for k in self.keys:
            if k <= nbip:
                return self.db.get(k)

    def __convert(self, addr):
        a, b, c, d = map(lambda x:int(x), addr.split("."))
        for n in (a, b, c, d):
            assert n >= 0 and n <= 255
        return str(((a*256+b)*256+c)*256+d)
