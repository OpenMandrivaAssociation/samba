Summary: Samba SMB server
Name: samba
Version: 3.5.8
Release: %mkrel 1
License: GPLv3
Group: System/Servers
Source: http://www.samba.org/samba/ftp/stable/samba-%{version}.tar.gz
URL: http://www.samba.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libacl-devel
BuildRequires: libattr-devel
BuildRequires: avahi-client-devel
BuildRequires: libcap-devel
BuildRequires: ext2fs-devel
BuildRequires: cups-devel
BuildRequires: libdm-devel
BuildRequires: fam-devel
BuildRequires: krb5-devel
BuildRequires: keyutils-devel
BuildRequires: openldap-devel
BuildRequires: pam-devel
BuildRequires: popt-devel
BuildRequires: readline-devel
BuildRequires: talloc-devel
BuildRequires: tdb-devel
BuildRequires: zlib-devel
BuildRequires: gtk+2-devel

%description
Samba provides an SMB server which can be used to provide
network services to SMB (sometimes called "Lan Manager")
clients, including various versions of MS Windows, OS/2,
and other Linux machines. Samba also provides some SMB
clients, which complement the built-in SMB filesystem
in Linux. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame)
protocol.

Samba-3.0 features working NT Domain Control capability and
includes the SWAT (Samba Web Administration Tool) that
allows samba's smb.conf file to be remotely managed using your
favourite web browser. For the time being this is being
enabled on TCP port 901 via xinetd. SWAT is now included in
it's own subpackage, samba-swat.

#-----------------------------------------------

%package common
Summary: Files used by both Samba servers and clients
Group: System/Servers

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.

%files common -f net.lang
%defattr(-,root,root)
%{_bindir}/net
%{_bindir}/ntlm_auth
%{_bindir}/rpcclient
%{_bindir}/smbcacls
%{_bindir}/smbcquotas
%{_bindir}/smbpasswd
%{_bindir}/smbtree
%{_bindir}/testparm
%dir %{_libdir}/samba
%dir %{_libdir}/samba/charset
%{_libdir}/samba/charset/CP437.so
%{_libdir}/samba/charset/CP850.so
%{_libdir}/samba/lowcase.dat
%{_libdir}/samba/upcase.dat
%{_libdir}/samba/valid.dat
%{_mandir}/man1/ntlm_auth.1*
%{_mandir}/man1/rpcclient.1*
%{_mandir}/man1/smbcacls.1*
%{_mandir}/man1/smbcquotas.1*
%{_mandir}/man1/smbtree.1*
%{_mandir}/man1/testparm.1*
%{_mandir}/man5/lmhosts.5*
%{_mandir}/man5/smb.conf.5*
%{_mandir}/man5/smbpasswd.5*
%{_mandir}/man8/net.8*
%{_mandir}/man8/smbpasswd.8*

#-----------------------------------------------

%package client
Summary: Samba (SMB) client programs
Group: Networking/Other
Requires: %{name}-common = %{version}

%description client
Samba-client provides some SMB clients, which complement the built-in
SMB filesystem in Linux. These allow the accessing of SMB shares, and
printing to SMB printers.

%pre
update-alternatives --remove-all smbclient

%files client
%defattr(-,root,root)
%{_bindir}/eventlogadm
%{_bindir}/findsmb
%{_bindir}/nmblookup
%{_bindir}/smbclient
%{_bindir}/smbget
%{_bindir}/smbspool
%{_bindir}/smbtar
%{_mandir}/man1/findsmb.1*
%{_mandir}/man1/nmblookup.1*
%{_mandir}/man1/smbclient.1*
%{_mandir}/man1/smbget.1*
%{_mandir}/man1/smbtar.1*
%{_mandir}/man5/smbgetrc.5*
%{_mandir}/man8/eventlogadm.8*
%{_mandir}/man8/smbspool.8*

#-----------------------------------------------

%package server
Summary: Samba (SMB) server programs
Requires: %{name}-common = %{version}
Group: Networking/Other

