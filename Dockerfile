FROM node:lts-stretch-slim

WORKDIR /usr/

COPY package*.json ./

RUN npm install

COPY . .

ENV INSTANCE_URL joinmastodon.org
ENV ACCESS_TOKEN eX4mPl37t0k3nfr0my0uRb07

CMD ["node", "./src/app.js"]