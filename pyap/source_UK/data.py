# -*- coding: utf-8 -*-

"""
    pyap.source_UK.data
    ~~~~~~~~~~~~~~~~~~~~

    This module provides regular expression definitions required for
    detecting US addresses.

    The module is expected to always contain 'full_address' variable containing
    all address parsing definitions.

    :copyright: (c) 2019 Ben Auffarth. Based on Vladimir Goncharov's code.
    :license: MIT, see LICENSE for more details.
"""


'''Numerals from one to nine
Note: here and below we use syntax like '[Oo][Nn][Ee]'
instead of '(one)(?i)' to match 'One' or 'oNe' because
Python Regexps don't seem to support turning On/Off
case modes for subcapturing groups.
'''
zero_to_nine = r"""(?:
    [Zz][Ee][Rr][Oo]\ |[Oo][Nn][Ee]\ |[Tt][Ww][Oo]\ |
    [Tt][Hh][Rr][Ee][Ee]\ |[Ff][Oo][Uu][Rr]\ |
    [Ff][Ii][Vv][Ee]\ |[Ss][Ii][Xx]\ |
    [Ss][Ee][Vv][Ee][Nn]\ |[Ee][Ii][Gg][Hh][Tt]\ |
    [Nn][Ii][Nn][Ee]\ |[Tt][Ee][Nn]\ |
    [Ee][Ll][Ee][Vv][Ee][Nn]\ |
    [Tt][Ww][Ee][Ll][Vv][Ee]\ |
    [Tt][Hh][Ii][Rr][Tt][Ee][Ee][Nn]\ |
    [Ff][Oo][Uu][Rr][Tt][Ee][Ee][Nn]\ |
    [Ff][Ii][Ff][Tt][Ee][Ee][Nn]\ |
    [Ss][Ii][Xx][Tt][Ee][Ee][Nn]\ |
    [Ss][Ee][Vv][Ee][Nn][Tt][Ee][Ee][Nn]\ |
    [Ee][Ii][Gg][Hh][Tt][Ee][Ee][Nn]\ |
    [Nn][Ii][Nn][Ee][Tt][Ee][Ee][Nn]\ 
    )"""

# Numerals - 10, 20, 30 ... 90
ten_to_ninety = r"""(?:
    [Tt][Ee][Nn]\ |[Tt][Ww][Ee][Nn][Tt][Yy]\ |
    [Tt][Hh][Ii][Rr][Tt][Yy]\ |
    [Ff][Oo][Rr][Tt][Yy]\ |
    [Ff][Oo][Uu][Rr][Tt][Yy]\ |
    [Ff][Ii][Ff][Tt][Yy]\ |[Ss][Ii][Xx][Tt][Yy]\ |
    [Ss][Ee][Vv][Ee][Nn][Tt][Yy]\ |
    [Ee][Ii][Gg][Hh][Tt][Yy]\ |
    [Nn][Ii][Nn][Ee][Tt][Yy]\ 
    )"""

# One hundred
hundred = r"""(?:
    [Hh][Uu][Nn][Dd][Rr][Ee][Dd]\ 
    )"""

# One thousand
thousand = r"""(?:
    [Tt][Hh][Oo][Uu][Ss][Aa][Nn][Dd]\ 
    )"""

'''
Regexp for matching street number.
Street number can be written 2 ways:
1) Using letters - "One thousand twenty two"
2) Using numbers
   a) - "1022"
   b) - "85-1190"
   c) - "85 1190"
'''
street_number = r"""(?P<street_number>
                        (?:
                            [Aa][Nn][Dd]\ 
                            |
                            {thousand}
                            |
                            {hundred}
                            |
                            {zero_to_nine}
                            |
                            {ten_to_ninety}
                        ){from_to}
                        |
                        (?:\d{from_to}
                            (?:\ ?\-?\ ?\d{from_to})?\ 
                        )
                    )
                """.format(thousand=thousand,
                           hundred=hundred,
                           zero_to_nine=zero_to_nine,
                           ten_to_ninety=ten_to_ninety,
                           from_to='{1,5}')

'''
Regexp for matching street name.
In example below:
"Hoover Boulevard": "Hoover" is a street name
'''
street_name = r"""(?P<street_name>
                  [a-zA-Z0-9\ \.]{0,31}  # Seems like the longest US street is
                                         # 'Northeast Kentucky Industrial
                                         # Parkway'
                                         # https://atkinsbookshelf.wordpress.com/tag/longest-street-name-in-us/
                 )
              """

