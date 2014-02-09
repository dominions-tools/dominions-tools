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

""" Weapons. """


__docformat__ = "reStructuredText"


from collections import (
    OrderedDict                 as _OrderedDict,
)

from sqlalchemy import (
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


from dominions.utils import (
    from_native_uint16      as _from_native_uint16,
    from_native_int16       as _from_native_int16,
    from_native_uint32      as _from_native_uint32,
    from_native_int64       as _from_native_int64,
    from_string             as _from_string,
    PLATFORM_LINUX          as _PLATFORM_LINUX,
    PLATFORM_MACOSX         as _PLATFORM_MACOSX,
    PLATFORM_WINDOWS        as _PLATFORM_WINDOWS,
    PrettyFormatConfig      as _PrettyFormatConfig,
)
from dominions.DataTable import (
    DataTableRow                as _DataTableRow,
    DataTable_CSV               as _DataTable_CSV,
    DataTableRow_ProgramImage   as _DataTableRow_ProgramImage,
    DataTable_ProgramImage      as _DataTable_ProgramImage,
    DataTableRow_NamedInteger   as _DataTableRow_NamedInteger,
    DataTable_NamedInteger      as _DataTable_NamedInteger,
    DataTableRow_UnknownField   as _DataTableRow_UnknownField,
)
from dominions.Attribute import (
    Attribute               as _Attribute,
    Attribute_ForeignKey    as _Attribute_ForeignKey,
)
from dominions.Effect import (
    Effect                  as _Effect,
)


class Weapon( _DataTableRow_NamedInteger, _DataTableRow_ProgramImage ):
    """ A weapon. """


    __tablename__   = "weapons"


    effect_record_id        = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey( _Effect.TABLE_NAME( ) + "." + _Effect.KEY_NAME( ) )
    )
    effect                  = _SQLA_relationship(
        _Effect, uselist = False, 
        primaryjoin = effect_record_id == _Effect.record_id
    )
    attack                  = _SQLA_Column( _SQLA_Integer ) 
    defense                 = _SQLA_Column( _SQLA_Integer )
    length                  = _SQLA_Column( _SQLA_Integer )
    attack_rate             = _SQLA_Column( _SQLA_Integer )
    attacks_total           = _SQLA_Column( _SQLA_Integer )
    secondary_effect_on_hit = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
            __tablename__ + "." + _DataTableRow_NamedInteger.KEY_NAME( )
        )
    )
    secondary_effect_always = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
            __tablename__ + "." + _DataTableRow_NamedInteger.KEY_NAME( )
        )
    )
    resource_cost           = _SQLA_Column( _SQLA_Integer )

    attributes              = _SQLA_relationship( "_WeaponAttribute" )
    unknown_fields          = _SQLA_relationship( "WeaponUnknownField" )


    _TITLE                      = "Weapon"
    _PROGRAM_IMAGE_RECORD_SIZES = {
        "4.03": 112, "4.04": 112,
    }


    @classmethod
    def from_program_image(
        cls, program_image, base_offset, number, dominions_version
    ):
        """ Creates an instance from a program image. """

        # TODO: Version this constant.
        NAME_LENGTH     = 36

        offset = base_offset
        
        unknowns = _OrderedDict( )
        
        name, __ = _from_string( program_image, offset, NAME_LENGTH )
        if "end" == name: raise StopIteration( )
        offset += NAME_LENGTH

        unknowns[ offset ], offset \
        = _from_native_uint32( program_image, offset )

        effect_argument, offset \
        = _from_native_int64( program_image, offset )

        attack, offset = _from_native_int16( program_image, offset )

        defense, offset = _from_native_int16( program_image, offset )

        effect_number, offset = _from_native_uint16( program_image, offset )

        length, offset = _from_native_uint16( program_image, offset )

        range_of_effect, offset = _from_native_int16( program_image, offset )

        attack_rate, offset = _from_native_int16( program_image, offset )

        attacks_total, offset = _from_native_uint16( program_image, offset )

        unknowns[ offset ], offset \
        = _from_native_uint16( program_image, offset )

        effect_modifiers, offset = _from_native_int64( program_image, offset )

        secondary_effect, offset = _from_native_int16( program_image, offset )
        if 0 > secondary_effect:
            secondary_effect_always = -secondary_effect
            secondary_effect_on_hit = 0
        else:
            secondary_effect_always = 0
            secondary_effect_on_hit = secondary_effect

        flight_sprite_number, offset \
        = _from_native_int16( program_image, offset )
        flight_sprite_length, offset \
        = _from_native_uint16( program_image, offset )

        explosion_sprite_number, offset \
        = _from_native_int16( program_image, offset )
        explosion_sprite_length, offset \
        = _from_native_uint16( program_image, offset )

        area_of_effect, offset = _from_native_uint16( program_image, offset )

        sound_number, offset = _from_native_uint16( program_image, offset )

        resource_cost, offset = _from_native_uint16( program_image, offset )

        attribute_keys = [ ]
        for i in range( 3 ):
            attribute_key, offset \
            = _from_native_uint32( program_image, offset )
            attribute_keys.append( attribute_key )

        attribute_values = [ ]
        for i in range( 3 ):
            attribute_value, offset \
            = _from_native_uint32( program_image, offset )
            attribute_values.append( attribute_value )

        attributes = [ ]
        for key, value in zip( attribute_keys, attribute_values ):
            if not key: continue
            attributes.append( _WeaponAttribute.from_raw_data(
                weapon_number = number,
                attribute_number = key,
                raw_value = value
            ) )

        unknown_fields = [
            WeaponUnknownField(
                weapon_number = number,
                offset = offset, value = value
            )
            for offset, value in unknowns.items( ) if value
        ]

        effect = _Effect.from_raw_data(
            effect_number = effect_number,
            object_type = cls.TITLE( ),
            raw_argument = effect_argument,
            modifiers_mask = effect_modifiers,
            raw_range = range_of_effect,
            raw_area = area_of_effect,
            sound_number = sound_number,
            flight_sprite_number = flight_sprite_number,
            flight_sprite_length = flight_sprite_length,
            explosion_sprite_number = explosion_sprite_number,
            explosion_sprite_length = explosion_sprite_length
        )

        return cls(
            number = number, name = name,
            effect_record_id = effect.record_id,
            effect = effect,
            attack = attack, defense = defense,
            attack_rate = attack_rate, attacks_total = attacks_total,
            length = length,
            secondary_effect_on_hit = secondary_effect_on_hit,
            secondary_effect_always = secondary_effect_always,
            resource_cost = resource_cost,
            attributes = attributes,
            unknown_fields = unknown_fields
        )


    def pformat_row( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the table row for display. """

        output = [ ]
        pformat_config_no_key_padding = pformat_config.clone(
            key_format = self._KEY_FORMAT
        )
        pformat_config_1 = pformat_config.clone(
            indent = pformat_config.indent + 4 * " "
        )
        pformat_config_2 = pformat_config_1.clone(
            indent = pformat_config_1.indent + 4 * " "
        )
        pformat_config_compact = pformat_config.clone(
            indent = "", render_title = False, render_compactly = True
        )

        indent = pformat_config.indent + 4 * " "

        output.append(
            (pformat_config.indent + "{title} #{number}: {name}").format(
                title = self._TITLE,
                number = self.pformat_key(
                    tables, pformat_config = pformat_config_no_key_padding
                ),
                name = self.name
            )
        )
        if pformat_config.render_compactly:
            return output[ 0 ]

        output.append( self.effect.pformat_object(
            tables, pformat_config = pformat_config_1
        ) )
        output.append( indent + "Attack {{Wpn: #att}}: {attack}".format(
            attack = self.attack
        ) )
        output.append( indent + "Defense {{Wpn: #def}}: {defense}".format(
            defense = self.defense
        ) )
        # TODO: Handle negative rates.
        output.append(
              indent
            + "Attack Rate {{Wpn: #nratt}}: {attack_rate}".format(
                attack_rate = self.attack_rate
            )
        )
        if self.attacks_total:
            output.append(
                  indent
                + "Attacks per Battle {{Wpn: #ammo}}: "
                  "{attacks_total}".format(
                    attacks_total = self.attacks_total
                )
            )
        output.append( indent + "Length {{Wpn: #len}}: {length}".format(
            length = self.length
        ) )
        if self.secondary_effect_on_hit:
            output.append(
                  indent + "On-Hit Secondary Effect {Wpn: #secondaryeffect}: "
                + tables[ Weapons_DataTable.LABEL( ) ].pformat_table_lookup(
                    self.secondary_effect_on_hit, tables,
                    pformat_config = pformat_config_compact
                )
            )
        if self.secondary_effect_always:
            output.append(
                  indent + "Always Secondary Effect "
                  "{Wpn: #secondaryeffectalways}: "
                + tables[ Weapons_DataTable.LABEL( ) ].pformat_table_lookup(
                    self.secondary_effect_always, tables,
                    pformat_config = pformat_config_compact
                )
            )
        output.append(
            indent + "Resource Cost {{Wpn: #rcost}}: {resource_cost}".format(
                resource_cost = self.resource_cost
            )
        )

        if self.attributes:
            for attribute in self.attributes:
                output.append( attribute.pformat_object(
                    tables, pformat_config = pformat_config_1
                ) )

        if not pformat_config.suppress_unknowns and self.unknown_fields:
            output.append( indent + "Unknowns" )
            for unknown_field in self.unknown_fields:
                output.append( unknown_field.pformat_object(
                    tables, pformat_config = pformat_config_2
                ) )

        return "\n".join( output ) + "\n"
        

class _Weapon_ForeignKey( _DataTableRow ):
    """ Abstraction for weapon number as a foreign key. """


    __abstract__    = True


    @_SQLA_declared_attr
    def weapon_number( cls ):
        return _SQLA_Column(
            _SQLA_Integer,
            _SQLA_ForeignKey(
                Weapon.TABLE_NAME( ) + "." + Weapon.KEY_NAME( )
            ),
            primary_key = True
        )


    _KEY_NAME       = "weapon_number"


class _WeaponAttribute( _Weapon_ForeignKey, _Attribute_ForeignKey ):
    

    __tablename__   = "attributes_by_weapon"


    attribute       = _SQLA_relationship( _Attribute )


    @classmethod
    def from_raw_data( cls, weapon_number, attribute_number, raw_value ):
        """ Creates an instance from a set of raw arguments. """

        attribute = _Attribute.from_raw_data(
            attribute_number = attribute_number,
            object_type = "Weapon",
            raw_value = raw_value
        )

        return cls(
            weapon_number = weapon_number,
            attribute_record_id = attribute.record_id,
            attribute = attribute
        )


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        return self.attribute.pformat_object(
            tables, pformat_config = pformat_config
        )


class WeaponUnknownField( _Weapon_ForeignKey, _DataTableRow_UnknownField ):
    """ An unknown field of a weapon record. """


    __tablename__   = "weapon_unknown_fields"


class Weapons_DataTable( _DataTable_NamedInteger, _DataTable_ProgramImage ):
    """ A table of weapons. """


    _TITLE          = "Weapons"
    _LABEL          = "Weapons"
    _FILE_NAME_BASE = "weapons"
    _ROW_CLASS      = Weapon


    _PROGRAM_IMAGE_BASE_OFFSETS = {
        _PLATFORM_LINUX( ): {
            "4.01": 0x961DA0, "4.03": 0x96E800, "4.04": 0x9B3260,
        }
    }


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #
