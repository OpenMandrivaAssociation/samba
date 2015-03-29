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
%define debug_package %{nil}

# Default options
%bcond_without ads
%bcond_with cifs
%bcond_with doc
%bcond_with gtk
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
%define libdcerpc %mklibname dcerpc %{major}
%define devdcerpc %mklibname -d dcerpc
%define libgensec %mklibname gensec %{major}
%define devgensec %mklibname -d gensec
%define libndr %mklibname ndr %{major}
%define devndr %mklibname -d ndr
%define libnetapi %mklibname netapi %{major}
%define devnetapi %mklibname -d netapi
%define libsambapassdb %mklibname sambapassdb %{major}
%define devsambapassdb %mklibname -d sambapassdb
%define libregistry %mklibname registry %{major}
%define devregistry %mklibname -d registry
%define libsambacredentials %mklibname samba-credentials %{major}
%define devsambacredentials %mklibname -d samba-credentials 
%define libsambahostconfig %mklibname samba-hostconfig %{major}
%define devsambahostconfig %mklibname -d samba-hostconfig
%define libsambapolicy %mklibname samba-policy %{major}
%define devsambapolicy %mklibname -d samba-policy
%define libsambautil %mklibname samba-util %{major}
%define devsambautil %mklibname -d samba-util
%define libsamdb %mklibname samdb %{major}
%define devsamdb %mklibname -d samdb
%define libsmbclient %mklibname smbclient %{major}
%define devsmbclient %mklibname -d smbclient 
%define libsmbconf %mklibname smbconf %{major}
%define devsmbconf %mklibname -d smbconf
%define libsmbldap %mklibname smbldap %{major}
%define devsmbldap %mklibname -d smbldap
%define libtevent_util %mklibname tevent-util %{major}
%define devtevent_util %mklibname -d tevent-util
%define libtorture %mklibname torture %{major}
%define devtorture %mklibname -d torture 
%define libwbclient %mklibname wbclient %{major}
%define devwbclient %mklibname -d wbclient

#Define sets of binaries that we can use in globs and loops:
%global commonbin	testparm,regdiff,regpatch,regshell,regtree
%global serverbin 	oLschema2ldif
%global serversbin	samba,samba_dnsupdate,samba_spnupdate
%global testbin 	smbtorture,masktest,locktest,gentest,ndrdump

%define build_expsam xml%{?_with_pgsql:,pgsql}%{?_with_mysql:,mysql}

%define _serverbuild_flags -fstack-protector-all

Summary:	Samba SMB server
Name:		samba
Epoch:		1
Version:	4.2.0
Release:	1
License:	GPLv3
Group:		System/Servers
Url:		https://www.samba.org
Source0:	https://ftp.samba.org/pub/samba/stable/samba-%{version}.tar.gz
Source99:	https://ftp.samba.org/pub/samba/stable/samba-%{version}.tar.asc
Source98:	https://ftp.samba.org/pub/samba/samba-pubkey.asc
Source1:	samba.log
Source3:	samba.xinetd
#Source7:	README.%{name}-mandrake-rpm
Source10:	samba-print-pdf.sh
Source100:	%{name}.rpmlintrc
#Sources that used to be in packaging patch:
Source20:	smbusers
Source21:	smbprint
#Source22:	smbadduser
Source23:	findsmb
Source26:	wrepld.init
Source28:	samba.pamd
Source29:	system-auth-winbind.pamd
Source30:	%{name}-tmpfiles.conf
# xdr_* functions have moved from glibc into libtirpc
# Patch2:		samba-4.0.0-tirpc.patch

BuildRequires:	docbook-style-xsl
BuildRequires:	gnupg
BuildRequires:	python-tdb
BuildRequires:	python-tevent
BuildRequires:	xsltproc
BuildRequires:	acl-devel
BuildRequires:	keyutils-devel
BuildRequires:	magic-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ctdb) >= 2.0
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(ldb)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(pyldb-util)
BuildRequires:	pkgconfig(pytalloc-util)
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(tdb) >= 1.2.1
BuildRequires:	pkgconfig(tevent)
%if %{with ads}
BuildRequires:	krb5-devel
%endif
%if %{build_mysql}
BuildRequires:	mysql-devel
%endif
%if %{build_pgsql}
BuildRequires:	postgresql-devel
%endif

