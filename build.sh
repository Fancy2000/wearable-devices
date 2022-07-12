#!/bin/bash
docker pull clickhouse/clickhouse-server
docker run -d --name some-clickhouse-server -p 8123:8123 --ulimit nofile=262144:262144 clickhouse/clickhouse-server