%description server
Samba-server provides a SMB server which can be used to provide
network services to SMB (sometimes called "Lan Manager")
clients. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame)
protocol.

Samba-3.0 features working NT Domain Control capability and
includes the SWAT (Samba Web Administration Tool) that
allows samba's smb.conf file to be remotely managed using your
favourite web browser. For the time being this is being
enabled on TCP port 901 via xinetd. SWAT is now included in
it's own subpackage, samba-swat.

Please refer to the WHATSNEW.txt document for fixup information.
This binary release includes encrypted password support.

Please read the smb.conf file and ENCRYPTION.txt in the
docs directory for implementation details.

%files server
%defattr(-,root,root)
/%_lib/security/pam_smbpass.so
%{_bindir}/pdbedit
%{_bindir}/profiles
%{_bindir}/sharesec
%{_bindir}/smbcontrol
%{_bindir}/smbstatus
%{_libdir}/samba/auth
%{_libdir}/samba/nss_info
%{_libdir}/samba/vfs
%{_sbindir}/nmbd
%{_sbindir}/smbd
%{_mandir}/man1/profiles.1*
%{_mandir}/man1/sharesec.1*
%{_mandir}/man1/smbcontrol.1*
%{_mandir}/man1/smbstatus.1*
%{_mandir}/man7/samba.7*
%{_mandir}/man8/idmap_ad.8*
%{_mandir}/man8/idmap_adex.8*
%{_mandir}/man8/idmap_hash.8*
%{_mandir}/man8/idmap_ldap.8*
%{_mandir}/man8/idmap_nss.8*
%{_mandir}/man8/idmap_rid.8*
%{_mandir}/man8/idmap_tdb.8*
%{_mandir}/man8/idmap_tdb2.8*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/pdbedit.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man8/vfs_acl_tdb.8*
%{_mandir}/man8/vfs_acl_xattr.8*
%{_mandir}/man8/vfs_audit.8*
%{_mandir}/man8/vfs_cacheprime.8*
%{_mandir}/man8/vfs_cap.8*
%{_mandir}/man8/vfs_catia.8*
%{_mandir}/man8/vfs_commit.8*
%{_mandir}/man8/vfs_default_quota.8*
%{_mandir}/man8/vfs_dirsort.8*
%{_mandir}/man8/vfs_extd_audit.8*
%{_mandir}/man8/vfs_fake_perms.8*
%{_mandir}/man8/vfs_fileid.8*
%{_mandir}/man8/vfs_full_audit.8*
%{_mandir}/man8/vfs_gpfs.8*
%{_mandir}/man8/vfs_netatalk.8*
%{_mandir}/man8/vfs_notify_fam.8*
%{_mandir}/man8/vfs_prealloc.8*
%{_mandir}/man8/vfs_preopen.8*
%{_mandir}/man8/vfs_readahead.8*
%{_mandir}/man8/vfs_readonly.8*
%{_mandir}/man8/vfs_recycle.8*
%{_mandir}/man8/vfs_scannedonly.8*
%{_mandir}/man8/vfs_shadow_copy.8*
%{_mandir}/man8/vfs_shadow_copy2.8*
%{_mandir}/man8/vfs_smb_traffic_analyzer.8*
%{_mandir}/man8/vfs_streams_depot.8*
%{_mandir}/man8/vfs_streams_xattr.8*
%{_mandir}/man8/vfs_xattr_tdb.8*

#-----------------------------------------------

%package swat
Summary: The Samba Web Administration Tool
Requires: %{name}-server = %{version}
Requires: xinetd
Group: System/Servers
Suggests: %{name}-doc

%description swat
SWAT (the Samba Web Administration Tool) allows samba's smb.conf file
to be remotely managed using your favourite web browser. For the time
being this is being enabled on TCP port 901 via xinetd. Note that
SWAT does not use SSL encryption, nor does it preserve comments in
your smb.conf file. Webmin uses SSL encryption by default, and
preserves comments in configuration files, even if it does not display
them, and is therefore the preferred method for remotely managing
Samba.

