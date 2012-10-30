%define _build_pkgcheck_set %{nil}
%define _build_pkgcheck_srpm %{nil}

%define pkg_name	samba
%define version		3.6.9
%define rel		1
%define epoch		1
#define	subrel		1
%define vscanver 	0.3.6c-beta5
%define libsmbmajor	0
%define netapimajor	0
%define smbsharemodesmajor	0
%define	tallocmajor	1
%define tdbmajor	1
%define	wbclientmajor	0

%define check_sig() export GNUPGHOME=%{_tmppath}/rpm-gpghome \
if [ -d "$GNUPGHOME" ] \
then echo "Error, GNUPGHOME $GNUPGHOME exists, remove it and try again"; exit 1 \
fi \
install -d -m700 $GNUPGHOME \
gpg --import %{1} \
gpg --trust-model always --verify %{2} %{?3} \
rm -Rf $GNUPGHOME \


# Samba has started using -Wl,z,nodefs upstream, without libtool (after patch
# submission to them, handled in samba bug 6792. To allow
# plugins to link now, we have to avoid any such flags by default
#define _disable_ld_no_undefined 1
# or, instead, filter them out of the right line in the Makefile, like before
# see LDSHFLAGS_MODULES below

%{!?lib: %global lib lib}
%{!?mklibname: %global mklibname(ds) %lib%{1}%{?2:%{2}}%{?3:_%{3}}%{-s:-static}%{-d:-devel}}

%{?!mkver:%define mkver(r:) %{-r:%(perl -e '$_="%{1}";m/(((\\d\\.?)+)(\\w\*))(.\*)/;$pre=$4;print "0.$pre." if $pre =~ /\\w\{2,\}/;print "%{-r*}"')}%{!-r:%(perl -e '$_="%{1}";m/(((\\d\\.?)+)(\\w\*))(.\*)/;$pre=$4;print "$2";print $pre if $pre !~ /\\w{2,}/')}}

%define libname %mklibname smbclient %libsmbmajor
%define libnetapi %mklibname netapi %netapimajor
%define netapidevel %mklibname -d netapi
%define libsmbsharemodes %mklibname smbsharemodes %smbsharemodesmajor
%define smbsharemodesdevel %mklibname -d smbsharemodes
%define libtalloc %mklibname talloc %tallocmajor
%define tallocdevel %mklibname -d talloc
%define libtdb %mklibname tdb %tdbmajor
%define tdbdevel %mklibname -d tdb
%define libwbclient %mklibname wbclient %wbclientmajor
%define wbclientdevel %mklibname -d wbclient

# Version and release replaced by samba-team at release from samba cvs
%define pversion PVERSION
%define prelease PRELEASE

#Check to see if p(version|release) has been replaced (1 if replaced)
%define have_pversion %(if [ "%pversion" = `echo "pversion" |tr '[:lower:]' '[:upper:]'` ];then echo 0; else echo 1; fi)

%if %have_pversion
%define source_ver 	%{pversion}
%define rel 2.%{prelease}
# Don't abort for stupid reasons on builds from tarballs:
%global	_unpackaged_files_terminate_build	0
%global	_missing_doc_files_terminate_build	0
%else
%define source_ver 	%{version}
%endif

%define prerel %mkver -r %rel %source_ver
%define real_version %mkver %source_ver
%define release %prerel
%define have_pre %([ "%version" == "%source_ver" ]; echo $?)

# Check to see if we are running a build from a tarball release from samba.org
# (%have_pversion) If so, disable vscan, unless explicitly requested
# (--with vscan).
#FIXME
%define build_vscan 	0
%if %have_pversion
%define build_vscan 	0
%{?_with_vscan: %define build_vscan 1}
%endif

# Default options
%define build_talloc 0
%define build_tdb 0
%define build_ldb 0
%define build_ctdb 1
%define build_alternatives	1
%define build_system	1
%define build_acl 	1
%define build_winbind 	1
%define build_wins 	1
%define build_ldap 	0
%define build_ads	1
%define build_scanners	0
%define build_test	0
# CUPS supports functionality for 'printcap name = cups' (9.0 and later):
%define build_cupspc	1
# %_{pre,postun}_service are provided by rpm-helper in 9.0 and later
%define have_rpmhelper	1
%define build_mysql	0
%define build_pgsql 	0

# Allow commandline option overrides (borrowed from Vince's qmail srpm):
# To use it, do rpm [-ba|--rebuild] --with 'xxx'
# Check if the rpm was built with the defaults, otherwise we inform the user
%define build_non_default 0
%{?_with_system: %global build_system 1}
%{?_without_system: %global build_system 0}
%{?_with_acl: %global build_acl 1}
%{?_with_acl: %global build_non_default 1}
%{?_without_acl: %global build_acl 0}
%{?_without_acl: %global build_non_default 1}
%{?_with_winbind: %global build_winbind 1}
%{?_with_winbind: %global build_non_default 1}
%{?_without_winbind: %global build_winbind 0}
%{?_without_winbind: %global build_non_default 1}
%{?_with_wins: %global build_wins 1}
%{?_with_wins: %global build_non_default 1}
%{?_without_wins: %global build_wins 0}
%{?_without_wins: %global build_non_default 1}
%{?_with_ldap: %global build_ldap 1}
%{?_with_ldap: %global build_non_default 1}
%{?_without_ldap: %global build_ldap 0}
%{?_without_ldap: %global build_non_default 1}
%{?_with_ads: %global build_ads 1}
%{?_with_ads: %global build_non_default 1}
%{?_without_ads: %global build_ads 0}
%{?_without_ads: %global build_non_default 1}
%{?_with_scanners: %global build_scanners 1}
%{?_with_scanners: %global build_non_default 1}
%{?_without_scanners: %global build_scanners 0}
%{?_without_scanners: %global build_non_default 1}
%{?_with_vscan: %global build_vscan 1}
%{?_with_vscan: %global build_non_default 1}
%{?_without_vscan: %global build_vscan 0}
%{?_without_vscan: %global build_non_default 1}
%{?_with_test: %global build_test 1}
%{?_with_test: %global build_non_default 1}
%{?_without_test: %global build_test 0}
%{?_without_test: %global build_non_default 1}
%{?_with_mysql: %global build_mysql 1}
%{?_with_pgsql: %global build_pgsql 1}
# As if that weren't enough, we're going to try building with antivirus
# support as an option also
%global build_antivir 	0
%global build_clamav 	0
%global build_fprot 	0
%global build_fsav 	0
%global build_icap 	0
%global build_kaspersky 0
%global build_mks 	0
%global build_nai 	0
%global build_openav	0
%global build_sophos 	0
%global build_symantec 	0
%global build_trend	0
%if %build_vscan
# These we build by default
%global build_clamav 	1
%global build_icap 	1
%endif
%if %build_vscan && %build_scanners
# These scanners are built if scanners are selected
# symantec requires their library present and must be selected 
# individually
%global build_fprot 	1
%global build_fsav 	1
%global build_kaspersky 1
%global build_mks 	1
%global build_nai 	1
%global build_openav	1
%global build_sophos 	1
%global build_trend 	1
%endif
%if %build_vscan
%{?_with_fprot: %{expand: %%global build_fprot 1}}
%{?_with_kaspersky: %{expand: %%global build_kaspersky 1}}
%{?_with_mks: %{expand: %%global build_mks 1}}
%{?_with_openav: %{expand: %%global build_openav 1}}
%{?_with_sophos: %{expand: %%global build_sophos 1}}
#%{?_with_symantec: %{expand: %%global build_symantec 1}}
%{?_with_trend: %{expand: %%global build_trend 1}}
%global vscandir samba-vscan-%{vscanver}
%endif
%global vfsdir examples.bin/VFS

#Standard texts for descriptions:
%define message_bugzilla() %(echo -e -n "Please file bug reports for this package at Mandriva bugzilla \\n(http://qa.mandriva.com) under the product name %{1}")
%define message_system %(echo -e -n "NOTE: These packages of samba-%{version}, are provided, parallel installable\\nwith samba-2.2.x, to allow easy migration from samba-2.2.x to samba-%{version},\\nbut are not officially supported")

#check gcc version to disable some optimisations on gcc-3.3.1
# gcc is not mandatory to do rpm queries on a .src.rpm, which is what the buildsystem
# ends up doing, so we need to guard against that
%define gcc331 %((gcc -dumpversion 2>/dev/null || echo 4.1.2) |awk '{if ($1>3.3) print 1; else print 0}')

#Define sets of binaries that we can use in globs and loops:
%global commonbin net,ntlm_auth,rpcclient,smbcacls,smbcquotas,smbpasswd,smbtree,testparm

%global serverbin 	pdbedit,profiles,smbcontrol,smbstatus,sharesec,smbta-util
%if %build_ldb
%global serverldbbin 	ldbadd,ldbdel,ldbedit,ldbmodify,ldbsearch,ldbrename
%endif
%global serversbin nmbd,samba,smbd

%global clientbin 	findsmb,nmblookup,smbclient,smbprint,smbspool,smbtar,smbget
%global client_sbin 	mount.smb,mount.smbfs
%global client_man	man1/findsmb.1,man1/nmblookup.1,man1/smbclient.1,man1/smbget.1,man1/smbtar.1,man5/smbgetrc.5,man8/smbspool.8

%global testbin 	debug2html,smbtorture,msgtest,masktest,locktest,locktest2,nsstest,vfstest

%ifarch alpha
%define build_expsam xml
%else
%define build_expsam xml%{?_with_pgsql:,pgsql}%{?_with_mysql:,mysql}
%endif

# Determine whether this is the system samba or not.
%if %build_system
%define samba_major	%{nil}
%else
%define samba_major	3
%endif
# alternatives_major is %{nil} if we aren't system and not using alternatives
%if !%build_system || %build_alternatives
%define alternative_major 3
%else
%define alternative_major %{nil}
%endif

Summary: Samba SMB server
Name: %{pkg_name}%{samba_major}

Version: %{source_ver}
Release: %{release}
Epoch:	%{epoch}

License: GPLv3
Group: System/Servers
Source: http://www.samba.org/samba/ftp/stable/samba-%{source_ver}.tar.gz
Source99: http://www.samba.org/samba/ftp/stable/samba-%{source_ver}.tar.asc
Source98: http://www.samba.org/samba/ftp/samba-pubkey.asc
URL:	http://www.samba.org
Source1: samba.log
Source3: samba.xinetd
Source4: swat_48.png
Source5: swat_32.png
Source6: swat_16.png
Source7: README.%{name}-mandriva-rpm
Source8: samba-vscan-%{vscanver}.tar.gz
%if %build_vscan
%endif
%if %build_vscan
BuildRequires: file-devel
%endif
Source10: samba-print-pdf.sh
Source11: smb-migrate

#Sources that used to be in packaging patch:
Source20:	smbusers
Source21:	smbprint
#Source22:	smbadduser
Source23:	findsmb
Source24:	smb.init
Source25:	winbind.init
Source26:	wrepld.init
Source27:	samba.pamd
Source28:	samba.pamd0_9
Source29:	system-auth-winbind.pamd
Source30:	smb.conf