post_direction = r"""
                    (?P<post_direction>
                        (?:
                            [Nn][Oo][Rr][Tt][Hh]\ |
                            [Ss][Oo][Uu][Tt][Hh]\ |
                            [Ee][Aa][Ss][Tt]\ |
                            [Ww][Ee][Ss][Tt]\ 
                        )
                        |
                        (?:
                            NW\ |NE\ |SW\ |SE\ 
                        )
                        |
                        (?:
                            N[\.\ ]|S[\.\ ]|E[\.\ ]|W[\.\ ]
                        )
                    )
                """

# Regexp for matching street type
street_type = r"""
            (?P<street_type>
                # Street
                [Ss][Tt][Rr][Ee][Ee][Tt]{div}|[Ss][Tt](?![A-Za-z]){div}|
                # Boulevard
                [Bb][Oo][Uu][Ll][Ee][Vv][Aa][Rr][Dd]{div}|[Bb][Ll][Vv][Dd]{div}|
                # Highway
                [Hh][Ii][Gg][Hh][Ww][Aa][Yy]{div}|[Hh][Ww][Yy]{div}|
                # Broadway
                [Bb][Rr][Oo][Aa][Dd][Ww][Aa][Yy]{div}|
                # Freeway
                [Ff][Rr][Ee][Ee][Ww][Aa][Yy]{div}|
                # Causeway
                [Cc][Aa][Uu][Ss][Ee][Ww][Aa][Yy]{div}|[Cc][Ss][Ww][Yy]{div}|
                # Expressway
                [Ee][Xx][Pp][Rr][Ee][Ss][Ss][Ww][Aa][Yy]{div}|
                # Way
                [Ww][Aa][Yy]{div}|
                # Walk
                [Ww][Aa][Ll][Kk]{div}|
                # Lane
                [Ll][Aa][Nn][Ee]{div}|[Ll][Nn]{div}|
                # Road
                [Rr][Oo][Aa][Dd]{div}|[Rr][Dd]{div}|
                # Avenue
                [Aa][Vv][Ee][Nn][Uu][Ee]{div}|[Aa][Vv][Ee]{div}|
                # Circle
                [Cc][Ii][Rr][Cc][Ll][Ee]{div}|[Cc][Ii][Rr]{div}|
                # Cove
                [Cc][Oo][Vv][Ee]{div}|[Cc][Vv]{div}|
                # Drive
                [Dd][Rr][Ii][Vv][Ee]{div}|[Dd][Rr]{div}|
                # Parkway
                [Pp][Aa][Rr][Kk][Ww][Aa][Yy]{div}|[Pp][Kk][Ww][Yy]{div}|
                # Park
                [Pp][Aa][Rr][Kk]{div}|
                # Court
                [Cc][Oo][Uu][Rr][Tt]{div}|[Cc][Tt]{div}|
                # Square
                [Ss][Qq][Uu][Aa][Rr][Ee]{div}|[Ss][Qq]{div}|
                # Loop
                [Ll][Oo][Oo][Pp]{div}|[Ll][Pp]{div}
            )
            (?P<route_id>
                [\(\ \,]{route_symbols}
                [Rr][Oo][Uu][Tt][Ee]\ [A-Za-z0-9]+[\)\ \,]{route_symbols}
            )?
            """.format(div="[\.\ ,]?", route_symbols='{0,3}')

floor = r"""
            (?P<floor>
                (?:
                \d+[A-Za-z]{0,2}\.?\ [Ff][Ll][Oo][Oo][Rr]\ 
                )
                |
                (?:
                    [Ff][Ll][Oo][Oo][Rr]\ \d+[A-Za-z]{0,2}\ 
                )
            )
        """

building = r"""
            (?:
                (?:
                    (?:[Bb][Uu][Ii][Ll][Dd][Ii][Nn][Gg])
                    |
                    (?:[Bb][Ll][Dd][Gg])
                )
                \ \d{0,2}[A-Za-z]?
            )
            """

