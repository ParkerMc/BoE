cd ../../
rm -R ppa
mkdir ppa
mkdir ppa/boeServer
mkdir ppa/bin
mkdir ppa/data
cp build_scripts/ppa/setup-server.py ppa/setup.py
cp build_scripts/ppa/MANIFEST.in ppa/
cp build_scripts/ppa/stdeb.cfg ppa/
cp build_scripts/ppa/boe-server ppa/bin/
cp -R Server/* ppa/boeServer
cp LICENSE ppa/boeServer
cd ppa
python setup.py --command-packages=stdeb.command bdist_deb
mkdir tmp
cd deb_dist
NAME="$(find -name '*.dsc')"
cd ../tmp
dpkg-source -x ../deb_dist/$NAME
cd boe-server*
sed -i -e 's/Depends: ${misc:Depends}/Depends: python-qt4, python-passlib, ${misc:Depends}/g' debian/control
sed -i -e 's/Package: python-boe/Package: boe/g' debian/control
debuild -S -sa
cd ..
NAME="$(find -name '*.changes')"
dput ppa:parkermc/boe $NAME
cd boe-server*
debuild -us -uc -b

