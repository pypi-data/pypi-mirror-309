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


class SubPeriodReturnRate(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        
        class properties:
            periodStart = schemas.DateSchema
            periodEnd = schemas.DateSchema
            
            
            class rateOfReturn(
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'rateOfReturn':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "periodStart": periodStart,
                "periodEnd": periodEnd,
                "rateOfReturn": rateOfReturn,
            }
        additional_properties = schemas.AnyTypeSchema
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["periodStart"]) -> MetaOapg.properties.periodStart: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["periodEnd"]) -> MetaOapg.properties.periodEnd: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["rateOfReturn"]) -> MetaOapg.properties.rateOfReturn: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> MetaOapg.additional_properties: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["periodStart"], typing_extensions.Literal["periodEnd"], typing_extensions.Literal["rateOfReturn"], str, ]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["periodStart"]) -> typing.Union[MetaOapg.properties.periodStart, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["periodEnd"]) -> typing.Union[MetaOapg.properties.periodEnd, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["rateOfReturn"]) -> typing.Union[MetaOapg.properties.rateOfReturn, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[MetaOapg.additional_properties, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["periodStart"], typing_extensions.Literal["periodEnd"], typing_extensions.Literal["rateOfReturn"], str, ]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        periodStart: typing.Union[MetaOapg.properties.periodStart, str, date, schemas.Unset] = schemas.unset,
        periodEnd: typing.Union[MetaOapg.properties.periodEnd, str, date, schemas.Unset] = schemas.unset,
        rateOfReturn: typing.Union[MetaOapg.properties.rateOfReturn, None, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[MetaOapg.additional_properties, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
    ) -> 'SubPeriodReturnRate':
        return super().__new__(
            cls,
            *args,
            periodStart=periodStart,
            periodEnd=periodEnd,
            rateOfReturn=rateOfReturn,
            _configuration=_configuration,
            **kwargs,
        )