occupancy = r"""
            (?:
                (?:
                    (?:
                        # Suite
                        [Ss][Uu][Ii][Tt][Ee]\ |[Ss][Tt][Ee]\.?\ 
                        |
                        # Apartment
                        [Aa][Pp][Tt]\.?\ |[Aa][Pp][Aa][Rr][Tt][Mm][Ee][Nn][Tt]\ 
                        |
                        # Room
                        [Rr][Oo][Oo][Mm]\ |[Rr][Mm]\.?\ 
                    )
                    (?:
                        [A-Za-z\#\&\-\d]{1,7}
                    )?
                )
                |
                (?:
                    \#[0-9]{,3}[A-Za-z]{1}
                )
            )\ ?
            """

po_box = r"""
            (?:
                [Pp]\.?\ ?[Oo]\.?\ [Bb][Oo][Xx]\ \d+
            )
        """

full_street = r"""
    (?:
        (?P<full_street>

            {street_number}
            {street_name}?\,?\ ?
            (?:[\ \,]{street_type})\,?\ ?
            {post_direction}?\,?\ ?
            {floor}?\,?\ ?

            (?P<building_id>
                {building}
            )?\,?\ ?

            (?P<occupancy>
                {occupancy}
            )?\,?\ ?

            {po_box}?
        )
    )""".format(street_number=street_number,
                street_name=street_name,
                street_type=street_type,
                post_direction=post_direction,
                floor=floor,
                building=building,
                occupancy=occupancy,
                po_box=po_box,
                )