%if !%have_pversion
# Version specific patches: current version
Patch11: samba-3.0-mandriva-packaging.patch
# https://bugzilla.samba.org/show_bug.cgi?id=3571, bug 21387
Patch19: samba-3.0.21c-swat-fr-translaction.patch
Patch30: samba-3.5-check-undefined-before-zdefs.patch
Patch31: samba-3.5.3-fix-nss-wins-syslog.patch
Patch33: samba-3.5.8-fix-netapi-examples-linking.patch
%else
# Version specific patches: upcoming version
%endif
# Limbo patches (applied to prereleases, but not preleases, ie destined for
# samba CVS)
%if %have_pversion && %have_pre
%endif
Requires: pam >= 0.64, samba-common = %{epoch}:%{version}
BuildRequires: pam-devel readline-devel ncurses-devel popt-devel glibc-devel
BuildRequires: libxml2-devel
# Samba 3.2 and later should be built with capabilities support:
# http://lists.samba.org/archive/samba/2009-March/146821.html
BuildRequires: libcap-devel
BuildRequires: gnupg
BuildRequires: avahi-client-devel
BuildRequires: libaio-devel
BuildRequires: libuuid-devel
%if %build_ctdb
BuildRequires: ctdb-devel >= 1.0.114.4
%endif
%if %build_pgsql
BuildRequires: postgresql-devel
%endif
%ifnarch alpha
%if %build_mysql
BuildRequires: mysql-devel
%endif
%endif
%if %build_acl
BuildRequires: acl-devel
%endif
BuildRequires: cups-devel cups-common
BuildRequires: libldap-devel
%if %build_ads
BuildRequires: libldap-devel krb5-devel
%endif
BuildRequires: keyutils-devel
%if !%build_tdb
BuildRequires: tdb-devel
%endif
%if !%build_ldb
#BuildRequires: ldb-devel
%endif
%if !%build_talloc
BuildRequires: talloc-devel
%endif
# for domain-join gui
BuildRequires: gtk2-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires(pre): chkconfig mktemp psmisc
Requires(pre): coreutils sed grep

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

Please refer to the WHATSNEW.txt document for fixup information.
This binary release includes encrypted password support.

Please read the smb.conf file and ENCRYPTION.txt in the
docs directory for implementation details.
%if %have_pversion
%message_bugzilla samba3
%endif 
%if !%build_system
%message_system
%endif
%if %build_non_default
WARNING: This RPM was built with command-line options. Please
see README.%{name}-mandriva-rpm in the documentation for
more information.
%endif

%package server
URL:	http://www.samba.org
Summary: Samba (SMB) server programs
Requires: %{name}-common = %{epoch}:%{version}
Requires: %libwbclient >= %{epoch}:%{version}
%if %have_rpmhelper
Requires(pre):		rpm-helper
%endif
Group: Networking/Other
%if %build_system
Provides: samba
Obsoletes: samba
Provides:  samba-server-ldap
Obsoletes: samba-server-ldap
Provides:  samba3-server
Obsoletes: samba3-server
%else
#Provides: samba-server
%endif

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
%if %have_pversion
%message_bugzilla samba3-server
%endif
%if !%build_system
%message_system
%endif

%package client
URL:	http://www.samba.org
Summary: Samba (SMB) client programs
Group: Networking/Other
Requires: %{name}-common = %{epoch}:%{version}
Requires: cifs-utils >= 4.4
%if %build_alternatives
#Conflicts:	samba-client < 2.2.8a-9mdk
%endif
%if %build_system
Provides:  samba3-client
Obsoletes: samba3-client
Obsoletes: smbfs
%else
#Provides: samba-client
%endif
%if !%build_system && %build_alternatives
Provides: samba-client
%endif

%description client
Samba-client provides some SMB clients, which complement the built-in
SMB filesystem in Linux. These allow the accessing of SMB shares, and
printing to SMB printers.
%if %have_pversion
%message_bugzilla samba3-client
%endif
%if !%build_system
%message_system
%endif

%package common
URL:	http://www.samba.org
Summary: Files used by both Samba servers and clients
Group: System/Servers
%if %build_system
Provides:  samba-common-ldap
Obsoletes: samba-common-ldap
Provides:  samba3-common
Obsoletes: samba3-common
%else
#Provides: samba-common
%endif

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.
%if %have_pversion
%message_bugzilla samba3-common
%endif
%if !%build_system
%message_system
%endif

%package doc
URL:	http://www.samba.org
Summary: Documentation for Samba servers and clients
Group: System/Servers
Requires: %{name}-common = %{epoch}:%{version}
BuildArch: noarch
%if %build_system
Obsoletes: samba3-doc
Provides:  samba3-doc
%else
#Provides: samba-doc
%endif

%description doc
Samba-doc provides documentation files for both the server and client
packages of Samba.
%if %have_pversion
%message_bugzilla samba3-doc
%endif
%if !%build_system
%message_system
%endif

%package swat
URL:	http://www.samba.org
Summary: The Samba Web Administration Tool
Requires: %{name}-server = %{epoch}:%{version}
Requires: xinetd
Group: System/Servers
%if %build_system
Provides:  samba-swat-ldap
Obsoletes: samba-swat-ldap
Provides:  samba3-swat
Obsoletes: samba3-swat
%else
#Provides: samba-swat
%endif
Conflicts: %{name}-server < 3.4.0
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
%if %have_pversion
%message_bugzilla samba3-swat
%endif
%if !%build_system
%message_system
%endif

%if %build_winbind
%package winbind
URL:	http://www.samba.org
Summary: Samba-winbind daemon, utilities and documentation
Group: System/Servers
Requires: %{name}-common = %{epoch}:%{version}
%endif
%if %build_winbind && !%build_system
Conflicts: samba-winbind
%endif
%if %build_winbind
%description winbind
Provides the winbind daemon and testing tools to allow authentication 
and group/user enumeration from a Windows or Samba domain controller.
%endif
%if %have_pversion
%message_bugzilla samba3-winbind
%endif
%if !%build_system
%message_system
%endif

%if %build_wins
%package -n nss_wins%{samba_major}
URL:	http://www.samba.org
Summary: Name Service Switch service for WINS
Group: System/Servers
Requires: %{name}-common = %{epoch}:%{version}
Requires(pre): glibc
%endif
%if %build_wins && !%build_system
Conflicts: nss_wins
%endif
%if %build_wins
%description -n nss_wins%{samba_major}
Provides the libnss_wins shared library which resolves NetBIOS names to 
IP addresses.
%endif
%if %have_pversion
%message_bugzilla nss_wins3
%endif
%if !%build_system
%message_system
%endif

%if %build_test
%package test
URL:	http://www.samba.org
Summary: Debugging and benchmarking tools for samba
Group: System/Servers
Requires: %{name}-common = %{epoch}:%{version}
%endif
%if %build_system && %build_test
Provides:  samba3-test samba3-debug
Obsoletes: samba3-test samba3-debug
%endif
%if !%build_system && %{build_test}
Provides: samba-test samba3-debug
Obsoletes: samba3-debug
%endif
%if %{build_test}

%description test
This package provides tools for benchmarking samba, and debugging
the correct operation of tools against smb servers.
%endif

%if %build_system
%package -n %{libname}
URL:		http://www.samba.org
Summary: 	SMB Client Library
Group:		System/Libraries
Provides:	libsmbclient

%description -n %{libname}
This package contains the SMB client library, part of the samba
suite of networking software, allowing other software to access
SMB shares.
%endif
%if %have_pversion && %build_system
%message_bugzilla %{libname}
%endif

%if %build_system
%package -n %{libname}-devel
URL:		http://www.samba.org
Summary: 	SMB Client Library Development files
Group:		Development/C
Provides:	libsmbclient-devel = %{epoch}:%{version}-%{release}
Requires:       %{libname} = %{epoch}:%{version}-%{release}

%description -n %{libname}-devel
This package contains the development files for the SMB client
library, part of the samba suite of networking software, allowing
the development of other software to access SMB shares.
%endif
%if %have_pversion && %build_system
%message_bugzilla %{libname}-devel
%endif

%if %build_system
%package -n %{libname}-static-devel
URL:            http://www.samba.org
Summary:        SMB Client Static Library Development files
Group:          Development/C
Provides:       libsmbclient-static-devel = %{epoch}:%{version}-%{release}
Requires:       %{libname}-devel = %{epoch}:%{version}-%{release}

%description -n %{libname}-static-devel
This package contains the static development files for the SMB
client library, part of the samba suite of networking software,
allowing the development of other software to access SMB shares.
%endif
%if %have_pversion && %build_system
%message_bugzilla %{libname}-devel
%endif

%package -n %libnetapi
Summary: Samba library for accessing functions in 'net' binary
Group: System/Libraries

%description -n %libnetapi
Samba library for accessing functions in 'net' binary

%package -n %netapidevel
Group: Development/C
Summary: Samba library for accessing functions in 'net' binary
Provides: netapi-devel = %{epoch}:%{version}-%{release}

%description -n %netapidevel
Samba library for accessing functions in 'net' binary

%package -n %libsmbsharemodes
Group: System/Libraries
Summary: Samba Library for accessing smb share modes (locks etc.)

%description -n %libsmbsharemodes
Samba Library for accessing smb share modes (locks etc.)

%package -n %smbsharemodesdevel
Group: Development/C
Summary: Samba Library for accessing smb share modes (locks etc.)
Provides: smbsharemodes-devel = %{epoch}:%{version}-%{release}

%description -n %smbsharemodesdevel
Samba Library for accessing smb share modes (locks etc.)

%if %build_talloc
%package -n %libtalloc
Group: System/Libraries
Summary: Library implementing Samba's memory allocator

%description -n %libtalloc
Library implementing Samba's memory allocator

%package -n %tallocdevel
Group: Development/C
Summary: Library implementing Samba's memory allocator
Provides: talloc-devel = %{epoch}:%{version}-%{release}

%description -n %tallocdevel
Library implementing Samba's memory allocator
%endif

%if %build_tdb
%package -n %libtdb
Group: System/Libraries
Summary: Library implementing Samba's embedded database

%description -n %libtdb
Library implementing Samba's embedded database

%package -n %tdbdevel
Group: Development/C
Summary: Library implementing Samba's embedded database
Provides: tdb-devel = %{epoch}:%{version}-%{release}
Requires: %libtdb
# because /usr/include/tdb.h was moved from libsmbclient0-devel to libtdb-devel
Conflicts: %{mklibname smbclient 0 -d} < 3.2.6-3

%description -n %tdbdevel
Library implementing Samba's embedded database
%endif

%package -n %libwbclient
Group: System/Libraries
Summary: Library providing access to winbindd

%description -n %libwbclient
Library providing access to winbindd

%package -n %wbclientdevel
Group: Development/C
Summary: Library providing access to winbindd
Provides: wbclient-devel = %{epoch}:%{version}-%{release}
Requires: %libwbclient >= %{epoch}:%{version}

%description -n %wbclientdevel
Library providing access to winbindd

#%package passdb-ldap
#URL:		http://www.samba.org
#Summary:	Samba password database plugin for LDAP
#Group:		System/Libraries
#
#%description passdb-ldap
#The passdb-ldap package for samba provides a password database
#backend allowing samba to store account details in an LDAP
#database
#_if %have_pversion
#_message_bugzilla samba3-passdb-ldap
#_endif
#_if !%build_system
#_message_system
#_endif

%ifnarch alpha
%if %{build_mysql}
%package passdb-mysql
URL:		http://www.samba.org
Summary:	Samba password database plugin for MySQL
Group:		System/Libraries
Requires:	%{name}-server = %{epoch}:%{version}-%{release}
%endif
%endif
%ifnarch alpha
%if %build_system && %{build_mysql}
Obsoletes:	samba3-passdb-mysql 
Provides:	samba3-passdb-mysql 
%endif
%endif
%ifnarch alpha
%if %{build_mysql}

%description passdb-mysql
The passdb-mysql package for samba provides a password database
backend allowing samba to store account details in a MySQL
database
%endif
%endif

