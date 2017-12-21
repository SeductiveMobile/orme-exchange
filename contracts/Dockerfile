FROM node:8.0.0-alpine

RUN apk add -t .gyp --no-cache git python g++ make \
    && npm install -g truffle \
    && apk del .gyp

RUN mkdir -p /dapp
WORKDIR /dapp

# Add current codebase to container
COPY . .

#RUN truffle init
#RUN npm init
#RUN npm install zeppelin-solidity
RUN truffle install zeppelin

EXPOSE 8080
#ENTRYPOINT ["sh"]
ENTRYPOINT ["/bin/sh", "truffle.sh"]