# _*_ coding: utf-8 _*_
"""©FHIR Data Primitive Types
https://www.hl7.org/fhir/datatypes.html#primitive
"""
import base64
import re

import isodate
from zope.interface import implementer

from fhirpath.thirdparty import ImmutableDict

from .interfaces import IFhirPrimitiveType


__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"

__all__ = [
    "FhirBoolean",
    "FhirInteger",
    "FhirString",
    "FhirDecimal",
    "FhirURI",
    "FhirURL",
    "FhirCanonical",
    "FhirBase64Binary",
    "FhirInstant",
    "FhirDate",
    "FhirDateTime",
    "FhirTime",
    "FhirCode",
    "FhirOid",
    "FhirId",
    "FhirMarkdown",
    "FhirUnsignedInt",
    "FhirPositiveInt",
    "FhirUUID",
    "PrimitiveDataTypes",
]


@implementer(IFhirPrimitiveType)
class FhirBoolean(str):
    """XML Representation: xs:boolean, except that 0 and 1 are not valid values
    JSON representation: JSON boolean (true or false)
    """

    __visit_name__ = "boolean"
    __regex__ = r"true|false"

    def _validate(self):
        """ """
        res = re.match(self.__regex__, self)
        if not res:
            raise ValueError("Invalid FHIR boolean value! should true or false")

    def to_python(self):
        """ """
        self._validate()

        return str(self) == "true"


@implementer(IFhirPrimitiveType)
class FhirInteger(str):
    """A signed integer in the range −2,147,483,648..2,147,483,647
    (32-bit; for larger values, use decimal)

    XML Representation: xs:int, except that leading 0 digits are not allowed
    JSON representation: JSON number (with no decimal point)
    """

    __visit_name__ = "integer"
    __regex__ = r"[0]|[-+]?[1-9][0-9]*"

    def _validate(self):
        """ """
        res = re.match(self.__regex__, self)
        if not res:
            raise ValueError(
                "Invalid FHIR integer value! A signed integer in the"
                "range −2,147,483,648..2,147,483,647"
            )

    def to_python(self):
        """ """
        self._validate()

        return int(self)


@implementer(IFhirPrimitiveType)
class FhirString(str):
    """A sequence of Unicode characters
    Note that strings SHALL NOT exceed 1MB (1024*1024 characters) in size.
    Strings SHOULD not contain Unicode character points below 32, except for u0009
    (horizontal tab), u0010 (carriage return) and u0013 (line feed).
    Leading and Trailing whitespace is allowed,
    but SHOULD be removed when using the XML format.
    Note: This means that a string that consists only of whitespace
    could be trimmed to nothing, which would be treated as an invalid element value.
    Therefore strings SHOULD always contain non-whitespace content

    XML Representation: xs:string
    JSON representation: JSON String
    """

    __visit_name__ = "string"
    __regex__ = r"[ \r\n\t\S]+"

    def _validate(self):
        """ """
        res = re.match(self.__regex__, self)
        if not res:
            raise ValueError(
                "Invalid FHIR integer value! A signed integer in the"
                "range −2,147,483,648..2,147,483,647"
            )

    def to_python(self):
        """ """
        return str(self)


@implementer(IFhirPrimitiveType)
class FhirDecimal(str):
    """Rational numbers that have a decimal representation.
    The precision of the decimal value has significance:

    - e.g. 0.010 is regarded as different to 0.01, and the original precision
    should be preserved
    - Implementations SHALL handle decimal values in ways that preserve and respect
    the precision of the value as represented for presentation purposes
    - Implementations are not required to perform calculations with these
    numbers differently, though they may choose to do so (i.e. preserve significance)
    - In object code, implementations that might meet this constraint are
    GMP implementations or equivalents to Java BigDecimal that implement arbitrary
    precision, or a combination of a (64 bit)
    floating point value with a precision field
    - Note that large and/or highly precise values are extremely rare in medicine.
    One element where highly precise decimals may be encountered is the Location
    coordinates. Irrespective of this, the limits documented in XML Schema apply

    XML Representation: union of xs:decimal and xs:double (see below for limitations)
    JSON representation: A JSON number (see below for limitations)
    """

    __visit_name__ = "decimal"
    __regex__ = r"-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?"

    def _validate(self):
        """ """
        res = re.match(self.__regex__, self)
        if not res:
            raise ValueError("Invalid FHIR decimal value!")

    def to_python(self):
        """ """
        self._validate()

        return float(self)


@implementer(IFhirPrimitiveType)
class FhirURI(str):
    """A Uniform Resource Identifier Reference (RFC 3986 ).
    Note: URIs are case sensitive.
    For UUID (urn:uuid:53fefa32-fcbb-4ff8-8a92-55ee120877b7) use all lowercase

    XML Representation: xs:anyURI
    JSON representation: A JSON string - a URI
    """

    __visit_name__ = "uri"
    __regex__ = r"\S*"

    def to_python(self):
        """"""
        return str(self)