#does postgresql build on alpha?
#ifnarch alpha
%if %{build_pgsql}
%package passdb-pgsql
URL:		http://www.samba.org
Summary:	Samba password database plugin for PostgreSQL
Group:		System/Libraries
Requires:	%{name}-server = %{epoch}:%{version}-%{release}
#endif
#ifnarch alpha && %build_system
%endif
%if %build_system && %{build_pgsql}
Obsoletes:	samba3-passdb-pgsql
Provides:	samba3-passdb-pgsql
%endif
%if %{build_pgsql}

%description passdb-pgsql
The passdb-pgsql package for samba provides a password database
backend allowing samba to store account details in a PostgreSQL
database
%endif

#Antivirus packages:
%if %build_antivir
%package vscan-antivir
Summary: On-access virus scanning for samba using Antivir
Group: System/Servers
Requires: %{name}-server = %{epoch}:%{version}
Provides: %{name}-vscan
%description vscan-antivir
A vfs-module for samba to implement on-access scanning using the
Antivir antivirus scanner daemon.
%endif


%if %build_clamav
%package vscan-clamav
Summary: On-access virus scanning for samba using Clam Antivirus
Group: System/Servers
Requires: %{name}-server = %{epoch}:%{version}
Provides: %{name}-vscan
Requires: clamd
%description vscan-clamav
A vfs-module for samba to implement on-access scanning using the
Clam antivirus scanner daemon.
%endif

%if %build_fprot
%package vscan-fprot
Summary: On-access virus scanning for samba using FPROT
Group: System/Servers
Requires: %{name}-server = %{epoch}:%{version}
Provides: %{name}-vscan
%description vscan-fprot
A vfs-module for samba to implement on-access scanning using the
FPROT antivirus software (which must be installed to use this).
%endif

%if %build_fsav
%package vscan-fsecure
Summary: On-access virus scanning for samba using F-Secure
Group: System/Servers
Requires: %{name}-server = %{epoch}:%{version}
Provides: %{name}-vscan
%description vscan-fsecure
A vfs-module for samba to implement on-access scanning using the
F-Secure antivirus software (which must be installed to use this).
%endif

%if %build_icap
%package vscan-icap
Summary: On-access virus scanning for samba using ICAP
Group: System/Servers
Requires: %{name}-server = %{epoch}:%{version}
Provides: %{name}-icap
%description vscan-icap
A vfs-module for samba to implement on-access scanning using
ICAP-capable antivirus software.
%endif

%if %build_kaspersky
%package vscan-kaspersky
Summary: On-access virus scanning for samba using Kaspersky
Group: System/Servers
Requires: %{name}-server = %{epoch}:%{version}
Provides: %{name}-vscan
%description vscan-kaspersky
A vfs-module for samba to implement on-access scanning using the
Kaspersky antivirus software (which must be installed to use this).
%endif

%if %build_mks
%package vscan-mks
Summary: On-access virus scanning for samba using MKS
Group: System/Servers
Requires: %{name}-server = %{epoch}:%{version}
Provides: %{name}-vscan
%description vscan-mks
A vfs-module for samba to implement on-access scanning using the
MKS antivirus software (which must be installed to use this).
%endif

%if %build_nai
%package vscan-nai
Summary: On-access virus scanning for samba using NAI McAfee
Group: System/Servers
Requires: %{name}-server = %{epoch}:%{version}
Provides: %{name}-vscan
%description vscan-nai
A vfs-module for samba to implement on-access scanning using the
NAI McAfee antivirus software (which must be installed to use this).
%endif

%if %build_openav
%package vscan-openav
Summary: On-access virus scanning for samba using OpenAntivirus
Group: System/Servers
Requires: %{name}-server = %{epoch}:%{version}
Provides: %{name}-vscan
%description vscan-openav
A vfs-module for samba to implement on-access scanning using the
OpenAntivirus antivirus software (which must be installed to use this).
%endif

%if %build_sophos
%package vscan-sophos
Summary: On-access virus scanning for samba using Sophos
Group: System/Servers
Requires: %{name}-server = %{epoch}:%{version}
Provides: %{name}-vscan
%description vscan-sophos
A vfs-module for samba to implement on-access scanning using the
Sophos antivirus software (which must be installed to use this).
%endif

%if %build_symantec
%package vscan-symantec
Summary: On-access virus scanning for samba using Symantec
Group: System/Servers
Requires: %{name}-server = %{epoch}:%{version}
Provides: %{name}-vscan
Autoreq: 0
%description vscan-symantec
A vfs-module for samba to implement on-access scanning using the
Symantec antivirus software (which must be installed to use this).
%endif


%if %build_trend
%package vscan-trend
Summary: On-access virus scanning for samba using Trend
Group: System/Servers
Requires: %{name}-server = %{epoch}:%{version}
Provides: %{name}-vscan
%description vscan-trend
A vfs-module for samba to implement on-access scanning using the
Trend antivirus software (which must be installed to use this).
%endif

%package domainjoin-gui
Summary: Domainjoin GUI
Requires: samba-common = %{epoch}:%{version}
Group: System/Configuration/Other

%description domainjoin-gui
The samba-domainjoin-gui package includes a domainjoin gtk application.

%prep

# Allow users to query build options with --with options:
#%%define opt_status(%1)	%(echo %{1})
%if %{?_with_options:1}%{!?_with_options:0}
%define opt_status(%{1})	%(if [ %{1} -eq 1 ];then echo enabled;else echo disabled;fi)
#exit 1
%{error: }
%{error:Build options available are:}
%{error:--with[out] system   Build as the system samba package [or as samba3]}
%{error:--with[out] acl      Build with support for file ACLs          - %opt_status %build_acl}
%{error:--with[out] winbind  Build with Winbind support                - %opt_status %build_winbind}
%{error:--with[out] wins     Build with WINS name resolution support   - %opt_status %build_wins}
%{error:--with[out] ldap     Build with legacy (samba2) LDAP support   - %opt_status %build_ldap}
%{error:--with[out] ads      Build with Active Directory support       - %opt_status %build_ads}
%{error:--with[out] mysql    Build MySQL passdb backend                - %opt_status %build_mysql}
%{error:--with[out] pgsql    Build PostgreSQL passdb backend           - %opt_status %build_pgsql}
%{error:--with[out] scanners Enable on-access virus scanners           - %opt_status %build_scanners}
%{error:--with[out] test     Enable testing and benchmarking tools     - %opt_status %build_test}
%{error: }
%else
#{error: }
#{error: This rpm has build options available, use --with options to see them}
#{error: }
echo -e "\n This rpm has build options available, use --with options to see them\n" >&2
sleep 1
%endif

%if %{?_with_options:1}%{!?_with_options:0} && %build_scanners
#{error:--with scanners enables the following:%{?build_clamav:clamav,}%{?build_icap:icap,}%{?build_fprot:fprot,}%{?build_mks:mks,}%{?build_openav:openav,}%{?build_sophos:sophos,}%{?build_symantec:symantec,}%{?build_trend:trend}}
%{error:--with scanners enables the following: antivir,clamav,icap,fprot,fsav,mks,nai,openav,sophos,trend}
%{error: }
%{error:To enable others (requires development libraries for the scanner):}
%{error:--with symantec           Enable on-access scanning with Symantec        - %opt_status %build_symantec}
%{error: }
%endif

%if %{?_with_options:1}%{!?_with_options:0}
clear
exit 1
%endif


%if %build_non_default
RPM_EXTRA_OPTIONS="\
%{?_with_system: --with system}\
%{?_without_system: --without system}\
%{?_with_acl: --with acl}\
%{?_without_acl: --without acl}\
%{?_with_winbind: --with winbind}\
%{?_without_winbind: --without winbind}\
%{?_with_wins: --with wins}\
%{?_without_wins: --without wins}\
%{?_with_ldap: --with ldap}\
%{?_without_ldap: --without ldap}\
%{?_with_ads: --with ads}\
%{?_without_ads: --without ads}\
%{?_with_scanners: --with scanners}\
%{?_without_scanners: --without scanners}\
"
echo "Building a non-default rpm with the following command-line arguments:"
echo "$RPM_EXTRA_OPTIONS"
echo "This rpm was built with non-default options, thus, to build ">%{SOURCE7}
echo "an identical rpm, you need to supply the following options">>%{SOURCE7}
echo "at build time: $RPM_EXTRA_OPTIONS">>%{SOURCE7}
echo -e "\n%{name}-%{version}-%{release}\n">>%{SOURCE7}
%else
echo "This rpm was built with default options">%{SOURCE7}
echo -e "\n%{name}-%{version}-%{release}\n">>%{SOURCE7}
%endif


#Try and validate signatures on source:
VERIFYSOURCE=%{SOURCE0}
VERIFYSOURCE=${VERIFYSOURCE%%.gz}
gzip -dc %{SOURCE0} > $VERIFYSOURCE
%check_sig %{SOURCE98} %{SOURCE99} $VERIFYSOURCE

%if %build_vscan
%setup -q -a 8 -n %{pkg_name}-%{source_ver}
%else
%setup -q -n %{pkg_name}-%{source_ver}
%endif
# Version specific patches: current version
%if !%have_pversion
echo "Applying patches for current version: %{ver}"
%patch11 -p1 -b .mdk
pushd source3
popd
%patch30 -p1 -b .checkflags
#patch31 -p1 -b .nss_wins_log
%patch33 -p1 -b .netapi_link

# patches from cvs/samba team
pushd source3
popd
%else
# Version specific patches: upcoming version
echo "Applying patches for new versions: %{pversion}"
%endif

# Limbo patches
%if %have_pversion && %have_pre
echo "Appling patches which should only be applied to prereleases"
%endif

cp %{SOURCE7} .

# Make a copy of examples so that we have a clean one for doc:
cp -a examples examples.bin

