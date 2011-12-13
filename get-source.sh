#!/bin/sh
set -e

package=hiphop-php
version=$(awk '/^Version:/{print $NF}' $package.spec)
repo_url=git://github.com/facebook/$package.git

export GIT_DIR=$package/.git

if [ ! -d $package ]; then
	git clone --depth 1 $repo_url $package
else
   	git pull
fi

git submodule init
git submodule update

#rm -rf src/third_party/libmbfl
#rm -rf src/third_party/xhp
#rm -rf src/third_party/libafdt

version=$(cd $package; (echo 'function HPHP_VERSION(v) { printf("%.3f", v)}; BEGIN{'; cat src/version; echo '}') | awk -f -)
version=${version}_$(git log -1 --format=%h)

git archive master --prefix $package-$version/ | bzip2 > $package-$version.tar.bz2

../dropin $package-$version.tar.bz2 &
