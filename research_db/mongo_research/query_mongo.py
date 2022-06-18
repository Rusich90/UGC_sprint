import time

import pymongo


def mongo_query():
    client = pymongo.MongoClient("mongodb", 27017)
    db = client.movie_db
    likes_collection = db.movie_likes

    movie_ids = [item["movie_id"] for item in likes_collection.find().limit(100)]

    print("---" * 20)
    print(f"Start read likes average score for 100 movies")
    time_avg = check_query_time(movie_ids, likes_collection, 'avg')
    print(f" Average time for read 1 movie average score {round(time_avg, 4)} second")
    print("---" * 20)

    print(f"Start read likes and dislikes count for 100 movies")
    time_avg = check_query_time(movie_ids, likes_collection)
    print(f"Average time for read 1 movie likes and dislikes count {round(time_avg, 4)} second")
    print("---" * 20)


def check_query_time(movie_ids, likes_collection, query=None):
    all_times = []
    for movie in movie_ids:
        if query == 'avg':
            query = make_avg_score_query(movie)
        else:
            query = make_likes_dislikes_query(movie)
        start_time = time.time()
        results = likes_collection.aggregate(query)
        for result in results:
            end_time = time.time() - start_time
            all_times.append(end_time)

    time_avg = sum(all_times) / len(all_times)
    return time_avg


def make_avg_score_query(movie):
    query = [
        {"$unwind": "$likes"},
        {"$match": {"movie_id": movie}},
        {"$group": {"_id": "$movie_id", "Avg grade": {"$avg": "$likes.score"}}},
    ]
    return query


def make_likes_dislikes_query(movie):
    query = [
        {
            "$match": {"movie_id": movie}
        },
        {
            "$addFields": {
                "likes": {"$size": {"$filter": {"input": "$likes", "cond": {"$gte": ["$$this.score", 10]}}}},
                "dislikes": {"$size": {"$filter": {"input": "$likes", "cond": {"$lte": ["$$this.score", 0]}}}},
            }
        },
    ]
    return query


if __name__ == "__main__":
    mongo_query()
