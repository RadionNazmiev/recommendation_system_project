import os

from dotenv import load_dotenv


load_dotenv()

PG_USER = os.getenv('PG_USER')
PG_PASS = os.getenv('PG_PASS')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')
COLUMNS = ['gender', 'age', 'country', 'city', 'exp_group', 'os', 'source', 'topic', 'TotalTfIdf', 'MaxTfIdf', 'MeanTfIdf', 'TextCluster', 'DistanceTo1thCluster', 'DistanceTo2thCluster', 'DistanceTo3thCluster', 'DistanceTo4thCluster', 'DistanceTo5thCluster', 'DistanceTo6thCluster', 'DistanceTo7thCluster', 'DistanceTo8thCluster', 'DistanceTo9thCluster', 'DistanceTo10thCluster', 'DistanceTo11thCluster', 'DistanceTo12thCluster', 'DistanceTo13thCluster', 'DistanceTo14thCluster', 'DistanceTo15thCluster', 'DistanceTo16thCluster', 'DistanceTo17thCluster', 'DistanceTo18thCluster', 'DistanceTo19thCluster', 'DistanceTo20thCluster', 'hour', 'month', 'target']