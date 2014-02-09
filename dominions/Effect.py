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

""" Effects used by weapons and spells. """


__docformat__ = "reStructuredText"


from collections import (
    namedtuple              as _namedtuple,
    OrderedDict             as _OrderedDict,
)

from sqlalchemy import (
    Table                   as _SQLA_Table,
    Column                  as _SQLA_Column,
    ForeignKey              as _SQLA_ForeignKey,
    Boolean                 as _SQLA_Boolean,
    Integer                 as _SQLA_Integer,
    String                  as _SQLA_String,
)
from sqlalchemy.ext.declarative import (
    declared_attr           as _SQLA_declared_attr,
)
from sqlalchemy.schema import (
    PrimaryKeyConstraint    as _SQLA_PrimaryKeyConstraint,
    ForeignKeyConstraint    as _SQLA_ForeignKeyConstraint,
)
from sqlalchemy.orm import (
    relationship            as _SQLA_relationship,
)
from sqlalchemy.orm.util import (
    polymorphic_union       as _SQLA_polymorphic_union,
)

from dominions.utils import (
    PrettyFormatConfig      as _PrettyFormatConfig,
    pprint_bit_names_table  as _pprint_bit_names_table,
    pprint_bitmask          as _pprint_bitmask,
)
from dominions.constants_tables import (
    Sound,
    Sounds_DataTable,
    MonsterTag,
    MonsterTags_DataTable,
    MagicPath,
    MagicPaths_DataTable,
    AnonymousProvinceEvent,
    AnonymousProvinceEvents_DataTable,
    SpecialUniqueSummon,
    SpecialUniqueSummons_DataTable,
    TerrainSpecificSummon,
    TerrainSpecificSummons_DataTable,
    OtherPlane,
    OtherPlanes_DataTable,
)
from dominions.DataTable import (
    DataTableRow                as _DataTableRow,
    DataTable_CSV               as _DataTable_CSV,
    DataTableRow_NamedInteger   as _DataTableRow_NamedInteger,
    DataTable_NamedInteger      as _DataTable_NamedInteger,
    DataTableRow_NamedBits      as _DataTableRow_NamedBits,
    DataTable_NamedBits         as _DataTable_NamedBits,
)


class SpecialDamageType( _DataTableRow_NamedBits ):
    """ A damage type bit. """


    __tablename__   = "special_damage_types"


class SpecialDamageTypes_DataTable( _DataTable_NamedBits, _DataTable_CSV ):
    """ A bitmask table of special damage types. """


    _TITLE          = "Special Damage Types {Spl: #damage, Wpn: #dmg}"
    _LABEL          = "Special Damage Types"
    _FILE_NAME_BASE = "special-damage-types"
    _ROW_CLASS      = SpecialDamageType


class Buffs1Type( _DataTableRow_NamedBits ):
    """ A Type I buff bit. """


    __tablename__   = "buffs_1_types"


class Buffs1Types_DataTable( _DataTable_NamedBits, _DataTable_CSV ):
    """ A bitmask table of Type I buffs. """


    _TITLE          = "Blessings/Buffs (Type I) {Spl: #damage, Wpn: #dmg}"
    _LABEL          = "Blessings/Buffs (Type I)"
    _FILE_NAME_BASE = "buffs-1-types"
    _ROW_CLASS      = Buffs1Type


class Buffs2Type( _DataTableRow_NamedBits ):
    """ An Type II buff bit. """


    __tablename__   = "buffs_2_types"


class Buffs2Types_DataTable( _DataTable_NamedBits, _DataTable_CSV ):
    """ A bitmask table of Type II buffs. """


    _TITLE          = "Blessings/Buffs (Type II) {Spl: #damage, Wpn: #dmg}"
    _LABEL          = "Blessings/Buffs (Type II)"
    _FILE_NAME_BASE = "buffs-2-types"
    _ROW_CLASS      = Buffs2Type


class Enchantment( _DataTableRow_NamedInteger ):
    """ An enchantment. """


    __tablename__   = "enchantments"


class Enchantments_DataTable( _DataTable_NamedInteger, _DataTable_CSV ):
    """ A table of enchantments. """


    _TITLE          = "Enchantments {Spl: #damage, Wpn: #dmg}"
    _LABEL          = "Enchantments"
    _FILE_NAME_BASE = "enchantments"
    _ROW_CLASS      = Enchantment


_EffectsBuilderData = _namedtuple(
    "EffectsBuilderData",
    "argument_table_name argument_title argument_mixin_class_name"
)

