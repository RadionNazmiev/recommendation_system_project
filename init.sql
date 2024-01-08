-- database="startml",
-- user="robot-startml-ro",\
-- password="pheiph0hahj1Vaif",
-- host="postgres.lab.karpov.courses",
-- port=6432

-- import pandas as pd

-- df = pd.read_sql(
--     """SELECT * FROM "feed_action" LIMIT 10 """,
--     con="postgresql://robot-startml-ro:pheiph0hahj1Vaif@"
--         "postgres.lab.karpov.courses:6432/startml"
-- )

-- df.head()

-- Creation of users table
CREATE TABLE IF NOT EXISTS users (
  id INT NOT NULL,
  gender SMALLINT NOT NULL,
  age SMALLINT NOT NULL,
  country VARCHAR(25) NOT NULL,
  city VARCHAR(30) NOT NULL,
  exp_group SMALLINT NOT NULL,
  os VARCHAR(15),
  source VARCHAR(15),
  PRIMARY KEY (id)
);

-- Creation of posts table
CREATE TABLE IF NOT EXISTS posts (
  id SMALLINT NOT NULL,
  text TEXT NOT NULL,
  topic VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
);

-- Creation of feeds table
CREATE TABLE IF NOT EXISTS feeds (
  user_id INT NOT NULL,
  post_id SMALLINT NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  action VARCHAR(15),
  target SMALLINT,
  CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id),
  CONSTRAINT fk_post FOREIGN KEY (post_id) REFERENCES posts (id)
);


SET SESSION sql_mode='';

COPY users FROM '/init_data/user_data.parquet';
COPY posts FROM '/init_data/post_text_df.parquet';
COPY feeds FROM '/init_data/feed_data.parquet';