# NOTES:
# - hphp/runtime/base/runtime-option.cpp evalJitDefault enables jit if /.hhvm-jit exists (yes, in filesystem root)
# TODO
# - system libevent2: https://github.com/facebook/hiphop-php/pull/421
# - system libmbfl, system xhp, sqlite3
%define		githash	f951cb8d8812c59344d5322454853b584b668636
Summary:	Virtual Machine, Runtime, and JIT for PHP
Name:		hhvm
Version:	2.3.2
Release:	0.21
License:	PHP 3.01
Group:		Development/Languages
Source0:	https://github.com/facebook/hhvm/archive/HHVM-%{version}.tar.gz
# Source0-md5:	471961d38ba52c66b7038c556b2b7bd8
# need fb.changes.patch, which is available for 1.4 only
Source1:	http://www.monkey.org/~provos/libevent-1.4.14b-stable.tar.gz
# Source1-md5:	a00e037e4d3f9e4fe9893e8a2d27918c
Source2:	https://github.com/facebook/folly/archive/4d6d659/folly-0.1-4d6d659.tar.gz
# Source2-md5:	2e7c941f737c8e0a449b8116e7615656
Source3:	%{name}-fcgi.init
Source4:	%{name}-fcgi.sysconfig
Source100:	get-source.sh
Patch0:		cmake-missing-library.patch
Patch1:		libevent14.patch
Patch3:		system-xhp.patch
Patch4:		system-libafdt.patch
Patch5:		system-folly.patch
Patch6:		checksum.patch
Patch7:		imap-gss.patch
Patch8:		hphpize.patch
Patch9:		notest.patch
URL:		http://wiki.github.com/facebook/hiphop-php/
BuildRequires:	apr-devel
BuildRequires:	autoconf
BuildRequires:	binutils-devel
BuildRequires:	boost-devel >= 1.50
BuildRequires:	cmake >= 2.8.7
BuildRequires:	curl-devel >= 7.29.0
BuildRequires:	elfutils-devel
BuildRequires:	expat-devel
BuildRequires:	gcc >= 6:4.6.0
BuildRequires:	gd-devel
BuildRequires:	glog-devel >= 0.3.2
BuildRequires:	imap-devel >= 1:2007
#BuildRequires:	jemalloc-devel >= 3.0.0
BuildRequires:	libcap-devel
BuildRequires:	libdwarf-devel
#BuildRequires:	libevent-devel >= 1.4.14
BuildRequires:	libicu-devel >= 4.2
#BuildRequires:	libmbfl-devel
BuildRequires:	libmcrypt-devel
BuildRequires:	libmemcached-devel >= 1.0.4
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	libunwind-devel
BuildRequires:	libxml2-devel
BuildRequires:	mysql-devel
BuildRequires:	oniguruma-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
#BuildRequires:	php-xhp-devel >= 1.3.9-6
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.675
BuildRequires:	tbb-devel >= 4.0.6000
BuildRequires:	zlib-devel
# check later, seem unused
#BuildRequires:	bison >= 2.3
#BuildRequires:	flex >= 2.5.35
#BuildRequires:	libafdt-devel >= 0.1.0
#BuildRequires:	re2c >= 0.13.0
Provides:	php(apc)
Provides:	php(bcmath)
Provides:	php(bz2)
Provides:	php(ctype)
Provides:	php(curl)
Provides:	php(date)
Provides:	php(dom)
Provides:	php(exif)
Provides:	php(fb)
Provides:	php(fileinfo)
Provides:	php(filter)
Provides:	php(gd)
Provides:	php(hash)
Provides:	php(hotprofiler)
Provides:	php(iconv)
Provides:	php(icu_num_fmt)
Provides:	php(icu_ucsdet)
Provides:	php(icu_uspoof)
Provides:	php(idn)
Provides:	php(imap)
Provides:	php(json)
Provides:	php(ldap)
Provides:	php(mbstring)
Provides:	php(mcrypt)
Provides:	php(memcache)
Provides:	php(memcached)
Provides:	php(mysql)
Provides:	php(openssl)
Provides:	php(pcntl)
Provides:	php(pcre)
Provides:	php(pdo)
Provides:	php(pdo_mysql)
Provides:	php(pdo_sqlite)
Provides:	php(phar)
Provides:	php(posix)
Provides:	php(reflection)
Provides:	php(server)
Provides:	php(session)
Provides:	php(simplexml)
Provides:	php(soap)
Provides:	php(sockets)
Provides:	php(spl)
Provides:	php(sqlite3)
Provides:	php(sysvmsg)
Provides:	php(sysvsem)
Provides:	php(sysvshm)
Provides:	php(thread)
Provides:	php(thrift_protocol)
Provides:	php(tokenizer)
Provides:	php(xhprof)
Provides:	php(xml)
Provides:	php(xmlreader)
Provides:	php(xmlwriter)
Provides:	php(zip)
Provides:	php(zlib)
Obsoletes:	hiphop-php < 2.3.2-0.2
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%prep
%setup -q -a1 -a2 -n %{name}-HHVM-%{version}

mv folly-*/* hphp/submodules/folly
# https://github.com/facebook/folly/pull/44
sed -i -e '21 d' hphp/third_party/folly/folly/detail/Malloc.h

%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
#%patch5 -p1

# prefer ones from system
rm CMake/FindBISON.cmake
rm CMake/FindBoost.cmake
rm CMake/FindFLEX.cmake

ln -s libevent-1.4.*-stable libevent
%{__patch} -d libevent -p1 < hphp/third_party/libevent-1.4.14.fb-changes.diff

%if 0
%patch0 -p1
%patch1 -p1
#%patch3 -p1
%patch4 -p1

#rm -rf src/third_party/libmbfl
#sed -i -e '/add_subdirectory(third_party\/libmbfl)/d' src/CMakeLists.txt

rm -rf src/third_party/xhp
rm -rf src/third_party/libafdt
%endif

%build
# build libevent 1.4 with fb patches
if [ ! -d libevent/.libs ]; then
	cd libevent
	# TODO: should use static linking, but then it fails to detect libraries due missing -lrt
	%configure \
		%{?0:--enable-static} \
		%{?0:--disable-shared}
	%{__make}
	ln -s .libs lib
	ln -s . include
	cd ..
fi

export HPHP_HOME=$(pwd)
export HPHP_LIB=$HPHP_HOME/bin
install -d $HPHP_LIB

# asm linking breaks on $CC containing spaces
if [[ "%{__cc}" = *ccache* ]]; then
	cat <<-'EOF' > $HPHP_LIB/gcc
	#!/bin/sh
	exec %{__cc} "$@"
	EOF
	chmod +x $HPHP_LIB/gcc
	CC=$HPHP_LIB/gcc
fi

%if 0
# out of dir build broken (can't find it's tools)
install -d build
cd build
%endif

%cmake \
	-DLIBEVENT_LIB=$HPHP_HOME/libevent/lib/libevent.so \
	-DLIBEVENT_INCLUDE_DIR=$HPHP_HOME/libevent \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-DUSE_JEMALLOC=OFF \
	-DUSE_TCMALLOC=OFF \
	-DHPHP_NOTEST=ON \
	./

# setup COMPILER_ID/HHVM_REPO_SCHEMA so it doesn't look it up from our package git repo
# see hphp/util/generate-buildinfo.sh
export COMPILER_ID=HPHP-%{version}-%{release}-%{githash}
export HHVM_REPO_SCHEMA=$(date +%N_%s)

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	HPHP_HOME=$(pwd) \
	DESTDIR=$RPM_BUILD_ROOT

ln -s hhvm $RPM_BUILD_ROOT%{_bindir}/php
ln -s hhvm $RPM_BUILD_ROOT%{_bindir}/hphp

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/hdf
cp -p hphp/doc/mime.hdf $RPM_BUILD_ROOT%{_datadir}/%{name}/hdf/static.mime-types.hdf

# install fastcgi initscript
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-fcgi
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/%{name}-fcgi

# install our libevent for now
install -d $RPM_BUILD_ROOT%{_libdir}
libtool --mode=install install -p libevent/libevent.la $RPM_BUILD_ROOT%{_libdir}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libevent.{a,la,so}

# setup -devel
install -d $RPM_BUILD_ROOT%{_datadir}/cmake/Modules
cp -a CMake/* $RPM_BUILD_ROOT%{_datadir}/cmake/Modules

HPHP_HOME=$(pwd)
sed -e "
	/HHVM_INCLUDE_DIRS/ s,$HPHP_HOME,%{_includedir},g
" hphp/tools/hphpize/hphpize.cmake > $RPM_BUILD_ROOT%{_datadir}/cmake/Modules/hphpize.cmake

oIFS=$IFS
IFS=";"
set -- $(sed -ne 's/set(HHVM_INCLUDE_DIRS "\(.*\)")/\1/p' hphp/tools/hphpize/hphpize.cmake)
IFS=$oIFS
set -- $(
	for dir in "$@"; do
		[[ "$dir" = $HPHP_HOME/hphp/* ]] && echo $dir
	done
)

set +x
for dir in "$@" \
	$HPHP_HOME/hphp/runtime \
	$HPHP_HOME/hphp/util \
	$HPHP_HOME/hphp/neo \
	$HPHP_HOME/hphp/system \
	$HPHP_HOME/hphp/parser \
; do
	echo "D %{_includedir}${dir#$HPHP_HOME}"
	find $dir -name '*.h' | while read path; do
		file=%{_includedir}${path#$HPHP_HOME}
		echo "F $file"
		install -Dp $path $RPM_BUILD_ROOT$file
	done
done
set -x

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
%doc README.md hphp/NEWS
%attr(755,root,root) %{_bindir}/hhvm
%attr(755,root,root) %{_bindir}/hphp
%attr(755,root,root) %{_libdir}/libevent-1.4.so.*.*.*
%ghost %{_libdir}/libevent-1.4.so.2

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/hdf
%{_datadir}/%{name}/hdf/static.mime-types.hdf

%files fcgi
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/%{name}-fcgi
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}-fcgi

%files program
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/php

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hphpize
%{_includedir}/hphp
%{_datadir}/cmake/Modules/hphpize.cmake
%{_datadir}/cmake/Modules/FindCClient.cmake
%{_datadir}/cmake/Modules/FindEditline.cmake
%{_datadir}/cmake/Modules/FindGD.cmake
%{_datadir}/cmake/Modules/FindGlog.cmake
%{_datadir}/cmake/Modules/FindICU.cmake
%{_datadir}/cmake/Modules/FindLdap.cmake
%{_datadir}/cmake/Modules/FindLibAfdt.cmake
%{_datadir}/cmake/Modules/FindLibCh.cmake
%{_datadir}/cmake/Modules/FindLibDL.cmake
%{_datadir}/cmake/Modules/FindLibDwarf.cmake
%{_datadir}/cmake/Modules/FindLibElf.cmake
%{_datadir}/cmake/Modules/FindLibEvent.cmake
%{_datadir}/cmake/Modules/FindLibEvent.cmake.bak
%{_datadir}/cmake/Modules/FindLibNuma.cmake
%{_datadir}/cmake/Modules/FindLibXed.cmake
%{_datadir}/cmake/Modules/FindLibiconv.cmake
%{_datadir}/cmake/Modules/FindLibinotify.cmake
%{_datadir}/cmake/Modules/FindLibmemcached.cmake
%{_datadir}/cmake/Modules/FindLibpam.cmake
%{_datadir}/cmake/Modules/FindMcrypt.cmake
%{_datadir}/cmake/Modules/FindMySQL.cmake
%{_datadir}/cmake/Modules/FindNcurses.cmake
%{_datadir}/cmake/Modules/FindONIGURUMA.cmake
%{_datadir}/cmake/Modules/FindPCRE.cmake
%{_datadir}/cmake/Modules/FindPThread.cmake
%{_datadir}/cmake/Modules/FindReadline.cmake
%{_datadir}/cmake/Modules/FindTBB.cmake
%{_datadir}/cmake/Modules/FollySetup.cmake
%{_datadir}/cmake/Modules/HPHPCompiler.cmake
%{_datadir}/cmake/Modules/HPHPFindLibs.cmake
%{_datadir}/cmake/Modules/HPHPFunctions.cmake
%{_datadir}/cmake/Modules/HPHPSetup.cmake
%{_datadir}/cmake/Modules/Options.cmake
