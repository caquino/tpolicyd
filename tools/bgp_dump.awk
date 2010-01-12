#!/usr/bin/awk -f
BEGIN {}
{
	if (NR > 7) {
		NETBLOCK=$2
		ASN=$(NF-1)
		split(NETBLOCK, BUFF, "/")
		print BUFF[1]";"BUFF[2]";"ASN
	}
}
END {}
