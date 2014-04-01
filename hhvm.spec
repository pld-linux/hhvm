# NOTES:
# - hphp/runtime/base/runtime-option.cpp evalJitDefault enables jit if /.hhvm-jit exists (yes, in filesystem root)
# TODO
# - system libmbfl, system xhp, sqlite3
# - libdwarf>20120410 issue: https://github.com/facebook/hhvm/issues/1337
# git show HHVM-3.0.0
%define		githash	59a8db46e4ebf5cfd205fadc12e27a9903fb7aae
%define		folly	d9c79af
Summary:	Virtual Machine, Runtime, and JIT for PHP
Name:		hhvm
Version:	3.0.0
Release:	0.1
License:	PHP 3.01
Group:		Development/Languages
Source0:	https://github.com/facebook/hhvm/archive/HHVM-%{version}.tar.gz
# Source0-md5:	7762f2a8a6fe402c68728ffb282caae7
# need fb.changes.patch, which is available for 1.4 only
Source2:	https://github.com/facebook/folly/archive/%{folly}/folly-0.1-%{folly}.tar.gz
# Source2-md5:	e14ff4b87c986dbe095547bdf0761dd1
Source3:	%{name}-fcgi.init
Source4:	%{name}-fcgi.sysconfig
Source100:	get-source.sh
Patch0:		cmake-missing-library.patch
Patch3:		system-xhp.patch
Patch4:		system-libafdt.patch
Patch5:		system-folly.patch
Patch8:		hphpize.patch
Patch9:		notest.patch
Patch10:	no-debug.patch
URL:		http://wiki.github.com/facebook/hiphop-php/
BuildRequires:	a52dec-libs-devel
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
BuildRequires:	libdwarf-devel >= 20130729
BuildRequires:	libicu-devel >= 4.2
#BuildRequires:	libmbfl-devel
BuildRequires:	libmcrypt-devel
BuildRequires:	libmemcached-devel >= 1.0.4
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	libunwind-devel
BuildRequires:	libxml2-devel
BuildRequires:	ImageMagick-devel
BuildRequires:	libxslt-devel
BuildRequires:	mysql-devel
BuildRequires:	ocaml-findlib
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
# foreach (get_loaded_extensions() as $ext) printf("Provides:\tphp(%s)\n", strtolower($ext));
Provides:	php(apache)
Provides:	php(apc)
Provides:	php(bcmath)
Provides:	php(bz2)
Provides:	php(ctype)
Provides:	php(curl)
Provides:	php(date)
Provides:	php(debugger)
Provides:	php(dom)
Provides:	php(exif)
Provides:	php(fb)
Provides:	php(fileinfo)
Provides:	php(filter)
Provides:	php(function)
Provides:	php(gd)
Provides:	php(hash)
Provides:	php(hh)
Provides:	php(hhvm.debugger)
Provides:	php(hhvm.ini)
Provides:	php(hotprofiler)
Provides:	php(iconv)
Provides:	php(idn)
Provides:	php(imagick)
Provides:	php(imap)
Provides:	php(intl)
Provides:	php(json)
Provides:	php(ldap)
Provides:	php(libxml)
Provides:	php(mbstring)
Provides:	php(mcrypt)
Provides:	php(memcache)
Provides:	php(memcached)
Provides:	php(misc)
Provides:	php(mysql)
Provides:	php(mysqli)
Provides:	php(openssl)
Provides:	php(pcntl)
Provides:	php(pcre)
Provides:	php(pdo)
Provides:	php(pdo_mysql)
Provides:	php(pdo_sqlite)
Provides:	php(phar)
Provides:	php(posix)
Provides:	php(redis)
Provides:	php(reflection)
Provides:	php(server)
Provides:	php(session)
Provides:	php(simplexml)
Provides:	php(soap)
Provides:	php(sockets)
Provides:	php(spl)
Provides:	php(sqlite3)
Provides:	php(stream)
Provides:	php(sysvmsg)
Provides:	php(sysvsem)
Provides:	php(sysvshm)
Provides:	php(thread)
Provides:	php(thrift_protocol)
Provides:	php(tokenizer)
Provides:	php(url)
Provides:	php(xhprof)
Provides:	php(xml)
Provides:	php(xmlreader)
Provides:	php(xmlwriter)
Provides:	php(xsl)
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
%setup -q -a2 -n %{name}-HHVM-%{version}

mv folly-*/* hphp/submodules/folly

%patch8 -p1
%patch9 -p1
%patch10 -p1
#%patch5 -p1

# prefer ones from system
rm CMake/FindBISON.cmake
rm CMake/FindFLEX.cmake
rm CMake/FindFreetype.cmake

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
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-DUSE_JEMALLOC=OFF \
	-DUSE_TCMALLOC=OFF \
	-DHPHP_NOTEST=ON \
	./

# setup COMPILER_ID/HHVM_REPO_SCHEMA so it doesn't look it up from our package git repo
# see hphp/util/generate-buildinfo.sh
export COMPILER_ID=HHVM-%{version}-%{release}-%{githash}
export HHVM_REPO_SCHEMA=$(date +%N_%s)

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
%{__make} install \
	HPHP_HOME=$(pwd) \
	DESTDIR=$RPM_BUILD_ROOT

# not packaged here
rm $RPM_BUILD_ROOT%{_includedir}/zip.h
rm $RPM_BUILD_ROOT%{_includedir}/zipconf.h
rm $RPM_BUILD_ROOT%{_prefix}/lib/libzip.a
rm $RPM_BUILD_ROOT%{_prefix}/lib/libzip.so

ln -s hhvm $RPM_BUILD_ROOT%{_bindir}/php
ln -s hhvm $RPM_BUILD_ROOT%{_bindir}/hphp

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/hdf
cp -p hphp/doc/mime.hdf $RPM_BUILD_ROOT%{_datadir}/%{name}/hdf/static.mime-types.hdf

# install fastcgi initscript
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-fcgi
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/%{name}-fcgi

# setup -devel
install -d $RPM_BUILD_ROOT%{_datadir}/cmake/Modules
cp -p CMake/*.cmake $RPM_BUILD_ROOT%{_datadir}/cmake/Modules

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
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %{_bindir}/hhvm
%attr(755,root,root) %{_bindir}/hphp

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
%{_datadir}/cmake/Modules/ExtZendCompat.cmake
%{_datadir}/cmake/Modules/FindCClient.cmake
%{_datadir}/cmake/Modules/FindEditline.cmake
%{_datadir}/cmake/Modules/FindGlog.cmake
%{_datadir}/cmake/Modules/FindICU.cmake
%{_datadir}/cmake/Modules/FindLdap.cmake
%{_datadir}/cmake/Modules/FindLibAfdt.cmake
%{_datadir}/cmake/Modules/FindLibCh.cmake
%{_datadir}/cmake/Modules/FindLibDL.cmake
%{_datadir}/cmake/Modules/FindLibDwarf.cmake
%{_datadir}/cmake/Modules/FindLibElf.cmake
%{_datadir}/cmake/Modules/FindLibJpeg.cmake
%{_datadir}/cmake/Modules/FindLibMagickWand.cmake
%{_datadir}/cmake/Modules/FindLibNuma.cmake
%{_datadir}/cmake/Modules/FindLibPng.cmake
%{_datadir}/cmake/Modules/FindLibUODBC.cmake
%{_datadir}/cmake/Modules/FindLibXed.cmake
%{_datadir}/cmake/Modules/FindLibYaml.cmake
%{_datadir}/cmake/Modules/FindLibiconv.cmake
%{_datadir}/cmake/Modules/FindLibinotify.cmake
%{_datadir}/cmake/Modules/FindLibmemcached.cmake
%{_datadir}/cmake/Modules/FindLibpam.cmake
%{_datadir}/cmake/Modules/FindMcrypt.cmake
%{_datadir}/cmake/Modules/FindMySQL.cmake
%{_datadir}/cmake/Modules/FindNcurses.cmake
%{_datadir}/cmake/Modules/FindOCaml.cmake
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
%{_datadir}/cmake/Modules/hphpize.cmake
