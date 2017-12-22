FROM node:8-alpine

RUN apk add -t .gyp --no-cache git python g++ make \
    && npm install -g truffle \
    && apk del .gyp

RUN mkdir -p /dapp
WORKDIR /dapp

# Add current codebase to container
COPY . .

#RUN truffle init
#RUN npm install zeppelin-solidity
RUN apk update && apk upgrade \
    && apk add --no-cache g++ ca-certificates python python-dev py-pip \
    && pip install web3

EXPOSE 8080
#ENTRYPOINT ["sh"]
#ENTRYPOINT ["/bin/sh"]
CMD /bin/sh truffle.sh