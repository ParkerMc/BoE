#!/usr/bin/env bash
cd ../../
mkdir -p linux/usr/bin
mkdir -p linux/usr/lib/boe/client
mkdir -p linux/usr/lib/boe/server
mkdir -p linux/usr/share/applications/
mkdir -p linux/usr/share/icons/hicolor/scalable/apps/
cp -R Client-Python/* linux/usr/lib/boe/client
cp -R Server/* linux/usr/lib/boe/server
cp build_scripts/BoE.desktop linux/usr/share/applications/BoE.desktop
mv linux/usr/lib/boe/client/assets/boe.svg linux/usr/share/icons/hicolor/scalable/apps/boe.svg
cp build_scripts/boe linux/usr/bin/boe
cp build_scripts/boe-server linux/usr/bin/boe-server
cd linux
tar -zcvf ../linux.tar.gz usr/
