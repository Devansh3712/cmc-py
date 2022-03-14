#!/usr/bin/env python

"""GraphQL Router for cryptocurrency module methods of cmc-py."""

import strawberry
from strawberry.fastapi import GraphQLRouter

from api.graphql.schemas import (
    CryptoCurrencyData,
    MostVisitedData,
    TopGainersData,
    TopLosersData,
    TrendingData,
    PricePredictionData,
    RankingData,
    RecentlyAddedData,
)
from api.utils.database import Database
from cmc import (
    CryptoCurrency,
    MostVisited,
    PricePrediction,
    Ranking,
    RecentlyAdded,
    TopGainers,
    TopLosers,
    Trending,
    InvalidCryptoCurrencyURL,
    InvalidPageURL,
)

redis = Database()


@strawberry.type
class Query:
    @strawberry.field
    async def cryptocurrency(self, name: str) -> CryptoCurrencyData:
        if redis.check_data(name):
            db_result = redis.get_data(name)
            return CryptoCurrencyData(**db_result)
        result = CryptoCurrency(name, as_dict=True).get_data
        redis.add_data(name, result)  # type: ignore
        return CryptoCurrencyData(**result)


schema = strawberry.Schema(query=Query)
cryptocurrency_router = GraphQLRouter(schema)