#### there is no straight samba rpm...
Requires(pre):	mktemp 
Requires(pre):	psmisc
Requires(pre):	coreutils
Requires(pre):	sed
Requires(pre):	grep
Requires:	pam >= 0.64
Requires:	samba-common = %{EVRD}

%define __noautoreq 'devel.*'

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
Requires(pre):	rpm-helper
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
Requires:	mount-cifs
# For samba-tool
Requires:	python-talloc
Requires:	python-ldb
Requires:	python-tdb
Requires:	ldb-utils
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
%rename 	samba-common-ldap
Conflicts:	samba3-common

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.

%package	libs
Summary:	Common libraries used by both Samba servers and clients
Group:		System/Libraries
Conflicts:	%{name}-server < 1:4.1.12-2

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
Requires(pre):	glibc

%description -n nss_wins
Provides the libnss_wins shared library which resolves NetBIOS names to 
IP addresses.

%package python
Summary:	Samba Python modules
Group:		Development/Python
BuildRequires:	pkgconfig(python2)

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

%package pidl
Summary:	Perl IDL compiler for Samba
Group:		Development/Perl

%description pidl
Perl Interface Description Language compiler for Samba.

%package -n %{libdcerpc}
Summary:	Library implementing DCE/RPC for Samba
Group:		System/Libraries

%description -n %{libdcerpc}
Library implementing DCE/RPC for Samba.

%package -n %{devdcerpc}
Summary:	Library implementing Samba's memory allocator
Group:		Development/C
Requires:	%{libdcerpc} = %{EVRD}

%description -n %{devdcerpc}
Library implementing Samba's memory allocator.

%package -n %{libgensec}
Summary:	Samba generic security library
Group:		System/Libraries

%description -n %{libgensec}
Samba generic security library.

%package -n %{devgensec}
Summary:	Development files for Samba generic security library
Group:		Development/C
Requires:	%{libgensec} = %{EVRD}

%description -n %{devgensec}
Development files for Samba generic security library.

%package -n %{libndr}
Summary:	Network Data Representation library from Samba
Group:		System/Libraries

%description -n %{libndr}
Network Data Representation library from Samba.

%package -n %{devndr}
Summary:	Development files for Network Data Representation library from Samba
Group:		Development/C
Requires:	%{libndr} = %{EVRD}

%description -n %{devndr}
Development files for Network Data Representation library from Samba.

%package -n %{libnetapi}
Summary:	Samba library for accessing functions in 'net' binary
Group:		System/Libraries

%description -n %{libnetapi}
Samba library for accessing functions in 'net' binary.

%package -n %{devnetapi}
Summary:	Samba library for accessing functions in 'net' binary
Group:		Development/C
Requires:	%{libnetapi} = %{EVRD}

%description -n %{devnetapi}
Samba library for accessing functions in 'net' binary.

%package -n %{libsambapassdb}
Summary:	Library for working with the Samba user database
Group:		System/Libraries

%description -n %{libsambapassdb}
Library for working with the Samba user database.

%package -n %{devsambapassdb}
Summary:	Development files for Samba user database library
Group:		Development/C
Requires:	%{libsambapassdb} = %{EVRD}
Provides:	samba-passdb-devel = %{EVRD}

%description -n %{devsambapassdb}
Development files for Samba user database library.

%package -n %{libregistry}
Summary:	Samba registry library
Group:		System/Libraries

%description -n %{libregistry}
Samba registry library.

%package -n %{devregistry}
Summary:	Development files for Samba registry library
Group:		Development/C
Requires:	%{libregistry} = %{EVRD}

%description -n %{devregistry}
Development files for Samba registry library.

%package -n %{libsambacredentials}
Summary:	Library for working with Samba credentials
Group:		System/Libraries

%description -n %{libsambacredentials}
Library for working with Samba credentials.

%package -n %{devsambacredentials}
Summary:	Development files for Samba credentials library
Group:		Development/C
Requires:	%{libsambacredentials} = %{EVRD}

