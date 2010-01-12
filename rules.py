# coding: utf-8

def process(map, tools):
    response = "OK"

    # WHITELIST (VOU PUXAR DO LDAP OS IPS)
    if map.client_address == 'xx.xx.xx.xx':
       return "DUNNO"

    country = tools.geoip_lookup(map.client_address)
    print "country is:", country

    # GREYLIST POR PAIS
    if country == 'JP' or country == 'CH':
       if map.os == 'Windows XP':
            return "REJECT Rejeitado pelo sistema antispam"
       else:
            response = "GREYLIST Greylist indicada pelo antispam (CRT-01)"
       
    #if map.asnclient != map.asnmx:
    #    action, reason = "GREYLIST", "Greylist indicada pelo antispam (ASN-01)"

    return response
