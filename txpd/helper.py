# coding: utf-8

from txpd import p0f
from twisted.enterprise import adbapi

class Tools(object):
    def __init__(self, ipdb_path):
        self.__db = adbapi.ConnectionPool("sqlite3", ipdb_path, check_same_thread=False)
        self.__p0f = p0f.lazyp0fConnectionPool()

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
        return self.__p0f.sendRequest(saddr, daddr)

#    def os_lookup(self, addr):
#        destination_address = '192.168.1.61'
#        response = ""
#        retry = 3
#        while retry > 0:
#            try:
#                p0f_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#                p0f_socket.connect('/var/run/p0f.sock')
#                query = struct.pack("IBI4s4sHH", 0x0defaced, 1, 0x12345678, socket.inet_aton(addr), socket.inet_aton(destination_address), 0, 25)
#                p0f_socket.send(query)
#                response = p0f_socket.recv(1024)
#                break
#            except:
#                retry -= 1
#                pass
#
#        if response != "":
#            retEx = []
#            for i in struct.unpack("I I B 20s 40s b 30s 30s B B B h H i", response):
#                if type(i) == str and i.find('\x00') != -1:
#                    retEx.append(i[:i.find('\x00')])
#                else:
#                    retEx.append(i)
#
#        return retEx