# region1 is actually a "state"
region1 = r"""
        (?P<region1>
            (?:
                # states abbreviations
                AL|AK|AZ|AR|CA|CO|CT|DE|DC|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|
                MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|
                VA|WA|WV|WI|WY|
                al|ak|az|ar|ca|co|ct|de|dc|fl|ga|hi|id|il|in|ia|ks|ky|la|me|md|ma|mi|
                mn|ms|mo|mt|ne|nv|nh|nj|nm|ny|nc|nd|oh|ok|or|pa|ri|sc|sd|tn|tx|ut|vt|
                va|wa|wv|wi|wy|
                # unincorporated & commonwealth territories
                AS|GU|MP|PR|VI|
                as|gu|mp|pr|vi
            )
            |
            (?:
                # states full
                [Aa][Ll][Aa][Bb][Aa][Mm][Aa]|
                [Aa][Ll][Aa][Ss][Kk][Aa]|
                [Aa][Rr][Ii][Zz][Oo][Nn][Aa]|
                [Aa][Rr][Kk][Aa][Nn][Ss][Aa][Ss]|
                [Cc][Aa][Ll][Ii][Ff][Oo][Rr][Nn][Ii][Aa]|
                [Cc][Oo][Ll][Oo][Rr][Aa][Dd][Oo]|
                [Cc][Oo][Nn][Nn][Ee][Cc][Tt][Ii][Cc][Uu][Tt]|
                [Dd][Ee][Ll][Aa][Ww][Aa][Rr][Ee]|
                [Dd][Ii][Ss][Tt][Rr][Ii][Cc][Tt]\ [Oo][Ff]\ 
                [Cc][Oo][Ll][Uu][Mm][Bb][Ii][Aa]|
                [Ff][Ll][Oo][Rr][Ii][Dd][Aa]|
                [Gg][Ee][Oo][Rr][Gg][Ii][Aa]|
                [Hh][Aa][Ww][Aa][Ii][Ii]|
                [Ii][Dd][Aa][Hh][Oo]|
                [Ii][Ll][Ll][Ii][Nn][Oo][Ii][Ss]|
                [Ii][Nn][Dd][Ii][Aa][Nn][Aa]|
                [Ii][Oo][Ww][Aa]|
                [Kk][Aa][Nn][Ss][Aa][Ss]|
                [Kk][Ee][Nn][Tt][Uu][Cc][Kk][Yy]|
                [Ll][Oo][Uu][Ii][Ss][Ii][Aa][Nn][Aa]|
                [Mm][Aa][Ii][Nn][Ee]|
                [Mm][Aa][Rr][Yy][Ll][Aa][Nn][Dd]|
                [Mm][Aa][Ss][Ss][Aa][Cc][Hh][Uu][Ss][Ee][Tt][Tt][Ss]|
                [Mm][Ii][Cc][Hh][Ii][Gg][Aa][Nn]|
                [Mm][Ii][Nn][Nn][Ee][Ss][Oo][Tt][Aa]|
                [Mm][Ii][Ss][Ss][Ii][Ss][Ss][Ii][Pp][Pp][Ii]|
                [Mm][Ii][Ss][Ss][Oo][Uu][Rr][Ii]|
                [Mm][Oo][Nn][Tt][Aa][Nn][Aa]|
                [Nn][Ee][Bb][Rr][Aa][Ss][Kk][Aa]|
                [Nn][Ee][Vv][Aa][Dd][Aa]|
                [Nn][Ee][Ww]\ [Hh][Aa][Mm][Pp][Ss][Hh][Ii][Rr][Ee]|
                [Nn][Ee][Ww]\ [Jj][Ee][Rr][Ss][Ee][Yy]|
                [Nn][Ee][Ww]\ [Mm][Ee][Xx][Ii][Cc][Oo]|
                [Nn][Ee][Ww]\ [Yy][Oo][Rr][Kk]|
                [Nn][Oo][Rr][Tt][Hh]\ [Cc][Aa][Rr][Oo][Ll][Ii][Nn][Aa]|
                [Nn][Oo][Rr][Tt][Hh]\ [Dd][Aa][Kk][Oo][Tt][Aa]|
                [Oo][Hh][Ii][Oo]|
                [Oo][Kk][Ll][Aa][Hh][Oo][Mm][Aa]|
                [Oo][Rr][Ee][Gg][Oo][Nn]|
                [Pp][Ee][Nn][Nn][Ss][Yy][Ll][Vv][Aa][Nn][Ii][Aa]|
                [Rr][Hh][Oo][Dd][Ee]\ [Ii][Ss][Ll][Aa][Nn][Dd]|
                [Ss][Oo][Uu][Tt][Hh]\ [Cc][Aa][Rr][Oo][Ll][Ii][Nn][Aa]|
                [Ss][Oo][Uu][Tt][Hh]\ [Dd][Aa][Kk][Oo][Tt][Aa]|
                [Tt][Ee][Nn][Nn][Ee][Ss][Ss][Ee][Ee]|
                [Tt][Ee][Xx][Aa][Ss]|
                [Uu][Tt][Aa][Hh]|
                [Vv][Ee][Rr][Mm][Oo][Nn][Tt]|
                [Vv][Ii][Rr][Gg][Ii][Nn][Ii][Aa]|
                [Ww][Aa][Ss][Hh][Ii][Nn][Gg][Tt][Oo][Nn]|
                [Ww][Ee][Ss][Tt]\ [Vv][Ii][Rr][Gg][Ii][Nn][Ii][Aa]|
                [Ww][Ii][Ss][Cc][Oo][Nn][Ss][Ii][Nn]|
                [Ww][Yy][Oo][Mm][Ii][Nn][Gg]|

                # unincorporated & commonwealth territories
                [Aa][Mm][Ee][Rr][Ii][Cc][Aa][Nn]\ [Ss][Aa][Mm][Oo][Aa]
                |[Gg][Uu][Aa][Mm]|
                [Nn][Oo][Rr][Tt][Hh][Ee][Rr][Nn]\ [Mm][Aa][Rr][Ii][Aa][Nn][Aa]\ 
                [Ii][Ss][Ll][Aa][Nn][Dd][Ss]|
                [Pp][Uu][Ee][Rr][Tt][Oo]\ [Rr][Ii][Cc][Oo]|
                [Vv][Ii][Rr][Gg][Ii][Nn]\ [Ii][Ss][Ll][Aa][Nn][Dd][Ss]
            )
        )
        """

# TODO: doesn't catch cities containing French characters
city = r"""
        (?P<city>
            [A-za-z]{1}[a-zA-Z\ \-\'\.]{2,20}
        )
        """

postal_code = r"""
            (?P<postal_code>
                (?:\d{5}(?:\-\d{4})?)
            )
            """

country = r"""
            (?:
                ([Uu]\.?[Ss]\.?[Aa]\.?)|
                ([Uu][Nn][Ii][Tt][Ee][Dd]\ [Ss][Tt][Aa][Tt][Ee][Ss])
                # we do not catch for "United States of America"
                # since nobody really uses that form to write an
                # address
            )
            """

full_address = r"""
                (?P<full_address>
                    {full_street} {div}
                    {city} {div}
                    (?:
                        (?:{postal_code}?\ ?,?{country}?)
                    )
                )
                """.format(
    full_street=full_street,
    div='[\, ]{,2}',
    city=city,
    region1=region1,
    country=country,
    postal_code=postal_code,
)
