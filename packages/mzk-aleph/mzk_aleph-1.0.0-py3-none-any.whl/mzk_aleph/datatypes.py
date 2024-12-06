from enum import Enum


class AlephField(Enum):
    Sysno = "SYS"
    Barcode = "BAR"
    Signature = "SIG"
    CNB = "CNB"
    ISBN = "SBN"
    ISSN = "SSN"
    ISMN = "SMN"


class AlephResponseStatus(Enum):
    AlephNotAvailable = "AlephNotAvailable"
    RequestFailed = "RequestFailed"
    RecordNotFound = "RecordNotFound"
    MultipleRecordsFound = "MultipleRecordsFound"
    InvalidSysno = "InvalidSysno"
    InvalidSysnoBase = "InvalidSysnoBase"
    Success = "Success"


class IssuanceType(Enum):
    Unit = "Unit"
    Volume = "Volume"
    Bundle = "Bundle"


class MaterialType(Enum):
    Book = "Book"
    ContinuingResource = "ContinuingResource"
    Graphic = "Graphic"
    Map = "Map"
    Music = "Music"
    Other = "Other"


class LibrarySigla(Enum):
    MZK = "BOA001"


class CatalogBase(Enum):
    SKC = "SKC-UTF"
    CNB = "CNB-UTF"
    MZK01 = "MZK01-UTF"