%files swat
%defattr(-,root,root)
%{_sbindir}/swat
%{_datadir}/samba/swat
%{_mandir}/man8/swat*.8*
%lang(de) %{_libdir}/%{name}/de.msg
%lang(en) %{_libdir}/%{name}/en.msg
%lang(fr) %{_libdir}/%{name}/fr.msg
%lang(it) %{_libdir}/%{name}/it.msg
%lang(ja) %{_libdir}/%{name}/ja.msg
%lang(nl) %{_libdir}/%{name}/nl.msg
%lang(pl) %{_libdir}/%{name}/pl.msg
%lang(tr) %{_libdir}/%{name}/tr.msg
%lang(fi) %{_libdir}/%{name}/fi.msg
%lang(ru) %{_libdir}/%{name}/ru.msg

#-----------------------------------------------

%package winbind
Summary: Samba-winbind daemon, utilities and documentation
Group: System/Servers
Requires: %{name}-common = %{version}

%description winbind
Provides the winbind daemon and testing tools to allow authentication 
and group/user enumeration from a Windows or Samba domain controller.

%files winbind -f pam_winbind.lang
%defattr(-,root,root)
%{_sbindir}/winbindd
%{_bindir}/wbinfo
/%{_lib}/security/pam_winbind*
/%{_lib}/libnss_winbind*
%{_libdir}/krb5/plugins/winbind_krb5_locator.so
%{_libdir}/%{name}/idmap
%{_mandir}/man8/winbindd*.8*
%{_mandir}/man8/pam_winbind.8*
%{_mandir}/man5/pam_winbind.conf.5.*
%{_mandir}/man7/winbind_krb5_locator.7.*
%{_mandir}/man1/wbinfo*.1*

#------------------------------------------------	

%define smbclient_major 0
%define libsmbclient %mklibname smbclient %smbclient_major

%package -n %libsmbclient
Summary: SMB Client Library
Group: System/Libraries

%description -n %libsmbclient
This package contains the SMB client library, part of the samba
suite of networking software, allowing other software to access
SMB shares.

%files -n %libsmbclient
%defattr(-,root,root)
%_libdir/libsmbclient.so.%{smbclient_major}*

#------------------------------------------------

%define smbclientdevel %mklibname -d smbclient

%package -n %smbclientdevel
Summary: SMB Client Library Development files
Group: Development/C
Provides: libsmbclient-devel = %{version}-%{release}
Requires: %libsmbclient = %{version}-%{release}
Obsoletes: %{_lib}smbclient0-devel < 3.5.8

%description -n %smbclientdevel
This package contains the development files for the SMB client
library, part of the samba suite of networking software, allowing
the development of other software to access SMB shares.

%files -n %smbclientdevel
%defattr(-,root,root)
%{_includedir}/libsmbclient.h
%{_libdir}/libsmbclient.so
%{_libdir}/pkgconfig/smbclient.pc
%{_mandir}/man7/libsmbclient.7*

#------------------------------------------------	

%define smbsharemodes_major 0
%define libsmbsharemodes %mklibname smbsharemodes %smbsharemodes_major

%package -n %libsmbsharemodes
Summary: Samba Library for accessing smb share modes (locks etc.)
Group: System/Libraries

%description -n %libsmbsharemodes
Samba Library for accessing smb share modes (locks etc.)

%files -n %libsmbsharemodes
%defattr(-,root,root)
%_libdir/libsmbsharemodes.so.%{smbsharemodes_major}*

#------------------------------------------------

%define smbsharemodesdevel %mklibname -d smbsharemodes

%package -n %smbsharemodesdevel
Group: Development/C
Summary: Samba Library for accessing smb share modes (locks etc.)
Requires: %libsmbsharemodes = %{version}-%{release}
Provides: smbsharemodes-devel = %{version}-%{release}

%description -n %smbsharemodesdevel
Samba Library for accessing smb share modes (locks etc.)

