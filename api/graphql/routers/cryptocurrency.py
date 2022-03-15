#!/usr/bin/env python

"""GraphQL Router for cryptocurrency module methods of cmc-py."""

from typing import List

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

    @strawberry.field
    async def mostvisited(self) -> List[MostVisitedData]:
        schema_list: List[MostVisitedData] = []
        if redis.check_data("mostvisited"):
            redis_result = redis.get_data("mostvisited")
            for data in redis_result:  # type: ignore
                schema_list.append(MostVisitedData(**redis_result[data]))  # type: ignore
            return schema_list
        result = MostVisited(as_dict=True).get_data
        redis.add_data("mostvisited", result)  # type: ignore
        for data in result:
            schema_list.append(MostVisitedData(**result[data]))
        return schema_list


schema = strawberry.Schema(query=Query)
cryptocurrency_router = GraphQLRouter(schema)