%if %build_vscan
cp -a %{vscandir} %{vfsdir}
#fix stupid directory names:
#mv %{vfsdir}/%{vscandir}/openantivirus %{vfsdir}/%{vscandir}/oav
# Inline replacement of config dir
for av in antivir clamav fprotd fsav icap kavp mksd mcdaemon oav sophos symantec trend
 do
	[ -e %{vfsdir}/%{vscandir}/*/vscan-$av.h ] && perl -pi -e \
	's,^#define PARAMCONF "/etc/samba,#define PARAMCONF "/etc/%{name},' \
	%{vfsdir}/%{vscandir}/*/vscan-$av.h
done
#Inline edit vscan header:
perl -pi -e 's/^# define SAMBA_VERSION_MAJOR 2/# define SAMBA_VERSION_MAJOR 3/g;s/# define SAMBA_VERSION_MINOR 2/# define SAMBA_VERSION_MINOR 0/g' %{vfsdir}/%{vscandir}/include/vscan-global.h
# dunno why samba-vscan keeps copmatability with ancient versions
# of samba but breaks  on samba versions with alpha chars in the name ...
perl -pi -e 's/SAMBA_VERSION_MAJOR==2 && SAMBA_VERSION_RELEASE>=4/SAMBA_VERSION_MAJOR==2/g' %{vfsdir}/%{vscandir}/*/vscan-*.c
%endif

# Edit some files when not building system samba:
%if !%build_system
perl -pi -e 's/%{pkg_name}/%{name}/g' source3/auth/pampass.c
%endif

#remove cvs internal files from docs:
find docs examples -name '.cvsignore' -exec rm -f {} \;

#make better doc trees:
chmod -R a+rX examples docs *Manifest* README  Roadmap COPYING
mkdir -p clean-docs/samba-doc
cp -a examples docs clean-docs/samba-doc
mv -f clean-docs/samba-doc/examples/libsmbclient clean-docs/
rm -Rf clean-docs/samba-doc/docs/{docbook,manpages,htmldocs,using_samba}
#ln -s %{_datadir}/swat%{samba_major}/using_samba clean-docs/samba-doc/docs/using_samba
mkdir clean-docs/samba-doc/docs/htmldocs
cp docs/htmldocs/*.{html,css} clean-docs/samba-doc/docs/htmldocs
ln -sf %{_datadir}/swat%{samba_major}/help/{Samba3-ByExample,Samba3-HOWTO,Samba3-Developers-Guide,using_samba,manpages} clean-docs/samba-doc/docs/htmldocs/

%build
%serverbuild
(cd source3
CFLAGS="`echo "$RPM_OPT_FLAGS"|sed -e 's/ -g / /g'` -DLDAP_DEPRECATED"
%if %gcc331
CFLAGS=`echo "$CFLAGS"|sed -e 's/-O2/-O/g'`
%endif
./autogen.sh
# Don't use --with-fhs now, since it overrides libdir, it sets configdir, 
# lockdir,piddir logfilebase,privatedir and swatdir
%configure      --prefix=%{_prefix} \
                --sysconfdir=%{_sysconfdir}/%{name} \
                --localstatedir=/var \
                --with-modulesdir=%{_libdir}/%{name} \
                --with-privatedir=%{_sysconfdir}/%{name} \
		--with-lockdir=/var/cache/%{name} \
		--with-piddir=/var/run \
                --with-swatdir=%{_datadir}/swat%{samba_major} \
                --with-configdir=%{_sysconfdir}/%{name} \
		--with-logfilebase=/var/log/%{name} \
                --with-pammodulesdir=%{_lib}/security/ \
                --with-rootsbindir=/bin \
%if %build_talloc
		--with-libtalloc=yes \
%else
		--enable-external-libtalloc=yes \
%endif
%if %build_tdb
		--with-libtdb = yes \
%else
		--enable-external-libtdb=yes \
%endif		
%if %build_ctdb
		--with-cluster-support \
%endif
%if !%build_ads
		--with-ads=no	\
%endif
                --with-automount \
                --with-pam \
                --with-pam_smbpass \
		--with-aio-support \
%if %build_ldap
		--with-ldapsam \
%endif
                --with-syslog \
                --with-quotas \
                --with-utmp \
%if %build_acl
		--with-acl-support      \
%endif
		--with-shared-modules=idmap_rid,idmap_ad \
		--enable-avahi \
		--with-dnsupdate \
		--program-suffix=%{samba_major} \
#		--with-expsam=%build_expsam \
#		--with-shared-modules=pdb_ldap,idmap_ldap \
#		--with-manpages-langs=en,ja,pl	\
#_if !%build_system
#                --with-smbwrapper \
#_endif		
		--without-nis
#                --with-fhs \

# Remove -Wl,--no-undefined for plugins:
grep ^LDSHFLAGS_MODULES Makefile
perl -pi -e 'if ( m/^LDSHFLAGS_MODULES/ ) { $_ =~ s/-Wl,--no-undefined//g;};' Makefile
grep ^LDSHFLAGS_MODULES Makefile

#Should be a patch instead?
%if !%build_talloc
perl -pi -e 's,-I./lib/talloc,,g;s,bin/libtalloc.so,,g;s,^(installlibs:: )installlibtalloc,$1,g' Makefile
%endif
%if !%build_tdb
perl -pi -e 's,-I./lib/tdb/include,,g;s,bin/libtdb.so,,g;s,^(installlibs:: )installlibtdb,$1,g' Makefile
%endif
%if !%build_ldb
perl -pi -e 's,\$\(BIN_PROGS4\),,g' Makefile
%endif

perl -pi -e 's|-Wl,-rpath,%{_libdir}||g;s|-Wl,-rpath -Wl,%{_libdir}||g' Makefile

make proto_exists || :
%make all libsmbclient smbfilter wins %{?_with_test: torture debug2html bin/log2pcap} bin/smbget
make -C lib/netapi/examples
)

%if %build_vscan
echo -e "\n\nBuild antivirus VFS modules\n\n"
pushd %{vfsdir}/%{vscandir}
%configure
#sed -i -e 's,openantivirus,oav,g' Makefile
sed -i -e 's,^\(.*clamd socket name.*=\).*,\1 /var/lib/clamav/clamd.socket,g' clamav/vscan-clamav.conf
make
popd
%endif

# Build antivirus vfs objects
%if %build_symantec
echo "Building Symantec"
make -C %{vfsdir}/%{vscandir} symantec
%endif

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

#Ensure all docs are readable
chmod a+r docs -R

# Any entries here mean samba makefile is *really* broken:
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_datadir}
mkdir -p %{buildroot}%{_libdir}/%{name}/vfs

(cd source3
make DESTDIR=%{buildroot} install installclientlib installmodules)

# we ship docs in the docs supackage, and lik it into swat, delete the extra copy:
rm -Rf %{buildroot}/%{_datadir}/swat/using_samba

#install -m755 source/bin/smbget %{buildroot}/%{_bindir}


#need to stay
mkdir -p %{buildroot}/{sbin,bin}
mkdir -p %{buildroot}%{_sysconfdir}/{logrotate.d,pam.d,xinetd.d}
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/var/cache/%{name}
mkdir -p %{buildroot}/var/log/%{name}
mkdir -p %{buildroot}/var/run/%{name}
mkdir -p %{buildroot}/var/spool/%{name}
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/{netlogon,profiles,printers}
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/printers/{W32X86,WIN40,W32ALPHA,W32MIPS,W32PPC}
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/codepages/src
mkdir -p %{buildroot}/%{_lib}/security
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{name}/vfs
mkdir -p %{buildroot}%{_datadir}/%{name}/scripts

install -m755 source3/bin/lib*.a %{buildroot}%{_libdir}/

# smbsh forgotten
#install -m 755 source/bin/smbsh %{buildroot}%{_bindir}/

%if %build_vscan
%makeinstall_std -C %{vfsdir}/%{vscandir}
install -m 644 %{vfsdir}/%{vscandir}/*/vscan-*.conf %{buildroot}/%{_sysconfdir}/%{name}
%endif
	
#libnss_* still not handled by make:
# Install the nsswitch library extension file
for i in wins winbind; do
  install -m755 nsswitch/libnss_${i}.so %{buildroot}/%{_lib}/libnss_${i}.so
done
# Make link for wins and winbind resolvers
( cd %{buildroot}/%{_lib}; ln -s libnss_wins.so libnss_wins.so.2; ln -s libnss_winbind.so libnss_winbind.so.2)
install -d %{buildroot}/%{_libdir}/krb5/plugins
install -m755 source3/bin/winbind_krb5_locator.so %{buildroot}/%{_libdir}/krb5/plugins

install -m 755 source3/lib/netapi/examples/bin/netdomjoin-gui %{buildroot}/%{_sbindir}/netdomjoin-gui
mkdir -p %{buildroot}%{_datadir}/pixmaps/%{name}
install -m 644 source3/lib/netapi/examples/netdomjoin-gui/samba.ico %{buildroot}/%{_datadir}/pixmaps/%{name}/samba.ico
install -m 644 source3/lib/netapi/examples/netdomjoin-gui/logo.png %{buildroot}/%{_datadir}/pixmaps/%{name}/logo.png
install -m 644 source3/lib/netapi/examples/netdomjoin-gui/logo-small.png %{buildroot}/%{_datadir}/pixmaps/%{name}/logo-small.png

%if %{build_test}
for i in {%{testbin}};do
  #install -m755 source/bin/${i} %{buildroot}/%{_bindir}/${i}%{samba_major}
done
%endif

# Install other stuff

#        install -m644 examples/VFS/recycle/recycle.conf %{buildroot}%{_sysconfdir}/samba/
        install -m644 %{SOURCE20} %{buildroot}%{_sysconfdir}/%{name}/smbusers
        install -m755 %{SOURCE21} %{buildroot}/%{_bindir}
        #install -m755 %{SOURCE22} %{buildroot}/usr/bin
        install -m755 %{SOURCE23} %{buildroot}/%{_bindir}
        install -m755 %{SOURCE24} %{buildroot}/%{_initrddir}/smb%{samba_major}
        install -m755 %{SOURCE24} %{buildroot}/%{_sbindir}/%{name}
	install -m755 %{SOURCE25} %{buildroot}/%{_initrddir}/winbind
	install -m755 %{SOURCE25} %{buildroot}/%{_sbindir}/winbind
#	install -m755 %{SOURCE26} %{buildroot}/%{_initrddir}/wrepld%{samba_major}
        install -m644 %{SOURCE28} %{buildroot}/%{_sysconfdir}/pam.d/%{name}
	install -m644 %{SOURCE29} %{buildroot}/%{_sysconfdir}/pam.d/system-auth-winbind
#
        install -m644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

# install pam_winbind.conf sample file
mkdir -p %{buildroot}%{_sysconfdir}/security
install -m 0644 examples/pam_winbind/pam_winbind.conf %{buildroot}%{_sysconfdir}/security/pam_winbind.conf

install -m755 examples/LDAP/convertSambaAccount %{buildroot}/%{_datadir}/%{name}/scripts/

# make a conf file for winbind from the default one:
	cat %{SOURCE30}|sed -e  's/^;  winbind/  winbind/g;s/^;  obey pam/  obey pam/g;s/   printer admin = @adm/#  printer admin = @adm/g; s/^#   printer admin = @"D/   printer admin = @"D/g;s/^;   password server = \*/   password server = \*/g;s/^;  template/  template/g; s/^   security = user/   security = domain/g' > packaging/Mandriva/smb-winbind.conf
        install -m644 packaging/Mandriva/smb-winbind.conf %{buildroot}/%{_sysconfdir}/%{name}/smb-winbind.conf

# Some inline fixes for smb.conf for non-winbind use
install -m644 %{SOURCE30} %{buildroot}/%{_sysconfdir}/%{name}/smb.conf
cat %{SOURCE30} | \
sed -e 's/^;   printer admin = @adm/   printer admin = @adm/g' >%{buildroot}/%{_sysconfdir}/%{name}/smb.conf
%if %build_cupspc
perl -pi -e 's/printcap name = lpstat/printcap name = cups/g' %{buildroot}/%{_sysconfdir}/%{name}/smb.conf
perl -pi -e 's/printcap name = lpstat/printcap name = cups/g' %{buildroot}/%{_sysconfdir}/%{name}/smb-winbind.conf
%endif

#%if !%build_system
# Fix script paths in smb.conf
#perl -pi -e 's,%{_datadir}/samba,%{_datadir}/%{name},g' %{buildroot}/%{_sysconfdir}/%{name}/smb*.conf
#%endif


        echo 127.0.0.1 localhost > %{buildroot}/%{_sysconfdir}/%{name}/lmhosts

# Link smbspool to CUPS (does not require installed CUPS)

        mkdir -p %{buildroot}/%{_prefix}/lib/cups/backend
        ln -s %{_bindir}/smbspool%{alternative_major} %{buildroot}/%{_prefix}/lib/cups/backend/smb%{alternative_major}

# xinetd support

        mkdir -p %{buildroot}/%{_sysconfdir}/xinetd.d
        install -m644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/xinetd.d/swat%{samba_major}

# menu support

mkdir -p %{buildroot}/%{_datadir}/applications
cat > %{buildroot}/%{_datadir}/applications/mandriva-%{name}-swat.desktop << EOF
[Desktop Entry]
Name=Samba Configuration (SWAT)
Comment=The Swat Samba Administration Tool
Exec=www-browser http://localhost:901/
Icon=swat%{samba_major}
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Configuration-Networking;
EOF

mkdir -p %{buildroot}%{_liconsdir} %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}

