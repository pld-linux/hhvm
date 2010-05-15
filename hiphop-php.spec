Summary:	HipHop for PHP transforms PHP source code into highly optimized C++
Name:		hiphop-php
Version:	0.1
Release:	0.1
License:	PHP 3.01
Group:		Development/Languages/PHP
# git clone git://github.com/facebook/hiphop-php.git
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	-
URL:		http://wiki.github.com/facebook/hiphop-php/
BuildRequires:	binutils-devel
BuildRequires:	bison
BuildRequires:	boost-devel >= 1.37
BuildRequires:	cmake >= 2.6.4
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	gd-devel
BuildRequires:	libcap-devel
BuildRequires:	libicu >= 4.2
BuildRequires:	libmbfl
BuildRequires:	libmcrypt
BuildRequires:	libstdc++-devel >= 6:4.1
BuildRequires:	libxml2
BuildRequires:	mysql-devel
BuildRequires:	oniguruma
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	re2c >= 0.13.0
BuildRequires:	tbb >= 2.2
BuildRequires:	zlib-devel
BuildArch:	noarch
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
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