%description -n %{devsambacredentials}
Development files for Samba credentials library.

%package -n %{libsambahostconfig}
Summary:	Samba's host configuration library
Group:		System/Libraries

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

%description -n %{libtevent_util}
Utility library for working with the Tevent library.

%package -n %{devtevent_util}
Group:		Development/C
Summary:	Development files for Tevent library
Requires:	%{libtevent_util} = %{EVRD}

%description -n %{devtevent_util}
Development files for Samba Tevent library.

%package -n %{libtorture}
Summary:	Samba testsuite torture library
Group:		Networking/Other

%description -n %{libtorture}
Samba testsuite torture library.

%package -n %{devtorture}
Summary:	Development files for Samba torture library
Group:		Development/C
Requires:	%{libtorture} = %{EVRD}

%description -n %{devtorture}
Development files for Samba torture library.

%package -n %{libwbclient}
Summary:	Library providing access to winbindd
Group:		System/Libraries

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

%setup -q
# %patch2 -p1 -b .tirpc~

%build
# samba doesnt support python3 yet
export PYTHON=%{__python2}

#LDFLAGS=-ltirpc %{__python} buildtools/bin/waf configure \
LDFLAGS=-ltirpc  %configure \
	--enable-fhs \
	--with-privatelibdir=%{_libdir}/%{name} \
	--bundled-libraries=ntdb,heimdal,!zlib,!popt,!talloc,!tevent,!tdb,!ldb \
	--enable-gnutls \
	--enable-cups \
	--enable-avahi \
	--with-pam \
	--with-pam_smbpass \
%if %{with winbind}
	--with-winbind \
%endif
%if %{with ads}
	--with-ads \
%else
	--without-ads \
%endif
	--with-ldap \
	--disable-rpath \
	--disable-rpath-install \
	--disable-rpath-private-install \
	--enable-pthreadpool \
	--enable-avahi \
	--with-iconv \
	--with-acl-support \
	--with-dnsupdate \
	--with-syslog \
	--with-automount \
	--with-aio-support \
	--with-cluster-support \
	--with-sendfile-support \
	--with-dnsupdate \
	--with-systemd \
	--with-piddir=/run \
	--without-cluster \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir} \
	--datadir=%{_datadir} \
	--localstatedir=%{_localstatedir} \
	--with-modulesdir=%{_libdir}/%{name} \
	-v -v -p \
	%{?_smp_mflags}

#	--with-system-mitkrb5 <--- probably a good idea, but causes
#	samba_upgradeprovision and friends not to be built

%{__python2} buildtools/bin/waf build -j10 -v -v %?_smp_mflags

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

PYTHON=%{__python2} %makeinstall_std
# PAM modules don't go to /usr...
if [ -e %{buildroot}%{_libdir}/security ]; then
	mkdir -p %{buildroot}/%{_lib}
	mv %{buildroot}%{_libdir}/security %{buildroot}/%{_lib}
fi

#need to stay
mkdir -p %{buildroot}/{sbin,bin}
mkdir -p %{buildroot}%{_sysconfdir}/{logrotate.d,pam.d,xinetd.d}
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
mkdir -p %{buildroot}%{_sbindir}
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
install -m644 packaging/LSB/smb.conf %{buildroot}/%{_sysconfdir}/%{name}/smb.conf
cat packaging/LSB/smb.conf | \
touch %{buildroot}/%{_sysconfdir}/%{name}/smb.conf
#sed -e 's/^;   printer admin = @adm/   printer admin = @adm/g' >%{buildroot}/%{_sysconfdir}/%{name}/smb.conf
%if %{build_cupspc}
#perl -pi -e 's/printcap name = lpstat/printcap name = cups/g' %{buildroot}/%{_sysconfdir}/%{name}/smb.conf
#perl -pi -e 's/printcap name = lpstat/printcap name = cups/g' %{buildroot}/%{_sysconfdir}/%{name}/smb-winbind.conf
# Link smbspool to CUPS (does not require installed CUPS)

        mkdir -p %{buildroot}/%{_libdir}/cups/backend
        ln -s %{_bindir}/smbspool %{buildroot}/%{_libdir}/cups/backend/smb
