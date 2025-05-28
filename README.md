# Image Moderation
An Image Moderation API made in FastAPI and basic HTML/CSS/JS

### Setup
- Docker should be installed to run the code in this repository
- Clone this repo using command
```sh
git clone https://github.com/salehairum/Image-Moderation.git
```

### Build
In root folder, run the following command to build images:
```sh
docker compose build --no-cache
```
By default,
- the frontend runs on port 3000
- the backend runs on port 7000
- mongodb runs on port 27017

To change the db port, go to .env file and modify it there.

To change the frontend or backend port, go to:

compose.yml->service name->ports->change the first port to desired port

Change that port in .env file within the urls.
### Run
The following command runs compose.yml:
```sh
docker compose up -d
```
to stop:
```sh
docker compose down
```
Visit localhost:7000 (or whatever port you have set) and the app will be running there!
