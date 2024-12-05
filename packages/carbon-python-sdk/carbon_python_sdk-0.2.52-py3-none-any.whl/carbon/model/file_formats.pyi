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


class FileFormats(
    schemas.EnumBase,
    schemas.StrSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """
    
    @schemas.classproperty
    def TXT(cls):
        return cls("TXT")
    
    @schemas.classproperty
    def CSV(cls):
        return cls("CSV")
    
    @schemas.classproperty
    def TSV(cls):
        return cls("TSV")
    
    @schemas.classproperty
    def PDF(cls):
        return cls("PDF")
    
    @schemas.classproperty
    def DOCX(cls):
        return cls("DOCX")
    
    @schemas.classproperty
    def PPTX(cls):
        return cls("PPTX")
    
    @schemas.classproperty
    def XLSX(cls):
        return cls("XLSX")
    
    @schemas.classproperty
    def XLSM(cls):
        return cls("XLSM")
    
    @schemas.classproperty
    def MD(cls):
        return cls("MD")
    
    @schemas.classproperty
    def RTF(cls):
        return cls("RTF")
    
    @schemas.classproperty
    def JSON(cls):
        return cls("JSON")
    
    @schemas.classproperty
    def HTML(cls):
        return cls("HTML")
    
    @schemas.classproperty
    def NOTION(cls):
        return cls("NOTION")
    
    @schemas.classproperty
    def GOOGLE_DOCS(cls):
        return cls("GOOGLE_DOCS")
    
    @schemas.classproperty
    def GOOGLE_SHEETS(cls):
        return cls("GOOGLE_SHEETS")
    
    @schemas.classproperty
    def GOOGLE_SLIDES(cls):
        return cls("GOOGLE_SLIDES")
    
    @schemas.classproperty
    def INTERCOM(cls):
        return cls("INTERCOM")
    
    @schemas.classproperty
    def CONFLUENCE(cls):
        return cls("CONFLUENCE")
    
    @schemas.classproperty
    def RSS_FEED(cls):
        return cls("RSS_FEED")
    
    @schemas.classproperty
    def GMAIL(cls):
        return cls("GMAIL")
    
    @schemas.classproperty
    def OUTLOOK(cls):
        return cls("OUTLOOK")
    
    @schemas.classproperty
    def ZENDESK(cls):
        return cls("ZENDESK")
    
    @schemas.classproperty
    def FRESHDESK(cls):
        return cls("FRESHDESK")
    
    @schemas.classproperty
    def WEB_SCRAPE(cls):
        return cls("WEB_SCRAPE")
    
    @schemas.classproperty
    def GITBOOK(cls):
        return cls("GITBOOK")
    
    @schemas.classproperty
    def SALESFORCE(cls):
        return cls("SALESFORCE")
    
    @schemas.classproperty
    def GITHUB(cls):
        return cls("GITHUB")
    
    @schemas.classproperty
    def SLACK(cls):
        return cls("SLACK")
    
    @schemas.classproperty
    def GURU(cls):
        return cls("GURU")
    
    @schemas.classproperty
    def SERVICENOW(cls):
        return cls("SERVICENOW")
    
    @schemas.classproperty
    def GONG(cls):
        return cls("GONG")
    
    @schemas.classproperty
    def JPG(cls):
        return cls("JPG")
    
    @schemas.classproperty
    def PNG(cls):
        return cls("PNG")
    
    @schemas.classproperty
    def MP3(cls):
        return cls("MP3")
    
    @schemas.classproperty
    def MP2(cls):
        return cls("MP2")
    
    @schemas.classproperty
    def AAC(cls):
        return cls("AAC")
    
    @schemas.classproperty
    def WAV(cls):
        return cls("WAV")
    
    @schemas.classproperty
    def FLAC(cls):
        return cls("FLAC")
    
    @schemas.classproperty
    def PCM(cls):
        return cls("PCM")
    
    @schemas.classproperty
    def M4A(cls):
        return cls("M4A")
    
    @schemas.classproperty
    def OGG(cls):
        return cls("OGG")
    
    @schemas.classproperty
    def OPUS(cls):
        return cls("OPUS")
    
    @schemas.classproperty
    def MPEG(cls):
        return cls("MPEG")
    
    @schemas.classproperty
    def MPG(cls):
        return cls("MPG")
    
    @schemas.classproperty
    def MP4(cls):
        return cls("MP4")
    
    @schemas.classproperty
    def WMV(cls):
        return cls("WMV")
    
    @schemas.classproperty
    def AVI(cls):
        return cls("AVI")
    
    @schemas.classproperty
    def MOV(cls):
        return cls("MOV")
    
    @schemas.classproperty
    def MKV(cls):
        return cls("MKV")
    
    @schemas.classproperty
    def FLV(cls):
        return cls("FLV")
    
    @schemas.classproperty
    def WEBM(cls):
        return cls("WEBM")
    
    @schemas.classproperty
    def EML(cls):
        return cls("EML")
    
    @schemas.classproperty
    def MSG(cls):
        return cls("MSG")