EFFECTS_BUILDER_DATA            = _OrderedDict( )
EFFECTS_BUILDER_DATA[ 0 ]       = _EffectsBuilderData(
    "null_arguments", "Nothing", "EffectArgument_Null"
)
EFFECTS_BUILDER_DATA[ 1 ]       = _EffectsBuilderData(
    "summons", "Summon", "EffectArgument_GenericSummon"
)
EFFECTS_BUILDER_DATA[ 2 ]       = _EffectsBuilderData(
    "normal_damage", "Damage (Hitpoints)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 3 ]       = _EffectsBuilderData(
    "stun_damage", "Damage (Stun)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 4 ]       = _EffectsBuilderData(
    "fear_type_1", "Fear (Type I)",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 7 ]       = _EffectsBuilderData(
    "mortal_poison", "Poison (Mortal)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 8 ]       = _EffectsBuilderData(
    "reinvigoration", "Healing (Fatigue) (?)",
    "EffectArgument_GenericHealing"
)
EFFECTS_BUILDER_DATA[ 10 ]      = _EffectsBuilderData(
    "buffs_1", "Bless/Buff (Type I)",
    "EffectArgument_Buffs1"
)
EFFECTS_BUILDER_DATA[ 11 ]      = _EffectsBuilderData(
    "special_damage", "Special Damage",
    "EffectArgument_SpecialDamage"
)
EFFECTS_BUILDER_DATA[ 13 ]      = _EffectsBuilderData(
    "healing", "Healing (Hitpoints) (?)",
    "EffectArgument_GenericHealing"
)
EFFECTS_BUILDER_DATA[ 15 ]      = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 19 ]      = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 20 ]      = _EffectsBuilderData(
    "blink_ranges", "Range (?)", "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 21 ]       = _EffectsBuilderData(
    "summons", "Monster (Commander)", "EffectArgument_GenericSummon"
)
EFFECTS_BUILDER_DATA[ 22 ]       = _EffectsBuilderData(
    "null_arguments", "Nothing", "EffectArgument_Null"
)
EFFECTS_BUILDER_DATA[ 23 ]      = _EffectsBuilderData(
    "buffs_2", "Bless/Buff (Type II)",
    "EffectArgument_Buffs2"
)
EFFECTS_BUILDER_DATA[ 24 ]      = _EffectsBuilderData(
    "holy_damage", "Holy Damage",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 25 ]      = _EffectsBuilderData(
    "null_arguments", "Nothing", "EffectArgument_Null"
)
EFFECTS_BUILDER_DATA[ 26 ]      = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 27 ]      = _EffectsBuilderData(
    "normal_damage", "Damage (Hitpoints) (?)",
    "EffectArgument_GenericDamage"
)
# TODO: Use a different superclass.
#       Damage 0 may have special meaning.
EFFECTS_BUILDER_DATA[ 28 ]      = _EffectsBuilderData(
    "monster_control", "Possession vs Monster (?)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 29 ]      = _EffectsBuilderData(
    "monster_control", "Charm vs Monster (?)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 30 ]      = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 31 ]      = _EffectsBuilderData(
    "summons", "Monster", "EffectArgument_GenericSummon"
)
EFFECTS_BUILDER_DATA[ 32 ]      = _EffectsBuilderData(
    "damage_vs_large", "Damage vs Large Monsters",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 33 ]      = _EffectsBuilderData(
    "damage_vs_small", "Damage vs Small Monsters",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 35 ]      = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 37 ]       = _EffectsBuilderData(
    "summons", "Monster", "EffectArgument_GenericSummon"
)
EFFECTS_BUILDER_DATA[ 38 ]       = _EffectsBuilderData(
    "summons", "Monster", "EffectArgument_GenericSummon"
)
EFFECTS_BUILDER_DATA[ 39 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 40 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 41 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 42 ]       = _EffectsBuilderData(
    "anon_province_events", "Anonymous Province Event",
    "EffectArgument_AnonymousProvinceEvent"
)
EFFECTS_BUILDER_DATA[ 43 ]      = _EffectsBuilderData(
    "summons", "Monster", "EffectArgument_GenericSummon"
)
EFFECTS_BUILDER_DATA[ 44 ]      = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 46 ]      = _EffectsBuilderData(
    "stun_poison", "Poison (Stun)",
    "EffectArgument_GenericValue"
)
# TODO: Use a different table.
EFFECTS_BUILDER_DATA[ 48 ]       = _EffectsBuilderData(
    "magic_paths", "Magic Path",
    "EffectArgument_MagicPath"
)
EFFECTS_BUILDER_DATA[ 49 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 50 ]       = _EffectsBuilderData(
    "summons", "Monster", "EffectArgument_GenericSummon"
)
EFFECTS_BUILDER_DATA[ 53 ]      = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 54 ]      = _EffectsBuilderData(
    "polymorphs", "Monster", "EffectArgument_GenericSummon"
)
EFFECTS_BUILDER_DATA[ 57 ]       = _EffectsBuilderData(
    "normal_damage", "Damage (Hitpoints) (?)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 62 ]       = _EffectsBuilderData(
    "summons", "Monster", "EffectArgument_GenericSummon"
)
EFFECTS_BUILDER_DATA[ 63 ]      = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 64 ]      = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 66 ]      = _EffectsBuilderData(
    "paralysis", "Paralysis",
    "EffectArgument_GenericValue"
)
# TODO? Use a different superclass.
EFFECTS_BUILDER_DATA[ 67 ]      = _EffectsBuilderData(
    "weakness", "Damage (Strength) (?)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 68 ]      = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 70 ]      = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 72 ]      = _EffectsBuilderData(
    "life_overload_damage", "Damage (Hitpoints) (?)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 73 ]      = _EffectsBuilderData(
    "damage_vs_magic", "Damage vs Magic Creatures",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 74 ]      = _EffectsBuilderData(
    "unlife_damage", "Unlife Damage (?)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 75 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 76 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 77 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 79 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 80 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 81 ]      = _EffectsBuilderData(
    "enchantments", "Enchantment", "EffectArgument_Enchantment"
)
EFFECTS_BUILDER_DATA[ 82 ]      = _EffectsBuilderData(
    "enchantments", "Enchantment", "EffectArgument_Enchantment"
)
EFFECTS_BUILDER_DATA[ 84 ]       = _EffectsBuilderData(
    "enchantments", "Enchantment", "EffectArgument_Enchantment"
)
EFFECTS_BUILDER_DATA[ 85 ]       = _EffectsBuilderData(
    "null_arguments", "No Argument", "EffectArgument_Null"
)
EFFECTS_BUILDER_DATA[ 86 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 89 ]       = _EffectsBuilderData(
    "special_unique_summons", "Unique Monster Group",
    "EffectArgument_SpecialUniqueSummon"
)
EFFECTS_BUILDER_DATA[ 90 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 91 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 92 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 93 ]       = _EffectsBuilderData(
    "summons", "Monster", "EffectArgument_GenericSummon"
)
EFFECTS_BUILDER_DATA[ 94 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 95 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 96 ]      = _EffectsBuilderData(
    "damage_vs_constructs", "Damage vs Constructs",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 97 ]      = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 98 ]       = _EffectsBuilderData(
    "null_arguments", "Nothing", "EffectArgument_Null"
)
EFFECTS_BUILDER_DATA[ 99 ]      = _EffectsBuilderData(
    "petrification", "Petrification (?)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 100 ]       = _EffectsBuilderData(
    "terrain_specific_summons", "Terrain-Specific Monster Group",
    "EffectArgument_TerrainSpecificSummon"
)
# TODO: Use a different superclass.
EFFECTS_BUILDER_DATA[ 101 ]     = _EffectsBuilderData(
    "aging", "Number of Years",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 102 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 103 ]     = _EffectsBuilderData(
    "life_drain", "Life Drain (Hitpoints) (?)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 104 ]     = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 105 ]     = _EffectsBuilderData(
    "null_arguments", "No Argument", "EffectArgument_Null"
)
EFFECTS_BUILDER_DATA[ 106 ]     = _EffectsBuilderData(
    "damage_vs_demons", "Damage (?)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 107 ]     = _EffectsBuilderData(
    "damage_vs_demons", "Damage",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 108 ]     = _EffectsBuilderData(
    "other_planes", "Plane", "EffectArgument_OtherPlane"
)
# TODO: Use a different superclass.
EFFECTS_BUILDER_DATA[ 109 ]     = _EffectsBuilderData(
    "capped_damage", "Capped Damage (Hitpoints)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 110 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 111 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 112 ]       = _EffectsBuilderData(
    "normal_damage", "Damage (Hitpoints) (?)",
    "EffectArgument_GenericDamage"
)
EFFECTS_BUILDER_DATA[ 113 ]       = _EffectsBuilderData(
    "null_arguments", "No Argument", "EffectArgument_Null"
)
EFFECTS_BUILDER_DATA[ 114 ]       = _EffectsBuilderData(
    "special_unique_summons", "Unique Monster Group",
    "EffectArgument_SpecialUniqueSummon"
)
EFFECTS_BUILDER_DATA[ 115 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 116 ]     = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 117 ]       = _EffectsBuilderData(
    "alchemy", "Gems", "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 118 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 119 ]       = _EffectsBuilderData(
    "summons", "Monster", "EffectArgument_GenericSummon"
)
EFFECTS_BUILDER_DATA[ 120 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 500 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 504 ]     = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 509 ]       = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 514 ]     = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 524 ]     = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 599 ]     = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 600 ]     = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 601 ]     = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)
EFFECTS_BUILDER_DATA[ 609 ]     = _EffectsBuilderData(
    "unknown_arguments", "<Unknown Argument Type>",
    "EffectArgument_GenericValue"
)


