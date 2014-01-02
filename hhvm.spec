# NOTES:
# - hphp/runtime/base/runtime-option.cpp evalJitDefault enables jit if /.hhvm-jit exists (yes, in filesystem root)
# TODO
# - system libevent2: https://github.com/facebook/hiphop-php/pull/421
# - system libmbfl, system xhp, sqlite3
%define		githash	f951cb8d8812c59344d5322454853b584b668636
Summary:	Virtual Machine, Runtime, and JIT for PHP
Name:		hhvm
Version:	2.3.2
Release:	0.2
License:	PHP 3.01
Group:		Development/Languages
Source0:	https://github.com/facebook/hhvm/archive/HHVM-%{version}.tar.gz
# Source0-md5:	471961d38ba52c66b7038c556b2b7bd8
# need fb.changes.patch, which is available for 1.4 only
Source1:	http://www.monkey.org/~provos/libevent-1.4.14b-stable.tar.gz
# Source1-md5:	a00e037e4d3f9e4fe9893e8a2d27918c
Source2:	https://github.com/facebook/folly/archive/4d6d659/folly-%{version}-4d6d659.tar.gz
Source100:	get-source.sh
Patch0:		cmake-missing-library.patch
Patch1:		libevent14.patch
Patch3:		system-xhp.patch
Patch4:		system-libafdt.patch
Patch5:		system-folly.patch
Patch6:		checksum.patch
Patch7:		imap-gss.patch
URL:		http://wiki.github.com/facebook/hiphop-php/
BuildRequires:	binutils-devel
BuildRequires:	bison >= 2.3
BuildRequires:	boost-devel >= 1.50
BuildRequires:	cmake >= 2.8.7
BuildRequires:	curl-devel >= 7.29.0
BuildRequires:	elfutils-devel
BuildRequires:	expat-devel
BuildRequires:	flex >= 2.5.35
BuildRequires:	gcc >= 6:4.6.0
BuildRequires:	gd-devel
BuildRequires:	glog-devel >= 0.3.2
BuildRequires:	imap-devel >= 1:2007
#BuildRequires:	jemalloc-devel >= 3.0.0
BuildRequires:	libafdt-devel >= 0.1.0
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
BuildRequires:	re2c >= 0.13.0
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.675
BuildRequires:	tbb-devel >= 4.0.6000
BuildRequires:	zlib-devel
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

%prep
%setup -q -a1 -a2 -n %{name}-HHVM-%{version}

mv folly-*/* hphp/submodules/folly

%patch6 -p1
%patch7 -p1

#%patch5 -p1

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
export LIBEVENT_PREFIX=$HPHP_HOME/libevent

	-DLibEvent_LIB=$HPHP_HOME/libevent/libevent.so \
	-DLibEvent_INCLUDE_PATHS=$HPHP_HOME/libevent \
	-DLibEvent_LIB_PATHS=$HPHP_HOME/libevent/.libs \
%endif

%if 0
# out of dir build broken (can't find it's tools)
install -d build
cd build
%endif

%cmake \
	-DLIBEVENT_LIB=$HPHP_HOME/libevent/lib/libevent.so \
	-DLIBEVENT_INCLUDE_DIR=$HPHP_HOME/libevent \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-DSKIP_BUNDLED_XHP=ON \
	-DUSE_JEMALLOC=OFF \
	-DUSE_TCMALLOC=OFF \
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

# install our libevent for now
install -d $RPM_BUILD_ROOT%{_libdir}
libtool --mode=install install -p libevent/libevent.la $RPM_BUILD_ROOT%{_libdir}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libevent.{a,la,so}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

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

%files program
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/php
