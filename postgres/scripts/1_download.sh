#!/bin/bash

set -e

wget 'https://fastupload.io/en/zjiFkdWHJd0G/U6FCmA0nVROz6ok/2WVGrP2K93kx7/feeds.csv'\
     -O /var/lib/postgresql/data/feeds.csv
wget 'https://fastupload.io/en/xLkb1yhOztnm/nBW0wvNM5Ye8TO9/9AqGQLO50zMn6/processed_posts.csv'\
     -O /var/lib/postgresql/data/processed_posts.csv
wget 'https://fastupload.io/en/BeShxtXuE5oX/Iw5seju81zCfhOO/E9Qz9ROp2GOL2/users.csv'\
     -O /var/lib/postgresql/data/users.csv
wget 'https://fastupload.io/en/06uDfuICwhZ7/66TI0jpjo4IPle2/qw1zeOA20mXyn/posts.csv'\
     -O /var/lib/postgresql/data/posts.csv