class EffectInfo( _DataTableRow_NamedInteger ):
    """ Information on an effect. """


    __tablename__   = "effects_info"


    _TITLE          = "Effect {Spl: #effect}"


class EffectsInfo_DataTable( _DataTable_NamedInteger, _DataTable_CSV ):
    """ A table of information on effects. """


    _TITLE          = "Effects Information {Spl: #effect}"
    _LABEL          = "Effects Information"
    _FILE_NAME_BASE = "effects-info"
    _ROW_CLASS      = EffectInfo


class EffectModifierBit( _DataTableRow_NamedBits ):
    """ An effect modifier bit. """


    __tablename__   = "effect_modifier_bits"


class EffectModifierBits_DataTable( _DataTable_NamedBits, _DataTable_CSV ):
    """ A bitmask table of effect modifiers. """


    _TITLE          = "Effect Modifiers {Spl: #spec}"
    _LABEL          = "Effect Modifier Bits"
    _FILE_NAME_BASE = "effect-modifier-bits"
    _ROW_CLASS      = EffectModifierBit


class FlightSprite( _DataTableRow_NamedInteger ):
    """ A sprite for an in-flight effect delivery. """


    __tablename__   = "flight_sprites"


    _TITLE          = "Flight Sprite {Spl: #flightspr, Wpn: #flyspr}"