# install html man pages for swat
install -d %{buildroot}/%{_datadir}/swat%{samba_major}/help/manpages
#install -m644 docs/htmldocs/manpages-3/* %{buildroot}/%{_datadir}/swat%{samba_major}/help/manpages

install %{SOURCE4} %{buildroot}%{_liconsdir}/swat%{samba_major}.png
install %{SOURCE5} %{buildroot}%{_iconsdir}/swat%{samba_major}.png
install %{SOURCE6} %{buildroot}%{_miconsdir}/swat%{samba_major}.png

install %{SOURCE10} %{buildroot}%{_datadir}/%{name}/scripts/print-pdf
install %{SOURCE11} %{buildroot}%{_datadir}/%{name}/scripts/smb-migrate

# Fix configs when not building system samba:

#Client binaries will have suffixes while we use alternatives, even
# if we are system samba
%if !%build_system || %build_alternatives
for OLD in %{buildroot}/%{_bindir}/{%{clientbin},eventlogadm} %{buildroot}/%{_prefix}/lib/cups/backend/smb
do
    NEW=`echo ${OLD}%{alternative_major}`
    [ -e $OLD ] && mv -f $OLD $NEW
done
for OLD in %{buildroot}/%{_mandir}/man?/{%{clientbin},eventlogadm}* 
do
    if [ -e $OLD ]
    then
        BASE=`perl -e '$_="'${OLD}'"; m,(%buildroot)(.*?)(\.[0-9]),;print "$1$2\n";'`
        EXT=`echo $OLD|sed -e 's,'${BASE}',,g'`
        NEW=`echo ${BASE}%{alternative_major}${EXT}`
        mv $OLD $NEW
    fi
done		
%endif
# Server/common binaries are versioned only if not system samba:
%if !%build_system
for OLD in %{buildroot}/%{_bindir}/{%{commonbin}} %{buildroot}/%{_bindir}/{%{serverbin}%{?serverldbbin:,%serverldbbin}} %{buildroot}/%{_sbindir}/{%{serversbin},swat}
do
    NEW=`echo ${OLD}%{alternative_major}`
    mv $OLD $NEW -f ||:
done
# And the man pages too:
for OLD in %{buildroot}/%{_mandir}/man?/{%{commonbin},%{serverbin}%{?serverldbbin:,%serverldbbin},%{serversbin},swat,{%testbin},smb.conf,lmhosts}*
do
    if [ -e $OLD ]
    then
        BASE=`perl -e '$_="'${OLD}'"; m,(%buildroot)(.*?)(\.[0-9]),;print "$1$2\n";'`
#        BASE=`perl -e '$name="'${OLD}'"; print "",($name =~ /(.*?)\.[0-9]/), "\n";'`
	EXT=`echo $OLD|sed -e 's,'${BASE}',,g'`
	NEW=`echo ${BASE}%{samba_major}${EXT}`
	mv $OLD $NEW
    fi
done		
# Replace paths in config files and init scripts:
for i in smb ;do
	perl -pi -e 's,/subsys/'$i',/subsys/'$i'%{samba_major},g' %{buildroot}/%{_initrddir}/${i}%{samba_major}
done
for i in %{_sysconfdir}/%{name}/smb.conf %{_initrddir}/smb%{samba_major} %{_sbindir}/%{name} %{_initrddir}/winbind /%{_sysconfdir}/logrotate.d/%{name} /%{_sysconfdir}/xinetd.d/swat%{samba_major} %{_initrddir}/wrepld%{samba_major}; do
	perl -pi -e 's,/%{pkg_name},/%{name},g; s,smbd,%{_sbindir}/smbd%{samba_major},g; s,nmbd,%{_sbindir}/nmbd%{samba_major},g; s,/usr/sbin/swat,%{_sbindir}/swat%{samba_major},g;s,wrepld,%{_sbindir}/wrepld%{samba_major},g' %{buildroot}/$i;
done
# Fix xinetd file for swat:
perl -pi -e 's,/usr/sbin,%{_sbindir},g' %{buildroot}/%{_sysconfdir}/xinetd.d/swat%{samba_major}
%endif

#Clean up unpackaged files:
#for i in %{_bindir}/pam_smbpass.so %{_bindir}/smbwrapper.so;do
#rm -f %{buildroot}/$i
#done
# the binary gets removed ... but not the man page ...
rm -f %{buildroot}/%{_mandir}/man1/testprns*

# (sb) make a smb.conf.clean we can use for the merge, since an existing
# smb.conf won't get overwritten
cp %{buildroot}/%{_sysconfdir}/%{name}/smb.conf %{buildroot}/%{_datadir}/%{name}/smb.conf.clean

# (sb) leave a README.mdk.conf to explain what has been done
cat << EOF > %{buildroot}/%{_datadir}/%{name}/README.mdk.conf
In order to facilitate upgrading an existing samba install, and merging
previous configuration data with any new syntax used by samba3, a merge
script has attempted to combine your local configuration data with the
new conf file format.  The merged data is in smb.conf, with comments like

	# *** merged from original smb.conf: ***

near the additional entries.  Any local shares should have been appended to
smb.conf.  A log of what took place should be in: 

	/var/log/samba/smb-migrate.log

A clean samba3 smb.conf is in /usr/share/samba, named smb.conf.clean.
Your original conf should be /etc/samba/smb.conf.tomerge.

The actual merge script is /usr/share/samba/scripts/smb-migrate.

EOF

# Development pkgconfig files

# 1. Generate the .pc files that are not done automatically
# (NB: This does not work when done at the same time as configure above)
for i in  \
%if %build_talloc
talloc \
%endif
%if %build_tdb
tdb \
%endif
; do
	pushd lib/$i
	./autogen.sh -V && ./configure --prefix=%{_prefix} --libdir=%{_libdir}
	popd
	install -m 644 lib/$i/$i.pc %{buildroot}%{_libdir}/pkgconfig/
done

# 2. Install them
for i in smbclient smbsharemodes netapi wbclient; do
	install -m 644 source3/pkgconfig/$i.pc %{buildroot}%{_libdir}/pkgconfig/
done

%if !%build_ldb
rm -f %{buildroot}/%{_bindir}/ldb*
rm -fr %{buildroot}%{_mandir}/man1/ldbadd.1
rm -fr %{buildroot}%{_mandir}/man1/ldbdel.1
rm -fr %{buildroot}%{_mandir}/man1/ldbedit.1
rm -fr %{buildroot}%{_mandir}/man1/ldbmodify.1
rm -fr %{buildroot}%{_mandir}/man1/ldbrename.1
rm -fr %{buildroot}%{_mandir}/man1/ldbsearch.1
%endif

%if %{build_test}
rm -fr %{buildroot}%{_mandir}/man1/log2pcap*.1*
%else
rm -fr %{buildroot}%{_mandir}/man1/vfstest%{samba_major}*.1*
rm -fr %{buildroot}%{_mandir}/man1/log2pcap*.1*
%endif

rm -fr %{buildroot}%{_mandir}/man8/tdb*.8*

%if %build_winbind
%find_lang pam_winbind
%endif
%find_lang net

%ifarch alpha
rm -f %{_bindir}/smb*m*nt%{samba_major}
rm -f %{_mandir}/man8/smb*m*nt*.8*
%endif

