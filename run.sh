docker stop app

docker build -t app .

docker run --rm -v ./:/app -p 8000:8000 --env-file .env --name app app 