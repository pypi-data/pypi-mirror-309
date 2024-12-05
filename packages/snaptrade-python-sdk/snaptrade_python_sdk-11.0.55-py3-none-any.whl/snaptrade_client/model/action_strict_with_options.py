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


class ActionStrictWithOptions(
    schemas.EnumBase,
    schemas.StrSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    The action describes the intent or side of a trade. This is either `BUY` or `SELL` for Equity symbols or `BUY_TO_OPEN`, `BUY_TO_CLOSE`, `SELL_TO_OPEN` or `SELL_TO_CLOSE` for Options.
    """


    class MetaOapg:
        enum_value_to_name = {
            "BUY": "BUY",
            "SELL": "SELL",
            "BUY_TO_OPEN": "BUY_TO_OPEN",
            "BUY_TO_CLOSE": "BUY_TO_CLOSE",
            "SELL_TO_OPEN": "SELL_TO_OPEN",
            "SELL_TO_CLOSE": "SELL_TO_CLOSE",
        }
    
    @schemas.classproperty
    def BUY(cls):
        return cls("BUY")
    
    @schemas.classproperty
    def SELL(cls):
        return cls("SELL")
    
    @schemas.classproperty
    def BUY_TO_OPEN(cls):
        return cls("BUY_TO_OPEN")
    
    @schemas.classproperty
    def BUY_TO_CLOSE(cls):
        return cls("BUY_TO_CLOSE")
    
    @schemas.classproperty
    def SELL_TO_OPEN(cls):
        return cls("SELL_TO_OPEN")
    
    @schemas.classproperty
    def SELL_TO_CLOSE(cls):
        return cls("SELL_TO_CLOSE")
