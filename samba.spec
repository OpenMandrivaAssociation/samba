%define libsmbmajor	0
%define netapimajor	0
%define smbsharemodesmajor	0
%define dcerpcmajor	0
%define hostconfigmajor	0
%define ndrmajor	0
%define	wbclientmajor	0
%define sambautilmajor	0
%define registrymajor 0
%define gensecmajor 0
%define samdbmajor 0
%define policymajor 0
%define pdbmajor 0
%define credentialsmajor 0
%define smbconfmajor 0
%define smbldapmajor 0
%define tevent_utilmajor 0

# Default options
%bcond_with doc
%bcond_without swat
%bcond_with cifs
%bcond_without ads
%define build_test	1
# CUPS supports functionality for 'printcap name = cups' (9.0 and later):
%define build_cupspc	0
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

%bcond_without gtk

%define libname %mklibname smbclient %libsmbmajor
%define libnetapi %mklibname netapi %netapimajor
%define netapidevel %mklibname -d netapi
%define libsmbsharemodes %mklibname smbsharemodes %smbsharemodesmajor
%define smbsharemodesdevel %mklibname -d smbsharemodes
%define libdcerpc %mklibname dcerpc %dcerpcmajor
%define dcerpcdevel %mklibname -d dcerpc
%define libsambahostconfig %mklibname samba-hostconfig %hostconfigmajor
%define sambahostconfigdevel %mklibname -d samba-hostconfig
%define libndr %mklibname ndr %ndrmajor
%define ndrdevel %mklibname -d ndr
%define libwbclient %mklibname wbclient %wbclientmajor
%define wbclientdevel %mklibname -d wbclient
%define libsambautil %mklibname samba-util %sambautilmajor
%define sambautildevel %mklibname -d samba-util
%define libregistry %mklibname registry %registrymajor
%define registrydevel %mklibname -d registry
%define libgensec %mklibname gensec %gensecmajor
%define gensecdevel %mklibname -d gensec
%define libpolicy %mklibname samba-policy %policymajor
%define libpolicydevel %mklibname -d samba-policy
%define libsamdb %mklibname samdb %samdbmajor
%define libsamdbdevel %mklibname -d samdb
%define libtorture %mklibname torture 0
%define libpdb %mklibname pdb %pdbmajor
%define libcredentials %mklibname samba-credentials %credentialsmajor
%define libsmbconf %mklibname smbconf %smbconfmajor
%define libsmbldap %mklibname smbldap %smbldapmajor
%define libtevent_util %mklibname tevent-util %tevent_utilmajor

#Define sets of binaries that we can use in globs and loops:
%global commonbin ntlm_auth,testparm,regdiff,regpatch,regshell,regtree

%global serverbin 	oLschema2ldif
%global serversbin samba,samba_dnsupdate,samba_spnupdate

%global clientbin 	samba-tool,nmblookup,smbclient,cifsdd
%global client_sbin 	mount.smb,mount.smbfs
%global clientbin_renameonly net,rpcclient,smbcacls,smbcquotas,smbpasswd,smbtree,profiles,pdbedit,sharesec,smbcontrol,smbstatus,smbta-util
%global cifs_bin	mount.cifs,umount.cifs
%global client_man	man1/nmblookup	

%global testbin 	smbtorture,masktest,locktest,gentest,ndrdump

%define build_expsam xml%{?_with_pgsql:,pgsql}%{?_with_mysql:,mysql}

Summary: Samba SMB server
Name: samba

Version: 4.0.1
Release: 1

License: GPLv3
Group: System/Servers
URL:	http://www.samba.org
Source0: http://ftp.samba.org/pub/samba/stable/samba-%version.tar.gz
Source99: http://ftp.samba.org/pub/samba/stable/samba-%version.tar.asc
Source98: http://ftp.samba.org/pub/samba/samba-pubkey.asc
Source1: samba.log
Source3: samba.xinetd
%if %{with swat}
Source4: swat_16.png
Source5: swat_32.png
Source6: swat_48.png
%endif
#Source7: README.%{name}-mandrake-rpm
BuildRequires: magic-devel
# For -fuse-ld
BuildRequires: gcc >= 4.6
Source10: samba-print-pdf.sh
Source100: %name.rpmlintrc

#Sources that used to be in packaging patch:
Source20:	smbusers
Source21:	smbprint
#Source22:	smbadduser
Source23:	findsmb
Source24:	smb.init
Source25:	winbind.init
Source26:	wrepld.init
Source28:	samba.pamd
Source29:	system-auth-winbind.pamd
Patch0:		samba4-socket-wrapper.patch
Patch1:		samba-4.0.0a20-compile.patch
# xdr_* functions have moved from glibc into libtirpc
Patch2:		samba-4.0.0-tirpc.patch
BuildRequires:	pkgconfig(libtirpc)

# Limbo patches (applied to prereleases, but not preleases, ie destined for
# samba CVS)
Requires: pam >= 0.64, samba-common = %{version}
BuildRequires: pam-devel readline-devel ncurses-devel popt-devel
BuildRequires: libxml2-devel
# Samba 3.2 and later should be built with capabilities support:
# http://lists.samba.org/archive/samba/2009-March/146821.html
BuildRequires: libcap-devel
BuildRequires: gnupg
# Required for ldb docs
BuildRequires: xsltproc docbook-style-xsl
%if %build_pgsql
BuildRequires: postgresql-devel
%endif
%if %build_mysql
BuildRequires: mysql-devel
%endif
BuildRequires: acl-devel
BuildRequires: libldap-devel
%if %{with ads}
BuildRequires: libldap-devel krb5-devel
%endif
BuildRequires: keyutils-devel
BuildRequires: pkgconfig(tdb) >= 1.2.1 python-tdb
BuildRequires: ldb-devel >= 1:1.1.7-0.beta8.1 pyldb-util-devel >= 1.1.7-0.beta8.1
BuildRequires: pkgconfig(tevent) python-tevent
BuildRequires: pkgconfig(talloc) pkgconfig(pytalloc-util)
BuildRequires: pkgconfig(ctdb) >= 2.0

Requires(pre): chkconfig mktemp psmisc
Requires(pre): coreutils sed grep

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
%if %build_non_default
WARNING: This RPM was built with command-line options. Please
see README.%{name}-mandrake-rpm in the documentation for
more information.
%endif

%package server
URL:	http://www.samba.org
Summary: Samba (SMB) server programs
Requires: %{name}-common = %{version}
# provision requires samba4-python
Requires: %{name}-python = %{version}
Requires(pre):		rpm-helper
Group: Networking/Other
Provides: samba = %version-%release
Obsoletes: samba < %version-%release
Provides:  samba-server-ldap = %version-%release
Obsoletes: samba-server-ldap < %version-%release

%description server
Samba-server provides a SMB server which can be used to provide
network services to SMB (sometimes called "Lan Manager")
clients. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame)
protocol.

Samba features working NT Domain Control capability and
includes the SWAT (Samba Web Administration Tool) that
allows samba's smb.conf file to be remotely managed using your
favourite web browser. For the time being this is being
enabled on TCP port 901 via xinetd. SWAT is now included in
it's own subpackage, samba-swat.

Please refer to the WHATSNEW.txt document for fixup information.
This binary release includes encrypted password support.

Please read the smb.conf file and ENCRYPTION.txt in the
docs directory for implementation details.

%package client
URL:	http://www.samba.org
Summary: Samba (SMB) client programs
Group: Networking/Other
Requires: %{name}-common = %{version}
Requires: mount-cifs
Provides:  samba3-client = %version-%release
Obsoletes: samba3-client < %version-%release
Obsoletes: smbfs
%ifarch x86_64
Conflicts:	cups < 1.2.0-0.5361.0mdk
%endif

%description client
Samba-client provides some SMB clients, which complement the built-in
SMB filesystem in Linux. These allow the accessing of SMB shares, and
printing to SMB printers.

%package common
URL:	http://www.samba.org
Summary: Files used by both Samba servers and clients
Group: System/Servers
# rpcclient etc. use samba python modules
Requires: %{name}-python = %{version}
Requires: %libpdb = %version-%release
Requires: %libcredentials = %version-%release
Requires: %libsmbconf = %version-%release
Requires: %libsmbldap = %version-%release
Requires: %libtevent_util = %version-%release
Provides:  samba-common-ldap = %version-%release
Obsoletes: samba-common-ldap < %version-%release

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.

%if %{with doc}
%package doc
URL:	http://www.samba.org
Summary: Documentation for Samba servers and clients
Group: System/Servers
Requires: %{name}-common = %{version}

%description doc
Samba-doc provides documentation files for both the server and client
packages of Samba.
%endif

%if %{with swat}
%package swat
URL:	http://www.samba.org
Summary: The Samba Web Administration Tool
Requires: %{name}-server = %{version}
Requires: xinetd
Group: System/Servers
Provides:  samba-swat-ldap = %version-%release
Obsoletes: samba-swat-ldap < %version-%release

%description swat
SWAT (the Samba Web Administration Tool) allows samba's smb.conf file
to be remotely managed using your favourite web browser. For the time
being this is being enabled on TCP port 901 via xinetd. Note that
SWAT does not use SSL encryption, nor does it preserve comments in
your smb.conf file. Webmin uses SSL encryption by default, and
preserves comments in configuration files, even if it does not display
them, and is therefore the preferred method for remotely managing
Samba.
%endif

%package winbind
URL:	http://www.samba.org
Summary: Samba-winbind daemon, utilities and documentation
Group: System/Servers
Requires: %{name}-common = %{version}

%description winbind
Provides the winbind daemon and testing tools to allow authentication 
and group/user enumeration from a Windows or Samba domain controller.

%package -n nss_wins
URL:	http://www.samba.org
Summary: Name Service Switch service for WINS
Group: System/Servers
Requires: %{name}-common = %{version}
Requires(pre): glibc

%description -n nss_wins
Provides the libnss_wins shared library which resolves NetBIOS names to 
IP addresses.

%package python
URL:	http://www.samba.org
Group:	Development/Python
Summary:	Samba Python modules
BuildRequires: python-devel

%description python
Samba Python modules

%if %build_test
%package test
URL:	http://www.samba.org
Summary: Debugging and benchmarking tools for samba
Group: System/Servers
Requires: %{name}-common = %{version}

%description test
This package provides tools for benchmarking samba, and debugging
the correct operation of tools against smb servers.
%endif

%package -n %{libname}
URL:		http://www.samba.org
Summary: 	SMB Client Library
Group:		System/Libraries
Provides:	libsmbclient

%description -n %{libname}
This package contains the SMB client library, part of the samba
suite of networking software, allowing other software to access
SMB shares.

%package -n %{libname}-devel
URL:		http://www.samba.org
Summary: 	SMB Client Library Development files
Group:		Development/C
Provides:	libsmbclient-devel = %{version}-%{release}
Requires:       %{libname} = %{version}-%{release}

%description -n %{libname}-devel
This package contains the development files for the SMB client
library, part of the samba suite of networking software, allowing
the development of other software to access SMB shares.

%package -n %{libname}-static-devel
URL:            http://www.samba.org
Summary:        SMB Client Static Library Development files
Group:          Development/C
Provides:       libsmbclient-static-devel = %{version}-%{release}
Requires:       %{libname}-devel = %{version}-%{release}

%description -n %{libname}-static-devel
This package contains the static development files for the SMB
client library, part of the samba suite of networking software,
allowing the development of other software to access SMB shares.

%package devel
Summary: Samba 4 development package
Group: Development/C
Requires: %{libname}-devel = %version-%release

%description devel
Samba 4 development libraries

%package pidl
Summary: Perl IDL compiler for Samba4
Group: Development/Perl

%description pidl
Perl Interface Description Language compiler for Samba4

%package -n %libnetapi
Summary: Samba library for accessing functions in 'net' binary
Group: System/Libraries

%description -n %libnetapi
Samba library for accessing functions in 'net' binary

%package -n %netapidevel
Group: Development/C
Summary: Samba library for accessing functions in 'net' binary
Provides: netapi-devel = %{version}-%{release}
Requires: %libnetapi = %{version}-%{release}

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
Provides: smbsharemodes-devel = %{version}-%{release}
Requires: %libsmbsharemodes = %{version}-%{release}

%description -n %smbsharemodesdevel
Samba Library for accessing smb share modes (locks etc.)

%package -n %libdcerpc
Group: System/Libraries
Summary: Library implementing DCE/RPC for Samba4

%description -n %libdcerpc
Library implementing DCE/RPC for Samba4

%package -n %dcerpcdevel
Group: Development/C
Summary: Library implementing Samba's memory allocator
Provides: dcerpc-devel = %version-%release
Requires: %libdcerpc = %version-%release

%description -n %dcerpcdevel
Library implementing Samba's memory allocator

%package -n %libndr
Group: System/Libraries
Summary: Network Data Representation library from Samba4

%description -n %libndr
Network Data Representation library from Samba4

%package -n %ndrdevel
Group: Development/C
Summary: Development files for Network Data Representation library from Samba4
Provides: ndr-devel = %version-%release
Requires: %libndr = %version-%release

%description -n %ndrdevel
Development files for Network Data Representation library from Samba4

%package -n %libsambahostconfig
Group: System/Libraries
Summary: Samba4's host configuration library

%description -n %libsambahostconfig
Samba4's host configuration library

%package -n %sambahostconfigdevel
Group: Development/C
Summary: Samba4's host configuration library
Provides: samba-hostconfig-devel = %version-%release
Requires: %libsambahostconfig = %version-%release

%description -n %sambahostconfigdevel
Samba4's host configuration library

%package -n %libwbclient
Group: System/Libraries
Summary: Library providing access to winbindd

%description -n %libwbclient
Library providing access to winbindd

%package -n %wbclientdevel
Group: Development/C
Summary: Library providing access to winbindd
Provides: wbclient-devel = %{version}-%{release}

%description -n %wbclientdevel
Library providing access to winbindd

%package -n %libsambautil
Group: System/Libraries
Summary: Samba4 utility library

%description -n %libsambautil
Samba4 utility library

%package -n %sambautildevel
Group: Development/C
Summary: Development files for Samba4 utility library
Provides: samba-util-devel = %version-%release
Requires: %libsambautil = %version-%release

%description -n %sambautildevel
Development files for Samba4 utility library

%package -n %libregistry
Group: System/Libraries
Summary: Samba4 registry library

%description -n %libregistry
Samba4 registry library

