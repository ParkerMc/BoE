# BoE /bō/

[![Build Status](https://travis-ci.org/ParkerMc/BOE.svg?branch=master)](https://travis-ci.org/ParkerMc/BOE) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/d92ad430e4c04741b2a563941fe89ed7)](https://www.codacy.com/app/ParkerMc/BOE?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ParkerMc/BOE&amp;utm_campaign=Badge_Grade) [![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/) [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

A chat platform that intends to look at other chat programs and take only the "Best of Everything".

[<img src="https://cdn.rawgit.com/ParkerMc/BOE/master/Client-Python/assets/B.o.E..png" alt="Icon" data-canonical-src="https://cdn.rawgit.com/ParkerMc/BOE/master/Client-Python/assets/B.o.E..png" width="200" height="200" />](https://github.com/ParkerMc/BOE) 

<sup><sup><sup>Icon by angelgal246.</sup></sup></sup>

#Install

####Ubuntu####
To install on Ubuntu you first need to add the ppa and import the key.
```
sudo add-apt-repository ppa:parkermc/boe
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 018486F9EEA44E0F
sudo apt-get update
```
Then install it with:
`sudo apt-get install boe`


Install files on other systems coming **very soon**

- - - -

[Mods](https://github.com/ParkerMc/BoE-Mods)

For the client on windows you need run setup-Windows.bat and install [PyQt4.](https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/)

For the voice testing you must have [pyaudio.](http://people.csail.mit.edu/hubert/pyaudio/)

Must have a ssl certificate run command and put ssl.pem in to the server folder.
`openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl.pem -out ssl.pem`
Or for a non self-signed 
`letsencrypt certonly --standalone -d domain.com`