@implementer(IFhirPrimitiveType)
class FhirURL(str):
    """A Uniform Resource Locator (RFC 1738 ).
    Note URLs are accessed directly using the specified protocol.
    Common URL protocols are ``http{s}:``, ``ftp:``, ``mailto``: and ``mllp:``,
    though many others are defined

    XML Representation: xs:anyURI
    JSON representation: A JSON string - a URL
    """

    __visit_name__ = "url"
    # xxx: restricted to defined protocol
    __regex__ = None

    def to_python(self):
        """ """
        return str(self)


@implementer(IFhirPrimitiveType)
class FhirCanonical(str):
    """A URI that refers to a resource by its canonical URL (resources with a url property).
    The canonical type differs from a uri in that it has special meaning in this
    specification, and in that it may have a version appended, separated by
    avertical bar (|).Note that the type canonical is not used for the actual canonical
    URLs that are the target of these references, but for the URIs that refer to them,
    and may have the version suffix in them. Like other URIs, elements of type
    canonical may also have #fragment references

    XML Representation: xs:anyURI
    JSON representation: A JSON string - a canonical URL
    """

    __visit_name__ = "canonical"

    __regex__ = None

    def to_python(self):
        """ """
        return str(self)


@implementer(IFhirPrimitiveType)
class FhirBase64Binary(bytes):
    """A stream of bytes, base64 encoded (RFC 4648 )
    There is no specified upper limit to the size of a binary,
    but systems will have to impose some implementation based limit
    to the size they support. This should be clearly documented, though
    there is no computable for this at this time

    XML Representation: xs:base64Binary
    JSON representation: A JSON string - base64 content
    """

    __visit_name__ = "base64Binary"
    __regex__ = r"(\s*([0-9a-zA-Z\+\=]){4}\s*)+"

    def to_python(self):
        """ """
        return base64.b64decode(self)


@implementer(IFhirPrimitiveType)
class FhirInstant(str):
    """An instant in time in the format YYYY-MM-DDThh:mm:ss.sss+zz:zz
    (e.g. 2015-02-07T13:28:17.239+02:00 or 2017-01-01T00:00:00Z).
    The time SHALL specified at least to the second and SHALL include a time zone.
    Note: This is intended for when precisely observed times are required (typically
    system logs etc.), and not human-reported times -
    for those, use date or dateTime (which can be as precise as instant,
    but is not required to be). instant is a more constrained dateTime

    XML Representation: xs:dateTime
    JSON representation: A JSON string - an xs:dateTime
    """

    __visit_name__ = "instant"
    __regex__ = r"([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))"  # noqa: E501

    def to_python(self):
        """ """
        if "T" in self:
            return isodate.parse_datetime(self)
        else:
            return isodate.parse_date(self)


@implementer(IFhirPrimitiveType)
class FhirDate(str):
    """A date, or partial date (e.g. just year or year + month) as
    used in human communication. The format is YYYY, YYYY-MM, or YYYY-MM-DD,
    e.g. 2018, 1973-06, or 1905-08-23. There SHALL be no time zone.
    Dates SHALL be valid dates

    XML Representation: union of xs:date, xs:gYearMonth, xs:gYear
    JSON representation: A JSON string - a union of xs:date, xs:gYearMonth, xs:gYear
    """

    __visit_name__ = "date"
    __regex__ = r"([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1]))?)?"  # noqa: E501

    def to_python(self):
        """ """
        return isodate.parse_date(self)


@implementer(IFhirPrimitiveType)
class FhirDateTime(str):
    """	A date, date-time or partial date (e.g. just year or year + month) as used in
    human communication. The format is YYYY, YYYY-MM, YYYY-MM-DD or
    YYYY-MM-DDThh:mm:ss+zz:zz, e.g. 2018, 1973-06, 1905-08-23,
    2015-02-07T13:28:17-05:00 or 2017-01-01T00:00:00.000Z.
    If hours and minutes are specified, a time zone SHALL be populated.
    Seconds must be provided due to schema type constraints but may be zero-filled
    and may be ignored at receiver discretion. Dates SHALL be valid dates.
    The time "24:00" is not allowed. Leap Seconds are allowed

    XML Representation: union of xs:dateTime, xs:date, xs:gYearMonth, xs:gYear
    JSON representation: A JSON string - a union of xs:dateTime,
    xs:date, xs:gYearMonth, xs:gYear
    """

    __visit_name__ = "dateTime"
    __regex__ = r"([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1])(T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)))?)?)?"  # noqa: E501

    def to_python(self):
        """ """
        return isodate.parse_datetime(self)


@implementer(IFhirPrimitiveType)
class FhirTime(str):
    """A time during the day, in the format hh:mm:ss.
    There is no date specified.
    Seconds must be provided due to schema type constraints but may be zero-filled and
    may be ignored at receiver discretion. The time "24:00" SHALL NOT be used.
    A time zone SHALL NOT be present.
    Times can be converted to a Duration since midnight.

    XML Representation: xs:time
    JSON representation: A JSON string - an xs:time
    """

    __visit_name__ = "time"
    __regex__ = r"([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?"

    def to_python(self):
        """ """
        return isodate.parse_time(self)


