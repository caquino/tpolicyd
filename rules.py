# coding: utf-8

from txpd import helper
from twisted.internet import defer

@defer.inlineCallbacks
def process(map):
    response = "OK"

    # WHITELIST (VOU PUXAR DO LDAP OS IPS)
    if map.client_address == 'xx.xx.xx.xx':
       defer.returnValue("DUNNO")

    x = 1/0
    country = yield helper.geoip_lookup(map.client_address)
    print "country is:", country

    # GREYLIST POR PAIS
    if country == 'JP' or country == 'CH':
       if map.os == 'Windows XP':
            defer.returnValue("REJECT Rejeitado pelo sistema antispam")
       else:
            response = "GREYLIST Greylist indicada pelo antispam (CRT-01)"
       
    #if map.asnclient != map.asnmx:
    #    action, reason = "GREYLIST", "Greylist indicada pelo antispam (ASN-01)"

    defer.returnValue(response)
