# py-cmc
Unofficial [CoinMarketCap](https://coinmarketcap.com/) API and Python wrapper. `py-cmc` uses `Selenium` and `BeautifulSoup` to scrape the website and return desired data.

[![mypy lint](https://github.com/Devansh3712/py-cmc/actions/workflows/lint.yml/badge.svg)](https://github.com/Devansh3712/py-cmc/actions/workflows/lint.yml) [![pytest](https://github.com/Devansh3712/py-cmc/actions/workflows/test.yml/badge.svg)](https://github.com/Devansh3712/py-cmc/actions/workflows/test.yml) [![codecov](https://github.com/Devansh3712/py-cmc/actions/workflows/codecov.yml/badge.svg)](https://github.com/Devansh3712/py-cmc/actions/workflows/codecov.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![codecov](https://codecov.io/gh/Devansh3712/py-cmc/branch/main/graph/badge.svg?token=HDZL3E43TR)](https://codecov.io/gh/Devansh3712/py-cmc)

### Installation

- Using `setup.py`
```shell
python setup.py install
```

- Using `Python Package Index`
```shell
pip install py-cmc
```

- Using `poetry`
```
poetry install
```

### Wrapper
`py-cmc` library can be used to fetch data for the following:
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
An API is also built using the `py-cmc` modules using `FastAPI` and `Redis`. Redis configurations can be set using the `config.yml` file, and it is used to cache the scraped data fetched through `py-cmc`.

```shell
uvicorn api.main:app
```
