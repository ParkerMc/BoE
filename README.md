# BoE /bō/

[![Build Status](https://travis-ci.org/ParkerMc/BoE.svg?branch=master)](https://travis-ci.org/ParkerMc/BoE)
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)

A chat platform that intends to look at other chat programs and take only the "Best of Everything".

[<img src="https://raw.githubusercontent.com/ParkerMc/BOE/master/B.o.E..png" alt="Icon" data-canonical-src="https://raw.githubusercontent.com/ParkerMc/BOE/master/B.o.E..png" width="200" height="200" />](https://github.com/ParkerMc/BOE)

<sup><sup>Icon by angelgal246.</sup></sup>

### Goals:

### Development:
Anyone is welcome to contribute to the project. You can check the projects page to see what is not currently being done.

Any commit must pass the following:
* [golint](https://github.com/golang/lint)
* [go vet](https://golang.org/cmd/vet/)
* [gofmt](https://golang.org/cmd/gofmt)
* [~~go test~~](https://golang.org/cmd/go/#hdr-Test_packages)- Not implemented yet
#### Setup:
After you clone the repository you need to clone the submodules with:
```bash
git submodule init
git submodule update
```
Then run `make setup`, which will automatically run `go get` for you to grab all of the dependencies.

#### Building:
To build to everything run `make build`.

#### Running:
To run the server in the development environment run `make run`.

#### Docker Database:
The make file includes a docker mongo database. If you already have a database hosted on your computer, you can use that instead.
To start the database run `start-database`.  
To stop it run `stop-database`.