class FlightSprites_DataTable( _DataTable_NamedInteger, _DataTable_CSV ):
    """ A table of sprites for in-flight effects delivery. """


    _TITLE          = "Flight Sprites {Spl: #flightspr, Wpn: #flyspr}"
    _LABEL          = "Flight Sprites"
    _FILE_NAME_BASE = "flight-sprites"
    _ROW_CLASS      = FlightSprite


class ExplosionSprite( _DataTableRow_NamedInteger ):
    """ A sprite for an explosion effect."""


    __tablename__   = "explosion_sprites"


    _TITLE          = "Explosion Sprite {Spl: #explspr, Wpn: #explspr}"


class ExplosionSprites_DataTable( _DataTable_NamedInteger, _DataTable_CSV ):
    """ A table of sprites for explosion effects."""


    _TITLE          = "Explosion Sprites {Spl: #explspr, Wpn: #explspr}"
    _LABEL          = "Explosion Sprites"
    _FILE_NAME_BASE = "explosion-sprites"
    _ROW_CLASS      = ExplosionSprite


class Effect( _DataTableRow ):
    """ A generic effect. """


    __tablename__   = "effects"


    record_id           = _SQLA_Column(
        _SQLA_Integer, primary_key = True, autoincrement = "ignore_fk"
    )
    effect_number       = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
              EffectInfo.TABLE_NAME( ) + "." + EffectInfo.KEY_NAME( )
        )
    )
    duration                = _SQLA_Column( _SQLA_Integer )
    ritual                  = _SQLA_Column( _SQLA_Boolean, default = False )
    # TODO? Place a foreign key on a table of object types.
    object_type             = _SQLA_Column( _SQLA_String )
    raw_argument            = _SQLA_Column( _SQLA_Integer )
    modifiers_mask          = _SQLA_Column( _SQLA_Integer )
    modifiers               = _SQLA_relationship( "EffectModifier" )
    range_base              = _SQLA_Column( _SQLA_Integer )
    range_per_level         = _SQLA_Column( _SQLA_Integer )
    range_strength_divisor  = _SQLA_Column( _SQLA_Integer )
    area_base               = _SQLA_Column( _SQLA_Integer )
    area_per_level          = _SQLA_Column( _SQLA_Integer )
    area_battlefield_pct    = _SQLA_Column( _SQLA_Integer )
    sound_number            = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey( Sound.TABLE_NAME( ) + "." + Sound.KEY_NAME( ) )
    )
    flight_sprite_number    = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
            FlightSprite.TABLE_NAME( ) + "." + FlightSprite.KEY_NAME( )
        )
    )
    flight_sprite_length    = _SQLA_Column( _SQLA_Integer )
    explosion_sprite_number = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
              ExplosionSprite.TABLE_NAME( ) + "."
            + ExplosionSprite.KEY_NAME( )
        )
    )
    explosion_sprite_length = _SQLA_Column( _SQLA_Integer )


    @classmethod
    def __declare_last__( cls ):
        # Perform late binding against abstract concrete bases.
        cls.argument = _SQLA_relationship( EffectArgument, uselist = False )


    _KEY_NAME       = "record_id"

    _AREA_BATTLEFIELD_PERCENTAGES = {
        666: 100, 663: 50, 665: 25, 664: 10, 662: 5
    }


    @classmethod
    def from_raw_data( cls,
        effect_number, object_type, raw_argument, modifiers_mask,
        raw_range, raw_area, sound_number,
        flight_sprite_number, flight_sprite_length,
        explosion_sprite_number, explosion_sprite_length
    ):
        """ Creates an instance from a set of raw arguments. """

        args = { "effect_number": effect_number % 1000 }
        args[ "object_type" ] = object_type

        if   10000 <= effect_number:
            args[ "ritual" ] = True
        elif 1000 <= effect_number:
            args[ "duration" ] = effect_number // 1000

        args[ "raw_argument" ] = raw_argument
        args[ "modifiers_mask" ] = modifiers_mask

        if 0 > raw_range:
            args[ "range_strength_divisor" ] = -raw_range
        else:
            args[ "range_base" ] = raw_range % 1000
            args[ "range_per_level" ] = raw_range // 1000

        if raw_area in cls._AREA_BATTLEFIELD_PERCENTAGES:
            args[ "area_battlefield_pct" ] \
            = cls._AREA_BATTLEFIELD_PERCENTAGES[ raw_area ]
        else:
            args[ "area_base" ] = raw_area % 1000
            args[ "area_per_level" ] = raw_area // 1000

        args[ "sound_number" ] = sound_number
        if 0 <= flight_sprite_number:
            args[ "flight_sprite_number" ] = flight_sprite_number
            args[ "flight_sprite_length" ] = flight_sprite_length
        if 0 <= explosion_sprite_number:
            args[ "explosion_sprite_number" ] = explosion_sprite_number
            args[ "explosion_sprite_length" ] = explosion_sprite_length

        self = cls( **args )

        self.argument = eval(
            "Effect{effect_number}Argument.from_raw_argument".format(
                effect_number = args[ "effect_number" ]
            )
        )(
            effect_record_id = self.record_id,
            raw_argument = raw_argument
        )

        modifiers = [ ]
        for bit_number in range( 64 ):
            bit_value = 2 ** bit_number
            if bit_value & modifiers_mask:
                modifiers.append( EffectModifier(
                    effect_record_id = self.record_id,
                    bit_value = bit_value
                ) )
        self.modifiers = modifiers

        return self


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        pformat_config_1 = pformat_config.clone(
            indent = pformat_config.indent + 4 * " "
        )
        pformat_config_title = pformat_config.clone(
            indent = ""
        )
        template = "{value}"
        args = {
            "value":
            self._pformat_object( tables, pformat_config = pformat_config_1 )
        }

        if pformat_config.render_title:
            args[ "title" ] \
            = tables[ EffectsInfo_DataTable.LABEL( ) ].pformat_table_lookup(
                self.effect_number, tables,
                pformat_config = pformat_config_title
            )
            template = "{title}\n" + template

        template = pformat_config.indent + template

        return template.format( **args )


    def _pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display.
            (Internal version - override as necessary.) """

        pformat_config_list = pformat_config.clone(
            indent = pformat_config.indent + 4 * " ", render_title = False
        )

        output = [ ]
        indent = pformat_config.indent

        if self.ritual:
            output.append( indent + "Ritual [{effect_number}]".format(
                effect_number = self.effect_number + 10000 
            ) )
        if self.duration:
            output.append(
                indent + "Duration (?): {duration} [{effect_number}]".format(
                    duration = self.duration,
                    effect_number = self.effect_number + 1000 * self.duration
                )
            )

        output.append( self.argument.pformat_object(
            tables, pformat_config = pformat_config
        ) )

        if self.modifiers:
            output.append(
                  indent
                + "Modifiers {{Spl: #spec}}: [Total Mask: {mask}]".format(
                    mask = self.modifiers_mask
                )
            )
            for modifier in self.modifiers:
                output.append( modifier.pformat_object(
                    tables, pformat_config = pformat_config_list
                ) )

        template = indent + "Range {{Spl: #range, Wpn: #range}}: "
        args = { }
        if self.range_base:
            template += "{range_base} squares"
            args[ "range_base" ] = self.range_base
            if self.range_per_level:
                template += " + {range_per_level} per caster level"
                args[ "range_per_level" ] = self.range_per_level
            output.append( template.format( **args ) )
        elif self.range_strength_divisor:
            template += "wielder's strength, "
            template += "divided by {range_strength_divisor}"
            args[ "range_strength_divisor" ] = self.range_strength_divisor
            output.append( template.format( **args ) )

        template = indent + "Area {{Spl: #aoe, Wpn: #aoe}}: "
        args = { }
        if self.area_base:
            template += "{area_base} squares"
            args [ "area_base" ] = self.area_base
            if self.area_per_level:
                template += " + {area_per_level} per caster level"
                args[ "area_per_level" ] = self.area_per_level
            output.append( template.format( **args ) )
        elif self.area_battlefield_pct:
            template += "{area_battlefield_pct}% of battlefield"
            args [ "area_battlefield_pct" ] = self.area_battlefield_pct
            output.append( template.format( **args ) )

        if self.sound_number:
            output.append(
                tables[ Sounds_DataTable.LABEL( ) ].pformat_table_lookup(
                    self.sound_number, tables,
                    pformat_config = pformat_config
                )
            )

        if self.flight_sprite_number:
            output.append(
                tables[ FlightSprites_DataTable.LABEL( ) ]\
                .pformat_table_lookup(
                    self.flight_sprite_number, tables,
                    pformat_config = pformat_config
                ) + " (Length: {length})".format(
                    length = self.flight_sprite_length
                )
            )

        if self.explosion_sprite_number:
            output.append(
                tables[ ExplosionSprites_DataTable.LABEL( ) ]\
                .pformat_table_lookup(
                    self.explosion_sprite_number, tables,
                    pformat_config = pformat_config
                ) + " (Length: {length})".format(
                    length = self.explosion_sprite_length
                )
            )

        return "\n".join( output )


class Effect_ForeignKey( _DataTableRow ):
    """ Abstraction for effect record ID as a foreign key. """


    __abstract__    = True


    @_SQLA_declared_attr
    def effect_record_id( cls ):
        return _SQLA_Column(
            _SQLA_Integer,
            _SQLA_ForeignKey(
                Effect.TABLE_NAME( ) + "." + Effect.KEY_NAME( )
            ),
            primary_key = True
        )


    _KEY_NAME       = "effect_record_id"
    _KEY_FORMAT     = "d"


class EffectModifier( Effect_ForeignKey ):
    """ A modifier of an effect. """


    __tablename__   = "effect_modifiers"


    bit_value       = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
              EffectModifierBit.TABLE_NAME( ) + "."
            + EffectModifierBit.KEY_NAME( )
        ),
        primary_key = True
    )


    _KEY_NAME       = "bit_value"
    _KEY_FORMAT     = "d"


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        return \
        tables[ EffectModifierBits_DataTable.LABEL( ) ].pformat_table_lookup(
            self.bit_value, tables, pformat_config = pformat_config
        )


class EffectArgument_BASE( _DataTableRow ):
    """ An argument to an effect. """


    __abstract__    = True


    _MOD_TAGS       = "{Spl: #damage, Wpn: #dmg}"


    @classmethod
    def TITLE( cls ):
        """ Returns the title of the object class. """

        return "{title} {mod_tags}".format(
            title = cls._TITLE, mod_tags = cls._MOD_TAGS
        )


    @classmethod
    def generated_SQLA_Table( cls, argument_table_name ):
        """ Returns a SQLAlchemy table to be mapped to an object. """

        return _SQLA_Table(
            argument_table_name + "_by_effect", cls.metadata, 
            _SQLA_Column( "record_id",  _SQLA_Integer, primary_key = True ),
            _SQLA_Column(
                "effect_record_id", _SQLA_Integer,
                _SQLA_ForeignKey(
                    Effect.TABLE_NAME( ) + "." + Effect.KEY_NAME( )
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
    def generated_SQLA_Mapper_arguments( cls, effect_number ):
        """ Returns additional arguments for the SQLAlchemy mapper. """

        return { }


    @classmethod
    def from_raw_argument( cls,
        effect_record_id, raw_argument
    ):
        """ Creates an instance from a raw argument.
            (Dummy implementation - override.) """

        return cls( effect_record_id = effect_record_id )


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        return pformat_config.indent + "{title}: <Unimplemented>".format(
            title = self.TITLE( )
        )


class EffectArgument_GenericValue( EffectArgument_BASE ):
    """ An argument to an effect. """


    __abstract__    = True


    @classmethod
    def _generated_SQLA_Table_columns( cls ):
        """ Returns additional SQLAlchemy columns for a table mapping. """

        return [
            _SQLA_Column( "value", _SQLA_Integer ) 
        ]


    @classmethod
    def from_raw_argument( cls, effect_record_id, raw_argument ):
        """ Creates an instance from a raw argument. """

        args = { "effect_record_id": effect_record_id }
        args[ "value" ] = raw_argument

        return cls( **args )


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        template = "{title}: {value}"
        args = { "title": self.TITLE( ), "value": self.value }

        template = pformat_config.indent + template

        return template.format( **args )


class EffectArgument_Null( EffectArgument_GenericValue ):
    """ An argument to an effect. """


    __abstract__    = True


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        template = "{title}"
        args = { "title": self.TITLE( ) }

        if self.value:
            template = "{title}: {value}"
            args[ "value" ] = self.value

        template = pformat_config.indent + template

        return template.format( **args )


class EffectArgument_GenericHealing( EffectArgument_BASE ):
    """ An argument to an effect. """


    __abstract__    = True


    @classmethod
    def _generated_SQLA_Table_columns( cls ):
        """ Returns additional SQLAlchemy columns for a table mapping. """

        # TODO? Break out base value and per-level value.
        return [
            _SQLA_Column( "healing", _SQLA_Integer ) 
        ]


    @classmethod
    def from_raw_argument( cls, effect_record_id, raw_argument ):
        """ Creates an instance from a raw argument. """

        args = { "effect_record_id": effect_record_id }
        # TODO? Break out base value and per-level value.
        args[ "healing" ] = raw_argument

        return cls( **args )


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        template = "{title}: {healing}"
        args = { "title": self.TITLE( ), "healing": self.healing }

        template = pformat_config.indent + template

        return template.format( **args )


class EffectArgument_GenericSummon( EffectArgument_BASE ):
    """ An argument to an effect. """


    __abstract__    = True


    @classmethod
    def _generated_SQLA_Table_columns( cls ):
        """ Returns additional SQLAlchemy columns for a table mapping. """

        return [
            # TODO: Add foreign key on monsters table.
            _SQLA_Column( "monster_number", _SQLA_Integer ),
            _SQLA_Column(
                "monster_group_tag",
                _SQLA_Integer,
                _SQLA_ForeignKey(
                    MonsterTag.TABLE_NAME( ) + "." + MonsterTag.KEY_NAME( )
                )
            ) 
        ]


    @classmethod
    def from_raw_argument( cls, effect_record_id, raw_argument ):
        """ Creates an instance from a raw argument. """

        args = { "effect_record_id": effect_record_id }
        if 0 > raw_argument:
            args[ "monster_group_tag" ] = raw_argument
        else:
            args[ "monster_number" ] = raw_argument

        return cls( **args )


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        template = ""
        args = { }

        if None is not self.monster_number:
            template += pformat_config.indent + "{title}: {monster_number}"
            args[ "title" ] = self.TITLE( )
            args[ "monster_number" ] = self.monster_number
        else:
            template += "{monster_group_summary}"
            args[ "monster_group_summary" ] \
            = tables[ MonsterTags_DataTable.LABEL( ) ].pformat_table_lookup(
                self.monster_group_tag, tables,
                pformat_config = pformat_config
            )

        return template.format( **args )


class EffectArgument_GenericDamage( EffectArgument_BASE ):
    """ An argument to an effect. """


    __abstract__    = True


    _SPECIAL_VALUE_TOTALLY_DAMAGE   = 999


    @classmethod
    def _generated_SQLA_Table_columns( cls ):
        """ Returns additional SQLAlchemy columns for a table mapping. """

        return [
            _SQLA_Column( "damage_base", _SQLA_Integer ),
            _SQLA_Column( "damage_per_level", _SQLA_Integer ),
            _SQLA_Column( "totally_damage", _SQLA_Boolean )
        ]


    @classmethod
    def from_raw_argument( cls, effect_record_id, raw_argument ):
        """ Creates an instance from a raw argument. """

        args = { "effect_record_id": effect_record_id }

        args[ "totally_damage" ] \
        = cls._SPECIAL_VALUE_TOTALLY_DAMAGE == raw_argument
        if not args[ "totally_damage" ]:
            if 0 > raw_argument:
                args[ "damage_base" ]       = raw_argument
                args[ "damage_per_level" ]  = 0
            else:
                args[ "damage_base" ]       = raw_argument % 1000
                args[ "damage_per_level" ]  = raw_argument // 1000

        return cls( **args )


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        template = "{title}: "
        args = { "title": self.TITLE( ) }

        if self.totally_damage:
            template = template + "{message} [{value}]"
            args[ "message" ] = self._MESSAGE_TOTALLY_DAMAGE
            args[ "value" ] = self._SPECIAL_VALUE_TOTALLY_DAMAGE
        else:
            template = template + "{damage_base}"
            args[ "damage_base" ] = self.damage_base
            if self.damage_per_level:
                template = template + " + {damage_per_level} per caster level"
                args[ "damage_per_level" ] = self.damage_per_level

        template = pformat_config.indent + template
        return template.format( **args )


_IndexAssociationTableBuilderData \
= _namedtuple(
    "IndexAssociationTableBuilderData",
    "class_name_base table_name_base key_name title_base"
)
for _builder_data in [
    _IndexAssociationTableBuilderData(
        "Enchantment", "enchantments", "enchantment", "Enchantment"
    ),
    _IndexAssociationTableBuilderData(
        "MagicPath", "magic_paths", "path", "Magic Path"
    ),
    _IndexAssociationTableBuilderData(
        "AnonymousProvinceEvent", "anon_province_events", "event",
        "Anonymous Province Event"
    ),
    _IndexAssociationTableBuilderData(
        "SpecialUniqueSummon", "special_unique_summons", "monster_group",
        "Special Unique Monster Group"
    ),
    _IndexAssociationTableBuilderData(
        "TerrainSpecificSummon", "terrain_specific_summons",
        "monster_group", "Terrain-Specific Monster Group"
    ),
    _IndexAssociationTableBuilderData(
        "OtherPlane", "other_planes", "plane", "Plane"
    ),
]:
    exec( """
