# sendCVnow
AI bot that automatically sends CV to job posting pages

## Installation

If your database is not on the cloud, you can create one locally using docker:

`docker run -p 5416:5432 --name fastAPIDBName -e POSTGRES_PASSWORD='123456' -d postgres:15`

Then start it with:

`sudo docker start fastAPIDBName`

Create a virtual environment:

`python3 -m venv ./venv`

Activate the environment:

`source ./venv/bin/activate`

Now install the pip packages:

`python3 -m pip install -r requirements.txt`



## Usage

Start the service:

`uvicorn main:app --reload`

### /create-user

Creates user on database

`curl --location 'http://127.0.0.1:8000/create_user' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "myemail@myemail2.com", 
    "username": "userExample", 
    "password": "123456789",
    "confirm_password": "123456789"

}'`

### /login-token

Generates token for user

`curl --location 'http://127.0.0.1:8000/token' \
--header 'Content-Type: application/json' \
--data '{
    "username": "userExample", 
    "password": "123456789",
    "grant_type": "password"
}'`


