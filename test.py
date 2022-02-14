import json
import time
from cmc import Ranking, CryptoCurrency, TopGainers, TopLosers, Trending

print(json.dumps(Ranking().get_data, indent=4))