%endif

        echo 127.0.0.1 localhost > %{buildroot}/%{_sysconfdir}/%{name}/lmhosts

install -c -m 755 %{SOURCE10} %{buildroot}%{_datadir}/%{name}/scripts/print-pdf

# Move some stuff where it belongs...
mkdir -p %{buildroot}%{_lib}
mv %{buildroot}%{_libdir}/libnss* %{buildroot}/%{_lib}/

rm -f %{buildroot}/%{_mandir}/man1/testprns*

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat >%{buildroot}%{_sysconfdir}/ld.so.conf.d/samba.conf <<EOF
%{_libdir}/samba
EOF

mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
cp -a packaging/systemd/*.service %{buildroot}%{_unitdir}/
cp -a packaging/systemd/samba.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/samba

# MD removal of orphan manpages 
rm -f %{buildroot}%{_mandir}/man1/log2pcap.1*
rm -f %{buildroot}%{_mandir}/man1/vfstest.1*

# tmpfiles for runtime dir creation
install -D -p -m 0644 %{SOURCE30} %{buildroot}%{_tmpfilesdir}/%{name}.conf

# install NM dispatcher file
install -d -m 0755 %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/
install -m 0755 packaging/NetworkManager/30-winbind-systemd %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/30-winbind

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
	perl -pi -e 's/ winbind//' %{_sysconfdir}/nsswitch.conf

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
	perl -pi -e 's/ wins//' %{_sysconfdir}/nsswitch.conf
fi

%files server
%(for i in %{_sbindir}/{%{serversbin}};do echo $i;done)
%(for i in %{_bindir}/%{serverbin};do echo $i;done)
%attr(755,root,root) /%{_lib}/security/pam_smbpass*
%{_libdir}/%{name}/vfs/*.so
%{_libdir}/samba/ldb
%{_libdir}/samba/service
%{_libdir}/samba/process_model
%{_libdir}/samba/gensec
%{_libdir}/samba/auth
%{_libdir}/samba/bind9
%dir %{_libdir}/samba/vfs
%{_libdir}/mit_samba.so
%{_sbindir}/smbd
%{_sbindir}/nmbd
%{_sbindir}/samba_upgradedns
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
%{_datadir}/samba/setup
%attr(0755,root,root) %{_datadir}/%{name}/scripts/print-pdf
%{_mandir}/man8/samba.8*
%{_unitdir}/samba.service
%{_unitdir}/smb.service
%{_unitdir}/nmb.service
%config(noreplace) %{_sysconfdir}/sysconfig/samba

%files libs
%dir %{_libdir}/%{name}
%{_libdir}/samba/libCHARSET3-samba4.so
%{_libdir}/samba/libHDB-SAMBA4-samba4.so
%{_libdir}/samba/libLIBWBCLIENT-OLD-samba4.so
%{_libdir}/samba/libMESSAGING-samba4.so
%{_libdir}/samba/libaddns-samba4.so
%{_sysconfdir}/ld.so.conf.d
%if %{with ads}
%{_libdir}/samba/libads-samba4.so
%endif
%{_libdir}/samba/libasn1-samba4.so.8*
%{_libdir}/samba/libasn1util-samba4.so
%{_libdir}/samba/libauth-samba4.so
%{_libdir}/samba/libauth4-samba4.so
%{_libdir}/samba/libauth-sam-reply-samba4.so
%{_libdir}/samba/libauth-unix-token-samba4.so
%{_libdir}/samba/libauthkrb5-samba4.so
%{_libdir}/samba/libccan-samba4.so
%{_libdir}/samba/libcli-ldap-common-samba4.so
%{_libdir}/samba/libcli-ldap-samba4.so
%{_libdir}/samba/libcli-nbt-samba4.so
%{_libdir}/samba/libcli-cldap-samba4.so
%{_libdir}/samba/libcli-smb-common-samba4.so
%{_libdir}/samba/libcli-spoolss-samba4.so
%{_libdir}/samba/libcliauth-samba4.so
%{_libdir}/samba/libcluster-samba4.so
%{_libdir}/samba/libcmdline-credentials-samba4.so
%{_libdir}/samba/libdb-glue-samba4.so
%{_libdir}/samba/libdbwrap-samba4.so
%{_libdir}/samba/libdcerpc-samba4.so
%{_libdir}/samba/libdcerpc-samba-samba4.so
%{_libdir}/samba/libdfs-server-ad-samba4.so
%{_libdir}/samba/libdlz-bind9-for-torture-samba4.so
%{_libdir}/samba/libdnsserver-common-samba4.so
%{_libdir}/samba/libdsdb-module-samba4.so
%{_libdir}/samba/liberrors-samba4.so
%{_libdir}/samba/libevents-samba4.so
%{_libdir}/samba/libflag-mapping-samba4.so
%{_libdir}/samba/libgpo-samba4.so
%{_libdir}/samba/libgse-samba4.so
%{_libdir}/samba/libgssapi-samba4.so.2*
%{_libdir}/samba/libhcrypto-samba4.so.5*
%{_libdir}/samba/libhdb-samba4.so.11*
%{_libdir}/samba/libheimbase-samba4.so.1*
%{_libdir}/samba/libheimntlm-samba4.so.1*
%{_libdir}/samba/libhx509-samba4.so.5*
%{_libdir}/samba/libhttp-samba4.so
%{_libdir}/samba/libidmap-samba4.so
%{_libdir}/samba/libinterfaces-samba4.so
%{_libdir}/samba/libkdc-samba4.so.2*
%{_libdir}/samba/libkrb5-samba4.so.26*
%{_libdir}/samba/libkrb5samba-samba4.so
%{_libdir}/samba/libldbsamba-samba4.so
%{_libdir}/samba/liblibcli-lsa3-samba4.so
%{_libdir}/samba/liblibcli-netlogon3-samba4.so
%{_libdir}/samba/liblibsmb-samba4.so
%{_libdir}/samba/libmsrpc3-samba4.so
%{_libdir}/samba/libndr-samba-samba4.so
%{_libdir}/samba/libndr-samba4.so
%{_libdir}/samba/libnet-keytab-samba4.so
%{_libdir}/samba/libnetif-samba4.so
%{_libdir}/samba/libnon-posix-acls-samba4.so
%{_libdir}/samba/libnpa-tstream-samba4.so
%{_libdir}/samba/libnss-info-samba4.so
%{_libdir}/samba/libntdb.so.1*
%{_libdir}/samba/libntvfs-samba4.so
%{_libdir}/samba/libpac-samba4.so
%{_libdir}/samba/libpopt-samba3-samba4.so
%{_libdir}/samba/libposix-eadb-samba4.so
%{_libdir}/samba/libprinting-migrate-samba4.so
%{_libdir}/samba/libprocess-model-samba4.so
%{_libdir}/samba/libreplace-samba4.so
%{_libdir}/samba/libroken-samba4.so.19*
%{_libdir}/samba/libsamba-cluster-support-samba4.so
%{_libdir}/samba/libsamba-debug-samba4.so
%{_libdir}/samba/libsamba-modules-samba4.so
%{_libdir}/samba/libsamba-net-samba4.so
%{_libdir}/samba/libsamba-security-samba4.so
%{_libdir}/samba/libsamba-sockets-samba4.so
%{_libdir}/samba/libsamba3-util-samba4.so
%{_libdir}/samba/libsamba-python-samba4.so
%{_libdir}/samba/libsamdb-common-samba4.so
%{_libdir}/samba/libsecrets3-samba4.so
%{_libdir}/samba/libserver-role-samba4.so
%{_libdir}/samba/libservice-samba4.so
%{_libdir}/samba/libshares-samba4.so
%{_libdir}/samba/libsmb-transport-samba4.so
%{_libdir}/samba/libsmbd-base-samba4.so
%{_libdir}/samba/libsmbd-conn-samba4.so
%{_libdir}/samba/libsmbd-shim-samba4.so
%{_libdir}/samba/libsmbldaphelper-samba4.so
%{_libdir}/samba/libsmbpasswdparser-samba4.so
%{_libdir}/samba/libsmbregistry-samba4.so
%{_libdir}/samba/libsocket-blocking-samba4.so
%{_libdir}/samba/libsubunit-samba4.so
%{_libdir}/samba/libtdb-wrap-samba4.so
%{_libdir}/samba/libtdb-compat-samba4.so
%{_libdir}/samba/libtrusts-util-samba4.so
%{_libdir}/samba/libutil-cmdline-samba4.so
%{_libdir}/samba/libutil-ntdb-samba4.so
%{_libdir}/samba/libutil-reg-samba4.so
%{_libdir}/samba/libutil-setid-samba4.so
%{_libdir}/samba/libutil-tdb-samba4.so
%{_libdir}/samba/libwinbind-client-samba4.so
%{_libdir}/samba/libwind-samba4.so.0*
%{_libdir}/samba/libxattr-tdb-samba4.so

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
%{_bindir}/eventlogadm
%{_bindir}/net
%{_bindir}/nmblookup
%{_bindir}/ntdbbackup
%{_bindir}/ntdbdump
%{_bindir}/ntdbrestore
%{_bindir}/ntdbtool
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
%{_bindir}/smbstatus
%{_bindir}/smbta-util
%{_bindir}/smbtree
%{_bindir}/smbtar
%{_sbindir}/samba_kcc
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
%{_mandir}/man1/smbstatus.1*
%{_mandir}/man5/smbpasswd.5*
%{_mandir}/man8/eventlogadm.8*
%{_mandir}/man8/net.8*
%{_mandir}/man8/ntdbbackup.8*
%{_mandir}/man8/ntdbdump.8*
%{_mandir}/man8/ntdbrestore.8*
%{_mandir}/man8/ntdbtool.8*
%{_mandir}/man8/pdbedit.8*
%{_mandir}/man8/samba-regedit.8*
%{_mandir}/man8/samba-tool.8*
%{_mandir}/man8/smbpasswd.8*
%{_mandir}/man8/smbspool.8*
%{_mandir}/man8/smbta-util.8*
%{_mandir}/man8/vfs_btrfs.8*
%{_mandir}/man8/vfs_linux_xfs_sgid.8*
%{_mandir}/man8/vfs_syncops.8*
%{_mandir}/man8/vfs_ceph.8.*
%{_mandir}/man8/vfs_fruit.8.*
%{_mandir}/man8/vfs_glusterfs.8.*
%{_mandir}/man8/vfs_snapper.8.*
%{_mandir}/man8/vfs_worm.8.*

# Link of smbspool to CUPS
%if %{build_cupspc}
%{_libdir}/cups/backend/smb
%endif

%files common
%dir /var/cache/%{name}
%dir /var/log/%{name}
%dir /var/run/%{name}
%dir /var/lib/%{name}/private
%(for i in %{_bindir}/{%{commonbin}};do echo $i;done)
%(for i in %{_mandir}/man?/{%{commonbin}}\.[0-9]*;do echo $i|grep -v testparm;done)
%dir %{_datadir}/%{name}
%{_datadir}/samba/codepages
%dir %{_sysconfdir}/%{name}
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smb.conf
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/lmhosts
%dir %{_localstatedir}/lib/%{name}
%attr(-,root,root) %{_localstatedir}/lib/%{name}/codepages
%{_tmpfilesdir}/%{name}.conf
%{_mandir}/man1/findsmb.1*
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbtree.1*
%{_mandir}/man1/testparm.1*
%{_mandir}/man5/lmhosts.5*
%{_mandir}/man5/smb.conf.5*
%{_mandir}/man5/smbgetrc.5*
%{_mandir}/man7/samba.7*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man8/vfs_acl_tdb.8*
%{_mandir}/man8/vfs_acl_xattr.8*
%{_mandir}/man8/vfs_aio_fork.8*
%{_mandir}/man8/vfs_aio_linux.8*
%{_mandir}/man8/vfs_aio_pthread.8*
%{_mandir}/man8/vfs_audit.8*
%{_mandir}/man8/vfs_cacheprime.8*
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
%{_mandir}/man8/vfs_gpfs.8*
%{_mandir}/man8/vfs_media_harmony.8*
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
%{_mandir}/man8/vfs_time_audit.8*
%{_mandir}/man8/vfs_tsmsm.8*
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
%{_libdir}/winbind_krb5_locator.so
%{_mandir}/man1/ntlm_auth.1*
%{_mandir}/man1/wbinfo.1*
%{_mandir}/man5/pam_winbind.conf.5*
%{_mandir}/man7/winbind_krb5_locator.7*
%{_mandir}/man8/idmap_*.8*
%{_mandir}/man8/pam_winbind.8*
%{_mandir}/man8/winbindd.8*

%files -n nss_wins
%attr(755,root,root) /%{_lib}/libnss_wins.so.*

%files python
%{py2_platsitedir}/samba
%{_libdir}/python2.7/site-packages/ntdb.so

%if %{build_test}
%files test
%(for i in %{_bindir}/{%{testbin}};do echo $i;done)
%(for i in %{_mandir}/man1/{%{testbin}}.1%{_extension};do echo $i|grep -v nsstest;done)
%endif

%files devel
%{_includedir}/samba-4.0/charset.h
%dir %{_includedir}/samba-4.0/core
%{_includedir}/samba-4.0/core/*.h
%{_includedir}/samba-4.0/dlinklist.h
%{_includedir}/samba-4.0/domain_credentials.h
%dir %{_includedir}/samba-4.0/gen_ndr
%{_includedir}/samba-4.0/gen_ndr/*.h
%{_includedir}/samba-4.0/ldap*.h
%{_includedir}/samba-4.0/param.h
%{_includedir}/samba-4.0/samba/
%{_includedir}/samba-4.0/share.h
%{_includedir}/samba-4.0/smb2_lease.h
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
%{_includedir}/samba-4.0/read_smb.h
%{_includedir}/samba-4.0/roles.h
%{_includedir}/samba-4.0/smb2.h
%{_includedir}/samba-4.0/smb2_constants.h
%{_includedir}/samba-4.0/smb2_create_blob.h
%{_includedir}/samba-4.0/smb2_signing.h
%{_includedir}/samba-4.0/smb_cli.h
%{_includedir}/samba-4.0/smb_cliraw.h
%{_includedir}/samba-4.0/smb_common.h
%{_includedir}/samba-4.0/smb_composite.h
%{_includedir}/samba-4.0/smb_constants.h
%{_includedir}/samba-4.0/smb_ldap.h
%{_includedir}/samba-4.0/smb_raw.h
%{_includedir}/samba-4.0/smb_raw_interfaces.h
%{_includedir}/samba-4.0/smb_raw_signing.h
%{_includedir}/samba-4.0/smb_raw_trans2.h
%{_includedir}/samba-4.0/smb_request.h
%{_includedir}/samba-4.0/smb_seal.h
%{_includedir}/samba-4.0/smb_signing.h
%{_includedir}/samba-4.0/smb_unix_ext.h
%{_includedir}/samba-4.0/smb_util.h
%{_includedir}/samba-4.0/smb2_lease_struct.h
%{_includedir}/samba-4.0/tstream_smbXcli_np.h
/%{_lib}/libnss_winbind.so
/%{_lib}/libnss_wins.so
%{_mandir}/man3/ntdb.3*

%files pidl
%{_bindir}/pidl
%{perl_vendorlib}/Parse/Pidl*
#%{perl_vendorlib}/Parse/Yapp*
%optional %{_mandir}/man1/pidl.1.*
%optional %{_mandir}/man3/Parse::Pidl*.3pm.*

%files -n %{libdcerpc}
%{_libdir}/libdcerpc.so.%{major}*
%{_libdir}/libdcerpc-atsvc.so.%{major}*
%{_libdir}/libdcerpc-binding.so.%{major}*
%{_libdir}/libdcerpc-samr.so.%{major}*
%{_libdir}/libdcerpc-server.so.%{major}*

%files -n %{devdcerpc}
%{_libdir}/pkgconfig/dcerpc*.pc
%{_includedir}/samba-4.0/dcerpc*.h
%{_libdir}/libdcerpc.so
%{_libdir}/libdcerpc-atsvc.so
%{_libdir}/libdcerpc-binding.so
%{_libdir}/libdcerpc-samr.so
%{_libdir}/libdcerpc-server.so

%files -n %{libgensec}
%{_libdir}/libgensec.so.%{major}*

%files -n %{devgensec}
%{_includedir}/samba-4.0/gensec.h
%{_libdir}/libgensec.so
%{_libdir}/pkgconfig/gensec.pc

%files -n %{libndr}
%{_libdir}/libndr.so.%{major}*
%{_libdir}/libndr-krb5pac.so.%{major}*
%{_libdir}/libndr-nbt.so.%{major}*
%{_libdir}/libndr-standard.so.%{major}*

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
%{_libdir}/libnetapi.so.%{major}*

%files -n %{devnetapi}
%{_libdir}/libnetapi*.so
%{_includedir}/samba-4.0/netapi.h
%{_libdir}/pkgconfig/netapi.pc

%files -n %{libsambapassdb}
%{_libdir}/libsamba-passdb.so.%{major}*

%files -n %{devsambapassdb}
%{_libdir}/libsamba-passdb.so

%files -n %{libregistry}
%{_libdir}/libregistry.so.%{major}*

%files -n %{devregistry}
%{_includedir}/samba-4.0/registry.h
%{_libdir}/libregistry.so
%{_libdir}/pkgconfig/registry.pc

%files -n %{libsambacredentials}
%{_libdir}/libsamba-credentials.so.%{major}*

%files -n %{devsambacredentials}
%{_includedir}/samba-4.0/credentials.h
%{_libdir}/libsamba-credentials.so
%{_libdir}/pkgconfig/samba-credentials.pc

%files -n %{libsambahostconfig}
%{_libdir}/libsamba-hostconfig.so.%{major}*

%files -n %{devsambahostconfig}
%{_libdir}/libsamba-hostconfig.so
%{_libdir}/pkgconfig/samba-hostconfig.pc

%files -n %{libsambapolicy}
%{_libdir}/libsamba-policy.so.%{major}*

%files -n %{devsambapolicy}
%{_includedir}/samba-4.0/policy.h
%{_libdir}/libsamba-policy.so
%{_libdir}/pkgconfig/samba-policy.pc

%files -n %{libsambautil}
%{_libdir}/libsamba-util.so.%{major}*

%files -n %{devsambautil}
%{_includedir}/samba-4.0/samba_util.h
%{_libdir}/libsamba-util.so
%{_libdir}/pkgconfig/samba-util.pc

%files -n %{libsamdb}
%{_libdir}/libsamdb.so.%{major}*

%files -n %{devsamdb}
%{_libdir}/libsamdb.so
%{_libdir}/pkgconfig/samdb.pc

%files -n %{libsmbclient}
%{_libdir}/libsmbclient.so.%{major}*
%{_libdir}/libsmbclient-raw.so.%{major}*

%files -n %{devsmbclient}
%{_includedir}/samba-4.0/libsmbclient.h
%{_libdir}/libsmbclient.so
%{_libdir}/libsmbclient-raw.so
%{_mandir}/man7/libsmbclient.7*
%{_libdir}/pkgconfig/smbclient.pc
%{_libdir}/pkgconfig/smbclient-raw.pc

%files -n %{libsmbconf}
%{_libdir}/libsmbconf.so.%{major}*

%files -n %{devsmbconf}
%{_includedir}/samba-4.0/smbconf.h
%{_libdir}/libsmbconf.so

%files -n %{libsmbldap}
%{_libdir}/libsmbldap.so.%{major}*

%files -n %{devsmbldap}
%{_includedir}/samba-4.0/smbldap.h
%{_libdir}/libsmbldap.so

%files -n %{libtevent_util}
%{_libdir}/libtevent-util.so.%{major}*

%files -n %{devtevent_util}
%{_libdir}/libtevent-util.so

%files -n %{libtorture}
%{_libdir}/libtorture.so.%{major}*

%files -n %{devtorture}
%{_includedir}/samba-4.0/torture.h
%{_libdir}/libtorture.so
%{_libdir}/pkgconfig/torture.pc

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

