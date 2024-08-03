# Useful commands for testing domain controller/OpenLDAP replacement
# functionality:
#
# Set up initial domain controller:
# samba-tool domain provision --realm=LINDEV.CH --domain=LINDEV --adminpass='PASSWORD' --server-role='domain controller'
# Query:
# ldapsearch -H ldap://127.0.0.1 -x -w 'PASSWORD' -b "DC=lindev,DC=ch" -D "CN=Administrator,CN=Users,DC=lindev,DC=ch"
# With TLS:
# ldapsearch -Z -H ldaps://127.0.0.1:636 -x -w 'PASSWORD' -b "DC=lindev,DC=ch" -D "CN=Administrator,CN=Users,DC=lindev,DC=ch"
%undefine _unpackaged_subdirs_terminate_build
%undefine _empty_manifest_terminate_build

# Default options
%bcond_without ads
%bcond_with cifs
%bcond_with doc
%bcond_with gtk
%ifarch %{x86_64}
%bcond_without winexe
%else
%bcond_with winexe
%endif
%define build_test	1
# CUPS supports functionality for 'printcap name = cups' (9.0 and later):
%define build_cupspc	1
# %_{pre,postun}_service are provided by rpm-helper in 9.0 and later
%define build_mysql	0
%define build_pgsql 	0

# Allow commandline option overrides (borrowed from Vince's qmail srpm):
# To use it, do rpm [-ba|--rebuild] --with 'xxx'
# Check if the rpm was built with the defaults, otherwise we inform the user
%define build_non_default 0
%{?_with_test: %global build_test 1}
%{?_with_test: %global build_non_default 1}
%{?_without_test: %global build_test 0}
%{?_without_test: %global build_non_default 1}
%{?_with_mysql: %global build_mysql 1}
%{?_with_pgsql: %global build_pgsql 1}
%global vfsdir examples.bin/VFS

%define	major	0
%define netapimajor	1
%define	ndrmajor	4
%define ndrsubmajor	0
%define libdcerpc %mklibname dcerpc
%define devdcerpc %mklibname -d dcerpc
%define libndr %mklibname ndr
%define devndr %mklibname -d ndr
%define libnetapi %mklibname netapi
%define devnetapi %mklibname -d netapi
%define libsambapassdb %mklibname sambapassdb
%define devsambapassdb %mklibname -d sambapassdb
%define libsambacredentials %mklibname samba-credentials
%define devsambacredentials %mklibname -d samba-credentials 
%define libsambaerrors %mklibname samba-errors
%define devsambaerrors %mklibname -d samba-errors
%define libsambahostconfig %mklibname samba-hostconfig
%define devsambahostconfig %mklibname -d samba-hostconfig
%define libsambapolicy %mklibname samba-policy
%define devsambapolicy %mklibname -d samba-policy
%define libsambautil %mklibname samba-util
%define devsambautil %mklibname -d samba-util
%define libsamdb %mklibname samdb
%define devsamdb %mklibname -d samdb
%define libsmbclient %mklibname smbclient
%define devsmbclient %mklibname -d smbclient 
%define libsmbconf %mklibname smbconf
%define devsmbconf %mklibname -d smbconf
%define ldapmajor 2
%define libsmbldap %mklibname smbldap
%define oldsmbldap %mklibname smbldap 0
%define devsmbldap %mklibname -d smbldap
%define libtevent_util %mklibname tevent-util
%define devtevent_util %mklibname -d tevent-util
%define libwbclient %mklibname wbclient
%define devwbclient %mklibname -d wbclient

#Define sets of binaries that we can use in globs and loops:
%global commonbin	testparm,regdiff,regpatch,regshell,regtree,mvxattr,dumpmscat
%global serverbin 	oLschema2ldif
%global serversbin	samba,samba_dnsupdate,samba_spnupdate,samba-gpupdate
%global testbin 	smbtorture,masktest,locktest,gentest,ndrdump

# filter out some bogues devel() requires
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}devel\\(lib.*-samba4

# filter out some bogus requires/provides
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libdir}/libnss_win.*\\.so
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}^%{_libdir}/libnss_win.*\\.so

# more filtering
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}lib.*samba4.so\\(
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}lib.*samba4.so\\(

# filter out perl requirements pulled in from examples in the docdir.
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_docdir}
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}^%{_docdir}/\[^/\]*/\[^M\]
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(VMS|^perl\\(Win32|^perl\\(DB\\)|^perl\\(UNIVERSAL\\)
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(VMS|^perl\\(Win32

%define build_expsam xml%{?_with_pgsql:,pgsql}%{?_with_mysql:,mysql}

%define _serverbuild_flags -fstack-protector-all

# (tpg) set here maximum supported ldb version
%define ldb_max_ver 2.9.999

#define beta rc4

Summary:	Samba SMB server
Name:		samba
Version:	4.20.3
License:	GPLv3
Group:		System/Servers
Url:		https://www.samba.org
Release:	%{?beta:0.%{beta}.}1
%if 0%{?beta:1}
Source0:	https://download.samba.org/pub/samba/rc/samba-%{version}%{beta}.tar.gz
Source99:	https://download.samba.org/pub/samba/rc/samba-%{version}%{beta}.tar.asc
%else
Source0:	https://ftp.samba.org/pub/samba/stable/samba-%{version}.tar.gz
Source99:	https://ftp.samba.org/pub/samba/stable/samba-%{version}.tar.asc
%endif
Source98:	https://ftp.samba.org/pub/samba/samba-pubkey.asc
Source1:	samba.log
#Source7:	README.%{name}-mandrake-rpm
Source10:	samba-print-pdf.sh
Source100:	%{name}.rpmlintrc
#Sources that used to be in packaging patch:
Source20:	smbusers
Source21:	smbprint
#Source22:	smbadduser
Source26:	wrepld.init
Source28:	samba.pamd
Source29:	system-auth-winbind.pamd
Source30:	%{name}-tmpfiles.conf
Source31:	smb.conf
#Patch1:		samba-4.11-compile.patch
Patch2:		samba-4.5.0-link-tirpc.patch
Patch3:		samba-4.5.0-bug12274.patch
# TODO: Fix broken net rap commands again (smb4k uses) https://bugzilla.samba.org/show_bug.cgi?id=12431
# (previous patch dropped from 4.14.x because it doesn't apply to new codebase easily
Patch5:		samba-4.13.2-libunwind.patch
Patch6:		samba-4.13.2-link-libunwind.patch

BuildRequires:	cups-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	docbook-dtd42-xml
BuildRequires:	gnupg
BuildRequires:	gpgme-devel
BuildRequires:	python-tdb
BuildRequires:	python-tevent >= 0.10.0
BuildRequires:	xsltproc
BuildRequires:	acl-devel
BuildRequires:	keyutils-devel
BuildRequires:	magic-devel
BuildRequires:	pkgconfig(ldap)
BuildRequires:	pam-devel
BuildRequires:	perl-devel
BuildRequires:	perl-Parse-Yapp
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ctdb) >= 2.0
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(ldb) >= 2.7.2
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(cmocka)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(libunwind)
BuildRequires:	python-ldb <= %{ldb_max_ver}
BuildRequires:	pyldb-util-devel >= 2.1.1
BuildRequires:	pyldb-util-devel <= %{ldb_max_ver}
BuildRequires:	python-talloc
BuildRequires:	pytalloc-util-devel
BuildRequires:	pkgconfig(talloc) >= 2.2.0
BuildRequires:	pkgconfig(tdb) >= 1.4.0
BuildRequires:	pkgconfig(tevent) >= 0.10.0
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(jansson)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(liburing)
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	python3dist(markdown)
BuildRequires:	python3-dns
# For asn1Parser
BuildRequires:	libtasn1-tools
%if %{with ads}
BuildRequires:	krb5-devel
# Needs to know the location of krb5kdc
BuildRequires:	krb5-server
%endif
%if %{build_mysql}
BuildRequires:	mysql-devel
%endif
%if %{build_pgsql}
BuildRequires:	postgresql-devel
%endif
%if %{with winexe}
BuildRequires:	cross-x86_64-w64-mingw32-binutils cross-x86_64-w64-mingw32-gcc cross-x86_64-w64-mingw32-libc
%endif

#### there is no straight samba rpm...
Requires(pre):	psmisc
Requires(pre):	coreutils
Requires(pre):	sed
Requires(pre):	grep
Requires:	pam >= 0.64
Requires:	samba-common = %{EVRD}

%description
Samba provides an SMB server which can be used to provide
network services to SMB (sometimes called "Lan Manager")
clients, including various versions of MS Windows, OS/2,
and other Linux machines. Samba also provides some SMB
clients, which complement the built-in SMB filesystem
in Linux. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame)
protocol.

Samba features working NT Domain Control capability.

Please refer to the WHATSNEW.txt document for fixup information.
This binary release includes encrypted password support.

Please read the smb.conf file and ENCRYPTION.txt in the
docs directory for implementation details.
%if %{build_non_default}
WARNING: This RPM was built with command-line options. Please
see README.%{name}-mandrake-rpm in the documentation for
more information.
%endif

%package server
Summary:	Samba (SMB) server programs
Group:		Networking/Other
Requires:	%{name}-common = %{EVRD}
# provision requires samba-python
Requires:	%{name}-python = %{EVRD}
Requires:	%{name}-libs = %{version}-%{release}
Requires(post,postun,preun):	rpm-helper
%rename	samba
%rename	samba-server-ldap
# SWAT is no longer included in 4.1.x. For now it has been removed
# without replacement, maybe it will come back later
Obsoletes:	%{name}-swat < 4.1.6
%if %{without gtk}
Obsoletes:	%{name}-domainjoin-gui < %{EVRD}
%endif

%description server
Samba-server provides a SMB server which can be used to provide
network services to SMB (sometimes called "Lan Manager")
clients. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame)
protocol.

Samba features working NT Domain Control capability.

Please refer to the WHATSNEW.txt document for fixup information.
This binary release includes encrypted password support.

Please read the smb.conf file and ENCRYPTION.txt in the
docs directory for implementation details.

%package client
Summary:	Samba (SMB) client programs
Group:		Networking/Other
Requires:	%{name}-common = %{EVRD}
Requires:	%{name}-libs = %{EVRD}
Requires(post,postun,preun):	rpm-helper
Requires:	mount-cifs
# For samba-tool
Requires:	python-talloc
Requires:	python-ldb <= %{ldb_max_ver}
Requires:	python-tdb
Requires:	ldb-utils <= %{ldb_max_ver}
%rename   	samba3-client
Obsoletes:	smbfs

%description client
Samba-client provides some SMB clients, which complement the built-in
SMB filesystem in Linux. These allow the accessing of SMB shares, and
printing to SMB printers.

%package	common
Summary:	Files used by both Samba servers and clients
Group:		System/Servers
# rpcclient etc. use samba python modules
Requires:	%{name}-python = %{EVRD}
Requires:	%{name}-libs = %{EVRD}
%rename 	samba-common-ldap
Conflicts:	samba3-common
Requires(post,postun,preun):	rpm-helper

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.

%package	libs
Summary:	Common libraries used by both Samba servers and clients
Group:		System/Libraries
Conflicts:	%{name}-server < 4.1.12-2
Obsoletes:	%{_lib}registry0 < %{EVRD}
Obsoletes:	%{_lib}gensec0 < %{EVRD}
%description libs
Samba-libs provides common libraries necessary for both the server and client
packages of Samba.

%if %{with doc}
%package doc
Summary:	Documentation for Samba servers and clients
Group:		System/Servers
Requires:	%{name}-common = %{EVRD}

%description doc
Samba-doc provides documentation files for both the server and client
packages of Samba.
%endif

%package winbind
Summary:	Samba-winbind daemon, utilities and documentation
Group:		System/Servers
Requires:	%{name}-common = %{EVRD}

%description winbind
Provides the winbind daemon and testing tools to allow authentication 
and group/user enumeration from a Windows or Samba domain controller.

%package -n nss_wins
Summary:	Name Service Switch service for WINS
Group:		System/Servers
Requires:	%{name}-common = %{EVRD}
Requires(post):	glibc
Requires(post,postun,preun):	rpm-helper

%description -n nss_wins
Provides the libnss_wins shared library which resolves NetBIOS names to 
IP addresses.

%package python
Summary:	Samba Python modules
Group:		Development/Python
BuildRequires:	pkgconfig(python3)

%description python
Samba Python modules

%if %{build_test}
%package test
Summary:	Debugging and benchmarking tools for samba
Group:		System/Servers
Requires:	%{name}-common = %{EVRD}

%description test
This package provides tools for benchmarking samba, and debugging
the correct operation of tools against smb servers.
%endif

%package devel
Summary:	Samba development package
Group:		Development/C
Requires:	%{devsmbclient} = %{EVRD}
%if "%_lib" == "lib64"
Provides:	devel(libdcerpc-samba(64bit))
%else
Provides:	devel(libdcerpc-samba)
%endif

%description devel
Samba development libraries.

%package -n %{libdcerpc}
Summary:	Library implementing DCE/RPC for Samba
Group:		System/Libraries
%rename %{mklibname dcerpc 0}

%description -n %{libdcerpc}
Library implementing DCE/RPC for Samba.

%package -n %{devdcerpc}
Summary:	Library implementing Samba's memory allocator
Group:		Development/C
Requires:	%{libdcerpc} = %{EVRD}

%description -n %{devdcerpc}
Library implementing Samba's memory allocator.

%package -n %{libndr}
Summary:	Network Data Representation library from Samba
Group:		System/Libraries
Obsoletes:	%{mklibname ndr 0} < %{EVRD}
Obsoletes:	%{mklibname ndr 1} < %{EVRD}
Obsoletes:	%{mklibname ndr 2} < %{EVRD}

%description -n %{libndr}
Network Data Representation library from Samba.

%package -n %{devndr}
Summary:       Development files for Network Data Representation library from Samba
Group:         Development/C
Requires:      %{libndr} = %{EVRD}

%description -n %{devndr}
Development files for Network Data Representation library from Samba.

%package -n %{libnetapi}
Summary:	Samba library for accessing functions in 'net' binary
Group:		System/Libraries
Obsoletes:	%{mklibname netapi 0} < %{EVRD}
%rename %{mklibname netapi 1}

%description -n %{libnetapi}
Samba library for accessing functions in 'net' binary.

%package -n %{devnetapi}
Summary:	Samba library for accessing functions in 'net' binary
Group:		Development/C
Requires:	%{libnetapi} = %{EVRD}
Requires:	samba-libs = %{EVRD}

%description -n %{devnetapi}
Samba library for accessing functions in 'net' binary.

%package -n %{libsambapassdb}
Summary:	Library for working with the Samba user database
Group:		System/Libraries
Obsoletes:	%{_lib}pdb0
%rename %{mklibname sambapassdb 0}

%description -n %{libsambapassdb}
Library for working with the Samba user database.

%package -n %{devsambapassdb}
Summary:	Development files for Samba user database library
Group:		Development/C
Requires:	%{libsambapassdb} = %{EVRD}
Provides:	samba-passdb-devel = %{EVRD}

%description -n %{devsambapassdb}
Development files for Samba user database library.

%package -n %{libsambacredentials}
Summary:	Library for working with Samba credentials
Group:		System/Libraries
Obsoletes:	%{mklibname samba-credentials 0} < %{EVRD}
%rename %{mklibname samba-credentials 1}

%description -n %{libsambacredentials}
Library for working with Samba credentials.

%package -n %{devsambacredentials}
Summary:	Development files for Samba credentials library
Group:		Development/C
Requires:	%{libsambacredentials} = %{EVRD}

%description -n %{devsambacredentials}
Development files for Samba credentials library.

%package -n %{libsambaerrors}
Summary:        Samba's errors library
Group:          System/Libraries
%rename %{mklibname samba-errors 1}

%description -n %{libsambaerrors}
Samba's erros library.

%package -n %{devsambaerrors}
Summary:        Samba's errors library
Group:          Development/C
Requires:       %{libsambaerrors} = %{EVRD}

%description -n %{devsambaerrors}
Samba's error library.

%package -n %{libsambahostconfig}
Summary:	Samba's host configuration library
Group:		System/Libraries
%rename %{mklibname samba-hostconfig 0}

%description -n %{libsambahostconfig}
Samba's host configuration library.

%package -n %{devsambahostconfig}
Summary:	Samba's host configuration library
Group:		Development/C
Requires:	%{libsambahostconfig} = %{EVRD}

%description -n %{devsambahostconfig}
Samba's host configuration library.

%package -n %{libsambapolicy}
Summary:	Samba policy library
Group:		System/Libraries
%rename %{mklibname samba-policy 0}

%description -n %{libsambapolicy}
Samba policy library.

%package -n %{devsambapolicy}
Summary:	Development files for Samba policy library
Group:		Development/C
Requires:	%{libsambapolicy} = %{EVRD}

%description -n %{devsambapolicy}
Development files for Samba policy library.

%package -n %{libsambautil}
Group:		System/Libraries
Summary:	Samba utility library
%rename %{mklibname samba-util 0}

%description -n %{libsambautil}
Samba utility library.

%package -n %{devsambautil}
Summary:	Development files for Samba utility library
Group:		Development/C
Requires:	%{libsambautil} = %{EVRD}

%description -n %{devsambautil}
Development files for Samba utility library.

%package -n %{libsamdb}
Summary:	Samba samdb library
Group:		System/Libraries
%rename %{mklibname samdb 0}

%description -n %{libsamdb}
Samba samdb library

%package -n %{devsamdb}
Summary:	Development files for Samba samdb library
Group:		Development/C
Requires:	%{libsamdb} = %{EVRD}

%description -n %{devsamdb}
Development files for Samba samdb library.

%package -n %{libsmbclient}
Summary:	SMB Client Library
Group:		System/Libraries
Provides:	libsmbclient = %{EVRD}
%rename %{mklibname smbclient 0}

%description -n %{libsmbclient}
This package contains the SMB client library, part of the samba
suite of networking software, allowing other software to access
SMB shares.

%package -n %{devsmbclient}
Summary:	SMB Client Library Development files
Group:		Development/C
Requires:	%{libsmbclient} = %{EVRD}

%description -n %{devsmbclient}
This package contains the development files for the SMB client
library, part of the samba suite of networking software, allowing
the development of other software to access SMB shares.

%package -n %{libsmbconf}
Summary:	Library for working with Samba config files
Group:		System/Libraries
%rename %{mklibname smbconf 0}

%description -n %{libsmbconf}
Library for working with Samba config files.

%package -n %{devsmbconf}
Summary:	Development files for Samba smbconf library
Group:		Development/C
Requires:	%{libsmbconf} = %{EVRD}

%description -n %{devsmbconf}
Development files for Samba smbconf library.

%package -n %{libsmbldap}
Summary:	Samba LDAP library
Group:		System/Libraries
Obsoletes:	%{oldsmbldap} < %{EVRD}
%rename %{mklibname smbldap 2}

%description -n %{libsmbldap}
Samba LDAP library

%package -n %{devsmbldap}
Summary:	Development files for Samba smbldap library
Group:		Development/C
Requires:	%{libsmbldap} = %{EVRD}

%description -n %{devsmbldap}
Development files for Samba smbldap library.

%package -n %{libtevent_util}
Summary:	Utility library for working with the Tevent library
Group:		System/Libraries
%rename %{mklibname tevent-util 0}

%description -n %{libtevent_util}
Utility library for working with the Tevent library.

%package -n %{devtevent_util}
Group:		Development/C
Summary:	Development files for Tevent library
Requires:	%{libtevent_util} = %{EVRD}

%description -n %{devtevent_util}
Development files for Samba Tevent library.

%package -n %{libwbclient}
Summary:	Library providing access to winbindd
Group:		System/Libraries
%rename %{mklibname wbclient 0}

%description -n %{libwbclient}
Library providing access to winbindd.

%package -n %{devwbclient}
Summary:	Library providing access to winbindd
Group:		Development/C
Requires:	%{libwbclient} = %{EVRD}

%description -n %{devwbclient}
Library providing access to winbindd.

%if %{build_mysql}
%package passdb-mysql
Summary:	Samba password database plugin for MySQL
Group:		System/Libraries
Requires:	%{name}-server = %{EVRD}

%description passdb-mysql
The passdb-mysql package for samba provides a password database
backend allowing samba to store account details in a MySQL
database
%endif

%if %{build_pgsql}
%package passdb-pgsql
Summary:	Samba password database plugin for PostgreSQL
Group:		System/Libraries
Requires:	%{name}-server = %{EVRD}
%endif
%if %{build_pgsql}

%description passdb-pgsql
The passdb-pgsql package for samba provides a password database
backend allowing samba to store account details in a PostgreSQL
database
%endif

%if %{with cifs}
%package -n mount-cifs
Summary:	CIFS filesystem mount helper
Group:		Networking/Other
Requires:	keyutils > 1.2

%description -n mount-cifs
This package provides the mount.cifs helper to mount cifs filesystems
using the cifs filesystem driver
%endif

%if %{with gtk}
%package domainjoin-gui
Summary:	Domainjoin GUI
Requires:	samba-common = %{EVRD}
Group:		System/Configuration/Other
BuildRequires:	pkgconfig(gtk+-2.0)

%description domainjoin-gui
The samba-domainjoin-gui package includes a domainjoin gtk application
%endif

#%package ctdb
#Summary:	A clustered implementation of TDB
#Requires:
#Group:
#BuildRequires:
#%description ctdb
#CTDB is a cluster implementation of the TDB database used by 
#Samba and other projects to store temporary data


%prep

# Allow users to query build options with --with options:
#%%define opt_status(%1)	%(echo %{1})
%if %{?_with_options:1}%{!?_with_options:0}
%define opt_status(%{1})	%(if [ %{1} -eq 1 ];then echo enabled;else echo disabled;fi)
#exit 1
%{error: }
%{error:Build options available are:}
%{error:--with[out] system   Build as the system samba package [or as samba3]}
%{error:--with[out] winbind  Build with Winbind support                - %opt_status %{with winbind}}
%{error:--with[out] ads      Build with Active Directory support       - %opt_status %{with ads}}
%{error:--with[out] mysql    Build MySQL passdb backend                - %opt_status %build_mysql}
%{error:--with[out] pgsql    Build PostgreSQL passdb backend           - %opt_status %build_pgsql}
%{error:--with[out] test     Enable testing and benchmarking tools     - %opt_status %build_test}
%{error: }
%else
echo -e "\n This rpm has build options available, use --with options to see them\n" >&2
sleep 1
%endif

%if %{?_with_options:1}%{!?_with_options:0}
clear
exit 1
%endif

%if %{build_non_default}
RPM_EXTRA_OPTIONS="\
%{?_with_system: --with system}\
%{?_without_system: --without system}\
%{?with winbind: --with winbind}\
%{?without winbind: --without winbind}\
%{?_with_ldap: --with ldap}\
%{?_without_ldap: --without ldap}\
%{?_with_ads: --with ads}\
%{?_without_ads: --without ads}\
"
%endif

#Try and validate signatures on source:
# FIXME: find public key used to sign samba releases
export GNUPGHOME=%{_tmppath}/samba-gpghome
if [ -d "$GNUPGHOME" ]
then echo "Error, GNUPGHOME $GNUPGHOME exists, remove it and try again"; exit 1
fi
install -d -m700 $GNUPGHOME
gpg --import %{SOURCE98}
VERIFYSOURCE=`basename %{SOURCE0}`
VERIFYSOURCE=%{_tmppath}/${VERIFYSOURCE%%.gz}
gzip -dc %{SOURCE0} > $VERIFYSOURCE
pushd %{_tmppath}
cp %{SOURCE99} .
#gpg --trust-model always --verify `basename %{SOURCE99}`
#VERIFIED=$?
VERIFIED=1
rm -f `basename %{SOURCE99}`
popd
rm -Rf $GNUPGHOME

rm -f $VERIFYSOURCE
if [ "$VERIFIED" -eq 0 ]
then
	echo "Verification of %{SOURCE0} against %{SOURCE99} with key %{SOURCE98} succeeded"
else
	echo "Source verification failed!" >&2
fi

%autosetup -p1 -n %{name}-%{version}%{?beta:%{beta}}
# samba is *weird* and requires all the libunwind sublibs
%ifarch %{x86_64}
sed -i -e 's,@LIBUNWIND_LIBS@,-L%{_libdir}/libunwind -lunwind -lunwind-x86_64,' wscript
%else
%ifarch %{aarch64}
sed -i -e 's,@LIBUNWIND_LIBS@,-L%{_libdir}/libunwind -lunwind -lunwind-aarch64,' wscript
%else
sed -i -e 's,@LIBUNWIND_LIBS@,-L%{_libdir}/libunwind -lunwind,' wscript
%endif
%endif

%build
# Looks like autoconf, but is actually a waf wrapper
# (and not compatible with the macro)
./configure \
	--enable-fhs \
	--with-privatelibdir=%{_libdir}/%{name} \
	--bundled-libraries=NONE \
	--enable-cups \
	--enable-avahi \
	--with-pam \
%if %{with winbind}
	--with-winbind \
%endif
%if %{with ads}
	--with-ads \
	--with-system-mitkrb5 --with-experimental-mit-ad-dc \
%else
	--without-ads \
%endif
	--with-ldap \
	--disable-rpath \
	--disable-rpath-install \
	--disable-rpath-private-install \
	--enable-pthreadpool \
	--enable-avahi \
	--with-libarchive \
	--with-pie \
    	--with-relro \
    	--without-fam \
	--with-iconv \
	--with-acl-support \
	--with-syslog \
	--with-automount \
	--with-cluster-support \
	--with-sendfile-support \
	--with-systemd \
	--with-piddir=/run/samba \
	--without-cluster \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir} \
	--datadir=%{_datadir} \
	--localstatedir=%{_localstatedir} \
	--with-modulesdir=%{_libdir}/%{name} \
	--with-sockets-dir=/run/samba \
	--with-piddir=/run/samba \
    	--with-lockdir=/var/lib/samba \
    	--with-cachedir=/var/lib/samba \
	--with-logdir=/var/log/samba \

