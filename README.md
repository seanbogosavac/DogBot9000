# DogBot9000

Doggo-spamming bot for the homies


## Launching project (Linux) :

Create the .env file and fill the information with these commands :
```bash
cp .env.example .env
nano .env
```

Launch container with :
```bash
docker build -t dogbot9000 .
docker run -d --env-file .env dogbot9000
```
