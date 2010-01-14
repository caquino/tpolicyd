# coding: utf-8

from txpd import p0f
from twisted.enterprise import adbapi

class Tools(object):
    def __init__(self, ipdb_path):
        self.__db = adbapi.ConnectionPool("sqlite3", ipdb_path, check_same_thread=False)

    def __wrap_rs(self, rs):
        return rs and rs[0][-1] or ""

    def geoip_lookup(self, addr):
        try:
            nbip = struct.unpack("!L", socket.inet_aton(addr))[0]
        except:
            return ""

        d = self.__db.runQuery("""
            SELECT * FROM ip_group_country WHERE ip_start <= ? 
            ORDER BY ip_start DESC LIMIT 1""", (nbip,))
        d.addCallback(self.__wrap_rs)
        return d

    def asn_lookup(self, addr):
        try:
            nbip = struct.unpack("!L", socket.inet_aton(addr))[0]
        except:
            return ""

        d = self.__db.runQuery("""
            SELECT * FROM ip_group_asn 
            WHERE ip_start <= ? AND ip_end >= ?
            ORDER BY ip_start DESC LIMIT 1""", (nbip, nbip,))
        d.addCallback(self.__wrap_rs)
        return d

    def os_lookup(self, saddr, daddr="192.168.1.61"):
        return p0f.makeRequest(saddr, daddr, 0, 25)
