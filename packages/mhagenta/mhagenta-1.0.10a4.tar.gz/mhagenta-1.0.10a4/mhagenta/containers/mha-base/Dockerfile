ARG SRC_IMAGE="mha-rabbitmq"
ARG SRC_VERSION="latest"
ARG PRE_VERSION="false"
FROM ${SRC_IMAGE}:${SRC_VERSION}
LABEL authors="Dmitry Gnatyshak"

RUN if [ "$PRE_VERSION" = "true" ] ; then pip install --pre mhagenta ; else pip install mhagenta ; fi
