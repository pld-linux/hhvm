Summary:	HipHop for PHP transforms PHP source code into highly optimized C++
Name:		hiphop-php
Version:	_
Release:	0.1
License:	- (enter GPL/GPL v2/GPL v3/LGPL/BSD/BSD-like/other license name here)
Group:		Development/Languages/PHP
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	-
URL:		http://developers.facebook.com/hiphop-php/
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
