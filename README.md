# DogBot9000

Doggo-spamming bot for the homies

```
Once pulled, the pictures have to be placed inside a pic/ folder at the root of the project
```

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
