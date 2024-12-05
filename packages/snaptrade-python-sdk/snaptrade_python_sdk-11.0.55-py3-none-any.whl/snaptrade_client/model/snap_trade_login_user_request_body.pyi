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


class SnapTradeLoginUserRequestBody(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    Data to login a user via SnapTrade Partner
    """


    class MetaOapg:
        
        class properties:
            broker = schemas.StrSchema
            immediateRedirect = schemas.BoolSchema
            customRedirect = schemas.StrSchema
            reconnect = schemas.StrSchema
            
            
            class connectionType(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def READ(cls):
                    return cls("read")
                
                @schemas.classproperty
                def TRADE(cls):
                    return cls("trade")
            
            
            class connectionPortalVersion(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def V4(cls):
                    return cls("v4")
                
                @schemas.classproperty
                def V3(cls):
                    return cls("v3")
                
                @schemas.classproperty
                def V2(cls):
                    return cls("v2")
            __annotations__ = {
                "broker": broker,
                "immediateRedirect": immediateRedirect,
                "customRedirect": customRedirect,
                "reconnect": reconnect,
                "connectionType": connectionType,
                "connectionPortalVersion": connectionPortalVersion,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["broker"]) -> MetaOapg.properties.broker: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["immediateRedirect"]) -> MetaOapg.properties.immediateRedirect: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["customRedirect"]) -> MetaOapg.properties.customRedirect: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["reconnect"]) -> MetaOapg.properties.reconnect: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["connectionType"]) -> MetaOapg.properties.connectionType: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["connectionPortalVersion"]) -> MetaOapg.properties.connectionPortalVersion: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["broker", "immediateRedirect", "customRedirect", "reconnect", "connectionType", "connectionPortalVersion", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["broker"]) -> typing.Union[MetaOapg.properties.broker, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["immediateRedirect"]) -> typing.Union[MetaOapg.properties.immediateRedirect, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["customRedirect"]) -> typing.Union[MetaOapg.properties.customRedirect, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["reconnect"]) -> typing.Union[MetaOapg.properties.reconnect, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["connectionType"]) -> typing.Union[MetaOapg.properties.connectionType, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["connectionPortalVersion"]) -> typing.Union[MetaOapg.properties.connectionPortalVersion, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["broker", "immediateRedirect", "customRedirect", "reconnect", "connectionType", "connectionPortalVersion", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        broker: typing.Union[MetaOapg.properties.broker, str, schemas.Unset] = schemas.unset,
        immediateRedirect: typing.Union[MetaOapg.properties.immediateRedirect, bool, schemas.Unset] = schemas.unset,
        customRedirect: typing.Union[MetaOapg.properties.customRedirect, str, schemas.Unset] = schemas.unset,
        reconnect: typing.Union[MetaOapg.properties.reconnect, str, schemas.Unset] = schemas.unset,
        connectionType: typing.Union[MetaOapg.properties.connectionType, str, schemas.Unset] = schemas.unset,
        connectionPortalVersion: typing.Union[MetaOapg.properties.connectionPortalVersion, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'SnapTradeLoginUserRequestBody':
        return super().__new__(
            cls,
            *args,
            broker=broker,
            immediateRedirect=immediateRedirect,
            customRedirect=customRedirect,
            reconnect=reconnect,
            connectionType=connectionType,
            connectionPortalVersion=connectionPortalVersion,
            _configuration=_configuration,
            **kwargs,
        )
