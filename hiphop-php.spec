# TODO
# - system libevent2: https://github.com/facebook/hiphop-php/pull/421
# - system libmbfl, system xhp, sqlite3
%define		githash	78394ee
%define		rel		0.4
Summary:	Virtual Machine, Runtime, and JIT for PHP
Name:		hiphop-php
Version:	2.1.0
Release:	0.%{githash}.%{rel}
License:	PHP 3.01
Group:		Development/Languages
Source0:	https://github.com/facebook/hiphop-php/archive/%{githash}/HPHP-%{version}.%{githash}.tar.gz
# Source0-md5:	81742a0535a6bab906208d3756b206d1
# need fb.changes.patch, which is available for 1.4 only
Source1:	http://www.monkey.org/~provos/libevent-1.4.14b-stable.tar.gz
# Source1-md5:	a00e037e4d3f9e4fe9893e8a2d27918c
Source2:	get-source.sh
Patch0:		cmake-missing-library.patch
Patch1:		libevent14.patch
Patch3:		system-xhp.patch
Patch4:		system-libafdt.patch
Patch5:		system-folly.patch
Patch6:		boost-system-category.patch
URL:		http://wiki.github.com/facebook/hiphop-php/
BuildRequires:	binutils-devel
BuildRequires:	bison >= 2.3
BuildRequires:	boost-devel >= 1.50
BuildRequires:	cmake >= 2.8.5
BuildRequires:	curl-devel >= 7.29.0
BuildRequires:	elfutils-devel
BuildRequires:	expat-devel
BuildRequires:	flex >= 2.5.35
BuildRequires:	gd-devel
BuildRequires:	glog-devel >= 0.3.2
BuildRequires:	imap-devel >= 1:2007
#BuildRequires:	jemalloc-devel
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
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	tbb-devel >= 4.0.6000
BuildRequires:	zlib-devel
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HipHop VM (HHVM) is a new open-source virtual machine designed for
executing programs written in PHP. HHVM uses a just-in-time
compilation approach to achieve superior performance while maintaining
the flexibility that PHP developers are accustomed to. HipHop VM (and
before it HPHPc) has realized > 5x increase in throughput for Facebook
compared with Zend PHP 5.2.

HipHop is most commonly run as a standalone server, replacing both
Apache and mod_php.

%prep
%setup -qc -a1
mv %{name}-%{githash}*/* .

#%patch5 -p1
%patch6 -p1

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

CPPFLAGS="%{rpmcppflags} -fno-permissive"
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
sha=$(echo %{name}-%{githash}*)
export COMPILER_ID=HPHP-%{version}-%{release}-${sha#%{name}-}
export HHVM_REPO_SCHEMA=$(date +%N_%s)

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	HPHP_HOME=$(pwd) \
	DESTDIR=$RPM_BUILD_ROOT

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
%attr(755,root,root) %{_libdir}/libevent-1.4.so.*.*.*
%ghost %{_libdir}/libevent-1.4.so.2

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/hdf
%{_datadir}/%{name}/hdf/static.mime-types.hdf
