SET search_path TO public;

-- Creation of users table
CREATE TABLE IF NOT EXISTS public.users (
  id INT NOT NULL,
  gender SMALLINT NOT NULL,
  age SMALLINT NOT NULL,
  country VARCHAR(25) NOT NULL,
  city VARCHAR(30) NOT NULL,
  exp_group SMALLINT NOT NULL,
  os VARCHAR(15),
  source VARCHAR(15)
);

-- Creation of posts table
CREATE TABLE IF NOT EXISTS public.posts (
  id SMALLINT NOT NULL,
  text TEXT NOT NULL,
  topic VARCHAR(50) NOT NULL
);

-- Creation of feeds table
CREATE TABLE IF NOT EXISTS public.feeds (
  timestamp TIMESTAMP NOT NULL,
  user_id INT NOT NULL,
  post_id SMALLINT NOT NULL,
  action VARCHAR(15),
  target SMALLINT
);

-- Creation of processed_posts table
CREATE TABLE IF NOT EXISTS public.processed_posts (
  id SMALLINT NOT NULL,
  text TEXT,
  topic VARCHAR(50),
  total_tfidf FLOAT,
  max_tfidf FLOAT,
  mean_tfidf FLOAT,
  text_cluster INTEGER,
  dist_to_1st FLOAT,
  dist_to_2st FLOAT,
  dist_to_3st FLOAT,
  dist_to_4st FLOAT,
  dist_to_5st FLOAT,
  dist_to_6st FLOAT,
  dist_to_7st FLOAT,
  dist_to_8st FLOAT,
  dist_to_9st FLOAT,
  dist_to_10st FLOAT,
  dist_to_11st FLOAT,
  dist_to_12st FLOAT,
  dist_to_13st FLOAT,
  dist_to_14st FLOAT,
  dist_to_15st FLOAT,
  dist_to_16st FLOAT,
  dist_to_17st FLOAT,
  dist_to_18st FLOAT,
  dist_to_19st FLOAT,
  dist_to_20st FLOAT
);


COPY public.users FROM '/init_data/users.csv' WITH (FORMAT CSV, HEADER);
COPY public.posts FROM '/init_data/posts.csv' WITH (FORMAT CSV, HEADER);
COPY public.processed_posts FROM '/init_data/processed_posts.csv'
WITH (FORMAT CSV, HEADER); 
COPY public.feeds FROM '/init_data/feeds.csv' WITH (FORMAT CSV, HEADER);