%if !%build_system
rm -f %{_libdir}/libsmbclient.so.*
rm -f %{_includedir}/*
rm -f %{_libdir}/libsmbclient.so
rm -f %{_libdir}/lib*.a
rm -f %{_mandir}/man8/libsmbclient.8*
rm -f %{_libdir}/pkgconfig/smbclient.pc
%endif

%if %build_vscan
rm -f %{buildroot} %{_libdir}/%{name}/vfs/vscan*.so

%if !%build_antivir
rm -f %{buildroot}%{_libdir}/%{name}/vfs/vscan-antivir.so
rm -f %{buildroot}%{_sysconfdir}/%{name}/vscan-antivir.conf
%endif

%if !%build_clamav
rm -f %{buildroot}%{_libdir}/%{name}/vfs/vscan-clamav.so
rm -f %{buildroot}%{_sysconfdir}/%{name}/vscan-clamav.conf
%endif

%if !%build_fprot
rm -f %{buildroot}%{_libdir}/%{name}/vfs/vscan-fprotd.so
rm -f %{buildroot}%{_sysconfdir}/%{name}/vscan-fprotd.conf
%endif

%if !%build_fsav
rm -f %{buildroot}%{_libdir}/%{name}/vfs/vscan-fsav.so
rm -f %{buildroot}%{_sysconfdir}/%{name}/vscan-fsav.conf
%endif

%if !%build_icap
rm -f %{buildroot}%{_libdir}/%{name}/vfs/vscan-icap.so
rm -f %{buildroot}%{_sysconfdir}/%{name}/vscan-icap.conf
%endif

%if !%build_kaspersky
rm -f %{buildroot}%{_libdir}/%{name}/vfs/vscan-kavp.so
rm -f %{buildroot}%{_sysconfdir}/%{name}/vscan-kavp.conf
%endif

%if !%build_mks
rm -f %{buildroot}%{_libdir}/%{name}/vfs/vscan-mksd.so
rm -f %{buildroot}%{_sysconfdir}/%{name}/vscan-mks*.conf
%endif

%if !%build_nai
rm -f %{buildroot}%{_libdir}/%{name}/vfs/vscan-mcdaemon.so
rm -f %{buildroot}%{_sysconfdir}/%{name}/vscan-mcdaemon.conf
%endif

%if !%build_openav
rm -f %{buildroot}%{_libdir}/%{name}/vfs/vscan-oav.so
rm -f %{buildroot}%{_sysconfdir}/%{name}/vscan-oav.conf
%endif

%if !%build_sophos
rm -f %{buildroot}%{_libdir}/%{name}/vfs/vscan-sophos.so
rm -f %{buildroot}%{_sysconfdir}/%{name}/vscan-sophos.conf
%endif

%if !%build_symantec
rm -rf %{buildroot}%{_sysconfdir}/%{name}/vscan-symantec.conf
%endif

%if !%build_trend
rm -f %{buildroot}%{_libdir}/%{name}/vfs/vscan-trend.so
rm -f %{buildroot}%{_sysconfdir}/%{name}/vscan-trend.conf
%endif
%endif

# these are provided by ldb-utils
rm -f %{buildroot}%{_mandir}/man1/ldbadd.1*
rm -f %{buildroot}%{_mandir}/man1/ldbdel.1*
rm -f %{buildroot}%{_mandir}/man1/ldbedit.1*
rm -f %{buildroot}%{_mandir}/man1/ldbmodify.1*
rm -f %{buildroot}%{_mandir}/man1/ldbrename.1*
rm -f %{buildroot}%{_mandir}/man1/ldbsearch.1*

# these are provided by tdb-utils
rm -f %{buildroot}%{_mandir}/man8/tdbbackup.8*
rm -f %{buildroot}%{_mandir}/man8/tdbdump.8*
rm -f %{buildroot}%{_mandir}/man8/tdbtool.8*

# these are not built
rm -f %{buildroot}%{_mandir}/man1/log2pcap.1*
rm -f %{buildroot}%{_mandir}/man1/vfstest.1*

%clean
rm -rf %{buildroot}

%post server

%_post_service smb%{samba_major}
#%_post_service wrepld%{samba_major}

# Add a unix group for samba machine accounts
groupadd -frg 421 machines

# Migrate tdb's from /var/lock/samba (taken from official samba spec file):
for i in /var/lock/samba/*.tdb
do
if [ -f $i ]; then
	newname=`echo $i | sed -e's|var\/lock\/samba|var\/cache\/samba|'`
	echo "Moving $i to $newname"
	mv $i $newname
fi
done

%post common
# Basic migration script for pre-2.2.1 users,
# since smb config moved from /etc to %{_sysconfdir}/samba

# Let's create a proper %{_sysconfdir}/samba/smbpasswd file
[ -f %{_sysconfdir}/%{name}/smbpasswd ] || {
	echo "Creating password file for samba..."
	touch %{_sysconfdir}/%{name}/smbpasswd
}

# And this too, in case we don't have smbd to create it for us
[ -f /var/cache/%{name}/unexpected.tdb ] || {
	touch /var/cache/%{name}/unexpected.tdb
}

# Let's define the proper paths for config files
perl -pi -e 's/(\/etc\/)(smb)/\1%{name}\/\2/' %{_sysconfdir}/%{name}/smb.conf

# Fix the logrotate.d file from smb and nmb to smbd and nmbd
if [ -f %{_sysconfdir}/logrotate.d/samba ]; then
        perl -pi -e 's/smb /smbd /' %{_sysconfdir}/logrotate.d/samba
        perl -pi -e 's/nmb /nmbd /' %{_sysconfdir}/logrotate.d/samba
fi

# And not loose our machine account SID
[ -f %{_sysconfdir}/MACHINE.SID ] && mv -f %{_sysconfdir}/MACHINE.SID %{_sysconfdir}/%{name}/ ||:

# FIXME: Can be removed in mandriva ?
%triggerpostun common -- samba-common < 3.0.1-3mdk
# (sb) merge any existing smb.conf with new syntax file
if [ $1 = 2 ]; then
	# (sb) save existing smb.conf for merge
	echo "Upgrade: copy smb.conf to smb.conf.tomerge for merging..."
	cp -f %{_sysconfdir}/%{name}/smb.conf %{_sysconfdir}/%{name}/smb.conf.tomerge
	echo "Upgrade: merging previous smb.conf..."
	if [ -f %{_datadir}/%{name}/smb.conf.clean ]; then
		cp %{_datadir}/%{name}/smb.conf.clean %{_sysconfdir}/%{name}/smb.conf
		cp %{_datadir}/%{name}/README.mdk.conf %{_sysconfdir}/%{name}/
		%{_datadir}/%{name}/scripts/smb-migrate commit
	fi
fi

%postun common
if [ -f %{_sysconfdir}/%{name}/README.mdk.conf ];then rm -f %{_sysconfdir}/%{name}/README.mdk.conf;fi

%if %build_winbind
%post winbind
if [ $1 = 1 ]; then
    /sbin/chkconfig winbind on
    cp -af %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/nsswitch.conf.rpmsave
    cp -af %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/nsswitch.conf.rpmtemp
    for i in passwd group;do
        grep ^$i %{_sysconfdir}/nsswitch.conf |grep -v 'winbind' >/dev/null
        if [ $? = 0 ];then
            echo "Adding a winbind entry to the $i section of %{_sysconfdir}/nsswitch.conf"
            awk '/^'$i'/ {print $0 " winbind"};!/^'$i'/ {print}' %{_sysconfdir}/nsswitch.conf.rpmtemp >%{_sysconfdir}/nsswitch.conf;
	    cp -af %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/nsswitch.conf.rpmtemp
        else
            echo "$i entry found in %{_sysconfdir}/nsswitch.conf"
        fi
    done
    if [ -f %{_sysconfdir}/nsswitch.conf.rpmtemp ];then rm -f %{_sysconfdir}/nsswitch.conf.rpmtemp;fi
fi

%preun winbind
if [ $1 = 0 ]; then
	echo "Removing winbind entries from %{_sysconfdir}/nsswitch.conf"
	perl -pi -e 's/ winbind//' %{_sysconfdir}/nsswitch.conf

	/sbin/chkconfig winbind reset
fi
%endif %build_winbind

%if %build_wins
%post -n nss_wins%{samba_major}
if [ $1 = 1 ]; then
    cp -af %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/nsswitch.conf.rpmsave
    grep '^hosts' %{_sysconfdir}/nsswitch.conf |grep -v 'wins' >/dev/null
    if [ $? = 0 ];then
        echo "Adding a wins entry to the hosts section of %{_sysconfdir}/nsswitch.conf"
        awk '/^hosts/ {print $0 " wins"};!/^hosts/ {print}' %{_sysconfdir}/nsswitch.conf.rpmsave >%{_sysconfdir}/nsswitch.conf;
    else
        echo "wins entry found in %{_sysconfdir}/nsswitch.conf"
    fi
#    else
#        echo "Upgrade, leaving nsswitch.conf intact"
fi

%preun -n nss_wins%{samba_major}
if [ $1 = 0 ]; then
	echo "Removing wins entry from %{_sysconfdir}/nsswitch.conf"
	perl -pi -e 's/ wins//' %{_sysconfdir}/nsswitch.conf
#else
#	echo "Leaving %{_sysconfdir}/nsswitch.conf intact"
fi
%endif %build_wins

%preun server

%_preun_service smb%{samba_major}
#%_preun_service wrepld%{samba_major}

#if [ $1 = 0 ] ; then
#    /sbin/chkconfig --level 35 smb reset
# Let's not loose /var/cache/samba
#
#    if [ -d /var/cache/%{name} ]; then
#      mv -f /var/cache/%{name} /var/cache/%{name}.BAK
#    fi
#fi

%post swat
if [ -f /var/lock/subsys/xinetd ]; then
        service xinetd reload >/dev/null 2>&1 || :
fi

%postun swat

# Remove swat entry from xinetd
if [ $1 = 0 -a -f %{_sysconfdir}/xinetd.conf ] ; then
rm -f %{_sysconfdir}/xinetd.d/swat%{samba_major}
	service xinetd reload &>/dev/null || :
fi

if [ "$1" = "0" -a -x /usr/bin/update-menus ]; then /usr/bin/update-menus || true ; fi

%if %build_alternatives
%post client

update-alternatives --install %{_bindir}/smbclient smbclient \
%{_bindir}/smbclient%{alternative_major} 10 \
$(for i in %{_bindir}/{%{clientbin},eventlogadm};do
j=`basename $i`
[ "$j" = "smbclient" ] || \
echo -n " --slave ${i} ${j} ${i}%{alternative_major}";done) \
$(for i in %{_mandir}/{%{client_man}};do
echo -n " --slave ${i}%{_extension} `basename $i` ${i%%.?}%{alternative_major}.${i##*.}%{_extension}";done) \
--slave %{_prefix}/lib/cups/backend/smb cups_smb %{_prefix}/lib/cups/backend/smb%{alternative_major} || \
update-alternatives --auto smbclient

%preun client
[ $1 = 0 ] && update-alternatives --remove smbclient %{_bindir}/smbclient%{alternative_major} ||:
%endif

%if %build_alternatives
%triggerpostun client -- samba-client, samba2-client
[ ! -e %{_bindir}/smbclient ] && update-alternatives --auto smbclient || :
%endif

%files server
%defattr(-,root,root)
%(for i in %{_sbindir}/{%{serversbin}}%{samba_major};do echo $i;done)
%(for i in %{_bindir}/{%{serverbin}%{?serverldbbin:,%serverldbbin}}%{samba_major};do echo $i;done)
%attr(755,root,root) /%{_lib}/security/pam_smbpass*
%dir %{_libdir}/%{name}/vfs
%{_libdir}/%{name}/vfs/*.so
%dir %{_libdir}/%{name}/pdb
%{_libdir}/%{name}/auth
#{_libdir}/%{name}/*.so
%dir %{_libdir}/%{name}/nss_info
%{_libdir}/%{name}/nss_info/rfc2307.so
%{_libdir}/%{name}/nss_info/sfu*.so

%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smbusers
%attr(-,root,root) %config(noreplace) %{_initrddir}/smb%{samba_major}
#%attr(-,root,root) %config(noreplace) %{_initrddir}/wrepld%{samba_major}
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/pam.d/%{name}
#%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/samba-slapd.include
%(for i in %{_mandir}/man?/{%{serverbin}%{?serverldbbin:,%serverldbbin},%{serversbin}}%{samba_major}\.[0-9]\\*;do echo $i|grep -v mkntpwd;done)
%attr(775,root,adm) %dir %{_localstatedir}/lib/%{name}/netlogon
%attr(755,root,root) %dir %{_localstatedir}/lib/%{name}/profiles
%attr(755,root,root) %dir %{_localstatedir}/lib/%{name}/printers
%attr(2775,root,adm) %dir %{_localstatedir}/lib/%{name}/printers/*
%attr(1777,root,root) %dir /var/spool/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/scripts
%attr(0755,root,root) %{_datadir}/%{name}/scripts/print-pdf
%attr(0755,root,root) %{_datadir}/%{name}/scripts/convertSambaAccount
%{_mandir}/man8/idmap_*.8*
%{_mandir}/man8/vfs_*.8*

%files doc
%defattr(-,root,root)
%doc README COPYING Manifest Read-Manifest-Now
%doc WHATSNEW.txt Roadmap
%doc README.%{name}-mandriva-rpm
%doc clean-docs/samba-doc/docs/*
%doc clean-docs/samba-doc/examples
#%attr(-,root,root) %{_datadir}/swat%{samba_major}/using_samba/
%attr(-,root,root) %{_datadir}/swat%{samba_major}/help/

%files swat
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xinetd.d/swat%{samba_major}
#%attr(-,root,root) /sbin/*
%{_sbindir}/swat%{samba_major}
%{_datadir}/applications/mandriva-%{name}-swat.desktop
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_iconsdir}/*.png
#%attr(-,root,root) %{_datadir}/swat%{samba_major}/help/
%attr(-,root,root) %{_datadir}/swat%{samba_major}/images/
%attr(-,root,root) %{_datadir}/swat%{samba_major}/include/
%lang(ja) %{_datadir}/swat%{samba_major}/lang/ja
%lang(tr) %{_datadir}/swat%{samba_major}/lang/tr
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
#%doc swat/README

%files client
%defattr(-,root,root)
%(for i in %{_bindir}/{%{clientbin},eventlogadm}%{alternative_major};do echo $i;done)
%(for i in %{_mandir}/man?/{%{clientbin}}%{alternative_major}.\\?.\\*;do echo $i|grep -v smbprint;done)
#xclude %{_mandir}/man?/smbget*
%{_mandir}/man5/smbgetrc%{alternative_major}.5*
%ifnarch alpha
#(for i in /sbin/{%{client_sbin}}%{alternative_major};do echo $i|grep -v "smb.*m.*nt";done)
%endif
%{_mandir}/man8/eventlogadm3.8*
# Link of smbspool to CUPS
%{_prefix}/lib*/cups/backend/smb%{alternative_major}

%files common -f net.lang
%defattr(-,root,root)
%dir /var/cache/%{name}
%dir /var/log/%{name}
%dir /var/run/%{name}
%(for i in %{_bindir}/{%{commonbin}}%{samba_major};do echo $i;done)
%(for i in %{_mandir}/man?/{%{commonbin}}%{samba_major}\.[0-9]\\*;do echo $i;done)
#%{_libdir}/smbwrapper%{samba_major}.so
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.dat
%{_libdir}/%{name}/charset
#%{_libdir}/%{name}/lowcase.dat
#%{_libdir}/%{name}/valid.dat
%dir %{_sysconfdir}/%{name}
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smb.conf
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smb-winbind.conf
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/lmhosts
%dir %{_localstatedir}/lib/%{name}
%attr(-,root,root) %{_localstatedir}/lib/%{name}/codepages
%{_mandir}/man5/smb.conf*.5*
%{_mandir}/man5/lmhosts*.5*
#%{_mandir}/man7/Samba*.7*
%dir %{_datadir}/swat%{samba_major}
%attr(0750,root,adm) %{_datadir}/%{name}/scripts/smb-migrate
%attr(-,root,root) %{_datadir}/%{name}/smb.conf.clean
%attr(-,root,root) %{_datadir}/%{name}/README.mdk.conf

