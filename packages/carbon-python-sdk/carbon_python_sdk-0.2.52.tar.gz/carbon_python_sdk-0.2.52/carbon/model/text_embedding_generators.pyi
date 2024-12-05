# coding: utf-8

"""
    Carbon

    Connect external data to LLMs, no matter the source.

    The version of the OpenAPI document: 1.0.0
    Generated by: https://konfigthis.com
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

from carbon import schemas  # noqa: F401


class TextEmbeddingGenerators(
    schemas.EnumBase,
    schemas.StrSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """
    
    @schemas.classproperty
    def OPENAI(cls):
        return cls("OPENAI")
    
    @schemas.classproperty
    def AZURE_OPENAI(cls):
        return cls("AZURE_OPENAI")
    
    @schemas.classproperty
    def COHERE_MULTILINGUAL_V3(cls):
        return cls("COHERE_MULTILINGUAL_V3")
    
    @schemas.classproperty
    def OPENAI_ADA_LARGE_256(cls):
        return cls("OPENAI_ADA_LARGE_256")
    
    @schemas.classproperty
    def OPENAI_ADA_LARGE_1024(cls):
        return cls("OPENAI_ADA_LARGE_1024")
    
    @schemas.classproperty
    def OPENAI_ADA_LARGE_3072(cls):
        return cls("OPENAI_ADA_LARGE_3072")
    
    @schemas.classproperty
    def OPENAI_ADA_SMALL_512(cls):
        return cls("OPENAI_ADA_SMALL_512")
    
    @schemas.classproperty
    def OPENAI_ADA_SMALL_1536(cls):
        return cls("OPENAI_ADA_SMALL_1536")
    
    @schemas.classproperty
    def AZURE_ADA_LARGE_256(cls):
        return cls("AZURE_ADA_LARGE_256")
    
    @schemas.classproperty
    def AZURE_ADA_LARGE_1024(cls):
        return cls("AZURE_ADA_LARGE_1024")
    
    @schemas.classproperty
    def AZURE_ADA_LARGE_3072(cls):
        return cls("AZURE_ADA_LARGE_3072")
    
    @schemas.classproperty
    def AZURE_ADA_SMALL_512(cls):
        return cls("AZURE_ADA_SMALL_512")
    
    @schemas.classproperty
    def AZURE_ADA_SMALL_1536(cls):
        return cls("AZURE_ADA_SMALL_1536")
    
    @schemas.classproperty
    def SOLAR_1_MINI(cls):
        return cls("SOLAR_1_MINI")
