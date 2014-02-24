###############################################################################
#                                dominions                                    #
#-----------------------------------------------------------------------------#
#                                                                             #
#   Licensed under the Apache License, Version 2.0 (the "License");           #
#   you may not use this file except in compliance with the License.          #
#   You may obtain a copy of the License at                                   #
#                                                                             #
#       http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                             #
#   Unless required by applicable law or agreed to in writing, software       #
#   distributed under the License is distributed on an "AS IS" BASIS,         #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and       #
#   limitations under the License.                                            #
#                                                                             #
###############################################################################

""" Attributes applied to instances of various Dominions types. """


__docformat__ = "reStructuredText"


from collections import (
    namedtuple              as _namedtuple,
    OrderedDict             as _OrderedDict,
)

from sqlalchemy import (
    Table                       as _SQLA_Table,
    Column                      as _SQLA_Column,
    ForeignKey                  as _SQLA_ForeignKey,
    Integer                     as _SQLA_Integer,
    String                      as _SQLA_String,
)
from sqlalchemy.ext.declarative import (
    declared_attr               as _SQLA_declared_attr,
)
from sqlalchemy.orm import (
    relationship                as _SQLA_relationship,
)
from sqlalchemy.orm.util import (
    polymorphic_union       as _SQLA_polymorphic_union,
)

from dominions.utils import (
    PrettyFormatConfig          as _PrettyFormatConfig,
)
from dominions.DataTable import (
    DataTableRow                as _DataTableRow,
)
from dominions.constants_tables import (
    AttributeKey,
    AttributeKeys_DataTable,
    MapTerrainType,
    MapTerrainTypes_DataTable,
)


_AttributesBuilderData = _namedtuple(
    "AttributesBuilderData",
    "value_table_name value_title value_mixin_class_name"
)

ATTRIBUTES_BUILDER_DATA             = _OrderedDict( )
ATTRIBUTES_BUILDER_DATA[ 35 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 36 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 41 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 43 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 46 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 47 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 52 ]      = _AttributesBuilderData(
    "capital_magic_sites", "Capital Magic Site {Ntn: #startsite}",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 59 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 69 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 73 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 74 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 75 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 76 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 77 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 78 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 79 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 80 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 81 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 82 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 83 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 84 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 85 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 90 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 91 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 92 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 93 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 94 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 95 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 100 ]      = _AttributesBuilderData(
    "capital_magic_sites",
    "Capital Magic Site (Unholy?) {Ntn: #startsite}",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 122 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 123 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 124 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 125 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 126 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 127 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 131 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 132 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 133 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 134 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 136 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 137 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 138 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 139 ]      = _AttributesBuilderData(
    "unique_heroes", "National Unique Hero {Ntn: #hero1}",
    "AttributeValue_Monster"
)
ATTRIBUTES_BUILDER_DATA[ 140 ]      = _AttributesBuilderData(
    "unique_heroes", "National Unique Hero {Ntn: #hero2}",
    "AttributeValue_Monster"
)
ATTRIBUTES_BUILDER_DATA[ 141 ]      = _AttributesBuilderData(
    "unique_heroes", "National Unique Hero {Ntn: #hero3}",
    "AttributeValue_Monster"
)
ATTRIBUTES_BUILDER_DATA[ 142 ]      = _AttributesBuilderData(
    "unique_heroes", "National Unique Hero {Ntn: #hero4}",
    "AttributeValue_Monster"
)
ATTRIBUTES_BUILDER_DATA[ 143 ]      = _AttributesBuilderData(
    "unique_heroes", "National Unique Hero {Ntn: #hero5}",
    "AttributeValue_Monster"
)
ATTRIBUTES_BUILDER_DATA[ 144 ]      = _AttributesBuilderData(
    "unique_heroes", "National Unique Hero {Ntn: #hero6}",
    "AttributeValue_Monster"
)
ATTRIBUTES_BUILDER_DATA[ 145 ]      = _AttributesBuilderData(
    "generic_heroes", "National Generic Hero {Ntn: #multihero1}",
    "AttributeValue_Monster"
)
ATTRIBUTES_BUILDER_DATA[ 146 ]      = _AttributesBuilderData(
    "generic_heroes", "National Generic Hero {Ntn: #multihero2}",
    "AttributeValue_Monster"
)
ATTRIBUTES_BUILDER_DATA[ 156 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 157 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 158 ]      = _AttributesBuilderData(
    "recruitable_units", "Coastal Fort Commander {Ntn: #coastcom1}",
    "AttributeValue_Monster"
)
ATTRIBUTES_BUILDER_DATA[ 159 ]      = _AttributesBuilderData(
    "recruitable_units", "Coastal Fort Commander {Ntn: #coastcom2}",
    "AttributeValue_Monster"
)
ATTRIBUTES_BUILDER_DATA[ 160 ]      = _AttributesBuilderData(
    "recruitable_units", "Coastal Fort Troop {Ntn: #coastunit1}",
    "AttributeValue_Monster"
)
ATTRIBUTES_BUILDER_DATA[ 161 ]      = _AttributesBuilderData(
    "recruitable_units", "Coastal Fort Troop {Ntn: #coastunit2}",
    "AttributeValue_Monster"
)
ATTRIBUTES_BUILDER_DATA[ 162 ]      = _AttributesBuilderData(
    "recruitable_units", "Coastal Fort Troop {Ntn: #coastunit3}",
    "AttributeValue_Monster"
)
ATTRIBUTES_BUILDER_DATA[ 163 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 167 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 168 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 169 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 170 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 171 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 172 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 173 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 174 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 175 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 176 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 177 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 178 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 179 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 180 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 185 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 186 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 187 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 188 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 189 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 190 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 191 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 193 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 194 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 195 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 196 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 197 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 198 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 199 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 200 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 205 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 207 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 210 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 211 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 213 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 217 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 220 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 221 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 222 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 223 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 261 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 263 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 264 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 265 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 266 ]      = _AttributesBuilderData(
    "boolean_values", "Material Composition: Ferrous",
    "AttributeValue_Boolean"
)
ATTRIBUTES_BUILDER_DATA[ 267 ]      = _AttributesBuilderData(
    "boolean_values", "Material Composition: Ferrous",
    "AttributeValue_Boolean"
)
ATTRIBUTES_BUILDER_DATA[ 268 ]      = _AttributesBuilderData(
    "boolean_values", "Material Composition: Flammable",
    "AttributeValue_Boolean"
)
ATTRIBUTES_BUILDER_DATA[ 269 ]      = _AttributesBuilderData(
    "boolean_values", "Material Composition: Flammable",
    "AttributeValue_Boolean"
)
ATTRIBUTES_BUILDER_DATA[ 270 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 271 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 272 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 273 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 274 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 275 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 278 ]      = _AttributesBuilderData(
    "restrict_to_nations", "Restrict to Nation {Spl: #restricted}",
    "AttributeValue_Nation"
)
ATTRIBUTES_BUILDER_DATA[ 279 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 280 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 287 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 288 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 289 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 290 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 293 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 294 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 295 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 296 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 297 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 298 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 299 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 300 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 302 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 303 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 304 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 305 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 306 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 404 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 426 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 477 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 700 ]      = _AttributesBuilderData(
    "map_ranges", "Map Range {Spl: #provrange}",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 701 ]      = _AttributesBuilderData(
    "map_terrain_types", "<Unknown Attribute>",
    "AttributeValue_MapTerrainType"
)
ATTRIBUTES_BUILDER_DATA[ 702 ]      = _AttributesBuilderData(
    "map_terrain_types", "Source Terrain (?) {Spl: #onlygeosrc}",
    "AttributeValue_MapTerrainType"
)
ATTRIBUTES_BUILDER_DATA[ 703 ]      = _AttributesBuilderData(
    "boolean_values", "Only Target Own Provinces (?) {Spl: #onlyowndst}",
    "AttributeValue_Boolean"
)
ATTRIBUTES_BUILDER_DATA[ 704 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 705 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 706 ]      = _AttributesBuilderData(
    "boolean_values", "No Path over Land (?) {Spl: #nolandtrace}",
    "AttributeValue_Boolean"
)
ATTRIBUTES_BUILDER_DATA[ 707 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 708 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 709 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)
ATTRIBUTES_BUILDER_DATA[ 711 ]      = _AttributesBuilderData(
    "unknown_values", "<Unknown Attribute>",
    "AttributeValue_GenericValue"
)


