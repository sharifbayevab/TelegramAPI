# Telegram Pyrogram Session Project

## Overview
This project uses Pyrogram for interacting with the Telegram API. It includes creating a session, processing messages, Docker configuration for deployment, and managing Python dependencies.

## Structure
- `create_pyrogram_session.py`: Creates a Pyrogram session and retrieves the Telegram ID.
- `main.py`: Main script for processing messages and managing scheduled tasks.
- `Dockerfile` & `docker-compose.yml`: Configuration for Docker container setup.
- `requirements.txt`: List of Python dependencies.

## Installation & Setup
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
2. Create file `.env` and write there your `API_ID` and `API_HASH`
   ```bash
   API_ID=your_api_id
   API_HASH=your_api_hash
3. Run script to set up the Pyrogram session: 
    ```bash
    python create_pyrogram_session.py 
4. Use Docker commands to build and run the container:
   ```bash
   docker-compose up --build
   ```

   !!! In case of problems with PostgreSQL, especially if the database 
   initialization is not completed properly or connection problems occur.
      ```bash
   docker-compose down
   docker-compose up -d
   ```