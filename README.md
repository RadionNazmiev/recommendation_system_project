# FastAPI Recommendation Service

This project implements a recommendation service using FastAPI and PostgreSQL. Docker Containers are added for ruture scalability. The service provides recommendations for posts based on user behavior such as likes and dislikes.

## Features

- **Recommendation System**: Utilizes a CatBoostClassifier model to predict user preferences and recommend posts accordingly.
- **Database Integration**: Integrates with a PostgreSQL database using SQLAlchemy for data storage and retrieval.
- **Asynchronous Support**: Leverages asynchronous programming to handle concurrent requests efficiently.
- **Chunked Data Retrieval**: Retrieves large datasets from the database in chunks to optimize performance.
- **Parquet File Handling**: Loads data from Parquet files if available, else loads from the database.
- **Logging**: Implements logging using the Loguru library for detailed runtime information.
- **Docker Containerization**: Utilizes Docker for containerizing the PostgreSQL database and FastAPI service for easy deployment and scaling.
- **Configurable**: Configuration settings are loaded from a YAML file for easy customization.


## Installation

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/RadionNazmiev/recommendation_system_project.git
    ```

2. Set up the database environment variables in the `.env` file:

    ```dotenv
    PG_HOST=postgres_db
    PG_PORT=5432
    PG_DB=your_database_name
    PG_USER=your_database_user
    PG_PASS=your_database_password
    API_PORT=8000
    ```

3. Build and run the Docker containers using Docker Compose:

    ```bash
    docker-compose up --build
    ```

4. Access the FastAPI service at `http://localhost:8000`.

## Usage

- **GET `/post/recommendations`**: Get recommended posts for a user at a specific time.
- **GET `/posts/{post_id}`**: Get details of a specific post by ID.
- **GET `/posts`**: Get a list of posts with optional limit parameter.
- **GET `/users/{user_id}`**: Get details of a specific user by ID.
- **GET `/users`**: Get a list of users with optional limit parameter.
- **GET `/feed`**: Get the feed, optionally filtered by user_id or post_id with a limit.

## Contributing

Contributions are welcome! Please check the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
