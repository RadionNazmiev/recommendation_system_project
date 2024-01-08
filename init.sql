CREATE SCHEMA IF NOT EXISTS recsys;


-- Creation of users table
CREATE TABLE IF NOT EXISTS recsys.users (
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
CREATE TABLE IF NOT EXISTS recsys.posts (
  id SMALLINT NOT NULL,
  text TEXT NOT NULL,
  topic VARCHAR(50) NOT NULL
);

-- Creation of feeds table
CREATE TABLE IF NOT EXISTS recsys.feeds (
  user_id INT NOT NULL,
  post_id SMALLINT NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  action VARCHAR(15),
  target SMALLINT
);


-- SET SESSION sql_mode='';

-- COPY users FROM '/init_data/user_data.parquet';
-- COPY posts FROM '/init_data/post_text_df.parquet';
-- COPY feeds FROM '/init_data/feed_data.parquet';