import os
import numpy as np

from dotenv import load_dotenv


load_dotenv()

PG_USER = os.getenv('PG_USER')
PG_PASS = os.getenv('PG_PASS')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')

POSTS_COLUMNS = ['id', 'topic', 'total_tfidf', 'max_tfidf', 'mean_tfidf', 'text_cluster', 'dist_to_1st', 'dist_to_2st', 'dist_to_3st', 'dist_to_4st', 'dist_to_5st', 'dist_to_6st', 'dist_to_7st', 'dist_to_8st', 'dist_to_9st', 'dist_to_10st', 'dist_to_11st', 'dist_to_12st', 'dist_to_13st', 'dist_to_14st', 'dist_to_15st', 'dist_to_16st', 'dist_to_17st', 'dist_to_18st', 'dist_to_19st', 'dist_to_20st']
USERS_COLUMNS = ["id", "age", "city", "country", "exp_group", "gender", "os", "source"]

DISTINCT_USER_POST = ["user_id", "post_id"]

TRAIN_SET_FEATURES = ['gender', 'age', 'country', 'city', 'exp_group', 'os', 'source', 'topic', 'TotalTfIdf', 'MaxTfIdf', 'MeanTfIdf', 'TextCluster', 'DistanceTo1thCluster', 'DistanceTo2thCluster', 'DistanceTo3thCluster', 'DistanceTo4thCluster', 'DistanceTo5thCluster', 'DistanceTo6thCluster', 'DistanceTo7thCluster', 'DistanceTo8thCluster', 'DistanceTo9thCluster','DistanceTo10thCluster', 'DistanceTo11thCluster', 'DistanceTo12thCluster', 'DistanceTo13thCluster', 'DistanceTo14thCluster', 'DistanceTo15thCluster', 'DistanceTo16thCluster', 'DistanceTo17thCluster', 'DistanceTo18thCluster', 'DistanceTo19thCluster', 'DistanceTo20thCluster', 'hour', 'month']

TRAIN_SET_TYPES = { 'gender': 'int64', 'age': 'int64', 'country': 'O', 'city': 'O', 'exp_group': 'int64', 'os': 'O', 'source': 'O', 'topic': 'O', 'TotalTfIdf': 'float64', 'MaxTfIdf': 'float64', 'MeanTfIdf': 'float64', 'TextCluster': 'int32', 'DistanceTo1thCluster': 'float64', 'DistanceTo2thCluster': 'float64', 'DistanceTo3thCluster': 'float64', 'DistanceTo4thCluster': 'float64', 'DistanceTo5thCluster': 'float64', 'DistanceTo6thCluster': 'float64', 'DistanceTo7thCluster': 'float64', 'DistanceTo8thCluster': 'float64', 'DistanceTo9thCluster': 'float64', 'DistanceTo10thCluster': 'float64', 'DistanceTo11thCluster': 'float64', 'DistanceTo12thCluster': 'float64', 'DistanceTo13thCluster': 'float64', 'DistanceTo14thCluster': 'float64', 'DistanceTo15thCluster': 'float64', 'DistanceTo16thCluster': 'float64', 'DistanceTo17thCluster': 'float64', 'DistanceTo18thCluster': 'float64', 'DistanceTo19thCluster': 'float64', 'DistanceTo20thCluster': 'float64', 'hour': 'int64', 'month': 'int64'}