class Effect{class_name_base}_ASSOCIATE( _DataTableRow ):
    ''' An indexed type associated with an effect. '''


    __tablename__   = "{table_name_base}_for_effects"


    effect_argument_record_id   = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey( "{table_name_base}_by_effect.record_id" ),
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


    _TITLE          = "{title_base}"
    _KEY_NAME       = "{key_name}"
    _KEY_FORMAT     = "d"


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        ''' Nicely formats the object for display. '''

        return \\
        tables[ {class_name_base}s_DataTable.LABEL( ) ]\\
        .pformat_table_lookup(
            self.{key_name}, tables,
            pformat_config = pformat_config
        )


class EffectArgument_{class_name_base}( EffectArgument_BASE ):
    ''' An argument to an effect. '''


    __abstract__    = True


    @_SQLA_declared_attr
    def {key_name}( cls ):
        return _SQLA_relationship(
            Effect{class_name_base}_ASSOCIATE, uselist = False
        ) 


    @classmethod
    def from_raw_argument( cls, effect_record_id, raw_argument ):
        ''' Creates an instance from a raw argument. '''

        args = {{ "effect_record_id": effect_record_id }}

        self = cls( **args )

        self.{key_name} = Effect{class_name_base}_ASSOCIATE(
            {key_name} = raw_argument
        )

        return self


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        ''' Nicely formats the object for display. '''

        pformat_config_1 = pformat_config.clone(
            indent = "", render_title = False
        )

        template \\
        = pformat_config.indent + "{{title}}: {{{key_name}}}"
        args = {{ "title": self.TITLE( ) }}
        args[ "{key_name}" ] \\
        = self.{key_name}.pformat_object(
            tables, pformat_config = pformat_config_1
        )

        return template.format( **args )


    """.format( **vars( _builder_data ) ) )


_BitmaskAssociationTableBuilderData \
= _namedtuple(
    "BitmaskAssociationTableBuilderData",
    "class_name_base table_name_base title_base"
)
for _builder_data in [
    _BitmaskAssociationTableBuilderData(
        "SpecialDamage", "special_damage", "Special Damage"
    ),
    _BitmaskAssociationTableBuilderData(
        "Buffs1", "buffs_1", "Blessings/Buffs (Type I)"
    ),
    _BitmaskAssociationTableBuilderData(
        "Buffs2", "buffs_2", "Blessings/Buffs (Type II)"
    ),
]:
    exec( """