%files -n %smbsharemodesdevel
%defattr(-,root,root)
%{_libdir}/libsmbsharemodes.so
%{_includedir}/smb_share_modes.h
%{_libdir}/pkgconfig/smbsharemodes.pc

#------------------------------------------------	

%define netapi_major 0
%define libnetapi %mklibname netapi %netapi_major

%package -n %libnetapi
Summary: Samba library for accessing functions in 'net' binary
Group: System/Libraries

%description -n %libnetapi
Samba library for accessing functions in 'net' binary

%files -n %libnetapi
%defattr(-,root,root)
%_libdir/libnetapi.so.%{netapi_major}*

#------------------------------------------------

%define netapidevel %mklibname -d netapi

%package -n %netapidevel
Group: Development/C
Summary: Samba library for accessing functions in 'net' binary
Requires: %libnetapi = %{version}-%{release}
Provides: netapi-devel = %{version}-%{release}

%description -n %netapidevel
Samba library for accessing functions in 'net' binary

%files -n %netapidevel
%defattr(-,root,root)
%{_libdir}/libnetapi*.so
%{_includedir}/netapi.h
%{_libdir}/pkgconfig/netapi.pc

#------------------------------------------------	

%define wbclient_major 0
%define libwbclient %mklibname wbclient %wbclient_major

%package -n %libwbclient
Summary: Library providing access to winbindd
Group: System/Libraries

%description -n %libwbclient
Library providing access to winbindd

%files -n %libwbclient
%defattr(-,root,root)
%_libdir/libwbclient.so.%{wbclient_major}*

#------------------------------------------------

%define wbclientdevel %mklibname -d wbclient

%package -n %wbclientdevel
Group: Development/C
Summary: Library providing access to winbindd
Requires: %libwbclient = %{version}-%{release}
Provides: wbclient-devel = %{version}-%{release}

%description -n %wbclientdevel
Library providing access to winbindd

%files -n %wbclientdevel
%defattr(-,root,root)
%{_libdir}/libwbclient.so
%{_includedir}/wbclient.h
%{_includedir}/wbc_async.h
%{_libdir}/pkgconfig/wbclient.pc

#------------------------------------------------

%package static-devel
Group: Development/C
Summary: SMB Static Library Development files
Obsoletes: %{_lib}smbclient0-static-devel < 3.5.8
Provides: libsmbclient-static-devel = %{version}-%{release}
Requires: %netapidevel = %{version}
Requires: %smbsharemodesdevel = %{version}
Requires: %smbclientdevel = %{version}

%description static-devel
This package contains the static development files for the SMB
client library, part of the samba suite of networking software,
allowing the development of other software to access SMB shares.

%files static-devel
%defattr(-,root,root)
%{_libdir}/libnetapi.a
%{_libdir}/libsmbclient.a
%{_libdir}/libsmbsharemodes.a

#-----------------------------------------------

%define libnsswin %mklibname nsswins 2
%package -n %libnsswin
Summary: Name Service Switch service for WINS
Group: System/Servers
Requires: %{name}-common = %{version}
Obsoletes: nss_wins < 3.5.8

%description -n %libnsswin
Provides the libnss_wins shared library which resolves NetBIOS names to 
IP addresses.

%files -n %libnsswin
%defattr(-,root,root)
/%{_lib}/libnss_wins.so*

#-----------------------------------------------

%package domainjoin-gui
Summary: Domainjoin GUI
Requires: samba-common = %{version}
Group: System/Configuration/Other

%description domainjoin-gui
The samba-domainjoin-gui package includes a domainjoin gtk application.

%files domainjoin-gui
%defattr(-,root,root)
%{_sbindir}/netdomjoin-gui
%dir %{_datadir}/pixmaps/samba
%{_datadir}/pixmaps/samba/samba.ico
%{_datadir}/pixmaps/samba/logo.png
%{_datadir}/pixmaps/samba/logo-small.png

#-----------------------------------------------

