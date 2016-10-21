cd ../../
mkdir ppa
mkdir ppa/boeClient
mkdir ppa/bin
mkdir ppa/data
cp build_scripts/ppa/setup.py ppa/
cp build_scripts/ppa/MANIFEST.in ppa/
cp build_scripts/ppa/stdeb.cfg ppa/
cp build_scripts/ppa/boe ppa/bin/
cp build_scripts/ppa/BoE.desktop ppa/data/
cp -R Client-Python/* ppa/boeClient
cp LICENSE ppa/boeClient
cd ppa
mv boeClient/assets/boe.svg data/boe.svg
rm boeClient/assets/BoE.ico
python setup.py --command-packages=stdeb.command bdist_deb
mkdir tmp
cd deb_dist
NAME="$(find -name '*.dsc')"
cd ../tmp
dpkg-source -x ../deb_dist/$NAME
cd boe-*
sed -i -e 's/Depends: ${misc:Depends}/Depends: python-qt4, python-passlib, python-websocket-client, ${misc:Depends}/g' debian/control
sed -i -e 's/Package: python-boe/Package: boe/g' debian/control
debuild -S -sa
#debuild -us -uc -b
cd ..
NAME="$(find -name '*.changes')"
dput ppa:parkermc/boe $NAME

