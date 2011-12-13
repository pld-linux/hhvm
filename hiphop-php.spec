# TODO
# - system libmbfl, system xhp, sqlite3
# - there should be a bit more packaged into files
# - linking segfaults
#   using bfd and gcc-6:4.6.2-2.x86_64 binutils-3:2.22.51.0.1-1.x86_64
#   cd /home/users/glen/rpm/packages/BUILD.x86_64-linux/hiphop-php-1.000_cf9b612/src/hphpi && /home/users/glen/rpm/BUILD.x86_64-linux/hiphop-php-1.000_cf9b612/build/src/hphp/hphp -t cpp -f exe --input-dir . -i hphpi.php -o gen -vEnableEval=2 --log=1
#   Segmentation fault
#   make[2]: *** [src/hphp/hphp] Error 139
#   relinking succeeds, but resulting binary segfaults as well:
#   0x0000000000b9cc0b in HPHP::Extension::LoadModules(HPHP::Hdf) ()
%define		snap	cf9b612
%define		rel		0.2
Summary:	HipHop for PHP transforms PHP source code into highly optimized C++
Name:		hiphop-php
Version:	1.000
Release:	%{rel}.%{snap}
License:	PHP 3.01
Group:		Development/Languages
Source0:	%{name}-%{version}_%{snap}.tar.bz2
# Source0-md5:	16b7928995a91001657b015fe7f8a06d
# need fb.changes.patch, which is available for 1.4 only
Source1:	http://www.monkey.org/~provos/libevent-1.4.14b-stable.tar.gz
# Source1-md5:	a00e037e4d3f9e4fe9893e8a2d27918c
Source2:	get-source.sh
Patch0:		cmake-missing-library.patch
Patch1:		libevent14.patch
Patch3:		system-xhp.patch
Patch4:		system-libafdt.patch
URL:		http://wiki.github.com/facebook/hiphop-php/
BuildRequires:	binutils-devel
BuildRequires:	bison >= 2.3
BuildRequires:	boost-devel >= 1.39
BuildRequires:	cmake >= 2.6.4
BuildRequires:	curl-devel >= 7.20.1-2
BuildRequires:	expat-devel
BuildRequires:	flex >= 2.5.35
BuildRequires:	gd-devel
BuildRequires:	jemalloc-devel
BuildRequires:	libafdt-devel >= 0.1.0
BuildRequires:	libcap-devel
#BuildRequires:	libevent-devel < 2.0
#BuildRequires:	libevent-devel >= 1.4.13-2
BuildRequires:	libicu-devel >= 4.2
#BuildRequires:	libmbfl-devel
BuildRequires:	libmcrypt
BuildRequires:	libmemcached-devel >= 0.39
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	libxml2-devel
BuildRequires:	mysql-devel
BuildRequires:	oniguruma-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	php-xhp-devel >= 1.3.9-6
BuildRequires:	re2c >= 0.13.0
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	tbb-devel >= 2.2
BuildRequires:	zlib-devel
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HipHop transforms your PHP source code into highly optimized C++ and
then compiles it with g++ to build binary files. You keep coding in
simpler PHP, then HipHop executes your source code in a semantically
equivalent manner and sacrifices some rarely used features - such as
eval() - in exchange for improved performance.

Facebook sees about a 50% reduction in CPU usage when serving equal
amounts of Web traffic when compared to Apache and PHP. Facebook's API
tier can serve twice the traffic using 30% less CPU.

%prep
%setup -qn %{name}-%{version}_%{snap} -a1
%patch0 -p1
%patch1 -p1
#%patch3 -p1
%patch4 -p1

ln -s libevent-1.4.*-stable libevent
%{__patch} -d libevent -p1 < src/third_party/libevent-1.4.14.fb-changes.diff

#rm -rf src/third_party/libmbfl
#sed -i -e '/add_subdirectory(third_party\/libmbfl)/d' src/CMakeLists.txt

rm -rf src/third_party/xhp
rm -rf src/third_party/libafdt

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

install -d build
cd build
%cmake \
	-DLibEvent_INCLUDE_PATHS=$HPHP_HOME/libevent \
	-DLibEvent_LIB_PATHS=$HPHP_HOME/libevent/.libs \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-DSKIP_BUNDLED_XHP=ON \
	-DUSE_JEMALLOC=ON \
	-DUSE_TCMALLOC=OFF \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p build/src/hphp/hphp $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hphp
