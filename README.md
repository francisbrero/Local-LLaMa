# FAQ_bot
Create an FAQ bot that can be used in Slack and is trained on public + private data


# Setup
## Virtual Environment
### Start virtual environment
```bash
python3 -m venv env
source env/bin/activate
```
### install requirements
```bash
pip install -r requirements.txt --upgrade
```
### Deactivate virtual environment
```bash
deactivate
```
## Configure environment variables
There is a `.env_sample` file. Rename it to `.env` and fill in the values.

## VectorDB
We'll run ChromaDB locally using Docker.
### Install Docker
Follow the instructions [here](https://docs.docker.com/get-docker/).

```bash
brew install docker-compose
```

### Install chroma
Follow the instructions [here](https://docs.trychroma.com/deployment).
```bash
git clone git@github.com:chroma-core/chroma.git
```

### Run chroma
Start docker
```bash
cd chroma
docker-compose up -d --build
```
You will likely run into an error which requires updating your docker config
```bash
nano ~/.docker/config.json
```
Remove the following line to the file and run the docker-compose command again
```json
"credSstore": "desktop"
```

### Run chroma
Start docker, then go to the chroma folder and run
```bash
docker-compose up -d --build
```
### Test chroma
The DB server is exposed to port 8000 on the host machine and we should be able to access it from the host machine at localhost:8000 . We can hit the heartbeat URL http://localhost:8000/api/v1/heartbeat to make sure the server is up and running.
If you see a JSON with a nanosecond EPOC timestamp, you're all set!

## LLM
### Install LLM
We will run llama2 locally.
Original instructions from [this article](https://medium.com/@auslei/llama-2-for-mac-m1-ed67bbd9a0c2)

Just in case, updated instructions for an M2 are also [here](./docs/install_llama.md). There's quite a bit that no longer works in their documentation.

### Test LLM
```bash
../../llama.cpp/main -m ../../llama/llama-2-7b-chat/ggml-model-f16_q4_0.gguf \
        -t 8 \
        -n 128 \
        -p 'The first man on the moon was '
```

# Run
## Get all the conent from zendesk using their API
```bash
python ./lib/get_zendesk_content.py
```

## Train the model


## Create the bot
```bash
python ./lib/main.py
```