class Attribute( _DataTableRow ):
    """ An attribute of a Dominions object. """


    __tablename__   = "attributes"


    record_id           = _SQLA_Column(
        _SQLA_Integer, primary_key = True, autoincrement = "ignore_fk"
    )
    attribute_number    = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
            AttributeKey.TABLE_NAME( ) + "." + AttributeKey.KEY_NAME( )
        )
    )
    object_type         = _SQLA_Column( _SQLA_String )
    raw_value           = _SQLA_Column( _SQLA_Integer )


    _KEY_NAME       = "record_id"


    @classmethod
    def __declare_last__( cls ):
        # Perform late binding against abstract concrete bases.
        cls.value = _SQLA_relationship( AttributeValue, uselist = False )


    @classmethod
    def from_raw_data( cls, attribute_number, object_type, raw_value ):
        """ Creates an instance from a set of raw arguments. """

        args = {
            "attribute_number": attribute_number,
            "object_type": object_type,
            "raw_value": raw_value,
        }

        self = cls( **args )

        self.value = eval(
            "Attribute{attribute_number}Value.from_raw_value".format(
                attribute_number = args[ "attribute_number" ]
            )
        )(
            attribute_record_id = self.record_id,
            attribute_number = attribute_number,
            raw_value = raw_value
        )

        return self


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        return self.value.pformat_object(
            tables, pformat_config = pformat_config
        )


class Attribute_ForeignKey( _DataTableRow ):
    """ Abstraction for attribute record ID as a foreign key. """


    __abstract__    = True


    @_SQLA_declared_attr
    def attribute_record_id( cls ):
        return _SQLA_Column(
            _SQLA_Integer,
            _SQLA_ForeignKey(
                Attribute.TABLE_NAME( ) + "." + Attribute.KEY_NAME( )
            ),
            primary_key = True
        )


    _KEY_NAME       = "attribute_record_id"
    _KEY_FORMAT     = "d"


class AttributeValue_BASE( _DataTableRow ):
    """ A value of an attribute. """


    __abstract__    = True


    @classmethod
    def generated_SQLA_Table( cls, value_table_name ):
        """ Returns a SQLAlchemy table to be mapped to an object. """

        return _SQLA_Table(
            value_table_name + "_by_attribute", cls.metadata, 
            _SQLA_Column( "record_id",  _SQLA_Integer, primary_key = True ),
            _SQLA_Column(
                "attribute_record_id", _SQLA_Integer,
                _SQLA_ForeignKey(
                    Attribute.TABLE_NAME( ) + "." + Attribute.KEY_NAME( )
                )
            ),
            _SQLA_Column(
                "attribute_number", _SQLA_Integer,
                _SQLA_ForeignKey(
                    AttributeKey.TABLE_NAME( ) + "." + AttributeKey.KEY_NAME( )
                )
            ),
            *cls._generated_SQLA_Table_columns( ),
            keep_existing = True
        )


    @classmethod
    def _generated_SQLA_Table_columns( cls ):
        """ Returns additional SQLAlchemy columns for a table mapping. """

        return [ ]


    @classmethod
    def generated_SQLA_Mapper_arguments( cls, attribute_number ):
        """ Returns additional arguments for the SQLAlchemy mapper. """

        return { }


    @classmethod
    def from_raw_value( cls,
        attribute_record_id, attribute_number, raw_value
    ):
        """ Creates an instance from a raw value.
            (Dummy implementation - override.) """

        return cls(
            attribute_record_id = attribute_record_id,
            attribute_number = attribute_number
        )


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        template = pformat_config.indent
        args = { }

        if pformat_config.render_title:
            template += "{title}"
            args[ "title" ] = self.TITLE( )
            if pformat_config.render_key_with_object:
                template += " [{attribute_number}]: "
                args[ "attribute_number" ] = self.attribute_number
            else:
                template += ": "
        else:
            if pformat_config.render_key_with_object:
                template += "{attribute_number}"
                args[ "attribute_number" ] = self.attribute_number

        template += "{value}"
        args[ "value" ] = self._pformat_object(
            tables, pformat_config = pformat_config
        )

        return template.format( **args )


class AttributeValue_Boolean( AttributeValue_BASE ):
    """ A value of an attribute. """


    __abstract__    = True


    @classmethod
    def _generated_SQLA_Table_columns( cls ):
        """ Returns additional SQLAlchemy columns for a table mapping. """

        return [
            _SQLA_Column( "value", _SQLA_Integer ) 
        ]


    @classmethod
    def from_raw_value( cls,
        attribute_record_id, attribute_number, raw_value
    ):
        """ Creates an instance from a raw value. """

        args = {
            "attribute_record_id": attribute_record_id,
            "attribute_number": attribute_number,
            "value": raw_value
        }

        return cls( **args )


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        template = pformat_config.indent
        args = { }

        if pformat_config.render_title:
            template += "{title}"
            args[ "title" ] = self.TITLE( )
            if pformat_config.render_key_with_object:
                template += " [{attribute_number}]"
                args[ "attribute_number" ] = self.attribute_number
        else:
            if pformat_config.render_key_with_object:
                template += "{attribute_number}"
                args[ "attribute_number" ] = self.attribute_number

        return template.format( **args )


class AttributeValue_GenericValue( AttributeValue_BASE ):
    """ A value of an attribute. """


    __abstract__    = True


    @classmethod
    def _generated_SQLA_Table_columns( cls ):
        """ Returns additional SQLAlchemy columns for a table mapping. """

        return [
            _SQLA_Column( "value", _SQLA_Integer ) 
        ]


    @classmethod
    def from_raw_value( cls,
        attribute_record_id, attribute_number, raw_value
    ):
        """ Creates an instance from a raw value. """

        args = {
            "attribute_record_id": attribute_record_id,
            "attribute_number": attribute_number,
            "value": raw_value
        }

        return cls( **args )


    def _pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        return self.value


class AttributeValue_Nation( AttributeValue_BASE ):
    """ A value of an attribute. """


    __abstract__    = True


    @classmethod
    def _generated_SQLA_Table_columns( cls ):
        """ Returns additional SQLAlchemy columns for a table mapping. """

        # TODO: Add foreign key against nations table.
        return [
            _SQLA_Column( "nation_number", _SQLA_Integer ) 
        ]


    @classmethod
    def from_raw_value( cls,
        attribute_record_id, attribute_number, raw_value
    ):
        """ Creates an instance from a raw value. """

        args = {
            "attribute_record_id": attribute_record_id,
            "attribute_number": attribute_number
        }
        args[ "nation_number" ] = raw_value - 100

        return cls( **args )


    def _pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        # TODO: Lookup nation name from nations table.
        return self.nation_number


class AttributeValue_Monster( AttributeValue_BASE ):
    """ A value of an attribute. """


    __abstract__    = True


    @classmethod
    def _generated_SQLA_Table_columns( cls ):
        """ Returns additional SQLAlchemy columns for a table mapping. """

        # TODO: Add foreign key against monster table.
        return [
            _SQLA_Column( "monster_number", _SQLA_Integer ) 
        ]


    @classmethod
    def from_raw_value( cls,
        attribute_record_id, attribute_number, raw_value
    ):
        """ Creates an instance from a raw value. """

        args = {
            "attribute_record_id": attribute_record_id,
            "attribute_number": attribute_number
        }
        args[ "monster_number" ] = raw_value

        return cls( **args )


    def _pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        # TODO: Lookup monster name from monsters table.
        return self.monster_number


_BitmaskAssociationTableBuilderData \
= _namedtuple(
    "BitmaskAssociationTableBuilderData",
    "class_name_base table_name_base key_name title_base"
)
for _builder_data in [
    _BitmaskAssociationTableBuilderData(
        "MapTerrainType", "map_terrain_types", "terrain_type",
        "Terrain Type"
    ),
]:
    exec( """
class Attribute{class_name_base}_ASSOCIATE( _DataTableRow ):
    ''' A bitmaskable type associated with an attribute. '''


    __tablename__   = "{table_name_base}_for_attributes"


    _TITLE          = "{title_base}"
    _KEY_NAME       = "{key_name}"
    _KEY_FORMAT     = "d"


    attribute_value_record_id   = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey( "{table_name_base}_by_attribute.record_id" ),
        primary_key = True
    )
    {key_name}                  = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
              {class_name_base}.TABLE_NAME( )
            + "." + {class_name_base}.KEY_NAME( )
        ),
        primary_key = True
    )


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        ''' Nicely formats the object for display. '''

        return \\
        tables[ {class_name_base}s_DataTable.LABEL( ) ]\\
        .pformat_table_lookup(
            self.{key_name}, tables, pformat_config = pformat_config
        )


class AttributeValue_{class_name_base}( AttributeValue_BASE ):
    ''' A value of an attribute. '''


    __abstract__    = True


    @_SQLA_declared_attr
    def {key_name}s( cls ):
        return _SQLA_relationship( Attribute{class_name_base}_ASSOCIATE )


    @classmethod
    def from_raw_value( cls,
        attribute_record_id, attribute_number, raw_value
    ):
        ''' Creates an instance from a raw value. '''

        args = {{
            "attribute_record_id": attribute_record_id,
            "attribute_number": attribute_number
        }}

        self = cls( **args )

        {key_name}s = [ ]
        for bit_position in range( 64 ):
            bit_value = 2 ** bit_position
            if raw_value & bit_value:
                {key_name}s.append( Attribute{class_name_base}_ASSOCIATE(
                    {key_name} = bit_value
                ) )
        self.{key_name}s = {key_name}s

        return self


    def _pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        ''' Nicely formats the object for display. '''

        pformat_config_1 = pformat_config.clone(
            indent = pformat_config.indent + 4 * " ", render_title = False
        )

        template = "\\n{{{key_name}s}}"
        args = {{ }}

        args[ "{key_name}s" ] = "\\n".join( [
            {key_name}.pformat_object(
                tables, pformat_config = pformat_config_1
            )
            for {key_name} in self.{key_name}s
        ] )

        return template.format( **args )


    """.format( **vars( _builder_data ) ) )


_attribute_tables_polymorphic_map = { }
for _attribute_number, _builder_data in ATTRIBUTES_BUILDER_DATA.items( ):
    exec( """
_attribute_tables_polymorphic_map[ {attribute_number} ] \\
= {value_mixin_class_name}.generated_SQLA_Table( "{value_table_name}" )
    """.format(
        attribute_number = _attribute_number,
        **vars( _builder_data )
    ) )

_attribute_tables_polymorphic_union = _SQLA_polymorphic_union(
    _attribute_tables_polymorphic_map, "attribute_number_VIRTUAL",
    aliasname = "attribute_union"
)


class AttributeValue( _DataTableRow ):
    """ A value of an attribute. """

    _punion         = _attribute_tables_polymorphic_union

    __table__       = _punion
    __mapper_args__ = { "polymorphic_on": _punion.c.attribute_number_VIRTUAL }


for _attribute_number, _builder_data in ATTRIBUTES_BUILDER_DATA.items( ):
    exec( """
class Attribute{attribute_number}Value(
    AttributeValue, {value_mixin_class_name}
):
    ''' A value of an attribute. '''


    __table__       = _attribute_tables_polymorphic_map[ {attribute_number} ]
    __mapper_args__ = {{
        "polymorphic_identity": {attribute_number},
        "concrete": True
    }}
    __mapper_args__.update(
        {value_mixin_class_name}.generated_SQLA_Mapper_arguments(
            {attribute_number}
        )
    )


    _TITLE          = "{value_title}"


    """.format(
        attribute_number = _attribute_number,
        **vars( _builder_data )
    ) )


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #
