ARG ELK_VERSION

FROM docker.elastic.co/logstash/logstash:${ELK_VERSION}
RUN logstash-plugin install logstash-integration-rabbitmq
RUN logstash-plugin install logstash-filter-json
RUN logstash-plugin install logstash-filter-json_encode