%package -n %registrydevel
Group: Development/C
Summary: Development files for Samba4 registry library
Provides: registry-devel = %version-%release
Requires: %libregistry = %version-%release

%description -n %registrydevel
Development files for Samba4 registry library

%package -n %libgensec
Group: System/Libraries
Summary: Samba4 generic security library

%description -n %libgensec
Samba4 generic security library

%package -n %gensecdevel
Group: Development/C
Summary: Development files for Samba4 generic security library
Provides: gensecdevel = %version-%release
Requires: %libgensec = %version-%release

%description -n %gensecdevel
Development files for Samba4 generic security library

%package -n %libpolicy
Group: System/Libraries
Summary: Samba4 policy library

%description -n %libpolicy
Samba4 policy library

%package -n %libpolicydevel
Group: Development/C
Summary: Development files for Samba4 policy library
Provides: policydevel = %version-%release
Requires: %libpolicy = %version-%release

%description -n %libpolicydevel
Development files for Samba4 policy library

%package -n %libsamdb
Group: System/Libraries
Summary: Samba4 samdb library

%description -n %libsamdb
Samba4 samdb library

%package -n %libsamdbdevel
Group: Development/C
Summary: Development files for Samba4 samdb library
Provides: samdbdevel = %version-%release
Requires: %libsamdb = %version-%release

%description -n %libsamdbdevel
Development files for Samba4 samdb library

%package -n %libpdb
Summary: Library for working with the Samba user database
Group: System/Libraries

%description -n %libpdb
Library for working with the Samba user database

%package -n %libcredentials
Summary: Library for working with Samba credentials
Group: System/Libraries

%description -n %libcredentials
Library for working with Samba credentials

%package -n %libsmbconf
Summary: Library for working with Samba config files
Group: System/Libraries

%description -n %libsmbconf
Library for working with Samba config files

%package -n %libsmbldap
Summary: Samba LDAP library
Group: System/Libraries

%description -n %libsmbldap
Samba LDAP library

%package -n %libtevent_util
Summary: Utility library for working with the Tevent library
Group: System/Libraries

%description -n %libtevent_util
Utility library for working with the Tevent library

#%package passdb-ldap
#URL:		http://www.samba.org
#Summary:	Samba password database plugin for LDAP
#Group:		System/Libraries
#
#%description passdb-ldap
#The passdb-ldap package for samba provides a password database
#backend allowing samba to store account details in an LDAP
#database

%if %{build_mysql}
%package passdb-mysql
URL:		http://www.samba.org
Summary:	Samba password database plugin for MySQL
Group:		System/Libraries
Requires:	%{name}-server = %{version}-%{release}

%description passdb-mysql
The passdb-mysql package for samba provides a password database
backend allowing samba to store account details in a MySQL
database
%endif

%if %{build_pgsql}
%package passdb-pgsql
URL:		http://www.samba.org
Summary:	Samba password database plugin for PostgreSQL
Group:		System/Libraries
Requires:	%{name}-server = %{version}-%{release}
%endif
%if %{build_pgsql}

%description passdb-pgsql
The passdb-pgsql package for samba provides a password database
backend allowing samba to store account details in a PostgreSQL
database
%endif

%if %{with cifs}
%package -n mount-cifs
URL:	http://www.samba.org
Summary: CIFS filesystem mount helper
Group: Networking/Other
Conflicts:	%{name}-client <= 3.0.11-1mdk
Requires:	keyutils > 1.2-%{mkrel 4}

%description -n mount-cifs
This package provides the mount.cifs helper to mount cifs filesystems
using the cifs filesystem driver
%endif

%package -n %libtorture
Summary: Samba testsuite torture library
Group: Networking/Other

%description -n %libtorture
Samba testsuite torture library

%if %{with gtk}
%package domainjoin-gui
Summary: Domainjoin GUI
Requires: samba-common = %{version}
Group: System/Configuration/Other
BuildRequires: pkgconfig(gtk+-2.0)

%description domainjoin-gui
The samba-domainjoin-gui package includes a domainjoin gtk application.
%endif

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
#{error: }
#{error: This rpm has build options available, use --with options to see them}
#{error: }
echo -e "\n This rpm has build options available, use --with options to see them\n" >&2
sleep 1
%endif

%if %{?_with_options:1}%{!?_with_options:0}
clear
exit 1
%endif

%if %build_non_default
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
# echo "Building a non-default rpm with the following command-line arguments:"
# echo "$RPM_EXTRA_OPTIONS"
# echo "This rpm was built with non-default options, thus, to build ">%{SOURCE7}
# echo "an identical rpm, you need to supply the following options">>%{SOURCE7}
# echo "at build time: $RPM_EXTRA_OPTIONS">>%{SOURCE7}
# echo -e "\n%{name}-%{version}-%{release}\n">>%{SOURCE7}
%else
# echo "This rpm was built with default options">%{SOURCE7}
# echo -e "\n%{name}-%{version}-%{release}\n">>%{SOURCE7}
%endif


#Try and validate signatures on source:
# FIXME: find public key used to sign samba4 releases
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
	#exit 1
fi


%setup -q
# Samba tries to force -fPIE into everything, including libraries.
# -fPIE overrides -fPIC though, causing anything that tries to link to
# a -fPIE library to fail on platforms that need -fPIC libraries.
sed -i -e 's,-fPIC,-fPIC -fno-PIE,g' source3/configure* lib/replace/*.m4 lib/iniparser/Makefile buildtools/wafsamba/wscript buildtools/wafadmin/Tools/gxx.py buildtools/wafadmin/Tools/gcc.py

#patch1 -p1 -b .compile~
%patch2 -p1 -b .tirpc~

%build
%serverbuild
# CFLAGS="`echo "$CFLAGS"|sed -e 's/ -g / /g;s/ -Wl,--no-undefined//g'` -DLDAP_DEPRECATED"
# CXXFLAGS="`echo "$CXXFLAGS"|sed -e 's/ -g / /g;s/ -Wl,--no-undefined//g'` -DLDAP_DEPRECATED"
# RPM_OPT_FLAGS="`echo "$RPM_OPT_FLAGS"|sed -e 's/ -g / /g;s/ -Wl,--no-undefined//g'` -DLDAP_DEPRECATED"

%ifarch x86_64
# Workaround for an apparent compiler bug present in both 4.6 and 4.7:
# Some files are not recognized as containing PIC code even though they're
# built with -fPIC
# So for now, we'll use the only code model that can support linking
# non-PIC code into a shared library...
# gold can't deal with that though (http://sourceware.org/bugzilla/show_bug.cgi?id=14324)
# So we force BFD LD at the same time
#EXTRAFLAGS="-mcmodel=large -fuse-ld=bfd"
%endif
buildtools/bin/waf configure --enable-fhs \
	--with-perl-archdir=%{perl_vendorlib} \
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
	--with-swat \
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
	--enable-nss-wrapper \
	--enable-socket-wrapper \
	--enable-uid-wrapper \
	--prefix=%_prefix \
	--libdir=%_libdir \
	--datadir=%_datadir \
	--localstatedir=%_localstatedir \
	--with-modulesdir=%_libdir/%name \
	-v -v -p \
	%?_smp_mflags

#	--with-system-mitkrb5 <--- probably a good idea, but causes
#	samba_upgradeprovision and friends not to be built

#sed -i -e "s|, '-Wl,--no-undefined'||g" bin/c4che/default.cache.py

buildtools/bin/waf build -v -v %?_smp_mflags

%if %{with gtk}
cd source3/lib/netapi/examples/netdomjoin-gui
%__cc %optflags `pkg-config --cflags gtk+-2.0` -I../../../../../bin/default/include/public -o netdomjoin-gui netdomjoin-gui.c -L../../../../../bin/default/source3/ -lnetapi `pkg-config --libs gtk+-2.0`
%endif

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

# Put stuff where it should go.
mkdir -p %buildroot/%{_datadir}/swat/include
mkdir -p %buildroot/%{_datadir}/swat/images
mkdir -p %buildroot/%{_datadir}/swat/lang
mkdir -p %buildroot/%{_libdir}/samba/
mkdir -p %buildroot/%{_datadir}/man/man8/


cp -R swat/include 	       		%buildroot/%{_datadir}/swat/include
cp -R swat/images              		%buildroot/%{_datadir}/swat/images
cp -R swat/lang                		%buildroot/%{_datadir}/swat
cp -R source3/po/*             		%buildroot/%{_libdir}/samba/
# cp docs-xml/manpages-3/swat.8.xml 	%buildroot/%{_datadir}/man/man8/

# Any entries here mean samba makefile is *really* broken:
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_datadir}
mkdir -p %{buildroot}%{_libdir}/%{name}/vfs

%makeinstall_std
# PAM modules don't go to /usr...
if [ -e %buildroot%_libdir/security ]; then
	mkdir -p %{buildroot}/%_lib
	mv %buildroot%_libdir/security %buildroot/%_lib
fi
# we ship docs in the docs supackage, and lik it into swat, delete the extra copy:
rm -Rf %{buildroot}/%{_datadir}/swat/using_samba

#Even though we tell waf above where to put perl it gets it wrong
mkdir -p %{buildroot}/%{perl_vendorlib}
mv %{buildroot}%_datadir/perl5/* %{buildroot}/%{perl_vendorlib}

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

# Fix some paths so provision works:
perl -pi -e 's,default_ldb_modules_dir = None,default_ldb_modules_dir = \"%{_libdir}/%{name}/ldb\",g' %{buildroot}/%{python_sitearch}/samba/__init__.py
#perl -pi -e 's,share/samba/setup,share/%{name}/setup,g' %{buildroot}/%{python_sitearch}/samba/provision.py

%if %{with gtk}
install -m 755 source3/lib/netapi/examples/netdomjoin-gui/netdomjoin-gui %{buildroot}/%{_sbindir}/netdomjoin-gui
mkdir -p %{buildroot}%{_datadir}/pixmaps/%{name}
install -m 644 source3/lib/netapi/examples/netdomjoin-gui/samba.ico %{buildroot}/%{_datadir}/pixmaps/%{name}/samba.ico
install -m 644 source3/lib/netapi/examples/netdomjoin-gui/logo.png %{buildroot}/%{_datadir}/pixmaps/%{name}/logo.png
install -m 644 source3/lib/netapi/examples/netdomjoin-gui/logo-small.png %{buildroot}/%{_datadir}/pixmaps/%{name}/logo-small.png
%endif

#libnss_* still not handled by make:
# Install the nsswitch library extension file
#for i in wins winbind; do
#  install -m755 source4/nsswitch/libnss_${i}.so %{buildroot}/%{_lib}/libnss_${i}.so
#done
# Make link for wins and winbind resolvers
#( cd %{buildroot}/%{_lib}; ln -s libnss_wins.so libnss_wins.so.2; ln -s libnss_winbind.so libnss_winbind.so.2)
#install -d %{buildroot}/%{_libdir}/krb5/plugins
#install -m755 source4/bin/winbind_krb5_locator.so %{buildroot}/%{_libdir}/krb5/plugins

%if %{build_test}
for i in {%{testbin}};do
  mv %{buildroot}/%{_bindir}/$i %{buildroot}/%{_bindir}/${i} || :
done
%endif

# Install other stuff

        install -m755 %{SOURCE24} %{buildroot}/%{_initrddir}/%{name}
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
#install -m644 packaging/Mandrake/smb.conf %{buildroot}/%{_sysconfdir}/%{name}/smb.conf
#cat packaging/Mandrake/smb.conf | \
#touch %{buildroot}/%{_sysconfdir}/%{name}/smb.conf
#sed -e 's/^;   printer admin = @adm/   printer admin = @adm/g' >%{buildroot}/%{_sysconfdir}/%{name}/smb.conf
%if %build_cupspc
perl -pi -e 's/printcap name = lpstat/printcap name = cups/g' %{buildroot}/%{_sysconfdir}/%{name}/smb.conf
perl -pi -e 's/printcap name = lpstat/printcap name = cups/g' %{buildroot}/%{_sysconfdir}/%{name}/smb-winbind.conf
# Link smbspool to CUPS (does not require installed CUPS)

        mkdir -p %{buildroot}/%{_prefix}/lib/cups/backend
        ln -s %{_bindir}/smbspool %{buildroot}/%{_prefix}/lib/cups/backend/smb
%endif

        echo 127.0.0.1 localhost > %{buildroot}/%{_sysconfdir}/%{name}/lmhosts

%if %{with swat}
# xinetd support

        mkdir -p %{buildroot}/%{_sysconfdir}/xinetd.d
        install -m644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/xinetd.d/swat

# menu support

mkdir -p %{buildroot}/%{_datadir}/applications
cat > %{buildroot}/%{_datadir}/applications/mandriva-%{name}-swat.desktop << EOF
[Desktop Entry]
Name=Samba Configuration (SWAT)
Comment=The Swat Samba Administration Tool
Exec=www-browser http://localhost:901/
Icon=swat
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Configuration-Networking;
EOF

mkdir -p %{buildroot}%{_liconsdir} %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}

# install html man pages for swat
install -d %{buildroot}/%{_datadir}/swat/help/manpages

cat %{SOURCE4} > %{buildroot}%{_miconsdir}/swat.png
cat %{SOURCE5} > %{buildroot}%{_iconsdir}/swat.png
cat %{SOURCE6} > %{buildroot}%{_liconsdir}/swat.png
%endif

install -c -m 755 %{SOURCE10} %{buildroot}%{_datadir}/%name/scripts/print-pdf

# Move some stuff where it belongs...
mkdir -p %buildroot%_lib
mv %buildroot%_libdir/libnss* %buildroot/%_lib/

rm -f %{buildroot}/%{_mandir}/man1/testprns*

%post server

%_post_service %{name}

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
#    else
#        echo "Upgrade, leaving nsswitch.conf intact"
fi

%preun -n nss_wins
if [ $1 = 0 ]; then
	echo "Removing wins entry from %{_sysconfdir}/nsswitch.conf"
	perl -pi -e 's/ wins//' %{_sysconfdir}/nsswitch.conf
#else
#	echo "Leaving %{_sysconfdir}/nsswitch.conf intact"
fi

%preun server
%_preun_service %{name}

%post swat
if [ -f /var/lock/subsys/xinetd ]; then
        service xinetd reload >/dev/null 2>&1 || :
fi

%postun swat
# Remove swat entry from xinetd
if [ $1 = 0 -a -f %{_sysconfdir}/xinetd.conf ] ; then
rm -f %{_sysconfdir}/xinetd.d/swat
	service xinetd reload &>/dev/null || :
fi

if [ "$1" = "0" -a -x /usr/bin/update-menus ]; then /usr/bin/update-menus || true ; fi

%files server
%(for i in %{_sbindir}/{%{serversbin}};do echo $i;done)
%(for i in %{_bindir}/%{serverbin};do echo $i;done)
%attr(755,root,root) /%{_lib}/security/pam_smbpass*
#%{_libdir}/%{name}/vfs
%{_libdir}/%{name}/vfs/*.so
#dir %{_libdir}/samba/pdb
%{_libdir}/samba/ldb
%{_libdir}/samba/service
%{_libdir}/samba/process_model
%{_libdir}/samba/gensec
%{_libdir}/samba/auth
%{_libdir}/samba/bind9
%{_libdir}/samba/genmsg
%lang(de) %_libdir/samba/de.msg
%lang(en) %_libdir/samba/en.msg
%lang(fi) %_libdir/samba/fi.msg
%lang(fr) %_libdir/samba/fr.msg
%lang(it) %_libdir/samba/it.msg
%lang(ja) %_libdir/samba/ja.msg
%lang(nl) %_libdir/samba/nl.msg
%lang(pl) %_libdir/samba/pl.msg
%lang(ru) %_libdir/samba/ru.msg
%lang(ru) %_libdir/samba/ru
%lang(tr) %_libdir/samba/tr.msg
# %{_libdir}/%{name}/*.so*
%{_libdir}/samba/libCHARSET3.so
%{_libdir}/samba/libHDB_SAMBA4.so
%{_libdir}/samba/libLIBWBCLIENT_OLD.so
%{_libdir}/samba/libMESSAGING.so
%{_libdir}/samba/libaddns.so
%if %{with ads}
%{_libdir}/samba/libads.so
%endif
%{_libdir}/samba/libasn1-samba4.so.8
%{_libdir}/samba/libasn1-samba4.so.8.0.0
%{_libdir}/samba/libasn1util.so
%{_libdir}/samba/libauth.so
%{_libdir}/samba/libauth4.so
%{_libdir}/samba/libauth_sam_reply.so
%{_libdir}/samba/libauth_unix_token.so
%{_libdir}/samba/libauthkrb5.so
%{_libdir}/samba/libccan.so
%{_libdir}/samba/libcli-ldap-common.so
%{_libdir}/samba/libcli-ldap.so
%{_libdir}/samba/libcli-nbt.so
%{_libdir}/samba/libcli_cldap.so
%{_libdir}/samba/libcli_smb_common.so
%{_libdir}/samba/libcli_spoolss.so
%{_libdir}/samba/libcliauth.so
%{_libdir}/samba/libcluster.so
%{_libdir}/samba/libcmdline-credentials.so
%{_libdir}/samba/libdb-glue.so
%{_libdir}/samba/libdbwrap.so
%{_libdir}/samba/libdcerpc-samba.so
%{_libdir}/samba/libdcerpc-samba4.so
%{_libdir}/samba/libdfs_server_ad.so
%{_libdir}/samba/libdlz_bind9_for_torture.so
%{_libdir}/samba/libdsdb-module.so
%{_libdir}/samba/liberrors.so
%{_libdir}/samba/libevents.so
%{_libdir}/samba/libflag_mapping.so
%{_libdir}/samba/libgpo.so
%{_libdir}/samba/libgse.so
%{_libdir}/samba/libgssapi-samba4.so.2
%{_libdir}/samba/libgssapi-samba4.so.2.0.0
%{_libdir}/samba/libhcrypto-samba4.so.5
%{_libdir}/samba/libhcrypto-samba4.so.5.0.1
%{_libdir}/samba/libhdb-samba4.so.11
%{_libdir}/samba/libhdb-samba4.so.11.0.2
%{_libdir}/samba/libheimbase-samba4.so.1
%{_libdir}/samba/libheimbase-samba4.so.1.0.0
%{_libdir}/samba/libheimntlm-samba4.so.1
%{_libdir}/samba/libheimntlm-samba4.so.1.0.1
%{_libdir}/samba/libhx509-samba4.so.5
%{_libdir}/samba/libhx509-samba4.so.5.0.0
%{_libdir}/samba/libidmap.so
%{_libdir}/samba/libiniparser.so
%{_libdir}/samba/libinterfaces.so
%{_libdir}/samba/libkdc-samba4.so.2
%{_libdir}/samba/libkdc-samba4.so.2.0.0
%{_libdir}/samba/libkrb5-samba4.so.26
%{_libdir}/samba/libkrb5-samba4.so.26.0.0
%{_libdir}/samba/libkrb5samba.so
%{_libdir}/samba/libldb-cmdline.so
%{_libdir}/samba/libldbsamba.so
%{_libdir}/samba/liblibcli_lsa3.so
%{_libdir}/samba/liblibcli_netlogon3.so
%{_libdir}/samba/liblibsmb.so
%{_libdir}/samba/libmsrpc3.so
%{_libdir}/samba/libndr-samba.so
%{_libdir}/samba/libndr-samba4.so
%{_libdir}/samba/libnet_keytab.so
%{_libdir}/samba/libnetif.so
%{_libdir}/samba/libnpa_tstream.so
%{_libdir}/samba/libnss_info.so
%{_libdir}/samba/libnss_wrapper.so
%{_libdir}/samba/libntvfs.so
%{_libdir}/samba/libpac.so
%{_libdir}/samba/libpopt_samba3.so
%{_libdir}/samba/libposix_eadb.so
%{_libdir}/samba/libprinting_migrate.so
%{_libdir}/samba/libprocess_model.so
%{_libdir}/samba/libreplace.so
%{_libdir}/samba/libroken-samba4.so.19
%{_libdir}/samba/libroken-samba4.so.19.0.1
%{_libdir}/samba/libsamba-modules.so
%{_libdir}/samba/libsamba-net.so
%{_libdir}/samba/libsamba-security.so
%{_libdir}/samba/libsamba-sockets.so
%{_libdir}/samba/libsamba3-util.so
%{_libdir}/samba/libsamba_python.so
%{_libdir}/samba/libsamdb-common.so
%{_libdir}/samba/libsecrets3.so
%{_libdir}/samba/libserver-role.so
%{_libdir}/samba/libservice.so
%{_libdir}/samba/libshares.so
%{_libdir}/samba/libsmb_transport.so
%{_libdir}/samba/libsmbd_base.so
%{_libdir}/samba/libsmbd_conn.so
%{_libdir}/samba/libsmbd_shim.so
%{_libdir}/samba/libsmbldaphelper.so
%{_libdir}/samba/libsmbpasswdparser.so
%{_libdir}/samba/libsmbregistry.so
%{_libdir}/samba/libsocket_wrapper.so
%{_libdir}/samba/libsubunit.so
%{_libdir}/samba/libtdb-wrap.so
%{_libdir}/samba/libtdb_compat.so
%{_libdir}/samba/libtrusts_util.so
%{_libdir}/samba/libuid_wrapper.so
%{_libdir}/samba/libutil_cmdline.so
%{_libdir}/samba/libutil_reg.so
%{_libdir}/samba/libutil_setid.so
%{_libdir}/samba/libutil_tdb.so
%{_libdir}/samba/libwinbind-client.so
%{_libdir}/samba/libwind-samba4.so.0
%{_libdir}/samba/libwind-samba4.so.0.0.0
%{_libdir}/samba/libxattr_tdb.so

%{_libdir}/mit_samba.so
%{_libdir}/%{name}/nss_info
%_sbindir/smbd
%_sbindir/nmbd
%_sbindir/samba_upgradedns
#attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smbusers
%attr(-,root,root) %config(noreplace) %{_initrddir}/%{name}
#%attr(-,root,root) %config(noreplace) %{_initrddir}/wrepld
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/pam.d/%{name}
#%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/samba-slapd.include
%(for i in %{_mandir}/man?/%{serverbin}\.[0-9]*;do echo $i;done)
%attr(775,root,adm) %dir %{_localstatedir}/lib/%{name}/netlogon
%attr(755,root,root) %dir %{_localstatedir}/lib/%{name}/profiles
%attr(755,root,root) %dir %{_localstatedir}/lib/%{name}/printers
%attr(2775,root,adm) %dir %{_localstatedir}/lib/%{name}/printers/*
%attr(1777,root,root) %dir /var/spool/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/scripts
%{_datadir}/samba/setup
%attr(0755,root,root) %{_datadir}/%name/scripts/print-pdf
#attr(0755,root,root) %{_datadir}/samba/scripts/convertSambaAccount
#{_mandir}/man8/idmap_*.8*
#{_mandir}/man8/vfs_*.8*
%{_mandir}/man8/samba.8*
%{_sbindir}/samba_upgradeprovision






%if %{with doc}
%files doc
%doc README COPYING Manifest Read-Manifest-Now
%doc WHATSNEW.txt Roadmap
%doc README.%{name}-mandrake-rpm
%doc clean-docs/samba-doc/docs/*
%doc clean-docs/samba-doc/examples
#%attr(-,root,root) %{_datadir}/swat/using_samba/
%attr(-,root,root) %{_datadir}/swat/help/
%endif

%if %{with swat}
%files swat
%config(noreplace) %{_sysconfdir}/xinetd.d/swat
#%attr(-,root,root) /sbin/*
%{_sbindir}/swat
%{_datadir}/applications/mandriva-%{name}-swat.desktop
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_iconsdir}/*.png
#%attr(-,root,root) %{_datadir}/swat/help/
%attr(-,root,root) %{_datadir}/swat/images/
%attr(-,root,root) %{_datadir}/swat/include/
%lang(ja) %{_datadir}/swat/lang/ja
%lang(tr) %{_datadir}/swat/lang/tr
%{_mandir}/man8/swat*.8*

#%doc swat/README
%{_datadir}/samba/swat/help/welcome-no-samba-doc.html
%{_datadir}/samba/swat/help/welcome.html
%{_datadir}/samba/swat/images/globals.gif
%{_datadir}/samba/swat/images/home.gif
%{_datadir}/samba/swat/images/passwd.gif
%{_datadir}/samba/swat/images/printers.gif
%{_datadir}/samba/swat/images/samba.gif
%{_datadir}/samba/swat/images/shares.gif
%{_datadir}/samba/swat/images/status.gif
%{_datadir}/samba/swat/images/viewconfig.gif
%{_datadir}/samba/swat/images/wizard.gif
%{_datadir}/samba/swat/include/footer.html
%{_datadir}/samba/swat/include/header.html
%{_datadir}/samba/swat/lang/ja/help/welcome.html
%{_datadir}/samba/swat/lang/tr/help/welcome.html
%{_datadir}/samba/swat/lang/tr/images/globals.gif
%{_datadir}/samba/swat/lang/tr/images/home.gif
%{_datadir}/samba/swat/lang/tr/images/passwd.gif
%{_datadir}/samba/swat/lang/tr/images/printers.gif
%{_datadir}/samba/swat/lang/tr/images/samba.gif
%{_datadir}/samba/swat/lang/tr/images/shares.gif
%{_datadir}/samba/swat/lang/tr/images/status.gif
%{_datadir}/samba/swat/lang/tr/images/viewconfig.gif

%endif

%files client
%{_bindir}/dbwrap_tool   
#{_bindir}/dbwrap_torture
#{_bindir}/debug2html  
%{_bindir}/eventlogadm
#{_bindir}/locktest2   
#{_bindir}/locktest3
#{_bindir}/log2pcap 
#{_bindir}/masktest3
#{_bindir}/msgtest
%{_bindir}/net
%_bindir/nmblookup4
%{_bindir}/pdbedit
#{_bindir}/pdbtest 
%{_bindir}/profiles
#{_bindir}/pthreadpooltest
#{_bindir}/rpc_open_tcp
%{_bindir}/rpcclient
#{_bindir}/samba-dig  
%{_sbindir}/samba_kcc  
%{_bindir}/sharesec
%{_bindir}/smbcacls
%_bindir/smbclient4
#{_bindir}/smbconftort
%{_bindir}/smbcontrol
%{_bindir}/smbcquotas
#{_bindir}/smbfilter  
%{_bindir}/smbget     
%{_bindir}/smbpasswd
%{_bindir}/smbspool   
%{_bindir}/smbstatus
%{_bindir}/smbta-util
#{_bindir}/smbtorture3
%{_bindir}/smbtree
#{_bindir}/split_tokens
#{_bindir}/ntdbbackup 
#{_bindir}/ntdbdump   
#{_bindir}/ntdbrestore
#{_bindir}/ntdbtool
#{_bindir}/test_lp_load
#{_bindir}/timelimit  
#{_bindir}/versiontest
#{_bindir}/vfstest
#{_bindir}/vlp


%(for i in %{_bindir}/{%{clientbin}};do echo $i;done)
# %{_mandir}/man1/nmblookup
# %(for i in %{_mandir}/%{client_man}.[0-9]%{_extension};do echo $i;done)

%_mandir/man8/samba-tool.8*

#xclude %{_mandir}/man?/smbget*
#{_mandir}/man5/smbgetrc.5*
#{_mandir}/man8/eventlogadm3.8*
# Link of smbspool to CUPS
%if %build_cupspc
%{_prefix}/lib*/cups/backend/smb
%endif

%files common
%dir /var/cache/%{name}
%dir /var/log/%{name}
%dir /var/run/%{name}
%(for i in %{_bindir}/{%{commonbin}};do echo $i;done)
%(for i in %{_mandir}/man?/{%{commonbin}}\.[0-9]*;do echo $i|grep -v testparm;done)
#%{_libdir}/smbwrapper.so
#dir %{_libdir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/samba/codepages
#{_libdir}/%{name}/charset
#%{_libdir}/%{name}/lowcase.dat
#%{_libdir}/%{name}/valid.dat
%dir %{_sysconfdir}/%{name}
#attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smb.conf
#attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smb-winbind.conf
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/lmhosts
%dir %{_localstatedir}/lib/%{name}
%attr(-,root,root) %{_localstatedir}/lib/%{name}/codepages
%{_mandir}/man1/findsmb.1*
%{_mandir}/man1/log2pcap.1*
%{_mandir}/man1/nmblookup.1*
%{_mandir}/man1/nmblookup4.1*
%{_mandir}/man1/profiles.1*
%{_mandir}/man1/rpcclient.1*
%{_mandir}/man1/sharesec.1*
%{_mandir}/man1/smbcacls.1*
%{_mandir}/man1/smbclient.1*
%{_mandir}/man1/smbcontrol.1*
%{_mandir}/man1/smbcquotas.1*
%{_mandir}/man1/smbget.1*
%{_mandir}/man1/smbstatus.1*
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbtree.1*
%{_mandir}/man1/testparm.1*
%{_mandir}/man1/vfstest.1*
%{_mandir}/man1/wbinfo.1*
%{_mandir}/man5/lmhosts.5*
%{_mandir}/man5/pam_winbind.conf.5*
%{_mandir}/man5/smb.conf.5*
%{_mandir}/man5/smbgetrc.5*
%{_mandir}/man5/smbpasswd.5*
%{_mandir}/man7/samba.7*
%{_mandir}/man7/winbind_krb5_locator.7*
%{_mandir}/man8/eventlogadm.8*
%{_mandir}/man8/idmap_ad.8*
%{_mandir}/man8/idmap_autorid.8*
%{_mandir}/man8/idmap_hash.8*
%{_mandir}/man8/idmap_ldap.8*
%{_mandir}/man8/idmap_nss.8*
%{_mandir}/man8/idmap_rid.8*
%{_mandir}/man8/idmap_tdb.8*
%{_mandir}/man8/idmap_tdb2.8*
%{_mandir}/man8/net.8*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/pam_winbind.8*
%{_mandir}/man8/pdbedit.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man8/smbpasswd.8*
%{_mandir}/man8/smbspool.8*
%{_mandir}/man8/smbta-util.8*
#{_mandir}/man8/tdbbackup.8*
#{_mandir}/man8/tdbdump.8*
#{_mandir}/man8/tdbrestore.8*
#{_mandir}/man8/tdbtool.8*
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
%{_mandir}/man8/winbindd.8*

%files -n %libpdb
%_libdir/libpdb.so.*

%files -n %libcredentials
%_libdir/libsamba-credentials.so.*

%files -n %libsmbconf
%_libdir/libsmbconf.so.*

%files -n %libsmbldap
%_libdir/libsmbldap.so.*

%files -n %libtevent_util
%_libdir/libtevent-util.so.*

%files winbind 
# %config(noreplace) %{_sysconfdir}/security/pam_winbind.conf
%{_sbindir}/winbindd
# %{_sbindir}/winbind
%{_bindir}/wbinfo
%attr(755,root,root) /%{_lib}/security/pam_winbind*
%attr(755,root,root) /%{_lib}/libnss_winbind*
%{_libdir}/%{name}/idmap
%{_libdir}/winbind_krb5_locator.so
# %attr(-,root,root) %config(noreplace) %{_initrddir}/winbind
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/pam.d/system-auth-winbind*
# %{_mandir}/man8/winbindd*.8*
# %{_mandir}/man7/pam_winbind.7*
# %{_mandir}/man7/winbind_krb5_locator.7.*
# %{_mandir}/man1/wbinfo*.1*

%files -n nss_wins
%attr(755,root,root) /%{_lib}/libnss_wins.so*

%files python
%{python_sitearch}/samba
#exclude %py_platsitedir/subunit

%if %{build_test}
%files test
%(for i in %{_bindir}/{%{testbin}};do echo $i;done)
%(for i in %{_mandir}/man1/{%{testbin}}.1%{_extension};do echo $i|grep -v nsstest;done)
#{_mandir}/man1/vfstest*.1*
#exclude %{_mandir}/man1/log2pcap*.1*
%else
#exclude %{_mandir}/man1/vfstest*.1*
#exclude %{_mandir}/man1/log2pcap*.1*
%endif

%files -n %{libname}
%{_libdir}/libsmbclient.so.%{libsmbmajor}*
%_libdir/libsmbclient-raw.so.*

%files -n %{libname}-devel
%{_includedir}/samba-4.0/libsmbclient.h
%{_libdir}/libsmbclient.so
%{_mandir}/man7/libsmbclient.7*
%{_libdir}/pkgconfig/smbclient.pc

#files -n %{libname}-static-devel
#{_libdir}/lib*.a

%files devel
%{_includedir}/samba-4.0/charset.h
%dir %{_includedir}/samba-4.0/core
%{_includedir}/samba-4.0/core/*.h
%{_includedir}/samba-4.0/credentials.h
%{_includedir}/samba-4.0/dlinklist.h
%{_includedir}/samba-4.0/domain_credentials.h
%dir %{_includedir}/samba-4.0/gen_ndr
%{_includedir}/samba-4.0/gen_ndr/*.h
%{_includedir}/samba-4.0/ldap*.h
%{_includedir}/samba-4.0/ndr.h
%{_includedir}/samba-4.0/ndr
%{_includedir}/samba-4.0/param.h
%{_includedir}/samba-4.0/samba/
%{_includedir}/samba-4.0/share.h
%{_includedir}/samba-4.0/tdr.h
%{_includedir}/samba-4.0/tsocket.h
%{_includedir}/samba-4.0/tsocket_internal.h
%{_includedir}/samba-4.0/torture.h
%{_includedir}/samba-4.0/rpc_common.h
%dir %{_includedir}/samba-4.0/util/
%{_includedir}/samba-4.0/util/*.h
%{_includedir}/samba-4.0/util_ldb.h
%{_includedir}/samba-4.0/ldb_wrap.h
%{_libdir}/pkgconfig/torture.pc
%{_libdir}/pkgconfig/samba-util.pc
%_libdir/libtorture.so
%_libdir/libpdb.so
%_libdir/libsamba-credentials.so
%_libdir/libsmbclient-raw.so
%_libdir/libsmbconf.so
%_libdir/libsmbldap.so
%_libdir/libtevent-util.so
%{_includedir}/samba-4.0/lookup_sid.h
%{_includedir}/samba-4.0/machine_sid.h
%{_includedir}/samba-4.0/passdb.h
%{_includedir}/samba-4.0/policy.h
%{_includedir}/samba-4.0/read_smb.h
%{_includedir}/samba-4.0/roles.h
%{_includedir}/samba-4.0/samba_util.h
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
%{_includedir}/samba-4.0/smbconf.h
%{_includedir}/samba-4.0/smbldap.h
%{_libdir}/pkgconfig/samba-credentials.pc
%{_libdir}/pkgconfig/smbclient-raw.pc

%files pidl
%{_bindir}/pidl
%{perl_vendorlib}/Parse/Pidl*
%{perl_vendorlib}/Parse/Yapp/*.pm
#{_mandir}/man1/pidl.1.*
#{_mandir}/man3/Parse::Pidl*.3pm.*

%files -n %libnetapi
%{_libdir}/libnetapi.so.%{netapimajor}*

%files -n %netapidevel
%{_libdir}/libnetapi*.so
%{_includedir}/samba-4.0/netapi.h
%_libdir/pkgconfig/netapi.pc

%files -n %libsmbsharemodes
%{_libdir}/libsmbsharemodes.so.%{smbsharemodesmajor}*

%files -n %smbsharemodesdevel
%{_libdir}/libsmbsharemodes.so
%{_includedir}/samba-4.0/smb_share_modes.h
%{_libdir}/pkgconfig/smbsharemodes.pc

%files -n %libdcerpc
%{_libdir}/libdcerpc.so.*
%{_libdir}/libdcerpc-samr.so.*
%{_libdir}/libdcerpc-atsvc.so.*
%_libdir/libdcerpc-binding.so.*
%{_libdir}/libdcerpc-server.so.*

%files -n %dcerpcdevel
%{_libdir}/pkgconfig/dcerpc*.pc
%{_includedir}/samba-4.0/dcerpc*.h
#dir %{_includedir}/samba-4.0/dcerpc-server
#{_includedir}/samba-4.0/dcerpc-server/*.h
%{_libdir}/libdcerpc.so
%{_libdir}/libdcerpc-samr.so
%{_libdir}/libdcerpc-atsvc.so
%_libdir/libdcerpc-binding.so
%{_libdir}/libdcerpc-server.so

%files -n %libndr
%{_libdir}/libndr*.so.*

%files -n %ndrdevel
%{_libdir}/pkgconfig/ndr*.pc
%{_libdir}/libndr*.so

%files -n %libsambautil
%{_libdir}/libsamba-util.so.*

%files -n %sambautildevel
%{_libdir}/libsamba-util.so

%files -n %libregistry
%{_libdir}/libregistry.so.*
%{_libdir}/pkgconfig/registry.pc

%files -n %registrydevel
%{_includedir}/samba-4.0/registry.h
%{_libdir}/libregistry.so

%files -n %libgensec
%{_libdir}/libgensec.so.*
%{_libdir}/pkgconfig/gensec.pc

%files -n %gensecdevel
%{_includedir}/samba-4.0/gensec.h
%{_libdir}/libgensec.so

%files -n %libsambahostconfig
%{_libdir}/libsamba-hostconfig.so.*

%files -n %sambahostconfigdevel
%{_libdir}/libsamba-hostconfig.so
%{_libdir}/pkgconfig/samba-hostconfig.pc

%files -n %libpolicy
%{_libdir}/libsamba-policy.so.*

%files -n %libpolicydevel
%{_libdir}/libsamba-policy.so
%{_libdir}/pkgconfig/samba-policy.pc

%files -n %libsamdb
%{_libdir}/libsamdb.so.*
%{_libdir}/pkgconfig/samdb.pc

%files -n %libsamdbdevel
%{_libdir}/libsamdb.so

%files -n %libwbclient
%{_libdir}/libwbclient.so.%{wbclientmajor}*

%files -n %wbclientdevel
%{_libdir}/libwbclient.so
%{_includedir}/samba-4.0/wbclient.h
%{_libdir}/pkgconfig/wbclient.pc

#%files passdb-ldap
#%{_libdir}/%{name}/*/*ldap.so

%if %{build_pgsql}
%files passdb-pgsql
%{_libdir}/%{name}/pdb/*pgsql.so
%endif

%if %{with cifs}
%files -n mount-cifs
%attr(4755,root,root) /*bin/*mount.cifs
#/*bin/cifs.upcall
#{_mandir}/man8/*mount.cifs*.8*
#{_mandir}/man8/cifs.upcall*.8*
%endif

#%exclude %{_mandir}/man1/smbsh*.1*
#%exclude %{_mandir}/man1/editreg*

%files -n %libtorture
%_libdir/libtorture.so.0*

%files domainjoin-gui
%defattr(-,root,root)
%{_sbindir}/netdomjoin-gui
%dir %{_datadir}/pixmaps/samba
%{_datadir}/pixmaps/samba/samba.ico
%{_datadir}/pixmaps/samba/logo.png
%{_datadir}/pixmaps/samba/logo-small.png


%changelog
* Wed May 16 2012 Zombie Ryushu <ryushu@mandriva.org> 4.0.0-0.7.alpha20
+ Revision: 799156
- We don't have those swat icons comment them
- We don't have those swat icons
- Add a bunch of install stuff to the files stage
- Add a bunch of install stuff to the files stage
- Add a bunch of install stuff to the files stage
- figure out how the paths have changed
- pam_winbind.conf is absent
- disable find_lang
- disable find_lang
- disable find_lang
- change build options to build talloc internally
- change build options to build talloc internally
- recompile with fPIC
- ncurses didn't like 64 bit
- I forgot a percent sign again
- Attempt at building Alpha 20

  + Bernhard Rosenkraenzer <bero@bero.eu>
    - Add workaround for compiler bug
    - Started updating spec file for 4.0.0a20 changes

  + Matthew Dawkins <mattydaw@mandriva.org>
    - new alpha version 18
    - cleaned up spec some

* Sat Nov 05 2011 Zombie Ryushu <ryushu@mandriva.org> 4.0.0-0.7.alpha15
+ Revision: 717769
- Increment release for rebuild

* Wed May 11 2011 Buchan Milne <bgmilne@mandriva.org> 4.0.0-0.6.alpha15
+ Revision: 673644
- Actually make the package work
- depend on standalone copies of talloc,tdb,tevent,ldb
- cleanups

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

  + Funda Wang <fwang@mandriva.org>
    - new version 4.0.0 alpha15

* Wed Nov 03 2010 Funda Wang <fwang@mandriva.org> 4.0.0-0.6.alpha11mdv2011.0
+ Revision: 592930
- delete file rather than exclude them
- rebuild for py2.7

* Tue Mar 02 2010 Buchan Milne <bgmilne@mandriva.org> 4.0.0-0.5.alpha11mdv2010.1
+ Revision: 513430
- Dont use remote stylesheets for building docs
- Build against standalone versions of talloc,tevent,tdb
-Split more libraries out

  + Funda Wang <fwang@mandriva.org>
    - use configure2_5x
    - new version 4.0.0 alpha11

* Thu Oct 08 2009 Buchan Milne <bgmilne@mandriva.org> 4.0.0-0.4.alpha8mdv2010.0
+ Revision: 456093
- Fix linking of glue.so (and use no-undefined)
- Make provision work (including not shipping an smb.conf by default)
- Ship a working init script

* Thu Oct 08 2009 Buchan Milne <bgmilne@mandriva.org> 4.0.0-0.3.alpha8mdv2010.0
+ Revision: 455864
- Fix building of shared libraries (by pkgconfig file)
- Fix most underlinking issues (except glue.so vs PyErr_SetLdbError)
- Temporary hacks to get the devel symlinks correct
- Fix directory locations
- Fix compilation against shipped standalone libs (gives us ldb modules)
- Ship shared development libraries correctly
- Require -python in -servers and -common

* Thu Aug 20 2009 Buchan Milne <bgmilne@mandriva.org> 4.0.0-0.2.alpha8mdv2010.0
+ Revision: 418539
- New version 4.0.0 alpha8

  + Gustavo De Nardin <gustavodn@mandriva.com>
    - Cruft cleanup: current/ inside current/.

* Fri Mar 27 2009 Buchan Milne <bgmilne@mandriva.org> 4.0.0-0.2.alpha7mdv2009.1
+ Revision: 361690
- Fix devel symlink typo

* Fri Mar 27 2009 Buchan Milne <bgmilne@mandriva.org> 4.0.0-0.1.alpha7mdv2009.1
+ Revision: 361625
- Adjustments to ship samba4 with libraries
- Start samba4 package from samba 3.3.2-1
- create samba4