%make_build

%if %{with gtk}
cd source3/lib/netapi/examples/netdomjoin-gui
%__cc %{optflags} `pkg-config --cflags gtk+-2.0` -I../../../../../bin/default/include/public -o netdomjoin-gui netdomjoin-gui.c -L../../../../../bin/default/source3/ -lnetapi `pkg-config --libs gtk+-2.0`
%endif

%install
mkdir -p %{buildroot}

# Put stuff where it should go.
mkdir -p %{buildroot}/%{_libdir}/samba/
mkdir -p %{buildroot}/%{_datadir}/man/man8/


# Any entries here mean samba makefile is *really* broken:
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_datadir}
mkdir -p %{buildroot}%{_libdir}/%{name}/vfs

%makeinstall_std
# PAM modules don't go to /usr...
if [ -e %{buildroot}%{_libdir}/security ]; then
	mkdir -p %{buildroot}/%{_lib}
	mv %{buildroot}%{_libdir}/security %{buildroot}/%{_lib}
fi

#need to stay
mkdir -p %{buildroot}%{_sysconfdir}/{logrotate.d,pam.d}
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/var/cache/%{name}
mkdir -p %{buildroot}/var/log/%{name}
mkdir -p %{buildroot}/var/run/%{name}
mkdir -p %{buildroot}/var/spool/%{name}
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/private
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/{netlogon,profiles,printers}
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/printers/{W32X86,WIN40,W32ALPHA,W32MIPS,W32PPC}
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/codepages/src
mkdir -p %{buildroot}/%{_lib}/security
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{name}/vfs
mkdir -p %{buildroot}%{_datadir}/%{name}/scripts

