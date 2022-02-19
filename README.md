# cmc-py
Unofficial [CoinMarketCap](https://coinmarketcap.com/) API and Python wrapper. `cmc-py` uses `Selenium` and `BeautifulSoup` to scrape the website and return desired data.

[![mypy lint](https://github.com/Devansh3712/cmc-py/actions/workflows/lint.yml/badge.svg)](https://github.com/Devansh3712/cmc-py/actions/workflows/lint.yml) [![pytest](https://github.com/Devansh3712/cmc-py/actions/workflows/test.yml/badge.svg)](https://github.com/Devansh3712/cmc-py/actions/workflows/test.yml) [![codecov](https://github.com/Devansh3712/cmc-py/actions/workflows/codecov.yml/badge.svg)](https://github.com/Devansh3712/cmc-py/actions/workflows/codecov.yml) [![PyPI](https://github.com/Devansh3712/cmc-py/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Devansh3712/cmc-py/actions/workflows/python-publish.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![codecov](https://codecov.io/gh/Devansh3712/cmc-py/branch/main/graph/badge.svg?token=HDZL3E43TR)](https://codecov.io/gh/Devansh3712/cmc-py)

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
import json
from cmc import Trending

top_30_trending = Trending().get_data
print(json.dumps(top_30_trending, indent=4, default=str))
```

- `Exchanges`
```python
import json
from cmc import Spot

spot_exchanges = Spot().get_data
print(json.dumps(spot_exchanges, indent=4, default=str))
```

- `Non Fungible Tokens (NFTs)`
```python
import json
from cmc import UpcomingSale

upcoming_nft_sales = UpcomingSale(pages=[1, 2]).get_data
print(json.dumps(upcoming_nft_sales, indent=4, default=str))
```

### API
An API is also built using the `cmc-py` modules using `FastAPI` and `Redis`. Redis configurations can be set using the `config.yml` file, and it is used to cache the scraped data fetched through `cmc-py`.

```shell
uvicorn api.main:app
```