class Effect{class_name_base}Type( _DataTableRow ):
    ''' A bitmaskable type associated with an effect. '''


    __tablename__   = "{table_name_base}_types_by_effect"


    _TITLE          = "{title_base} Type"
    _KEY_NAME       = "{table_name_base}_type"
    _KEY_FORMAT     = "d"


    effect_argument_record_id   = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey( "{table_name_base}_by_effect.record_id" ),
        primary_key = True
    )
    {table_name_base}_type      = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
              {class_name_base}Type.TABLE_NAME( )
            + "." + {class_name_base}Type.KEY_NAME( )
        ),
        primary_key = True
    )


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        ''' Nicely formats the object for display. '''

        return \\
        tables[ {class_name_base}Types_DataTable.LABEL( ) ]\\
        .pformat_table_lookup(
            self.{table_name_base}_type, tables,
            pformat_config = pformat_config
        )


class EffectArgument_{class_name_base}( EffectArgument_BASE ):
    ''' An argument to an effect. '''


    __abstract__    = True


    @_SQLA_declared_attr
    def {table_name_base}_types( cls ):
        return _SQLA_relationship( Effect{class_name_base}Type )


    @classmethod
    def from_raw_argument( cls, effect_record_id, raw_argument ):
        ''' Creates an instance from a raw argument. '''

        args = {{ "effect_record_id": effect_record_id }}

        self = cls( **args )

        {table_name_base}_types = [ ]
        for bit_position in range( 64 ):
            bit_value = 2 ** bit_position
            if raw_argument & bit_value:
                {table_name_base}_types.append( Effect{class_name_base}Type(
                    {table_name_base}_type = bit_value
                ) )
        self.{table_name_base}_types = {table_name_base}_types

        return self


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        ''' Nicely formats the object for display. '''

        pformat_config_1 = pformat_config.clone(
            indent = pformat_config.indent + 4 * " ", render_title = False
        )

        template \\
        = pformat_config.indent + "{{title}}:\\n{{{table_name_base}_types}}"
        args = {{ "title": self.TITLE( ) }}
        args[ "{table_name_base}_types" ] = "\\n".join( [
            {table_name_base}_type.pformat_object(
                tables, pformat_config = pformat_config_1
            )
            for {table_name_base}_type in self.{table_name_base}_types
        ] )

        return template.format( **args )


    """.format( **vars( _builder_data ) ) )


_effect_tables_polymorphic_map = { }
for _effect_number, _builder_data in EFFECTS_BUILDER_DATA.items( ):
    exec( """