@implementer(IFhirPrimitiveType)
class FhirCode(str):
    """Indicates that the value is taken from a set of controlled
    strings defined elsewhere (see Using codes for further discussion).
    Technically, a code is restricted to a string which has at least one
    character and no leading or trailing whitespace, and where there is no
    whitespace other than single spaces in the contents

    XML Representation: xs:token
    JSON representation: JSON string
    """

    __visit_name__ = "code"
    __regex__ = r"[^\s]+(\s[^\s]+)*"

    def to_python(self):
        """ """
        return str(self)


@implementer(IFhirPrimitiveType)
class FhirOid(str):
    """An OID represented as a URI (RFC 3001 ); e.g. urn:oid:1.2.3.4.5

    XML Representation: xs:anyURI
    JSON representation: JSON string - uri
    """

    __visit_name__ = "oid"
    __regex__ = r"urn:oid:[0-2](\.(0|[1-9][0-9]*))+"

    def to_python(self):
        """ """
        return str(self)


@implementer(IFhirPrimitiveType)
class FhirId(str):
    """Any combination of upper- or lower-case ASCII letters
    ('A'..'Z', and 'a'..'z', numerals ('0'..'9'), '-' and '.', with a length limit
    of 64 characters. (This might be an integer, an un-prefixed OID, UUID or any other
    identifier pattern that meets these constraints.)

    XML Representation: xs:string
    JSON representation: JSON string
    """

    __visit_name__ = "id"
    __regex__ = r"[A-Za-z0-9\-\.]{1,64}"

    def to_python(self):
        """ """
        return str(self)


@implementer(IFhirPrimitiveType)
class FhirMarkdown(str):
    """A FHIR string (see above) that may contain markdown syntax
    for optional processing by a markdown presentation engine,
    in the GFM extension of CommonMark format (see below)

    About the markdown datatype:
    -   This specification requires and uses the GFM (Github Flavored Markdown)
    extensions on CommonMark  format
    - Note that GFM prohibits Raw HTML
    - Systems are not required to have markdown support, so the content of a
    string should be readable without markdown processing, per markdown philosophy
    - Markdown content SHALL NOT contain Unicode character points below 32, except for
    u0009 (horizontal tab), u0010 (carriage return) and u0013 (line feed)
    - Markdown is a string, and subject to the same rules (e.g. length limit)
    - Converting an element that has the type string to markdown in a later version of
    this FHIR specification is not considered a breaking change (neither is adding
    markdown as a choice to an optional element that already has a choice of data types)

    XML Representation: xs:string
    JSON representation: JSON string
    """

    __visit_name__ = "markdown"
    __regex__ = r"\s*(\S|\s)*"

    def to_python(self):
        """"""
        return str(self)


@implementer(IFhirPrimitiveType)
class FhirUnsignedInt(str):
    """Any non-negative integer in the range 0..2,147,483,647

    XML Representation: xs:nonNegativeInteger
    JSON representation: JSON number
    """

    __visit_name__ = "unsignedInt"
    __regex__ = r"[0]|([1-9][0-9]*)"

    def to_python(self):
        """ """
        return int(self)


@implementer(IFhirPrimitiveType)
class FhirPositiveInt(str):
    """Any positive integer in the range 1..2,147,483,647

    XML Representation: xs:positiveInteger
    JSON representation: JSON number
    """

    __visit_name__ = "positiveInt"
    __regex__ = r"+?[1-9][0-9]*"

    def to_python(self):
        """ """
        return int(self)


@implementer(IFhirPrimitiveType)
class FhirUUID(str):
    """A UUID (aka GUID) represented as a URI (RFC 4122 );
    e.g. urn:uuid:c757873d-ec9a-4326-a141-556f43239520

    XML Representation: xs:anyURI
    JSON representation: JSON string - uri
    """

    __visit_name__ = "uuid"
    __regex__ = None

    def to_python(self):
        """ """
        return str(self)


# FHIR Primitive Data Types
PrimitiveDataTypes = ImmutableDict(
    [
        (FhirBoolean.__visit_name__, FhirBoolean),
        (FhirInteger.__visit_name__, FhirInteger),
        (FhirString.__visit_name__, FhirString),
        (FhirDecimal.__visit_name__, FhirDecimal),
        (FhirURI.__visit_name__, FhirURI),
        (FhirURL.__visit_name__, FhirURL),
        (FhirCanonical.__visit_name__, FhirCanonical),
        (FhirBase64Binary.__visit_name__, FhirBase64Binary),
        (FhirInstant.__visit_name__, FhirInstant),
        (FhirDate.__visit_name__, FhirDate),
        (FhirDateTime.__visit_name__, FhirDateTime),
        (FhirTime.__visit_name__, FhirTime),
        (FhirCode.__visit_name__, FhirCode),
        (FhirOid.__visit_name__, FhirOid),
        (FhirId.__visit_name__, FhirId),
        (FhirMarkdown.__visit_name__, FhirMarkdown),
        (FhirUnsignedInt.__visit_name__, FhirUnsignedInt),
        (FhirPositiveInt.__visit_name__, FhirPositiveInt),
        (FhirUUID.__visit_name__, FhirUUID),
    ]
)
