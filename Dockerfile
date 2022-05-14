FROM python:3.7-alpine

ARG APP_DIR='/message_gateway'
ENV APP_DIR ${APP_DIR}

WORKDIR ${APP_DIR}

ADD ./src $APP_DIR

RUN set -ex;pip3 install --upgrade -r $APP_DIR/requirements.txt --no-cache-dir

CMD ${APP_DIR}/startup.sh

RUN  chmod +x $APP_DIR/startup.sh

EXPOSE 80
