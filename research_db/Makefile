generate-mongo-data:
	docker-compose exec -T app python mongo_research/generate_data_mongo.py 1000 10000

query-mongo-data:
	docker-compose exec -T app python mongo_research/query_mongo.py

create-db-clickhouse:
	docker-compose exec -T clickhouse clickhouse-client -q "CREATE DATABASE movies;"
	docker-compose exec -T clickhouse clickhouse-client -q "CREATE TABLE movies.likes (movie_id UUID, user_id UUID, score Int8) Engine=MergeTree() ORDER BY (movie_id);"

generate-clickhouse-data:
	docker-compose exec -T app python clickhouse_research/generate_data_clickhouse.py 1000 10000

query-clickhouse-data:
	docker-compose exec -T app python clickhouse_research/query_clickhouse.py

first-up:
	docker-compose up -d
	sleep 5
	make generate-mongo-data
	make create-db-clickhouse
	make generate-clickhouse-data

insert-clickhouse-data:
	docker-compose exec -T app python clickhouse_research/generate_data_clickhouse.py 100 1000

insert-mongo-data:
	docker-compose exec -T app python mongo_research/generate_data_mongo.py 100 1000
