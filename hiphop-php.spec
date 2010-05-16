# TODO
# - offline build (without git)
Summary:	HipHop for PHP transforms PHP source code into highly optimized C++
Name:		hiphop-php
Version:	0.1
Release:	0.1
License:	PHP 3.01
Group:		Development/Languages
# git clone git://github.com/facebook/hiphop-php.git
# tar -cjf hiphop-php.tar.bz2 hiphop-php
Source0:	%{name}.tar.bz2
# Source0-md5:	fbeaba0785d6ae3a6f513576867fb5a6
URL:		http://wiki.github.com/facebook/hiphop-php/
BuildRequires:	binutils-devel
BuildRequires:	bison
BuildRequires:	boost-devel >= 1.37
BuildRequires:	cmake >= 2.6.4
BuildRequires:	curl-devel >= 7.20.1-2
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	gd-devel
BuildRequires:	git-core
BuildRequires:	libcap-devel
BuildRequires:	libevent-devel >= 1.4.13-2
BuildRequires:	libicu-devel >= 4.2
#BuildRequires:	libmbfl-devel
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

%build
export HPHP_HOME=$(pwd)
export HPHP_LIB=$HPHP_HOME/bin

git submodule init
git submodule update

%cmake .
%{__make}

%{__sed} -i -e 's,/usr/local/bin/php,/usr/bin/php,g' src/crutch.php

%install
rm -rf $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