%package doc
Summary: Documentation for Samba servers and clients
Group: System/Servers
Requires: %{name}-common = %{version}
BuildArch: noarch

%description doc
Samba-doc provides documentation files for both the server and client
packages of Samba.

%files doc
%defattr(-,root,root)
%doc README COPYING Manifest Read-Manifest-Now
%doc WHATSNEW.txt Roadmap
%doc clean-docs/samba-doc/docs/*
%doc clean-docs/samba-doc/examples

#-----------------------------------------------

%prep
%setup -qDT

%if 0

#make better doc trees:
chmod -R a+rX examples docs *Manifest* README  Roadmap COPYING
mkdir -p clean-docs/samba-doc
cp -a examples docs clean-docs/samba-doc
mv -f clean-docs/samba-doc/examples/libsmbclient clean-docs/
rm -Rf clean-docs/samba-doc/docs/{docbook,manpages,htmldocs,using_samba}
mkdir clean-docs/samba-doc/docs/htmldocs
cp docs/htmldocs/*.{html,css} clean-docs/samba-doc/docs/htmldocs

%build
pushd source3
%serverbuild
%configure2_5x --with-fhs --with-pammodulesdir=/%_lib/security \
	--with-cifsmount=no --with-cifsumount=no --with-cifsupcall=no
perl -pi -e 'if ( m/^LDSHFLAGS_MODULES/ ) { $_ =~ s/-Wl,--no-undefined//g;};' Makefile
%make
LD_LIBRARY_PATH=`pwd`/bin %make -C lib/netapi/examples
popd
%endif
%install
rm -fr %buildroot
%makeinstall_std -C source3

# these are provided by ldb-utils
rm -f %{buildroot}%{_mandir}/man1/ldb* %{buildroot}%{_bindir}/ldb*

# these are provided by tdb-utils
rm -f %{buildroot}%{_mandir}/man8/tdb*

# these are not built
rm -f %{buildroot}%{_mandir}/man1/log2pcap.1*
rm -f %{buildroot}%{_mandir}/man1/vfstest.1*
rm -f %{buildroot}%{_mandir}/man8/mount.cifs.8* %{buildroot}%{_mandir}/man8/umount.cifs.8*

# install pkgconfig files
mkdir -p %buildroot%_libdir/pkgconfig
install -m0644 source3/pkgconfig/*.pc %buildroot%_libdir/pkgconfig

# install static libs
install -m0644 source3/bin/{libnetapi.a,libsmbclient.a,libsmbsharemodes.a} %buildroot%_libdir

#libnss_* still not handled by make:
# Install the nsswitch library extension file
for i in wins winbind; do
  install -m755 nsswitch/libnss_${i}.so %buildroot/%{_lib}/libnss_${i}.so
done
# Make link for wins and winbind resolvers
( cd %buildroot/%{_lib}; ln -s libnss_wins.so libnss_wins.so.2; ln -s libnss_winbind.so libnss_winbind.so.2)
install -d %{buildroot}/%{_libdir}/krb5/plugins
install -m755 source3/bin/winbind_krb5_locator.so %{buildroot}/%{_libdir}/krb5/plugins

# install netdomjoin-gui
install -m 755 source3/lib/netapi/examples/bin/netdomjoin-gui %buildroot/%{_sbindir}/netdomjoin-gui
mkdir -p %buildroot%{_datadir}/pixmaps/%{name}
install -m 644 source3/lib/netapi/examples/netdomjoin-gui/samba.ico %buildroot/%{_datadir}/pixmaps/%{name}/samba.ico
install -m 644 source3/lib/netapi/examples/netdomjoin-gui/logo.png %buildroot/%{_datadir}/pixmaps/%{name}/logo.png
install -m 644 source3/lib/netapi/examples/netdomjoin-gui/logo-small.png %buildroot/%{_datadir}/pixmaps/%{name}/logo-small.png

%find_lang net
%find_lang pam_winbind

%clean
rm -fr %buildroot
