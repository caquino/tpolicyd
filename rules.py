# coding: utf-8

from twisted.internet import defer

@defer.inlineCallbacks
def process(map, tools):
    """
    The `process` function may process `map` using `tools` or not,
    and return a Deferred OR a String with the contents that will
    be replied to the Postfix.

    `map` is a dict-like object where keys may also be represented
    as object's attributes.

    common keys (with sample values) are:
    request=smtpd_access_policy
    protocol_state=RCPT
    protocol_name=SMTP
    helo_name=some.domain.tld
    queue_id=8045F2AB23
    sender=foo@hotmail.com.br
    recipient=bar@uol.com.br
    recipient_count=0
    client_address=1.2.3.4
    client_name=another.domain.tld
    reverse_client_name=another.domain.tld
    instance=123.456.7
    sasl_method=plain
    sasl_username=you
    sasl_sender=
    size=12345
    ccert_subject=solaris9.porcupine.org
    ccert_issuer=Wietse+20Venema
    ccert_fingerprint=C2:9D:F4:87:71:73:73:D9:18:E7:C2:F3:C1:DA:6E:04
    encryption_protocol=TLSv1/SSLv3
    encryption_cipher=DHE-RSA-AES256-SHA
    encryption_keysize=256
    etrn_domain=

    `tools` is an object that provides helper methods for processing
    data on demand. Currently, these methods are available:
    * geoip_lookup(_ip_address_): returns a deferred wich will be fired
      when the 2-letter country code for that _ip_address_ is available.
    * asn_lookup(_ip_address_): return a deferred wich will be fired
      when the ASN number for that _ip_address_ is available.
    """
    response = "OK"

    # WHITELIST (VOU PUXAR DO LDAP OS IPS)
    if map.client_address == 'xx.xx.xx.xx':
       defer.returnValue("DUNNO")

    country = yield tools.geoip_lookup(map.client_address)
    print "country is:", country

    # GREYLIST POR PAIS
    if country == 'JP' or country == 'CH':
       if map.os == 'Windows XP':
            defer.returnValue("REJECT Rejeitado pelo sistema antispam")
       else:
            response = "GREYLIST Greylist indicada pelo antispam (CRT-01)"
       
    asn = yield tools.asn_lookup(map.client_address)
    print "asn is:", asn
    #if map.asnclient != map.asnmx:
    #    action, reason = "GREYLIST", "Greylist indicada pelo antispam (ASN-01)"

    defer.returnValue(response)
