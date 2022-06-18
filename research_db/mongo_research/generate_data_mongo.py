import random
import sys
import time
import uuid

import pymongo


def generate_data(movies_count: int, users_count: int):
    client = pymongo.MongoClient("mongodb", 27017)
    db = client.movie_db
    likes = db.movie_likes
    movies_ids = (str(uuid.uuid4()) for _ in range(movies_count))
    users_ids = [str(uuid.uuid4()) for _ in range(users_count)]

    print(f"Start inserting {movies_count * users_count} likes")
    start_time = time.time()
    for movie in movies_ids:
        likes.insert_one(
            {"movie_id": movie, "likes": [{"user_id": user, "score": random.randint(0, 10)} for user in users_ids]}
        )
    end_time = time.time() - start_time

    print(f"Insert {movies_count * users_count} likes in {round(end_time, 4)} seconds")


if __name__ == "__main__":
    generate_data(int(sys.argv[1]), int(sys.argv[2]))
