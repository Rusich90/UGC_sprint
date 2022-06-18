
first-up:
	make up-clickhouse
	sleep 10
	make create_db
	docker-compose up -d

up-clickhouse:
	docker-compose up -d clickhouse-node1

create_db: node-1 node-3

logs-etl:
	docker-compose -f docker-compose.yml logs -f etl

console-clickhouse:
	docker-compose -f docker-compose.yml exec clickhouse-node1 bash

node-1:
	docker-compose -f docker-compose.yml exec -T clickhouse-node1 clickhouse-client -q "CREATE DATABASE shard;"
	docker-compose -f docker-compose.yml exec -T clickhouse-node1 clickhouse-client -q "CREATE DATABASE replica;"
	docker-compose -f docker-compose.yml exec -T clickhouse-node1 clickhouse-client -q "CREATE TABLE shard.views (user_id UUID, movie_id UUID, time_frame Int64, event_time DateTime, event_type String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/views', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY movie_id;"
	docker-compose -f docker-compose.yml exec -T clickhouse-node1 clickhouse-client -q "CREATE TABLE replica.views (user_id UUID, movie_id UUID, time_frame Int64, event_time DateTime, event_type String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/views', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY movie_id;"
	docker-compose -f docker-compose.yml exec -T clickhouse-node1 clickhouse-client -q "CREATE TABLE default.views (user_id UUID, movie_id UUID, time_frame Int64, event_time DateTime, event_type String) ENGINE = Distributed('company_cluster', '', views, rand());"

node-3:
	docker-compose -f docker-compose.yml exec -T clickhouse-node3 clickhouse-client -q "CREATE DATABASE shard;"
	docker-compose -f docker-compose.yml exec -T clickhouse-node3 clickhouse-client -q "CREATE DATABASE replica;"
	docker-compose -f docker-compose.yml exec -T clickhouse-node3 clickhouse-client -q "CREATE TABLE shard.views (user_id UUID, movie_id UUID, time_frame Int64, event_time DateTime, event_type String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/views', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY movie_id;"
	docker-compose -f docker-compose.yml exec -T clickhouse-node3 clickhouse-client -q "CREATE TABLE replica.views (user_id UUID, movie_id UUID, time_frame Int64, event_time DateTime, event_type String) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/views', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY movie_id;"
	docker-compose -f docker-compose.yml exec -T clickhouse-node3 clickhouse-client -q "CREATE TABLE default.views (user_id UUID, movie_id UUID, time_frame Int64, event_time DateTime, event_type String) ENGINE = Distributed('company_cluster', '', views, rand());"
