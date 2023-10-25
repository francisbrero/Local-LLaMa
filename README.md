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
pip install -r requirements.txt
```
### Deactivate virtual environment
```bash
deactivate
```
### Configure environment variables
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

Just in case, updated instructions are also [here](./docs/install_llama.md). There's quite a bit that no longer works in their documentation.

### Test LLM
```bash
llm -m l2c 'Tell me a joke about a Kudu'
```

# Run
## Create scraper
```bash
python -m scrapy startproject crawler
```
This will create a folder `crawler`

## Copy the scraper into our server
```bash
cd crawler
cp ../lib/scrape_help_center.py ./crawler/spiders/crawler.py
```

## Update the settings.py with 
```
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
```
## Test
```bash
scrapy crawl website -o ../data/scraped_urls_website.json
# scrapy crawl help_center -o ../data/scraped_urls_support.json
```

## Scraping data
### Start with getting the urls by scraping the help center
```bash
scrapy crawl website -o ../data/scraped_urls_website.json
```

### Then, get the data from Notion

## Train the model


## Create the bot
```bash
python ./lib/main.py
```

