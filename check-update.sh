#!/bin/sh
curl -L https://download.samba.org/pub/samba/stable/ 2>/dev/null |grep .tar.gz |tail -n1 |sed -e 's,.*>samba-,,;s,\.tar\.gz.*,,'
