# FINANCE APP

## REQUIREMENTS
### 1. Docker
- Install docker
- Run this command in folder contains 'docker-compose.yml':
```shell
docker-compose up -d
```
### 2. Restore mongodb data
- Download dump data: [link](https://drive.google.com/file/d/1HwC0rEE3RXPnjt82Y6QCT4skFeSglkGs/view?usp=sharing)
- Remove folder admin after extract
- Copy folder dump to docker container
```shell
docker cp ./dump mongo_db:/data/
```
- Connect to container in powershell
```shell
docker exec -it mongo_db bash
```
- Restore data:
```shell
cd /data

mongorestore --username admin --password admin --authenticationDatabase admin
```

### 3. Install python environment
```shell
python -m venv .venv

.venv/Scripts/activate

pip install -r requirements.txt
```

## Start app
Run:
```shell
streamlit run app.py
```