_effect_tables_polymorphic_map[ {effect_number} ] \\
= {argument_mixin_class_name}.generated_SQLA_Table( "{argument_table_name}" )
    """.format(
        effect_number = _effect_number,
        **vars( _builder_data )
    ) )

_effect_tables_polymorphic_union = _SQLA_polymorphic_union(
    _effect_tables_polymorphic_map, "effect_number",
    aliasname = "effect_union"
)


class EffectArgument( _DataTableRow ):
    """ An argument to an effect. """

    _punion         = _effect_tables_polymorphic_union

    __table__       = _punion
    __mapper_args__ = { "polymorphic_on": _punion.c.effect_number }


for _effect_number, _builder_data in EFFECTS_BUILDER_DATA.items( ):
    exec( """
class Effect{effect_number}Argument(
    EffectArgument, {argument_mixin_class_name}
):
    ''' The argument to an effect. '''


    __table__           = _effect_tables_polymorphic_map[ {effect_number} ]
    __mapper_args__ = {{
        "polymorphic_identity": {effect_number},
        "concrete": True
    }}
    __mapper_args__.update(
        {argument_mixin_class_name}.generated_SQLA_Mapper_arguments(
            {effect_number}
        )
    )


    _TITLE         = "{argument_title}"


    """.format(
        effect_number = _effect_number,
        **vars( _builder_data )
    ) )


Effect2Argument._MESSAGE_TOTALLY_DAMAGE = "Instant Death on Hit"
Effect3Argument._MESSAGE_TOTALLY_DAMAGE = "Instant Unconsciousness on Hit"
Effect27Argument._MESSAGE_TOTALLY_DAMAGE = "Instant Death on Hit"
Effect28Argument._MESSAGE_TOTALLY_DAMAGE = "Instantly Controlled on Hit"
Effect29Argument._MESSAGE_TOTALLY_DAMAGE = "Instantly Charmed on Hit"
Effect57Argument._MESSAGE_TOTALLY_DAMAGE = "Instantly Feeble-Minded on Hit (?)"
# TODO? Use a different superclass.
Effect67Argument._MESSAGE_TOTALLY_DAMAGE = "Instant Death on Hit (?)"
Effect72Argument._MESSAGE_TOTALLY_DAMAGE = "Instant Death on Hit (?)"
Effect73Argument._MESSAGE_TOTALLY_DAMAGE = "Instant Banishment on Hit (?)"
Effect96Argument._MESSAGE_TOTALLY_DAMAGE = "Instant Destruction on Hit (?)"
Effect99Argument._MESSAGE_TOTALLY_DAMAGE = "Instant Petrification on Hit"
Effect103Argument._MESSAGE_TOTALLY_DAMAGE = "Instant Death on Hit (?)"
# TODO: Use a different superclass.
Effect109Argument._MESSAGE_TOTALLY_DAMAGE = "Instant Death on Hit"
Effect112Argument._MESSAGE_TOTALLY_DAMAGE = "Instant Death on Hit"
     

###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #
