# coding: utf-8

"""
    SnapTrade

    Connect brokerage accounts to your app for live positions and trading

    The version of the OpenAPI document: 1.0.0
    Contact: api@snaptrade.com
    Created by: https://snaptrade.com/
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from snaptrade_client import schemas  # noqa: F401


class HoldingsStatus(
    schemas.AnyTypeSchema,
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    Status of account holdings sync. SnapTrade syncs holdings from the brokerage under the following conditions:
1. Initial connection - SnapTrade syncs all holdings (positions, balances, recent orders, and transactions) immediately after the connection is established.
2. Daily sync - Once a day SnapTrade refreshes all holdings from the brokerage.
3. Manual sync - You can trigger a refresh of holdings with the [manual refresh](/reference/Connections/Connections_refreshBrokerageAuthorization) endpoint.

    """


    class MetaOapg:
        
        class properties:
            initial_sync_completed = schemas.BoolSchema
        
            @staticmethod
            def last_successful_sync() -> typing.Type['HoldingsSyncStatusDateNullable']:
                return HoldingsSyncStatusDateNullable
            __annotations__ = {
                "initial_sync_completed": initial_sync_completed,
                "last_successful_sync": last_successful_sync,
            }

    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["initial_sync_completed"]) -> MetaOapg.properties.initial_sync_completed: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_successful_sync"]) -> 'HoldingsSyncStatusDateNullable': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["initial_sync_completed", "last_successful_sync", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["initial_sync_completed"]) -> typing.Union[MetaOapg.properties.initial_sync_completed, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_successful_sync"]) -> typing.Union['HoldingsSyncStatusDateNullable', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["initial_sync_completed", "last_successful_sync", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
        initial_sync_completed: typing.Union[MetaOapg.properties.initial_sync_completed, bool, schemas.Unset] = schemas.unset,
        last_successful_sync: typing.Union['HoldingsSyncStatusDateNullable', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'HoldingsStatus':
        return super().__new__(
            cls,
            *args,
            initial_sync_completed=initial_sync_completed,
            last_successful_sync=last_successful_sync,
            _configuration=_configuration,
            **kwargs,
        )

from snaptrade_client.model.holdings_sync_status_date_nullable import HoldingsSyncStatusDateNullable
