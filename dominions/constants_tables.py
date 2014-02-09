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

""" Tables of constants. """


__docformat__ = "reStructuredText"


from sqlalchemy import (
    Column                      as _SQLA_Column,
    Integer                     as _SQLA_Integer,
    String                      as _SQLA_String,
)
from sqlalchemy.ext.declarative import (
    declarative_base        as _SQLA_declarative_base,
)


from dominions.DataTable import (
    DataTable_CSV               as _DataTable_CSV,
    DataTableRow_NamedInteger   as _DataTableRow_NamedInteger,
    DataTable_NamedInteger      as _DataTable_NamedInteger,
    DataTableRow_NamedBits      as _DataTableRow_NamedBits,
    DataTable_NamedBits         as _DataTable_NamedBits,
)


class AttributeKey( _DataTableRow_NamedInteger ):
    """ An attribute key. """


    __tablename__   = "attribute_keys"


class AttributeKeys_DataTable( _DataTable_NamedInteger, _DataTable_CSV ):
    """ A table of attribute keys. """


    _TITLE          = "Attribute Keys"
    _LABEL          = "Attribute Keys"
    _FILE_NAME_BASE = "attribute-keys"
    _ROW_CLASS      = AttributeKey


class Sound( _DataTableRow_NamedInteger ):
    """ A sound effect. """


    __tablename__   = "sounds"


    _TITLE          = "Sound {Spl: #sound, Wpn: #sound}"


class Sounds_DataTable( _DataTable_NamedInteger, _DataTable_CSV ):
    """ A table of sound effects. """


    _TITLE          = "Sounds {Spl: #sound, Wpn: #sound}"
    _LABEL          = "Sounds"
    _FILE_NAME_BASE = "sounds"
    _ROW_CLASS      = Sound


class MonsterTag( _DataTableRow_NamedInteger ):
    """ A monster tag. """


    __tablename__   = "monster_tags"


    _TITLE          = "Monster Group {Spl: #damage, Wpn: #dmg}"


class MonsterTags_DataTable( _DataTable_NamedInteger, _DataTable_CSV ):
    """ A table of monster tags. """


    _TITLE          = "Monster Tags {Spl: #damage, Wpn: #dmg}"
    _LABEL          = "Monster Tags"
    _FILE_NAME_BASE = "monster-tags"
    _ROW_CLASS      = MonsterTag


class MagicSchool( _DataTableRow_NamedInteger ):
    """ A magic school. """


    __tablename__   = "magic_schools"

    _TITLE          = "School of Magic {Spl: #school}"


class MagicSchools_DataTable( _DataTable_NamedInteger, _DataTable_CSV ):
    """ A table of magic schools. """


    _TITLE          = "Schools of Magic {Spl: #school}"
    _LABEL          = "Schools of Magic"
    _FILE_NAME_BASE = "magic-schools"
    _ROW_CLASS      = MagicSchool


class MagicPath( _DataTableRow_NamedInteger ):
    """ A magic path. """


    __tablename__   = "magic_paths"


class MagicPaths_DataTable( _DataTable_NamedInteger, _DataTable_CSV ):
    """ A table of magic paths. """


    _TITLE          = "Magic Paths {Spl: #path, #damage; Wpn: #dmg}"
    _LABEL          = "Magic Paths"
    _FILE_NAME_BASE = "magic-paths"
    _ROW_CLASS      = MagicPath


class AnonymousProvinceEvent( _DataTableRow_NamedInteger ):
    """ An anonymous province event. """


    __tablename__   = "anon_province_events"


class AnonymousProvinceEvents_DataTable(
    _DataTable_NamedInteger, _DataTable_CSV
):
    """ A table of anonymous province events. """


    _TITLE          = "Anonymous Province Events {Spl: #damage, Wpn: #dmg}"
    _LABEL          = "Anonymous Province Events"
    _FILE_NAME_BASE = "anon-province-events"
    _ROW_CLASS      = AnonymousProvinceEvent


class SpecialUniqueSummon( _DataTableRow_NamedInteger ):
    """ A special unique summon. """


    __tablename__   = "special_unique_summons"


class SpecialUniqueSummons_DataTable(
    _DataTable_NamedInteger, _DataTable_CSV
):
    """ A table of special unique summons. """


    _TITLE          = "Special Unique Summons {Spl: #damage, Wpn: #dmg}"
    _LABEL          = "Special Unique Summons"
    _FILE_NAME_BASE = "special-unique-summons"
    _ROW_CLASS      = SpecialUniqueSummon


class TerrainSpecificSummon( _DataTableRow_NamedInteger ):
    """ A terrain-specific summon. """


    __tablename__   = "terrain_specific_summons"


class TerrainSpecificSummons_DataTable(
    _DataTable_NamedInteger, _DataTable_CSV
):
    """ A table of terrain-specific summons. """


    _TITLE          = "Terrain-Specific Summons {Spl: #damage, Wpn: #dmg}"
    _LABEL          = "Terrain-Specific Summons"
    _FILE_NAME_BASE = "terrain-specific-summons"
    _ROW_CLASS      = TerrainSpecificSummon


class OtherPlane( _DataTableRow_NamedInteger ):
    """ Another plane. """


    __tablename__   = "other_planes"


class OtherPlanes_DataTable(
    _DataTable_NamedInteger, _DataTable_CSV
):
    """ A table of other planes. """


    _TITLE          = "Other Planes {#damage, Wpn: #dmg}"
    _LABEL          = "Other Planes"
    _FILE_NAME_BASE = "other-planes"
    _ROW_CLASS      = OtherPlane


class MapTerrainType( _DataTableRow_NamedBits ):
    """ A map terrain type. """


    __tablename__   = "map_terrain_types"


class MapTerrainTypes_DataTable( _DataTable_NamedBits, _DataTable_CSV ):
    """ A bitmask table of map terrain types. """


    _TITLE          = "Map Terrain Types"
    _LABEL          = "Map Terrain Types"
    _FILE_NAME_BASE = "map-terrain-types"
    _ROW_CLASS      = MapTerrainType


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #
