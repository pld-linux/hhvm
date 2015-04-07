#
# Conditional build:
%bcond_without	system_dconv	# system double-conversion
%bcond_without	system_sqlite	# system sqlite3
%bcond_without	system_lz4	# system lz4
%bcond_without	system_fastlz	# system fastlz
%bcond_with	system_libafdt	# system libafdt
%bcond_without	system_libzip	# system libzip
%bcond_with	fastcgi		# enable FastCGI protocol
%bcond_without	async_mysql		# enable async MySQL
%bcond_without	mcrouter		# Build the mcrouter library and extension

%bcond_with	jemalloc		# enable jemalloc
# cotire breaks sqlite3 on builders: https://github.com/facebook/hhvm/issues/4524
%bcond_with	cotire			# cotire (compile time reducer): Speed up the build by precompiling headers

# TODO
# - system xhp
# - system proxygen & fbthrift (for fastcgi)
# - gdb package

# NOTES:
# - hphp/runtime/base/runtime-option.cpp evalJitDefault enables jit if /.hhvm-jit exists (yes, in filesystem root)

# must be in sync with source. extra check ensuring that it is so is done in %%build
%define		hhvm_api_version	20150212
# hphp/system/idl/constants.idl.json defines it as 5.6.99-hhvm, but use some saner value
%define		php_version			5.6.0

# git show HHVM-3.6.1
%define		githash	c051feff88ba8050f33f10f7b1fb07f8d3415f9e
# these hashes are git submodules (be sure to check them on proper branch)
# GIT_DIR=third-party/.git git log -1
%define		thirdparty	3bf14f9
# 6e46d468cf2876dd59c7a4dddcb4e37abf070b7a
# GIT_DIR=third-party/folly/src/.git git log -1
%define		folly		0.26.0
%define		fbthrift	d30280a
%define		webscalesql	004b6b3
%define		squangle	269cd2e
%define		proxygen	d17b4e7
%define		mcrouter	addcc91
Summary:	Virtual Machine, Runtime, and JIT for PHP
Name:		hhvm
# we prefer LTS versions, see
# http://hhvm.com/blog/6083/hhvm-long-term-support
# http://hhvm.com/blog/8849/hhvm-3-6-0
Version:	3.6.1
Release:	0.1
License:	PHP 3.01 and BSD
Group:		Development/Languages
Source0:	https://github.com/facebook/hhvm/archive/HHVM-%{version}.tar.gz
# Source0-md5:	42dd1d75b4dd0785d3284e7809600c9e
Source2:	https://github.com/facebook/folly/archive/v%{folly}/folly-%{folly}.tar.gz
# Source2-md5:	c76a3fd2e86215d523a9fe18ba9087a1
Source3:	https://github.com/hhvm/hhvm-third-party/archive/%{thirdparty}/third_party-%{thirdparty}.tar.gz
# Source3-md5:	494d37347bb6448ed514fd3dfacf7c88
Source4:	https://github.com/facebook/fbthrift/archive/%{fbthrift}/fbthrift-%{fbthrift}.tar.gz
# Source4-md5:	a049ddb82e4a94f1ff7a63e9a94008ac
Source5:	https://github.com/webscalesql/webscalesql-5.6/archive/%{webscalesql}/webscalesql-5.6-%{webscalesql}.tar.gz
# Source5-md5:	5ee76824913ff96ba70b68d8aeb50e49
Source6:	https://github.com/facebook/squangle/archive/%{squangle}/squangle-%{squangle}.tar.gz
# Source6-md5:	c379594b56398f1f886391360b9577a8
Source7:	https://github.com/facebook/proxygen/archive/%{proxygen}/proxygen-%{proxygen}.tar.gz
# Source7-md5:	0cc887c0055172f52aa18cba9d66159a
Source8:	https://github.com/facebook/mcrouter/archive/%{mcrouter}/mcrouter-%{mcrouter}.tar.gz
# Source8-md5:	7817451ce6bd6e4d74c6bb8b222a2ebb
Source10:	%{name}-fcgi.init
Source11:	%{name}-fcgi.sysconfig
Source12:	php.ini
Source100:	get-source.sh
Patch2:		hphpize.patch
Patch5:		cmake.patch
Patch6:		webscalesql-5.6-build.patch
Patch7:		disable-fastcgi.patch
Patch8:		folly-malloc_usable_size.patch
Patch9:		mcrouter-chrono.patch
URL:		https://github.com/facebook/hhvm/wiki
BuildRequires:	ImageMagick-devel
BuildRequires:	a52dec-libs-devel
BuildRequires:	apr-devel
BuildRequires:	autoconf
BuildRequires:	binutils-devel
# CMake/HPHPFindLibs.cmake:364 - FIND_LIBRARY (BFD_LIB libbfd.a)
BuildRequires:	binutils-static
BuildRequires:	boost-devel >= 1.50
BuildRequires:	cmake >= 2.8.5
BuildRequires:	curl-devel >= 7.29.0
%{?with_system_dconv:BuildRequires:	double-conversion-devel >= 1.1.1}
BuildRequires:	elfutils-devel
BuildRequires:	expat-devel
%{?with_system_fastlz:BuildRequires:	fastlz-devel >= 0.1.0-0.r12}
BuildRequires:	gcc >= 6:4.6.0
BuildRequires:	gd-devel
BuildRequires:	glog-devel >= 0.3.2
BuildRequires:	imap-devel >= 1:2007
%{?with_jemalloc:BuildRequires:	jemalloc-devel >= 3.0.0}
%{?with_system_libafdt:BuildRequires:	libafdt-devel >= 0.1.0}
BuildRequires:	libcap-devel
BuildRequires:	libdwarf-devel >= 20130729
BuildRequires:	libicu-devel >= 4.2
#BuildRequires:	libmbfl-devel
BuildRequires:	libmcrypt-devel
BuildRequires:	libmemcached-devel >= 1.0.4
BuildRequires:	libstdc++-devel >= 6:4.8
BuildRequires:	libunwind-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
%{?with_system_libzip:BuildRequires:	libzip-devel >= 0.11.2}
%{?with_system_lz4:BuildRequires:	lz4-devel >= 0.0-1.r119}
BuildRequires:	mysql-devel
BuildRequires:	ocaml-findlib
BuildRequires:	oniguruma-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel >= 8.32
#BuildRequires:	php-xhp-devel >= 1.3.9-6
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.675
%{?with_system_sqlite:BuildRequires:	sqlite3-devel >= 3.7.15.2}
BuildRequires:	tbb-devel >= 4.0.6000
BuildRequires:	zlib-devel
# check later, seem unused
#BuildRequires:	bison >= 2.3
#BuildRequires:	flex >= 2.5.35
BuildRequires:	libafdt-devel >= 0.1.0
#BuildRequires:	re2c >= 0.13.0
Provides:	%{name}(api) = %{hhvm_api_version}
Provides:	php(core) = %{php_version}
# foreach (get_loaded_extensions() as $ext) printf("Provides:\tphp(%s)\n", strtolower($ext));
Provides:	php(apc)
Provides:	php(array)
Provides:	php(asio)
Provides:	php(async_mysql)
Provides:	php(bcmath)
Provides:	php(bz2)
Provides:	php(calendar)
Provides:	php(ctype)
Provides:	php(curl)
Provides:	php(date)
Provides:	php(debugger)
Provides:	php(dom)
Provides:	php(domdocument)
Provides:	php(enum)
Provides:	php(exif)
Provides:	php(fb)
Provides:	php(fileinfo)
Provides:	php(filter)
Provides:	php(fribidi)
Provides:	php(ftp)
Provides:	php(gd)
Provides:	php(gettext)
Provides:	php(gmp)
Provides:	php(hash)
Provides:	php(hh)
Provides:	php(hhvm.debugger)
Provides:	php(hhvm.ini)
Provides:	php(hotprofiler)
Provides:	php(iconv)
Provides:	php(idn)
Provides:	php(imagick)
Provides:	php(imap)
Provides:	php(intervaltimer)
Provides:	php(intl)
Provides:	php(json)
Provides:	php(ldap)
Provides:	php(libxml)
Provides:	php(mail)
Provides:	php(mailparse)
Provides:	php(mbstring)
Provides:	php(mcrouter)
Provides:	php(mcrypt)
Provides:	php(memcache)
Provides:	php(memcached)
Provides:	php(mysql)
Provides:	php(mysqli)
Provides:	php(oauth)
Provides:	php(objprof)
Provides:	php(openssl)
Provides:	php(pcntl)
Provides:	php(pcre)
Provides:	php(pcre_zend_compat)
Provides:	php(pdo)
Provides:	php(pdo_mysql)
Provides:	php(pdo_sqlite)
Provides:	php(phar)
Provides:	php(posix)
Provides:	php(readline)
Provides:	php(redis)
Provides:	php(reflection)
Provides:	php(server)
Provides:	php(session)
Provides:	php(simplexml)
Provides:	php(soap)
Provides:	php(sockets)
Provides:	php(spl)
Provides:	php(sqlite3)
Provides:	php(standard)
Provides:	php(standard_zend_compat)
Provides:	php(stream)
Provides:	php(string)
Provides:	php(sysvmsg)
Provides:	php(sysvsem)
Provides:	php(sysvshm)
Provides:	php(thread)
Provides:	php(thrift_protocol)
Provides:	php(tokenizer)
Provides:	php(url)
Provides:	php(wddx)
Provides:	php(xenon)
Provides:	php(xhprof)
Provides:	php(xml)
Provides:	php(xmlreader)
Provides:	php(xmlwriter)
Provides:	php(xsl)
Provides:	php(yaml)
Provides:	php(zip)
Provides:	php(zlib)
Obsoletes:	hiphop-php < 2.3.2-0.2
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		hhvm_extensiondir	%{_libdir}/hhvm

%description
HHVM (aka the HipHop Virtual Machine) is a new open-source virtual
machine designed for executing programs written in PHP. HHVM uses a
just-in-time compilation approach to achieve superior performance
while maintaining the flexibility that PHP developers are accustomed
to. To date, HHVM (and its predecessor HPHPc before it) has realized
over a 9x increase in web request throughput and over a 5x reduction
in memory consumption for Facebook compared with the Zend PHP 5.2
engine + APC.

HHVM can be run as a standalone webserver (i.e. without the Apache
webserver and the "mod_php" extension). HHVM can also be used together
with a FastCGI-based webserver, and work is in progress to make HHVM
work smoothly with Apache.

%package fcgi
Summary:	Init script to start HHVM as FastCGI daemon
Group:		Development/Languages/PHP
Requires:	%{name} = %{version}-%{release}
Provides:	php(fcgi)
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description fcgi
Init script to start HHVM as FastCGI daemon

%package program
Summary:	/usr/bin/php symlink
Summary(pl.UTF-8):	Dowiązanie symboliczne /usr/bin/php
Group:		Development/Languages/PHP
Requires:	%{name} = %{version}-%{release}
Obsoletes:	/usr/bin/php

%description program
Package providing /usr/bin/php symlink to PHP CLI.

%description program -l pl.UTF-8
Pakiet dostarczający dowiązanie symboliczne /usr/bin/php do PHP CLI.

%package devel
Summary:	Files for HHVM modules development
Group:		Development/Languages/PHP
URL:		https://github.com/facebook/hhvm/wiki/Extension-API
Requires:	boost-devel >= 1.50
Requires:	cmake >= 2.8.5
Requires:	glog-devel >= 0.3.2
Requires:	libstdc++-devel >= 6:4.3
Requires:	tbb-devel >= 4.0.6000
Requires:	zlib-devel

%description devel
HHVM provides a set of APIs for adding built-in functionality to the
runtime either by way of pure PHP code, or a combination of PHP and
C++.

%package gdb
Summary:	HHVM GDB Python bindings
Group:		Development/Debuggers
Requires:	gdb

%description gdb
HHVM GDB Python bindings.

%prep
%setup -q -n %{name}-HHVM-%{version} -a2 -a3 -a4 -a5 -a6 -a7 -a8

# handle git submodules
rmdir third-party
mv hhvm-third-party-* third-party
rmdir third-party/folly/src
mv folly-* third-party/folly/src
rmdir third-party/thrift/src
mv fbthrift-* third-party/thrift/src
rmdir third-party/webscalesqlclient/webscalesql-5.6
mv webscalesql-* third-party/webscalesqlclient/webscalesql-5.6
rmdir third-party/squangle/squangle
mv squangle-* third-party/squangle/squangle
rmdir third-party/proxygen/src
mv proxygen-* third-party/proxygen/src
rmdir third-party/mcrouter/src/
mv mcrouter-* third-party/mcrouter/src

%patch2 -p1
#%patch5 -p1
%patch6 -p1 -d third-party/webscalesqlclient/webscalesql-5.6
%patch7 -p1
%patch8 -p1 -d third-party
%patch9 -p1

# prefer ones from system
rm CMake/FindBISON.cmake
rm CMake/FindFLEX.cmake
rm CMake/FindFreetype.cmake

# ensure system libs get used
cd third-party
rm -r pcre \
	%{?with_system_sqlite:libsqlite3} \
	%{?with_system_lz4:lz4} \
	%{?with_system_dconv:double-conversion} \
	%{?with_system_fastlz:fastlz} \
	%{?with_system_libafdt:libafdt} \
	%{?with_system_libzip:libzip} \
	%{nil}

%build
# also in: hphp/tools/hphpize/hphpize.cmake
API=$(awk '/#define HHVM_API_VERSION/{v=$3; sub(/L$/, "", v); print v}' hphp/runtime/ext/extension.h)

if [ $API != %{hhvm_api_version} ]; then
	echo "Set %%define hhvm_api_version to $API and re-run."
	exit 1
fi

# out of dir build broken (can't find it's tools, or headers)
#install -d build
#cd build

# handle cmake & ccache
# http://stackoverflow.com/questions/1815688/how-to-use-ccache-with-cmake
# ASM fix: http://lists.busybox.net/pipermail/buildroot/2013-March/069436.html
if [[ "%{__cc}" = *ccache* ]]; then
	cc="%{__cc}"
	cxx="%{__cxx}"
	ccache="
	-DCMAKE_C_COMPILER="ccache" -DCMAKE_C_COMPILER_ARG1="${cc#ccache }" \
	-DCMAKE_CXX_COMPILER="ccache" -DCMAKE_CXX_COMPILER_ARG1="${cxx#ccache }" \
	-DCMAKE_ASM_COMPILER="${cc#ccache }" \
	"
fi

./configure --help || :

%cmake \
	$ccache \
	-DCMAKE_INSTALL_BINDIR=bin \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DHHVM_DYNAMIC_EXTENSION_DIR=%{hhvm_extensiondir} \
	-DMYSQL_UNIX_SOCK_ADDR=/var/lib/mysql/mysql.sock \
	-DUSE_JEMALLOC=%{!?with_jemalloc:OFF}%{?with_jemalloc:ON} \
	-DUSE_TCMALLOC=OFF \
	-DTEST_BIN=OFF \
	-DENABLE_FASTCGI=%{!?with_fastcgi:OFF}%{?with_fastcgi:ON} \
	-DENABLE_ASYNC_MYSQL=%{!?with_async_mysql:OFF}%{?with_async_mysql:ON} \
	-DENABLE_MCROUTER=%{!?with_mcrouter:OFF}%{?with_mcrouter:ON} \
	-DENABLE_COTIRE=%{!?with_cotire:OFF}%{?with_cotire:ON} \
	.