%if %build_winbind
%files winbind -f pam_winbind.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/security/pam_winbind.conf
%{_sbindir}/winbindd
%{_sbindir}/winbind
%{_bindir}/wbinfo
%attr(755,root,root) /%{_lib}/security/pam_winbind*
%attr(755,root,root) /%{_lib}/libnss_winbind*
%{_libdir}/%{name}/idmap
%{_libdir}/krb5/plugins/winbind_krb5_locator.so
%attr(-,root,root) %config(noreplace) %{_initrddir}/winbind
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/pam.d/system-auth-winbind*
%{_mandir}/man8/winbindd*.8*
%{_mandir}/man8/pam_winbind.8*
%{_mandir}/man5/pam_winbind.conf.5.*
%{_mandir}/man7/winbind_krb5_locator.7.*
%{_mandir}/man1/wbinfo*.1*
%endif

%if %build_wins
%files -n nss_wins%{samba_major}
%defattr(-,root,root)
%attr(755,root,root) /%{_lib}/libnss_wins.so*
%endif

%if %{build_test}
%files test
%defattr(-,root,root)
%(for i in %{_bindir}/{%{testbin}}%{samba_major};do echo $i;done)
%{_mandir}/man1/vfstest%{samba_major}*.1*
%endif

%if %build_system
%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libsmbclient.so.%{libsmbmajor}
%endif

%if %build_system
%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/libsmbclient.h
%{_libdir}/libsmbclient.so
%doc clean-docs/libsmbclient/*
%{_mandir}/man7/libsmbclient.7*
%{_libdir}/pkgconfig/smbclient.pc
%endif

%if %build_system
%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/lib*.a
%endif

%files -n %libnetapi
%defattr(-,root,root)
%{_libdir}/libnetapi.so.%{netapimajor}*

%files -n %netapidevel
%defattr(-,root,root)
%{_libdir}/libnetapi*.so
%{_includedir}/netapi.h
%{_libdir}/pkgconfig/netapi.pc

%files -n %libsmbsharemodes
%defattr(-,root,root)
%{_libdir}/libsmbsharemodes.so.%{smbsharemodesmajor}*

%files -n %smbsharemodesdevel
%defattr(-,root,root)
%{_libdir}/libsmbsharemodes.so
%{_includedir}/smb_share_modes.h
%{_libdir}/pkgconfig/smbsharemodes.pc

%if %build_talloc
%files -n %libtalloc
%defattr(-,root,root)
%{_libdir}/libtalloc.so.%{tallocmajor}*

%files -n %tallocdevel
%defattr(-,root,root)
%{_libdir}/libtalloc.so
%{_includedir}/talloc.h
%{_libdir}/pkgconfig/talloc.pc
%endif

%if %build_tdb
%files -n %libtdb
%defattr(-,root,root)
%{_libdir}/libtdb.so.%{tdbmajor}*

%files -n %tdbdevel
%defattr(-,root,root)
%{_libdir}/libtdb.so
%{_includedir}/tdb.h
%{_libdir}/pkgconfig/tdb.pc
%endif

%files -n %libwbclient
%defattr(-,root,root)
%{_libdir}/libwbclient.so.%{wbclientmajor}

%files -n %wbclientdevel
%defattr(-,root,root)
%{_libdir}/libwbclient.so
%{_includedir}/wbclient.h
%{_libdir}/pkgconfig/wbclient.pc

#%files passdb-ldap
#%defattr(-,root,root)
#%{_libdir}/%{name}/*/*ldap.so

%ifnarch alpha
%if %{build_mysql}
%files passdb-mysql
%defattr(-,root,root)
%{_libdir}/%{name}/pdb/*mysql.so
%endif
%endif

%if %{build_pgsql}
%files passdb-pgsql
%defattr(-,root,root)
%{_libdir}/%{name}/pdb/*pgsql.so
%endif

#Files for antivirus support:
%if %build_antivir
%files vscan-antivir
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-antivir.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-antivir.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif

%if %build_clamav
%files vscan-clamav
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-clamav.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-clamav.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif

%if %build_fprot
%files vscan-fprot
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-fprotd.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-fprotd.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif

%if %build_fsav
%files vscan-fsecure
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-fsav.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-fsav.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif

%if %build_icap
%files vscan-icap
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-icap.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-icap.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif

%if %build_kaspersky
%files vscan-kaspersky
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-kavp.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-kavp.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif

%if %build_mks
%files vscan-mks
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-mksd.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-mks*.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif

%if %build_nai
%files vscan-nai
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-mcdaemon.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-mcdaemon.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif

%if %build_openav
%files vscan-openav
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-oav.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-oav.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif

%if %build_sophos
%files vscan-sophos
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-sophos.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-sophos.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif

%if %build_symantec
%files vscan-symantec
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-symantec.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-symantec.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif

%if %build_trend
%files vscan-trend
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-trend.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-trend.conf
%doc %{vfsdir}/%{vscandir}/INSTALL
%endif

%files domainjoin-gui
%defattr(-,root,root)
%{_sbindir}/netdomjoin-gui
%dir %{_datadir}/pixmaps/samba
%{_datadir}/pixmaps/samba/samba.ico
%{_datadir}/pixmaps/samba/logo.png
%{_datadir}/pixmaps/samba/logo-small.png


%changelog
* Tue Jun 12 2012 Crispin Boylan <crisb@mandriva.org> 1:3.6.5-4
+ Revision: 805255
- Fix versioned requires

* Tue Jun 12 2012 Crispin Boylan <crisb@mandriva.org> 1:3.6.5-3
+ Revision: 805250
- Bump epoch to fix wbclient conflict with samba 4

  + Bernhard Rosenkraenzer <bero@bero.eu>
    - Rebuild because of libwbclient smb3<->smb4 conflict

* Sat May 05 2012 Oden Eriksson <oeriksson@mandriva.com> 3.6.5-2
+ Revision: 796622
- make the ugly macro work
- try to bump the release (fugly spec file!)
- fix deps

* Tue May 01 2012 Oden Eriksson <oeriksson@mandriva.com> 3.6.5-1
+ Revision: 794701
- 3.6.5

* Tue May 01 2012 Oden Eriksson <oeriksson@mandriva.com> 3.6.4-1
+ Revision: 794689
- sync with samba-3.6.4-1.mga2.src.rpm

* Tue May 01 2012 Oden Eriksson <oeriksson@mandriva.com> 3.5.15-1
+ Revision: 794688
- 3.5.15

* Wed Apr 11 2012 Oden Eriksson <oeriksson@mandriva.com> 3.5.14-1
+ Revision: 790289
- fix deps
- disable rpmlint "wouldn't touch it with a ten foot pole - zz top"
- 3.5.14

* Thu Dec 15 2011 Oden Eriksson <oeriksson@mandriva.com> 3.5.12-1
+ Revision: 741675
- fix deps
- 3.5.12

* Wed Aug 17 2011 Buchan Milne <bgmilne@mandriva.org> 3.5.11-1
+ Revision: 694853
- update to new version 3.5.11

* Wed Jul 27 2011 Oden Eriksson <oeriksson@mandriva.com> 3.5.10-1
+ Revision: 691879
- 3.5.10

* Tue Jun 28 2011 Buchan Milne <bgmilne@mandriva.org> 3.5.9-1
+ Revision: 687769
- update to new version 3.5.9

* Mon May 02 2011 Buchan Milne <bgmilne@mandriva.org> 3.5.8-1
+ Revision: 662322
- Explicitly request external tdb and talloc
- Try and fix netapi example linking
- Enable dns updates
- Remove some old patches
- Revert some pointless (taking into account samba4) non-maintainer changes
- Fix build with gcc-4.6 optflags

  + Funda Wang <fwang@mandriva.org>
    - more file list cleanup
    - merge various scripts and conf files
    - about to mergeback

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - fix %%exclude abuse
    - escape wildcards in shell so that they won't get expanded before %%files

  + Oden Eriksson <oeriksson@mandriva.com>
    - also add the sources...
    - a futile version bump...
    - giving up on this because it's too complex to fix and i have no time...
    - fix file list
    - 3.5.7

* Wed Sep 15 2010 Buchan Milne <bgmilne@mandriva.org> 3.5.5-1mdv2011.0
+ Revision: 578669
- update to new version 3.5.5

* Thu Sep 02 2010 Thierry Vignaud <tv@mandriva.org> 3.5.4-2mdv2011.0
+ Revision: 575203
- let the doc subpackage be noarch

* Sat Jul 31 2010 Funda Wang <fwang@mandriva.org> 3.5.4-1mdv2011.0
+ Revision: 563896
- new version 3.5.4

* Tue Jun 08 2010 Buchan Milne <bgmilne@mandriva.org> 3.5.3-3mdv2010.1
+ Revision: 547249
- Add group to domainjoin-gui package
- Correct license tag
- Commit missing patch that tries to fix 'not a string literal' in netdomjoin-gui
- Cleaner fix for NULL pname in setup_logging (mdv#59677) (samba#7499)
- Enable domain join gui
- Prevent segfault due to previous patch if setup_logging is called with NULL pname

  + Thomas Backlund <tmb@mandriva.org>
    - fix typo

  + Luca Berra <bluca@mandriva.org>
    - fix nss_wins overwriting daemon syslog ident (#59677)

* Thu Jun 03 2010 Frederic Crozat <fcrozat@mandriva.com> 3.5.3-2mdv2010.1
+ Revision: 547046
+ rebuild (emptylog)

* Tue Jun 01 2010 Buchan Milne <bgmilne@mandriva.org> 3.5.3-1mdv2010.1
+ Revision: 546828
- New release 3.5.3
- Should fix Mdv bug #58877, Mdv bug #59265 and possibly others related to
  accessing files via libsmbclient (smb:// in Dolphin, Nautilus etc.)

* Thu Apr 08 2010 Buchan Milne <bgmilne@mandriva.org> 3.5.2-1mdv2010.1
+ Revision: 533210
- update to new version 3.5.2

* Thu Apr 08 2010 Buchan Milne <bgmilne@mandriva.org> 3.5.1-1mdv2010.1
+ Revision: 533162
- Try alternate method for removing --no-undefined from plugin flags, and show
 plugin flags along with other flags
- Require newer ctdb
- New version 3.5.1
- Drop patch 29 (upstreamed), and disable undefined as upstream now sets -z defs
  by default - not doing this results in undefined symbols in plugins
- Other minor changes (files,excludes)
- Notable upstream change: mount.cifs no longer allows undefined non-root mounts

* Tue Mar 09 2010 Buchan Milne <bgmilne@mandriva.org> 3.4.7-1mdv2010.1
+ Revision: 517012
- update to new version 3.4.7
- update to new version 3.4.6

* Thu Feb 25 2010 Zombie Ryushu <ryushu@mandriva.org> 3.4.6-1mdv2010.1
+ Revision: 511083
- First Attempt at Samba 3.4.6
- First Attempt at Samba 3.4.6

  + Buchan Milne <bgmilne@mandriva.org>
    - Fix Buildrequires and add explicit options to configure

* Mon Jan 25 2010 Zombie Ryushu <ryushu@mandriva.org> 3.4.5-1mdv2010.1
+ Revision: 496286
- Attempt to update to 3.4.5 in cooker
- Attempt to update to 3.4.5 in cooker

* Fri Jan 08 2010 Buchan Milne <bgmilne@mandriva.org> 3.4.4-1mdv2010.1
+ Revision: 487529
- New version 3.4.4
- Update some items in the default smb.conf (bug #56894)

* Wed Dec 16 2009 Buchan Milne <bgmilne@mandriva.org> 3.4.3-2mdv2010.1
+ Revision: 479214
- Fix libsmbclient workgroup browsing (Mdv bug #56063)
- Fix build on 2009.0 and older (without samba4 providing ldb/tdb/talloc)

* Thu Oct 29 2009 Buchan Milne <bgmilne@mandriva.org> 3.4.3-1mdv2010.1
+ Revision: 460067
- New version 3.4.3
- Drop patches 24 and 26, applied upstream with bug 6791

* Thu Oct 01 2009 Oden Eriksson <oeriksson@mandriva.com> 3.4.2-1mdv2010.0
+ Revision: 452236
- 3.4.2

* Sun Sep 13 2009 Buchan Milne <bgmilne@mandriva.org> 3.4.1-1mdv2010.0
+ Revision: 438980
- New version 3.4.1
- Disable patches merged since 3.4.1
- New version 3.4.0
- Adjust paths which have changed in source tree since 3.3.x
- Move some swat translations to swat package (with conflicts)
- Add suggests on samba-doc to samba-swat

* Fri Aug 14 2009 Thomas Backlund <tmb@mandriva.org> 3.3.7-2mdv2010.0
+ Revision: 416267
- rebuild due to missing mount-cifs-3.3.7 on x86_64

* Wed Aug 12 2009 Buchan Milne <bgmilne@mandriva.org> 3.3.7-1mdv2010.0
+ Revision: 415582
- New version 3.3.7
- Change default server string, as some Windows versions dont like it to change
- Move smb.conf out of packaging patch so it is under direct version control

* Wed Jun 24 2009 Buchan Milne <bgmilne@mandriva.org> 3.3.6-1mdv2010.0
+ Revision: 388816
- update to new version 3.3.6

* Wed Jun 17 2009 Buchan Milne <bgmilne@mandriva.org> 3.3.5-1mdv2010.0
+ Revision: 386659
- New version 3.3.5

* Wed Jun 17 2009 Buchan Milne <bgmilne@mandriva.org> 3.3.4-1mdv2010.0
+ Revision: 386579
- update to new version 3.3.4

* Wed Jun 17 2009 Buchan Milne <bgmilne@mandriva.org> 3.3.3-1mdv2010.0
+ Revision: 386571
+ rebuild (emptylog)

* Thu Apr 16 2009 Buchan Milne <bgmilne@mandriva.org> 3.3.3-0mdv2009.1
+ Revision: 367753
- New version 3.3.3
- Buildrequire avahi-client-devel to enable (new) avahi support
- Fix winbind password expiry (Samba bug #6253), from Emmanuel Blindauer
- Enable ctdb support

* Sat Mar 28 2009 Anssi Hannula <anssi@mandriva.org> 3.3.2-3mdv2009.1
+ Revision: 361796
- fix linking order of rpcclient and libwbclient (fix-linking-order.patch,
  with the libwbclient case fixing undefined references in libwbclient.so)

* Fri Mar 27 2009 Buchan Milne <bgmilne@mandriva.org> 3.3.2-2mdv2009.1
+ Revision: 361668
- Build against system (samba4) libtalloc, libtdb, and dont ship talloc, tdb, ldb
 on 2009.1 or later

* Fri Mar 13 2009 Buchan Milne <bgmilne@mandriva.org> 3.3.2-1mdv2009.1
+ Revision: 354732
- New version 3.3.2
- Buildrequire libcap-devel, oplock buffering requires it on 3.2 and later

* Wed Feb 25 2009 Buchan Milne <bgmilne@mandriva.org> 3.3.1-3mdv2009.1
+ Revision: 344895
- Fix conflict between libsmbclient-devel and other devel packages

* Wed Feb 25 2009 Oden Eriksson <oeriksson@mandriva.com> 3.3.1-2mdv2009.1
+ Revision: 344715
- rebuilt against new readline

  + Buchan Milne <bgmilne@mandriva.org>
    - New version 3.3.1

* Thu Feb 19 2009 Oden Eriksson <oeriksson@mandriva.com> 3.2.8-3mdv2009.1
+ Revision: 343000
- add "BuildConflicts: libcap-devel" to prevent unknown future borkiness and fjukiness...

* Thu Feb 19 2009 Oden Eriksson <oeriksson@mandriva.com> 3.2.8-2mdv2009.1
+ Revision: 342815
- fix a silly typo
- fix deps because /usr/include/tdb.h was moved from
  libsmbclient0-devel to libtdb-devel.

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - new release
    - rediff modules separation patch

* Tue Feb 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.2.7-2mdv2009.1
+ Revision: 337185
- keep bash completion in its own package

* Tue Jan 06 2009 Buchan Milne <bgmilne@mandriva.org> 3.2.7-1mdv2009.1
+ Revision: 325478
- update to new version 3.2.7

* Mon Jan 05 2009 Oden Eriksson <oeriksson@mandriva.com> 3.2.6-3mdv2009.1
+ Revision: 325110
- fix deps
- fix a file conflict

* Sun Jan 04 2009 Oden Eriksson <oeriksson@mandriva.com> 3.2.6-2mdv2009.1
+ Revision: 324355
- fix php-tdb build (P20 from debian)

* Sat Dec 13 2008 Buchan Milne <bgmilne@mandriva.org> 3.2.6-1mdv2009.1
+ Revision: 313997
-New version 3.2.6

* Fri Nov 28 2008 Buchan Milne <bgmilne@mandriva.org> 3.2.4-3mdv2009.1
+ Revision: 307414
- Security fix (CVE-2008-4314)
- Add patch fixing LDAP password modify exop (samba bug #5886)

* Thu Oct 30 2008 Buchan Milne <bgmilne@mandriva.org> 3.2.4-2mdv2009.1
+ Revision: 298718
- Drop dangling mount.smb/mount.smbfs symlinks
- Make mount-cifs require new enough keyutils for krb5 support

* Thu Oct 16 2008 Buchan Milne <bgmilne@mandriva.org> 3.2.4-1mdv2009.1
+ Revision: 294197
- New version 3.2.4

* Thu Oct 02 2008 Buchan Milne <bgmilne@mandriva.org> 3.2.3-3mdv2009.0
+ Revision: 290748
- Include the rest of the MODULESDIR-related changes (fixes bug #43924)

* Sat Sep 13 2008 Colin Guthrie <cguthrie@mandriva.org> 3.2.3-2mdv2009.0
+ Revision: 284482
- Install pkgconfig .pc files for the various libraries

* Tue Sep 02 2008 Buchan Milne <bgmilne@mandriva.org> 3.2.2-1mdv2009.0
+ Revision: 279222
- New version 3.2.3
- New version 3.2.2
- Use patch from git to fix separation of shared libraries and plugins
- Fix configure options, and avoid overriding variables at install time
- Ship cifs.upcall, and buildrequire keyutils on distributions with keyutils
- Fix linking order for cifs.upcall

* Thu Aug 07 2008 Buchan Milne <bgmilne@mandriva.org> 3.2.1-1mdv2009.0
+ Revision: 265872
- New version 3.2.1
- Add verification of source signatures

* Mon Jul 28 2008 Buchan Milne <bgmilne@mandriva.org> 3.2.0-1mdv2009.0
+ Revision: 251195
- New version 3.2.0
- Drop smbmount et al and related patches
- Add new library packages
- Conditionalise postgresql and mysql buildrequires
- Disable vscan support for now

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Jun 03 2008 Buchan Milne <bgmilne@mandriva.org> 3.0.30-1mdv2009.0
+ Revision: 214823
- Remove recursive autoconf macros
  Drop some obsolete patches
- New version 3.0.30
  Drop upstreamed patches (CVE-2008-1105)
  Drop packaging of internal smbldap-tools (dropped upstream)

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Oden Eriksson <oeriksson@mandriva.com>
    - P22: security fix for CVE-2008-1105

* Sun Mar 23 2008 Emmanuel Andry <eandry@mandriva.org> 3.0.28a-2mdv2008.1
+ Revision: 189635
- Fix static-devel group
- protect major

* Tue Mar 11 2008 Buchan Milne <bgmilne@mandriva.org> 3.0.28a-1mdv2008.1
+ Revision: 186720
- New version 3.0.28a

  + Thierry Vignaud <tv@mandriva.org>
    - fix summary-not-capitalized

* Sun Jan 13 2008 Funda Wang <fwang@mandriva.org> 3.0.28-4mdv2008.1
+ Revision: 150850
- rebuild against latest gnutls

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Dec 21 2007 Buchan Milne <bgmilne@mandriva.org> 3.0.28-3mdv2008.1
+ Revision: 136361
- Rebuild for new openldap (2.4) with new soname

* Fri Dec 21 2007 Thierry Vignaud <tv@mandriva.org> 3.0.28-2mdv2008.1
+ Revision: 136255
- rebuild with latest ldap
- kill re-definition of %%buildroot on Pixel's request

* Mon Dec 10 2007 Buchan Milne <bgmilne@mandriva.org> 3.0.28-1mdv2008.1
+ Revision: 117061
- New version 3.0.28

* Wed Nov 21 2007 Buchan Milne <bgmilne@mandriva.org> 3.0.27a-1mdv2008.1
+ Revision: 110969
- New version 3.0.27a

* Sun Nov 18 2007 Funda Wang <fwang@mandriva.org> 3.0.27-1mdv2008.1
+ Revision: 109971
- New version 3.0.27

* Wed Oct 10 2007 Buchan Milne <bgmilne@mandriva.org> 3.0.26a-1mdv2008.1
+ Revision: 96878
- Update to 3.0.26a and samba-vscan 0.3.6c-beta5

  + Oden Eriksson <oeriksson@mandriva.com>
    - make mount.cifs umount.cifs build

  + Thierry Vignaud <tv@mandriva.org>
    - s/Mandrake/Mandriva/

* Wed Sep 12 2007 Buchan Milne <bgmilne@mandriva.org> 3.0.25b-4mdv2008.0
+ Revision: 84705
- Add patch for CVE-2007-4138

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's error: string list key "Categories" in group "Desktop Entry" does not have a semicolon (";") as trailing character

* Mon Aug 27 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.0.25b-3mdv2008.0
+ Revision: 71811
- bash completion

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 3.0.25b-2mdv2008.0
+ Revision: 69948
- fileutils, sh-utils & textutils have been obsoleted by coreutils a long time ago
- fix man pages extension

* Mon Jul 02 2007 Andreas Hasenack <andreas@mandriva.com> 3.0.25b-1mdv2008.0
+ Revision: 47103
- updated to version 3.0.25b

* Wed Jun 27 2007 Andreas Hasenack <andreas@mandriva.com> 3.0.25a-2mdv2008.0
+ Revision: 44948
- re-enable serverbuild, rebuild with new rpm-mandriva-setup (-fstack-protector)

* Thu May 31 2007 Buchan Milne <bgmilne@mandriva.org> 3.0.25a-1mdv2008.0
+ Revision: 33289
- Update default-quota-ignore-error patch

  + Andreas Hasenack <andreas@mandriva.com>
    - updated to version 3.0.25a
    - updated vscan to 0.3.6c-beta4 (this one builds with samba 3.0.25a)
    - dropped smbw patch, target is not available anymore

