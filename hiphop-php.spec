# TODO
# - system libmbfl, system xhp, sqlite3
# - there should be a bit more packaged into files
# - build fail:
#Linking CXX executable hphp
#Building hphpi
#Exception: ParseError: [<string>:1] Unable to parse line hphpi_build.hdf
#make[2]: *** [src/hphp/hphp] Error 255
#make[1]: *** [src/hphp/CMakeFiles/hphp.dir/all] Error 2
Summary:	HipHop for PHP transforms PHP source code into highly optimized C++
Name:		hiphop-php
Version:	0.1
Release:	0.1
License:	PHP 3.01
Group:		Development/Languages
# git clone git://github.com/facebook/hiphop-php.git
# rm -rf hiphop-php/src/third_party/libmbfl
# tar --exclude-vcs -cjf hiphop-php.tar.bz2 hiphop-php
Source0:	%{name}.tar.bz2
# Source0-md5:	fbeaba0785d6ae3a6f513576867fb5a6
Patch0:		cmake-missing-library.patch
Patch1:		system-libmbfl.patch
Patch2:		gcc45.patch
URL:		http://wiki.github.com/facebook/hiphop-php/
BuildRequires:	binutils-devel
BuildRequires:	bison >= 2.3
BuildRequires:	boost-devel >= 1.37
BuildRequires:	cmake >= 2.6.4
BuildRequires:	curl-devel >= 7.20.1-2
BuildRequires:	expat-devel
BuildRequires:	flex >= 2.5.35
BuildRequires:	gd-devel
BuildRequires:	libcap-devel
BuildRequires:	libevent-devel >= 1.4.13-2
BuildRequires:	libicu-devel >= 4.2
BuildRequires:	libmbfl-devel
BuildRequires:	libmcrypt
BuildRequires:	libstdc++-devel >= 6:4.1
BuildRequires:	libxml2-devel
BuildRequires:	mysql-devel
BuildRequires:	oniguruma-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	re2c >= 0.13.0
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

Keep up to date on HipHop development by joining the HipHop for PHP
Discussion Group.

%prep
%setup -qn %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__sed} -i -e 's,/usr/local/bin/php,/usr/bin/php,g' src/crutch.php

%build
export HPHP_HOME=$(pwd)
export HPHP_LIB=$HPHP_HOME/bin

%cmake . \
	-DCMAKE_BUILD_TYPE=%{!?debug:Release}%{?debug:Debug} \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_includedir}/afdt.h
%{_libdir}/libafdt.a
%{_libdir}/libxhp.a
