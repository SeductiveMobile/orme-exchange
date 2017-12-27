# README

To install dependencies run in terminal:
$ truffle install zeppelin

To run tests run in terminal:
$ truffle test

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

## Mining

You need gas for running contracts operations. Gas is not free, you should have Ethereum in the wallet to use gas.
In order to get ethereum you should enable mining. At first you need to connect to Ethereum console:
`docker exec -it ormeexchange_eth_1 geth attach ipc://root/.ethereum/devchain/geth.ipc`

Inside console you should run `miner.start(1)` to start mining using a single thread of your CPU.
You could check current mining status on http://localhost:3000
Mining takes lot of CPU resources, so once you have enough ethereum/gas you can turn it off by typing `miner.stop()` in Ethereum console.

## Application login via JSON Web Tokens

1. Get authentication token by POSTing into http://localhost:8000/auth a JSON with 'email' and 'password' fields.
2. You should get a JSON with access_token variable.
3. For each protected resource you shuld provide "Authorization" header of 'Bearer <access_token>' format.