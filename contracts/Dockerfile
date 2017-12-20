FROM node:8.0.0-alpine

RUN apk add -t .gyp --no-cache git python g++ make \
    && npm install -g truffle zeppelin-solidity \
    && apk del .gyp

RUN mkdir -p /dapp
WORKDIR /dapp

RUN truffle install zeppelin

EXPOSE 8080
#ENTRYPOINT ["sh"]
ENTRYPOINT ["truffle"]