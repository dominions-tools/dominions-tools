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

""" Armor. """


__docformat__ = "reStructuredText"


from collections import (
    OrderedDict             as _OrderedDict,
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
from dominions.constants_tables import (
    AttributeKey                as _AttributeKey,
)
from dominions.Attribute import (
    Attribute                   as _Attribute,
    Attribute_ForeignKey        as _Attribute_ForeignKey,
)


class ArmorType( _DataTableRow_NamedInteger ):
    """ An armor type. """


    __tablename__   = "armor_types"


    _TITLE          = "Armor Type {Arm: #type}"


class ArmorTypes_DataTable( _DataTable_NamedInteger, _DataTable_CSV ):
    """ A table of armor types. """


    _TITLE          = "Armor Types {Arm: #type}"
    _LABEL          = "Armor Types"
    _FILE_NAME_BASE = "armor-types"
    _ROW_CLASS      = ArmorType


class ArmorProtectionZone( _DataTableRow_NamedInteger ):
    """ An armor protection zone. """


    __tablename__   = "armor_protection_zones"


class ArmorProtectionZones_DataTable(
    _DataTable_NamedInteger, _DataTable_CSV
):
    """ A table of armor protection zones. """


    _TITLE          = "Armor Protection Zones"
    _LABEL          = "Armor Protection Zones"
    _FILE_NAME_BASE = "armor-protection-zones"
    _ROW_CLASS      = ArmorProtectionZone


class Armor( _DataTableRow_NamedInteger, _DataTableRow_ProgramImage ):
    """ An armor. """


    __tablename__               = "armors"


    _TITLE                      = "Armor"
    _PROGRAM_IMAGE_RECORD_SIZES = {
        "4.03": 96, "4.04": 96,
    }


    armor_type      = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
            ArmorType.TABLE_NAME( ) + "." + ArmorType.KEY_NAME( )
        )
    )
    # TODO: Add field for calculated protection value.
    defense         = _SQLA_Column( _SQLA_Integer )
    encumbrance     = _SQLA_Column( _SQLA_Integer )
    resource_cost   = _SQLA_Column( _SQLA_Integer )

    protections     = _SQLA_relationship( "ArmorProtection" )
    attributes      = _SQLA_relationship( "_ArmorAttribute" )
    unknown_fields  = _SQLA_relationship( "ArmorUnknownField" )


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

        protections = [ ]
        for i in range( 6 ):
            protection_zone, offset \
            = _from_native_uint16( program_image, offset )
            protection_amount, offset = _from_native_uint16(
                program_image, offset
            )
            if protection_zone:
                protections.append( ArmorProtection(
                    armor_number = number,
                    zone_number = protection_zone,
                    protection = protection_amount
                ) )

        unknowns[ offset ], offset \
        = _from_native_uint16( program_image, offset )
        
        defense, offset = _from_native_int16( program_image, offset )

        encumbrance, offset = _from_native_uint16( program_image, offset )

        armor_type, offset = _from_native_uint16( program_image, offset )

        resource_cost, offset = _from_native_uint16( program_image, offset )

        unknowns[ offset ], offset \
        = _from_native_uint16( program_image, offset )

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
            attributes.append( _ArmorAttribute.from_raw_data(
                armor_number = number,
                attribute_number = key,
                raw_value = value
            ) )

        unknown_fields = [
            ArmorUnknownField(
                armor_number = number,
                offset = offset, value = value
            )
            for offset, value in unknowns.items( ) if value
        ]

        return cls(
            number = number, name = name,
            armor_type = armor_type,
            protections = protections, defense = defense,
            encumbrance = encumbrance,
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

        output.append(
            tables[ ArmorTypes_DataTable.LABEL( ) ].pformat_table_lookup(
                self.armor_type, tables, pformat_config = pformat_config_1
            )
        )
        # TODO: Output actual protection.
        if self.protections:
            output.append( indent + "Protection by Zone" )
            for protection in self.protections:
                output.append( protection.pformat_object(
                    tables, pformat_config = pformat_config_2
                ) )
        output.append( indent + "Defense {{Arm: #def}}: {defense}".format(
            defense = self.defense
        ) )
        output.append(
            indent + "Encumbrance {{Arm: #enc}}: {encumbrance}".format(
                encumbrance = self.encumbrance
            )
        )
        output.append(
            indent + "Resource Cost {{Arm: #rcost}}: {resource_cost}".format(
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
        

class _Armor_ForeignKey( _DataTableRow ):
    """ Abstraction for armor number as a foreign key. """


    __abstract__    = True


    @_SQLA_declared_attr
    def armor_number( cls ):
        return _SQLA_Column(
            _SQLA_Integer,
            _SQLA_ForeignKey( Armor.TABLE_NAME( ) + "." + Armor.KEY_NAME( ) ),
            primary_key = True
        )


class ArmorProtection( _Armor_ForeignKey ):
    """ A protection value for a zone of an armor. """


    __tablename__   = "protections_by_armor"


    _KEY_NAME       = "zone_number"
    _KEY_FORMAT     = "d"


    zone_number     = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
              ArmorProtectionZone.TABLE_NAME( ) + "."
            + ArmorProtectionZone.KEY_NAME( )
        ),
        primary_key = True
    )
    protection      = _SQLA_Column( _SQLA_Integer )


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        pformat_config_zone = pformat_config.clone( render_title = False )

        template = "{zone_name}: {protection}"
        args = {
            "zone_name":
            tables[ ArmorProtectionZones_DataTable.LABEL( ) ]\
            .pformat_table_lookup(
                self.zone_number, tables, pformat_config = pformat_config_zone
            ),
            "protection": self.protection
        }

        return template.format( **args )


class _ArmorAttribute( _Armor_ForeignKey, _Attribute_ForeignKey ):
    

    __tablename__   = "attributes_by_armor"


    attribute       = _SQLA_relationship( _Attribute )


    @classmethod
    def from_raw_data( cls, armor_number, attribute_number, raw_value ):
        """ Creates an instance from a set of raw arguments. """

        attribute = _Attribute.from_raw_data(
            attribute_number = attribute_number,
            object_type = "Armor",
            raw_value = raw_value
        )

        return cls(
            armor_number = armor_number,
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


class ArmorUnknownField( _Armor_ForeignKey, _DataTableRow_UnknownField ):
    """ An unknown field of an armor record. """


    __tablename__   = "armor_unknown_fields"


class Armors_DataTable( _DataTable_NamedInteger, _DataTable_ProgramImage ):
    """ A table of armors. """


    _TITLE          = "Armors"
    _LABEL          = "Armors"
    _FILE_NAME_BASE = "armors"
    _ROW_CLASS      = Armor


    _PROGRAM_IMAGE_BASE_OFFSETS = {
        _PLATFORM_LINUX( ): {
            "4.01": 0x9988E0, "4.03": 0x9A5340, "4.04": 0x98BFE0,
        }
    }


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #
