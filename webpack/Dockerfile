FROM node:11-alpine

ENV HOME /home/
ENV APP $HOME/webpack-node

WORKDIR $APP

# Copy all the required files
COPY ./webpack-node $APP

RUN cd $APP && npm install

CMD npm run dev

