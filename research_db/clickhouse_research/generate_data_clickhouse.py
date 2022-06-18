import random
import sys
import time
import uuid

from clickhouse_driver import Client


def generate_data(movies_count: int, users_count: int):
    client = Client(host="clickhouse")
    movies_ids = (str(uuid.uuid4()) for _ in range(movies_count))
    users_ids = [str(uuid.uuid4()) for _ in range(users_count)]

    print(f"Start inserting {movies_count * users_count} likes")
    start_time = time.time()
    for movie in movies_ids:
        likes = [(movie, user, random.randint(0, 10)) for user in users_ids]
        client.execute(
            """
            INSERT INTO movies.likes (movie_id, user_id, score) VALUES
            """,
            likes,
        )
    end_time = time.time() - start_time

    print(f"Insert {movies_count * users_count} likes in {round(end_time, 4)} seconds")


if __name__ == "__main__":
    generate_data(int(sys.argv[1]), int(sys.argv[2]))
