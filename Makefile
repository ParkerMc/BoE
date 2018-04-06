.PHONY: help run build clean setup start-database

help: ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

start-database: ## Start the database
	@echo Starting the database container

	@if [ $(shell docker ps -a | grep -ci boe-mongo) -eq 0 ]; then \
		docker run --name boe-mongo -p 27017:27017 -d mongo --storageEngine wiredTiger > /dev/null; \
	elif [ $(shell docker ps | grep -ci boe-mongo) -eq 0 ]; then \
		docker start boe-mongo > /dev/null; \
	fi

stop-database: ## Stop the database
	@echo Stoping the database container

	@if [ $(shell docker ps -a | grep -ci boe-mongo) -eq 1 ]; then \
		docker stop boe-mongo > /dev/null; \
	fi

run: ## Run BoE
run: build
	@echo Running BoE

	mkdir -p run/ss
	rm -rf run/client
	rm -rf run/bin
	cp -r build/* run/

	cd run/; ENV=DEV ./bin/boe


build: ## Build BoE
build: setup
	@echo Building BoE

	cd boe-web && $(MAKE) build
	rm -rf build
	mkdir -p build/client/
	mkdir -p build/bin/
	go build -o build/bin/boe main.go

	cp -r boe-web/build/* build/client/

setup: ## Setup the project
	@echo Setting up the project

	go get ./...

clean: ## Clean up the build files and web app
clean: stop-database
	@echo Cleaning

	cd boe-web && $(MAKE) clean
	rm -rf build
	rm -rf run

	@if [ $(shell docker ps -a | grep -ci boe-mongo) -eq 1 ]; then \
		docker rm -v boe-mongo > /dev/null; \
	fi
