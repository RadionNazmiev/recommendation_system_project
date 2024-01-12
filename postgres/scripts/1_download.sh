#!/bin/bash

set -e

wget 'https://fastupload.io/en/K8uOy3PV5XOq/7uTVuhDZpgTmXPo/qPez49g2YGOYn/feeds.csv'\
     -O /var/lib/postgresql/data/feeds.csv
wget 'https://fastupload.io/en/L9RZe3N8SVcG/wBBLzq7p84exlLT/1RgzRg77oGbpB/processed_posts.csv'\
     -O /var/lib/postgresql/data/processed_posts.csv
wget 'https://fastupload.io/en/WgvxrZr5K3Us/i4RFGMXRNDmVxcN/l76mZbwwnmanY/users.csv'\
     -O /var/lib/postgresql/data/users.csv
wget 'https://fastupload.io/en/gGoaOEVuttMH/WYvYJlJst9V0T6S/9QWmp811kmEB6/posts.csv'\
     -O /var/lib/postgresql/data/posts.csv