# setup COMPILER_ID/HHVM_REPO_SCHEMA so it doesn't look it up from our package git repo
# see hphp/util/generate-buildinfo.sh
export COMPILER_ID=HHVM-%{version}-%{release}-g%{githash}
export HHVM_REPO_SCHEMA=$(date +%N_%s)

%{__make}

%install
# make install relinks all outputs which is very slow,
# so to speedup rebuild, use timestamps to record states
#test %{_specdir}/%{name}.spec -nt makeinstall.stamp && %{__rm} -f makeinstall.stamp
if [ ! -f makeinstall.stamp -o ! -d $RPM_BUILD_ROOT ]; then
	rm -rf makeinstall.stamp installed.stamp $RPM_BUILD_ROOT

	%{__make} install \
		DESTDIR=$RPM_BUILD_ROOT

	touch makeinstall.stamp
fi

rm -rf $RPM_BUILD_ROOT%{_docdir}
if [ ! -f installed.stamp ]; then
# begin install block

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_libdir}/%{name}}
cp -p %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

ln -s hhvm $RPM_BUILD_ROOT%{_bindir}/php
ln -s hhvm $RPM_BUILD_ROOT%{_bindir}/hphp

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/hdf
cp -p hphp/doc/mime.hdf $RPM_BUILD_ROOT%{_datadir}/%{name}/hdf/static.mime-types.hdf

# install fastcgi initscript
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}
cp -p %{SOURCE10} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-fcgi
cp -p %{SOURCE11} $RPM_BUILD_ROOT/etc/sysconfig/%{name}-fcgi

install -p hphp/hack/bin/hh_{server,client} $RPM_BUILD_ROOT%{_bindir}

# end of install block
touch installed.stamp; fi

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post fcgi
/sbin/chkconfig --add %{name}-fcgi
%service %{name}-fcgi restart

%preun fcgi
if [ "$1" = "0" ]; then
	%service -q %{name}-fcgi stop
	/sbin/chkconfig --del %{name}-fcgi
fi

%files
%defattr(644,root,root,755)
%doc README.md NEWS LICENSE.PHP LICENSE.ZEND
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/php.ini
%attr(755,root,root) %{_bindir}/hhvm
%attr(755,root,root) %{_bindir}/hphp
%attr(755,root,root) %{_bindir}/hh_client
%attr(755,root,root) %{_bindir}/hh_server

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/hdf
%{_datadir}/%{name}/hdf/static.mime-types.hdf

# dir for extensions
%dir %{_libdir}/%{name}

%files fcgi
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/%{name}-fcgi
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}-fcgi

%files program
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/php

%files devel
%doc CONTRIBUTING.md
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hphpize
%{_includedir}/hphp
%dir %{_libdir}/hhvm
%{_libdir}/hhvm/CMake
%{_libdir}/hhvm/hphpize

%files gdb
%defattr(644,root,root,755)
%{_bindir}/hhvm-gdb
%dir %{_libdir}/hhvm/gdb
%{_libdir}/hhvm/gdb/gdbutils.py
%{_libdir}/hhvm/gdb/hashes.py
%{_libdir}/hhvm/gdb/hhbc.py
%{_libdir}/hhvm/gdb/hhvm.py
%{_libdir}/hhvm/gdb/idx.py
%{_libdir}/hhvm/gdb/lookup.py
%{_libdir}/hhvm/gdb/nameof.py
%{_libdir}/hhvm/gdb/pretty.py
%{_libdir}/hhvm/gdb/sizeof.py
%{_libdir}/hhvm/gdb/stack.py
%{_libdir}/hhvm/gdb/unit.py
%{_libdir}/hhvm/gdb/util.py
