# SOCIAL NETWORK (test task)

Project Overview: 
    Simple RESTful API using FastAPI for a social networking application.
    
Features:
- JWT-based registration
    - User authentication and registration
    - Create, update, view, and delete records
    - Like and dislike records (excluding own records)
    - API documentation (Swagger/Redoc)
    - (Bonus) Email existence check during registration

Tech Stack:
    - FastAPI 0.95
    - FastAPI Users
    - PostgreSQL
    - SQLAlchemy


# How to run

Before running, make sure you have Docker and Docker Compose installed.


## Step 1

Create a project folder and execute the following command:

```
git clone https://github.com/Nikolrusik/social-network.git /yourfolder
```

## Step 2 (Optional)

Navigate to the project folder and edit the variables in the .env file according to your needs or leave them as they are.

(The .env file is provided for easy testing purposes)


## Step 3

Let Docker do the work for you! Execute the following commands:

```
docker-compose build
docker-compose up
```

## Step 4

Go to http://127.0.0.1:8000/docs to view the API documentation!

**Done!**