# Fix some paths so provision works:
perl -pi -e 's,default_ldb_modules_dir = None,default_ldb_modules_dir = \"%{_libdir}/%{name}/ldb\",g' %{buildroot}/%{py_platsitedir}/samba/__init__.py

%if %{with gtk}
install -m 755 source3/lib/netapi/examples/netdomjoin-gui/netdomjoin-gui %{buildroot}/%{_sbindir}/netdomjoin-gui
mkdir -p %{buildroot}%{_datadir}/pixmaps/%{name}
install -m 644 source3/lib/netapi/examples/netdomjoin-gui/samba.ico %{buildroot}/%{_datadir}/pixmaps/%{name}/samba.ico
install -m 644 source3/lib/netapi/examples/netdomjoin-gui/logo.png %{buildroot}/%{_datadir}/pixmaps/%{name}/logo.png
install -m 644 source3/lib/netapi/examples/netdomjoin-gui/logo-small.png %{buildroot}/%{_datadir}/pixmaps/%{name}/logo-small.png
%endif

%if %{build_test}
for i in {%{testbin}};do
	mv %{buildroot}/%{_bindir}/$i %{buildroot}/%{_bindir}/${i} || :
done
%endif

# Install other stuff

        install -m644 %{SOURCE28} %{buildroot}/%{_sysconfdir}/pam.d/%{name}
        install -m644 %{SOURCE29} %{buildroot}/%{_sysconfdir}/pam.d/system-auth-winbind
