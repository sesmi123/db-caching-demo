# db-caching-demo
A simple demo of different database caching strategies using Angular, Flask and Redis


## Local Setup

1. Redis cache

    Install and setup redis with data persistence enabled.

    Follow [installation guide](https://redis.io/docs/install/install-redis/)

    OR

    Use docker: 
    ```sh
    mkdir redis-data
    docker run -d --name my-redis -p 6379:6379 -v $(pwd)/redis-data:/data redis:latest --appendonly yes
    ```

    OR 

    Use free redis database in the cloud. Create a [free account](https://redis.com/try-free/).

    Optionally, install Redis Insight.

2. Create a virtual environment and install dependencies.

    ```sh
    python -m venv .venv
    . venv/bin/activate
    pip install -r requirements.txt
    ```

3. Start the application.

    ```sh
    python main.py
    ```


