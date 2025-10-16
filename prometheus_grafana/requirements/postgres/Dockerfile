FROM quay.io/prometheuscommunity/postgres-exporter as postgres-exporter

FROM postgres:14.12-alpine3.20

RUN mkdir /prometheus

COPY --from=postgres-exporter /bin/postgres_exporter /prometheus/postgres_exporter