#
        install -m644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

# install pam_winbind.conf sample file
mkdir -p %{buildroot}%{_sysconfdir}/security

# make a conf file for winbind from the default one:
#	cat packaging/Mandrake/smb.conf|sed -e  's/^;  winbind/  winbind/g;s/^;  obey pam/  obey pam/g;s/   printer admin = @adm/#  printer admin = @adm/g; s/^#   printer admin = @"D/   printer admin = @"D/g;s/^;   password server = \*/   password server = \*/g;s/^;  template/  template/g; s/^   security = user/   security = domain/g' > packaging/Mandrake/smb-winbind.conf
#        install -m644 packaging/Mandrake/smb-winbind.conf %{buildroot}/%{_sysconfdir}/%{name}/smb-winbind.conf

# Some inline fixes for smb.conf for non-winbind use
install -m644 %{SOURCE31} %{buildroot}/%{_sysconfdir}/%{name}/smb.conf
#cat %{SOURCE31} | \
#touch %{buildroot}/%{_sysconfdir}/%{name}/smb.conf
#sed -e 's/^;   printer admin = @adm/   printer admin = @adm/g' >%{buildroot}/%{_sysconfdir}/%{name}/smb.conf
%if %{build_cupspc}
#perl -pi -e 's/printcap name = lpstat/printcap name = cups/g' %{buildroot}/%{_sysconfdir}/%{name}/smb.conf
#perl -pi -e 's/printcap name = lpstat/printcap name = cups/g' %{buildroot}/%{_sysconfdir}/%{name}/smb-winbind.conf
# Link smbspool to CUPS (does not require installed CUPS)

        mkdir -p %{buildroot}/%{_prefix}/lib/cups/backend
        ln -s %{_bindir}/smbspool %{buildroot}/%{_prefix}/lib/cups/backend/smb
%endif

        echo 127.0.0.1 localhost > %{buildroot}/%{_sysconfdir}/%{name}/lmhosts

install -c -m 755 %{SOURCE10} %{buildroot}%{_datadir}/%{name}/scripts/print-pdf

# Move some stuff where it belongs...
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libnss* %{buildroot}/%{_lib}/

rm -f %{buildroot}/%{_mandir}/man1/testprns*

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat >%{buildroot}%{_sysconfdir}/ld.so.conf.d/samba.conf <<EOF
%{_libdir}/samba
EOF

mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
cp -a bin/default/packaging/systemd/*.service %{buildroot}%{_unitdir}/
cp -a packaging/systemd/samba.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/samba

# MD removal of orphan manpages 
rm -f %{buildroot}%{_mandir}/man1/log2pcap.1*
rm -f %{buildroot}%{_mandir}/man1/vfstest.1*

# tmpfiles for runtime dir creation
install -D -p -m 0644 %{SOURCE30} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-samba.preset << EOF
disable nmb.service
disable smb.service
disable winbind.service
EOF

# install NM dispatcher file
install -d -m 0755 %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/
install -m 0755 packaging/NetworkManager/30-winbind-systemd %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/30-winbind

# install findsmb
install -c -m 755 examples/scripts/nmb/findsmb %{buildroot}%{_bindir}/findsmb

# User shares, for kdenetwork-filesharing
# https://community.kde.org/Distributions/Packaging_Recommendations
mkdir -p %{buildroot}/var/lib/samba/usershares

%post server

# Add a unix group for samba machine accounts
groupadd -frg 421 machines

%post common
# And this too, in case we don't have smbd to create it for us
[ -f /var/cache/%{name}/unexpected.tdb ] || {
	touch /var/cache/%{name}/unexpected.tdb
}

%postun common
if [ -f %{_sysconfdir}/%{name}/README.mdk.conf ];then rm -f %{_sysconfdir}/%{name}/README.mdk.conf;fi

%post winbind
if [ $1 = 1 ]; then
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
	sed -i -e 's/ winbind//' %{_sysconfdir}/nsswitch.conf

fi

%post -n nss_wins
if [ $1 = 1 ]; then
    cp -af %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/nsswitch.conf.rpmsave
    grep '^hosts' %{_sysconfdir}/nsswitch.conf |grep -v 'wins' >/dev/null
    if [ $? = 0 ];then
        echo "Adding a wins entry to the hosts section of %{_sysconfdir}/nsswitch.conf"
        awk '/^hosts/ {print $0 " wins"};!/^hosts/ {print}' %{_sysconfdir}/nsswitch.conf.rpmsave >%{_sysconfdir}/nsswitch.conf;
    else
        echo "wins entry found in %{_sysconfdir}/nsswitch.conf"
    fi
fi

%preun -n nss_wins
if [ $1 = 0 ]; then
	echo "Removing wins entry from %{_sysconfdir}/nsswitch.conf"
	sed -i -e 's/ wins//' %{_sysconfdir}/nsswitch.conf
fi

%files server
%(for i in %{_sbindir}/{%{serversbin}};do echo $i;done)
%(for i in %{_bindir}/%{serverbin};do echo $i;done)
%{_libdir}/%{name}/vfs/*.so
%{_libdir}/samba/ldb
%{_libdir}/samba/service
%{_libdir}/samba/process_model
%{_libdir}/samba/gensec
#%{_libdir}/samba/auth
%{_libdir}/samba/bind9
%dir %{_libdir}/samba/vfs
%{_sbindir}/samba-log-parser
%{_sbindir}/smbd
%{_sbindir}/nmbd
%{_sbindir}/samba_upgradedns
%{_sbindir}/samba_downgrade_db
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/pam.d/%{name}
%(for i in %{_mandir}/man?/%{serverbin}\.[0-9]*;do echo $i;done)
%attr(775,root,adm) %dir %{_localstatedir}/lib/%{name}/netlogon
%attr(755,root,root) %dir %{_localstatedir}/lib/%{name}/profiles
%attr(755,root,root) %dir %{_localstatedir}/lib/%{name}/printers
%attr(2775,root,adm) %dir %{_localstatedir}/lib/%{name}/printers/*
%attr(1777,root,root) %dir /var/spool/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/scripts
%{_datadir}/%{name}/admx
%{_datadir}/samba/setup
%attr(0755,root,root) %{_datadir}/%{name}/scripts/print-pdf
%{_mandir}/man8/samba.8*
%{_mandir}/man8/samba-gpupdate.8*
%{_mandir}/man8/samba_downgrade_db.8*
%{_mandir}/man1/samba-log-parser.1*
%{_unitdir}/samba.service
%{_unitdir}/smb.service
%{_unitdir}/nmb.service
%config(noreplace) %{_sysconfdir}/sysconfig/samba
%{_datadir}/samba/mdssvc
%if %{with winexe}
%{_bindir}/winexe
%{_mandir}/man1/winexe.1*
%endif
%dir %attr(1770,root,users) /var/lib/samba/usershares

%files libs
%dir %{_libdir}/%{name}
%{_libdir}/samba/libCHARSET3-private-samba.so
%{_libdir}/samba/libLIBWBCLIENT-OLD-private-samba.so
%{_libdir}/samba/libMESSAGING-private-samba.so
%{_libdir}/samba/libaddns-private-samba.so
%{_libdir}/samba/libdsdb-garbage-collect-tombstones-private-samba.so
%{_libdir}/samba/libmscat-private-samba.so
%{_libdir}/samba/libscavenge-dns-records-private-samba.so
%dir %{_libdir}/samba/krb5
%{_libdir}/samba/krb5/async_dns_krb5_locator.so
%{_sysconfdir}/ld.so.conf.d
%if %{with ads}
%{_libdir}/samba/libads-private-samba.so
%{_libdir}/samba/libad-claims-private-samba.so
%{_libdir}/krb5/plugins/kdb/samba.so
%{_libdir}/samba/krb5/winbind_krb5_localauth.so
%{_mandir}/man8/winbind_krb5_localauth.8*
%endif
%{_libdir}/samba/libasn1util-private-samba.so
%{_libdir}/samba/libauth-private-samba.so
%{_libdir}/samba/libauth4-private-samba.so
%{_libdir}/samba/libauth-unix-token-private-samba.so
%{_libdir}/samba/libauthn-policy-util-private-samba.so
%{_libdir}/samba/libauthkrb5-private-samba.so
%{_libdir}/samba/libcli-ldap-common-private-samba.so
%{_libdir}/samba/libcli-ldap-private-samba.so
%{_libdir}/samba/libcli-nbt-private-samba.so
%{_libdir}/samba/libcli-cldap-private-samba.so
%{_libdir}/samba/libcli-smb-common-private-samba.so
%{_libdir}/samba/libcli-spoolss-private-samba.so
%{_libdir}/samba/libcliauth-private-samba.so
%{_libdir}/samba/libclidns-private-samba.so
%{_libdir}/samba/libsamba-net.cpython*.so
%{_libdir}/samba/libsamba-python.cpython*.so
%{_libdir}/samba/libcluster-private-samba.so
%{_libdir}/samba/libcmdline-contexts-private-samba.so
%{_libdir}/samba/libcmdline-private-samba.so
%{_libdir}/samba/libdcerpc-pkt-auth-private-samba.so
%{_libexecdir}/samba/samba-bgqd
%{_unitdir}/samba-bgqd.service
%{_libexecdir}/samba/rpcd_*
%{_libexecdir}/samba/samba-dcerpcd
%{_libdir}/samba/libcommon-auth-private-samba.so
%{_libdir}/samba/libdb-glue-private-samba.so
%{_libdir}/samba/libdbwrap-private-samba.so
#{_libdir}/samba/libdcerpc-private-samba.so
%{_libdir}/samba/libdcerpc-samba-private-samba.so
%{_libdir}/samba/libdcerpc-samba4-private-samba.so
%{_libdir}/samba/libREG-FULL-private-samba.so
%{_libdir}/samba/libRPC-SERVER-LOOP-private-samba.so
%{_libdir}/samba/libRPC-WORKER-private-samba.so
%{_libdir}/samba/libdfs-server-ad-private-samba.so
%{_libdir}/samba/libdlz-bind9-for-torture-private-samba.so
%{_libdir}/samba/libdnsserver-common-private-samba.so
%{_libdir}/samba/libdsdb-module-private-samba.so
%{_libdir}/samba/libevents-private-samba.so
%{_libdir}/samba/libflag-mapping-private-samba.so
%{_libdir}/samba/libgensec-private-samba.so
%{_libdir}/samba/libgenrand-private-samba.so
%{_libdir}/samba/libgpext-private-samba.so
%{_libdir}/samba/libgpo-private-samba.so
%{_libdir}/samba/libgse-private-samba.so
%{_libdir}/samba/libhttp-private-samba.so
%{_libdir}/samba/libidmap-private-samba.so
%{_libdir}/samba/libinterfaces-private-samba.so
%{_libdir}/samba/libiov-buf-private-samba.so
%{_libdir}/samba/libkrb5samba-private-samba.so
%{_libdir}/samba/libldbsamba-private-samba.so
%{_libdir}/samba/liblibcli-lsa3-private-samba.so
%{_libdir}/samba/liblibcli-netlogon3-private-samba.so
%{_libdir}/samba/liblibsmb-private-samba.so
%{_libdir}/samba/libmessages-dgm-private-samba.so
%{_libdir}/samba/libmessages-util-private-samba.so
%{_libdir}/samba/libMESSAGING-SEND-private-samba.so
%{_libdir}/samba/libmsghdr-private-samba.so
%{_libdir}/samba/libmsrpc3-private-samba.so
%{_libdir}/samba/libndr-samba-private-samba.so
%{_libdir}/samba/libndr-samba4-private-samba.so
%{_libdir}/samba/libnet-keytab-private-samba.so
%{_libdir}/samba/libnetif-private-samba.so
%{_libdir}/samba/libnpa-tstream-private-samba.so
%{_libdir}/samba/libnss-info-private-samba.so
%{_libdir}/samba/libpac-private-samba.so
%{_libdir}/samba/libposix-eadb-private-samba.so
%{_libdir}/samba/libprinter-driver-private-samba.so
%{_libdir}/samba/libprinting-migrate-private-samba.so
%{_libdir}/samba/libprocess-model-private-samba.so
%{_libdir}/samba/libregistry-private-samba.so
%{_libdir}/samba/libreplace-private-samba.so
%{_libdir}/samba/libsamba-cluster-support-private-samba.so
%{_libdir}/samba/libsamba-debug-private-samba.so
%{_libdir}/samba/libsamba-modules-private-samba.so
%{_libdir}/samba/libsamba-security-private-samba.so
%{_libdir}/samba/libsamba-sockets-private-samba.so
%{_libdir}/samba/libsamba3-util-private-samba.so
%{_libdir}/samba/libsamdb-common-private-samba.so
%{_libdir}/samba/libsecrets3-private-samba.so
%{_libdir}/samba/libserver-id-db-private-samba.so
%{_libdir}/samba/libserver-role-private-samba.so
%{_libdir}/samba/libservice-private-samba.so
%{_libdir}/samba/libshares-private-samba.so
%{_libdir}/samba/libsmb-transport-private-samba.so
%{_libdir}/samba/libsmbclient-raw-private-samba.so
%{_libdir}/samba/libsmbd-base-private-samba.so
%{_libdir}/samba/libsmbd-shim-private-samba.so
%{_libdir}/samba/libsmbldaphelper-private-samba.so
%{_libdir}/samba/libsmbpasswdparser-private-samba.so
%{_libdir}/samba/libsys-rw-private-samba.so
%{_libdir}/samba/libsocket-blocking-private-samba.so
%{_libdir}/samba/libtalloc-report-private-samba.so
%{_libdir}/samba/libtalloc-report-printf-private-samba.so
%{_libdir}/samba/libtdb-wrap-private-samba.so
%{_libdir}/samba/libtime-basic-private-samba.so
%{_libdir}/samba/libtorture-private-samba.so
%{_libdir}/samba/libtrusts-util-private-samba.so
%{_libdir}/samba/libutil-reg-private-samba.so
%{_libdir}/samba/libutil-setid-private-samba.so
%{_libdir}/samba/libutil-tdb-private-samba.so
#{_libdir}/samba/libwinbind-client-private-samba.so
%{_libdir}/samba/libxattr-tdb-private-samba.so
%{_libdir}/samba/libstable-sort-private-samba.so

%if %{with doc}
%files doc
%doc README COPYING Manifest Read-Manifest-Now
%doc WHATSNEW.txt Roadmap
%doc README.%{name}-mandrake-rpm
%doc clean-docs/samba-doc/docs/*
%doc clean-docs/samba-doc/examples
%endif

%files client
%{_bindir}/cifsdd
%{_bindir}/dbwrap_tool
%{_sbindir}/eventlogadm
%{_bindir}/findsmb
%{_bindir}/mdsearch
%{_bindir}/net
%{_bindir}/nmblookup
%{_bindir}/pdbedit
%{_bindir}/profiles
%{_bindir}/rpcclient
%{_bindir}/sharesec
%{_bindir}/samba-regedit
%{_bindir}/samba-tool
%{_bindir}/smbcacls
%{_bindir}/smbclient
%{_bindir}/smbcontrol
%{_bindir}/smbcquotas
%{_bindir}/smbget
%{_bindir}/smbpasswd
%{_bindir}/smbspool
%{_libexecdir}/samba/smbspool_krb5_wrapper
%{_bindir}/smbstatus
%{_bindir}/smbtree
%{_bindir}/smbtar
%{_sbindir}/samba_kcc
%{_bindir}/wspsearch
%{_mandir}/man1/dbwrap_tool.1*
%{_mandir}/man1/nmblookup.1*
%{_mandir}/man1/profiles.1*
%{_mandir}/man1/rpcclient.1*
%{_mandir}/man1/sharesec.1*
%{_mandir}/man1/smbcacls.1*
%{_mandir}/man1/smbclient.1*
%{_mandir}/man1/smbcontrol.1*
%{_mandir}/man1/smbcquotas.1*
%{_mandir}/man1/smbget.1*
%{_mandir}/man1/mdsearch.1*
%{_mandir}/man1/smbstatus.1*
%{_mandir}/man1/wspsearch.1*
%{_mandir}/man5/smbpasswd.5*
%{_mandir}/man8/samba-dcerpcd.8.*
%{_mandir}/man8/eventlogadm.8*
%{_mandir}/man8/net.8*
%{_mandir}/man8/pdbedit.8*
%{_mandir}/man8/samba-regedit.8*
%{_mandir}/man8/samba-tool.8*
%{_mandir}/man8/smbpasswd.8*
%{_mandir}/man8/smbspool.8*
%{_mandir}/man8/smbspool_krb5_wrapper.8*
%{_mandir}/man8/vfs_btrfs.8*
%{_mandir}/man8/vfs_expand_msdfs.8.*
%{_mandir}/man8/vfs_gpfs.8*
%{_mandir}/man8/vfs_glusterfs_fuse.8*
%{_mandir}/man8/vfs_io_uring.8*
%{_mandir}/man8/vfs_linux_xfs_sgid.8*
%{_mandir}/man8/vfs_syncops.8*
%{_mandir}/man8/vfs_fruit.8*
%{_mandir}/man8/vfs_snapper.8*
%{_mandir}/man8/vfs_widelinks.8*
%{_mandir}/man8/vfs_worm.8*
%{_mandir}/man8/samba-bgqd.8*

# Link of smbspool to CUPS
%if %{build_cupspc}
%{_prefix}/lib/cups/backend/smb
%endif

%if "%{_lib}" != "lib"
# FIXME workaround for versions up to 4.19.3-1 (after OMLx 5.0, before ROME 23.12)
# containing %{_libdir}/cups/backend/smb when cups wants %{_prefix}/lib
%post client
if ! [ -h %{_libdir}/cups ]; then
	rm -rf %{_libdir}/cups
	ln -s ../lib/cups %{_libdir}/cups
fi
%endif


%files common
%dir /var/cache/%{name}
%dir /var/log/%{name}
%dir /var/run/%{name}
%dir /var/lib/%{name}/private
%(for i in %{_bindir}/{%{commonbin}};do echo $i;done)
%(for i in %{_mandir}/man?/{%{commonbin}}\.[0-9]*;do echo $i|grep -vE '(testparm|dumpmscat)';done)
%dir %{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smb.conf
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/lmhosts
%dir %{_localstatedir}/lib/%{name}
%attr(-,root,root) %{_localstatedir}/lib/%{name}/codepages
%{_tmpfilesdir}/%{name}.conf
%{_presetdir}/86-samba.preset
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbtree.1*
%{_mandir}/man1/testparm.1*
%{_mandir}/man5/lmhosts.5*
%{_mandir}/man5/smb.conf.5*
%{_mandir}/man7/samba.7*
%{_mandir}/man8/cifsdd.8*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man7/traffic_learner.7.*
%{_mandir}/man7/traffic_replay.7.*
%{_mandir}/man8/vfs_acl_tdb.8*
%{_mandir}/man8/vfs_acl_xattr.8*
%{_mandir}/man8/vfs_aio_fork.8*
%{_mandir}/man8/vfs_aio_pthread.8*
%{_mandir}/man8/vfs_audit.8*
%{_mandir}/man8/vfs_cap.8*
%{_mandir}/man8/vfs_catia.8*
%{_mandir}/man8/vfs_commit.8*
%{_mandir}/man8/vfs_crossrename.8*
%{_mandir}/man8/vfs_default_quota.8*
%{_mandir}/man8/vfs_dirsort.8*
%{_mandir}/man8/vfs_extd_audit.8*
%{_mandir}/man8/vfs_fake_perms.8*
%{_mandir}/man8/vfs_fileid.8*
%{_mandir}/man8/vfs_full_audit.8*
%{_mandir}/man8/vfs_media_harmony.8*
#{_mandir}/man8/vfs_netatalk.8*
%{_mandir}/man8/vfs_offline.8*
%{_mandir}/man8/vfs_preopen.8*
%{_mandir}/man8/vfs_readahead.8*
%{_mandir}/man8/vfs_readonly.8*
%{_mandir}/man8/vfs_recycle.8*
%{_mandir}/man8/vfs_shadow_copy.8*
%{_mandir}/man8/vfs_shadow_copy2.8*
%{_mandir}/man8/vfs_shell_snap.8*
%{_mandir}/man8/vfs_streams_depot.8*
%{_mandir}/man8/vfs_streams_xattr.8*
%{_mandir}/man8/vfs_time_audit.8*
%{_mandir}/man8/vfs_unityed_media.8*
%{_mandir}/man8/vfs_virusfilter.8*
%{_mandir}/man8/vfs_xattr_tdb.8*

%files winbind
#config(noreplace) %{_sysconfdir}/security/pam_winbind.conf
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/pam.d/system-auth-winbind*
%{_sysconfdir}/NetworkManager/dispatcher.d/30-winbind
%{_unitdir}/winbind.service
%{_bindir}/ntlm_auth
%{_bindir}/wbinfo
%{_sbindir}/winbindd
%attr(755,root,root) /%{_lib}/security/pam_winbind.so
%attr(755,root,root) /%{_lib}/libnss_winbind.so.*
%{_libdir}/%{name}/idmap
%{_libdir}/%{name}/nss_info
%{_libdir}/samba/krb5/winbind_krb5_locator.so
%{_mandir}/man1/ntlm_auth.1*
%{_mandir}/man1/wbinfo.1*
%{_mandir}/man5/pam_winbind.conf.5*
%{_mandir}/man8/winbind_krb5_locator.8*
%{_mandir}/man8/idmap_*.8*
%{_mandir}/man8/pam_winbind.8*
%{_mandir}/man8/winbindd.8*

%files -n nss_wins
%attr(755,root,root) /%{_lib}/libnss_wins.so.*

%files python
%{py_platsitedir}/samba

%if %{build_test}
%files test
%(for i in %{_bindir}/{%{testbin}};do echo $i;done)
%(for i in %{_mandir}/man1/{%{testbin}}.1%{_extension};do echo $i|grep -v nsstest;done)
%endif

%files devel
%{_includedir}/samba-4.0/charset.h
%dir %{_includedir}/samba-4.0/core
%{_includedir}/samba-4.0/core/*.h
%{_includedir}/samba-4.0/domain_credentials.h
%dir %{_includedir}/samba-4.0/gen_ndr
%{_includedir}/samba-4.0/gen_ndr/*.h
%{_includedir}/samba-4.0/param.h
%{_includedir}/samba-4.0/samba/
%{_includedir}/samba-4.0/share.h
%{_includedir}/samba-4.0/tdr.h
%{_includedir}/samba-4.0/tsocket.h
%{_includedir}/samba-4.0/tsocket_internal.h
%{_includedir}/samba-4.0/rpc_common.h
%dir %{_includedir}/samba-4.0/util/
%{_includedir}/samba-4.0/util/*.h
%{_includedir}/samba-4.0/util_ldb.h
%{_includedir}/samba-4.0/ldb_wrap.h
%{_includedir}/samba-4.0/lookup_sid.h
%{_includedir}/samba-4.0/machine_sid.h
%{_includedir}/samba-4.0/passdb.h
%{_includedir}/samba-4.0/smb_ldap.h
%{_includedir}/samba-4.0/smb2_lease_struct.h
%{_includedir}/samba-4.0/smb3posix.h
%{_includedir}/samba-4.0/dcesrv_core.h
#/%{_lib}/libnss_winbind.so
#/%{_lib}/libnss_wins.so

%files -n %{libdcerpc}
%{_libdir}/libdcerpc.so.%{major}*
%{_libdir}/libdcerpc-binding.so.%{major}*
%{_libdir}/libdcerpc-samr.so.%{major}*
%{_libdir}/libdcerpc-server.so.%{major}*
%{_libdir}/libdcerpc-server-core.so.%{major}*

%files -n %{devdcerpc}
%{_libdir}/pkgconfig/dcerpc*.pc
%{_includedir}/samba-4.0/dcerpc*.h
%{_libdir}/libdcerpc.so
%{_libdir}/libdcerpc-binding.so
%{_libdir}/libdcerpc-samr.so
%{_libdir}/libdcerpc-server.so
%{_libdir}/libdcerpc-server-core.so

%files -n %{libndr}
%{_libdir}/libndr.so.%{ndrmajor}*
%{_libdir}/libndr-krb5pac.so.%{ndrsubmajor}*
%{_libdir}/libndr-nbt.so.%{ndrsubmajor}*
%{_libdir}/libndr-standard.so.%{ndrsubmajor}*

%files -n %{devndr}
%{_includedir}/samba-4.0/ndr.h
%{_includedir}/samba-4.0/ndr
%{_libdir}/pkgconfig/ndr.pc
%{_libdir}/pkgconfig/ndr_krb5pac.pc
%{_libdir}/pkgconfig/ndr_nbt.pc
%{_libdir}/pkgconfig/ndr_standard.pc
%{_libdir}/libndr.so
%{_libdir}/libndr-krb5pac.so
%{_libdir}/libndr-nbt.so
%{_libdir}/libndr-standard.so

%files -n %{libnetapi}
%{_libdir}/libnetapi.so.%{netapimajor}*

%files -n %{devnetapi}
%{_libdir}/libnetapi*.so
%{_includedir}/samba-4.0/netapi.h
%{_libdir}/pkgconfig/netapi.pc

%files -n %{libsambapassdb}
%{_libdir}/libsamba-passdb.so.%{major}*

%files -n %{devsambapassdb}
%{_libdir}/libsamba-passdb.so

%files -n %{libsambacredentials}
%{_libdir}/libsamba-credentials.so.1*

%files -n %{devsambacredentials}
%{_includedir}/samba-4.0/credentials.h
%{_libdir}/libsamba-credentials.so
%{_libdir}/pkgconfig/samba-credentials.pc

%files -n %{libsambaerrors}
%{_libdir}/libsamba-errors.so.1*

%files -n %{devsambaerrors}
%{_libdir}/libsamba-errors.so

%files -n %{libsambahostconfig}
%{_libdir}/libsamba-hostconfig.so.%{major}*

%files -n %{devsambahostconfig}
%{_libdir}/libsamba-hostconfig.so
%{_libdir}/pkgconfig/samba-hostconfig.pc

%files -n %{libsambapolicy}
%{_libdir}/libsamba-policy.cpython*.so.%{major}*

%files -n %{devsambapolicy}
%{_includedir}/samba-4.0/policy.h
%{_libdir}/libsamba-policy.cpython*.so
%{_libdir}/pkgconfig/samba-policy.cpython*.pc

%files -n %{libsambautil}
%{_libdir}/libsamba-util.so.%{major}*

%files -n %{devsambautil}
%{_libdir}/libsamba-util.so
%{_libdir}/pkgconfig/samba-util.pc

%files -n %{libsamdb}
%{_libdir}/libsamdb.so.%{major}*

%files -n %{devsamdb}
%{_libdir}/libsamdb.so
%{_libdir}/pkgconfig/samdb.pc

%files -n %{libsmbclient}
%{_libdir}/libsmbclient.so.%{major}*

%files -n %{devsmbclient}
%{_includedir}/samba-4.0/libsmbclient.h
%{_libdir}/libsmbclient.so
%{_mandir}/man7/libsmbclient.7*
%{_libdir}/pkgconfig/smbclient.pc

%files -n %{libsmbconf}
%{_libdir}/libsmbconf.so.%{major}*

%files -n %{devsmbconf}
%{_includedir}/samba-4.0/smbconf.h
%{_libdir}/libsmbconf.so

%files -n %{libsmbldap}
%{_libdir}/libsmbldap.so.%{ldapmajor}*

%files -n %{devsmbldap}
%{_includedir}/samba-4.0/smbldap.h
%{_libdir}/libsmbldap.so

%files -n %{libtevent_util}
%{_libdir}/libtevent-util.so.%{major}*

%files -n %{devtevent_util}
%{_libdir}/libtevent-util.so

%files -n %{libwbclient}
%{_libdir}/libwbclient.so.%{major}*

%files -n %{devwbclient}
%{_libdir}/libwbclient.so
%{_includedir}/samba-4.0/wbclient.h
%{_libdir}/pkgconfig/wbclient.pc

%if %{build_pgsql}
%files passdb-pgsql
%{_libdir}/%{name}/pdb/*pgsql.so
%endif

%if %{with cifs}
%files -n mount-cifs
%attr(4755,root,root) /*bin/*mount.cifs
%endif

%if %{with gtk}
%files domainjoin-gui
%{_sbindir}/netdomjoin-gui
%dir %{_datadir}/pixmaps/samba
%{_datadir}/pixmaps/samba/samba.ico
%{_datadir}/pixmaps/samba/logo.png
%{_datadir}/pixmaps/samba/logo-small.png
%endif
