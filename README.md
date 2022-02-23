# cmc-py
Unofficial [CoinMarketCap](https://coinmarketcap.com/) API and Python wrapper. `cmc-py` uses `Selenium` and `BeautifulSoup` to scrape the website and return desired data.

[![mypy lint](https://github.com/Devansh3712/cmc-py/actions/workflows/lint.yml/badge.svg)](https://github.com/Devansh3712/cmc-py/actions/workflows/lint.yml) [![pytest](https://github.com/Devansh3712/cmc-py/actions/workflows/test.yml/badge.svg)](https://github.com/Devansh3712/cmc-py/actions/workflows/test.yml) [![codecov](https://github.com/Devansh3712/cmc-py/actions/workflows/codecov-coverage.yml/badge.svg)](https://github.com/Devansh3712/cmc-py/actions/workflows/codecov-coverage.yml) [![PyPI](https://github.com/Devansh3712/cmc-py/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Devansh3712/cmc-py/actions/workflows/python-publish.yml) [![pages-build-deployment](https://github.com/Devansh3712/cmc-py/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/Devansh3712/cmc-py/actions/workflows/pages/pages-build-deployment) [![Docker Image CI](https://github.com/Devansh3712/cmc-py/actions/workflows/docker-image.yml/badge.svg)](https://github.com/Devansh3712/cmc-py/actions/workflows/docker-image.yml) [![Docker Build and Push Image](https://github.com/Devansh3712/cmc-py/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/Devansh3712/cmc-py/actions/workflows/docker-publish.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![codecov](https://codecov.io/gh/Devansh3712/cmc-py/branch/main/graph/badge.svg?token=HDZL3E43TR)](https://codecov.io/gh/Devansh3712/cmc-py)

### Installation

- Using `setup.py`
```shell
python setup.py install
```

- Using `Python Package Index`
```shell
pip install cmc-py-wrapper
```

- Using `poetry`
```
poetry install
```

### Wrapper
`cmc-py` library can be used to fetch data for the following:
- `CryptoCurrencies`
```python
from cmc import Trending, format_data

top_30_trending = Trending().get_data
print(format_data(top_30_trending))
```

- `Exchanges`
```python
from cmc import Spot, format_data

spot_exchanges = Spot().get_data
print(format_data(spot_exchanges))
```

- `Non Fungible Tokens (NFTs)`
```python
from cmc import UpcomingSale, format_data

upcoming_nft_sales = UpcomingSale(pages=[1, 2]).get_data
print(format_data(upcoming_nft_sales))
```

### API
An API is also built using the `cmc-py` modules using `FastAPI` and `Redis`. Redis configurations can be set using the `config.yml` file, and it is used to cache the scraped data fetched through `cmc-py`. `Redis` server should be running in the background in order to cache API calls. An instance of the API is hosted on [Heroku](https://cmc-api.herokuapp.com/docs#/).

- Running the API locally
```shell
uvicorn api.main:app
```

- Building the API using `Dockerfile`
```shell
docker build -t cmc .
docker compose up -d
```

- Running the API using [`Docker Image`](https://hub.docker.com/r/devansh3712/cmc-api)
```shell
docker pull devansh3712/cmc-api
docker run devansh3712/cmc-api
```
