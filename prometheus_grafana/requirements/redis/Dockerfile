FROM redis:7.2.0

RUN mkdir /prometheus

COPY ./redis_exporter /prometheus/redis_exporter

RUN mkdir /etc/redis_conf

COPY ./redis_7.2.conf /etc/redis_conf/redis_7.2.conf
