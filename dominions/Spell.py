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

""" Spells. """


__docformat__ = "reStructuredText"


from collections import (
    OrderedDict                 as _OrderedDict,
)

from textwrap import (
    TextWrapper                 as _TextWrapper,
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
    from_native_uint8       as _from_native_uint8,
    from_native_int8        as _from_native_int8,
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
    DataTableRow_ProgramImage   as _DataTableRow_ProgramImage,
    DataTable_ProgramImage      as _DataTable_ProgramImage,
    DataTableRow_NamedInteger   as _DataTableRow_NamedInteger,
    DataTable_NamedInteger      as _DataTable_NamedInteger,
    DataTableRow_UnknownField   as _DataTableRow_UnknownField,
)
from dominions.constants_tables import (
    MagicPath,
    MagicPaths_DataTable,
    MagicSchool,
    MagicSchools_DataTable,
)
from dominions.Attribute import (
    Attribute               as _Attribute,
    Attribute_ForeignKey    as _Attribute_ForeignKey,
)
from dominions.Effect import (
    Effect                  as _Effect,
)


class Spell( _DataTableRow_NamedInteger, _DataTableRow_ProgramImage ):
    """ A spell. """


    __tablename__   = "spells"


    school                  = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
            MagicSchool.TABLE_NAME( ) + "." + MagicSchool.KEY_NAME( )
        )
    )
    research_level          = _SQLA_Column( _SQLA_Integer )
    path_0                  = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
            MagicPath.TABLE_NAME( ) + "." + MagicPath.KEY_NAME( )
        )
    )
    path_level_0            = _SQLA_Column( _SQLA_Integer )
    path_1                  = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
            MagicPath.TABLE_NAME( ) + "." + MagicPath.KEY_NAME( )
        )
    )
    path_level_1            = _SQLA_Column( _SQLA_Integer )
    effect_record_id        = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey( _Effect.TABLE_NAME( ) + "." + _Effect.KEY_NAME( ) )
    )
    effect                  = _SQLA_relationship(
        _Effect, uselist = False, 
        primaryjoin = effect_record_id == _Effect.record_id
    )
    effects_count           = _SQLA_Column( _SQLA_Integer )
    precision               = _SQLA_Column( _SQLA_Integer )
    fatigue                 = _SQLA_Column( _SQLA_Integer )
    gem_cost                = _SQLA_Column( _SQLA_Integer )
    next_spell              = _SQLA_Column(
        _SQLA_Integer,
        _SQLA_ForeignKey(
            __tablename__ + "." + _DataTableRow_NamedInteger.KEY_NAME( )
        )
    )
    description             = _SQLA_Column( _SQLA_String )

    attributes              = _SQLA_relationship( "_SpellAttribute" )
    unknown_fields          = _SQLA_relationship( "SpellUnknownField" )


    _TITLE                      = "Spell"
    _PROGRAM_IMAGE_RECORD_SIZES = {
        "4.03": 200, "4.04": 200,
    }


    @classmethod
    def from_program_image(
        cls, program_image, base_offset, number, dominions_version
    ):
        """ Creates an instance from a program image. """

        # TODO: Version this constant.
        NAME_LENGTH     = 36

        offset = base_offset
        
        args = { "number": number }
        effect_args = { }
        unknowns = _OrderedDict( )
        
        args[ "name" ], __ = _from_string( program_image, offset, NAME_LENGTH )
        if "end" == args[ "name" ]: raise StopIteration( )
        offset += NAME_LENGTH

        args[ "school" ], offset = _from_native_int8( program_image, offset )
        args[ "research_level" ], offset \
        = _from_native_uint8( program_image, offset )

        path_mask, offset = _from_native_int16( program_image, offset )
        if 0 > path_mask:
            if -1 == path_mask:
                args[ "path_0" ] = -1
                args[ "path_1" ] = -1
            else:
                args[ "path_0" ] = 256 + path_mask
                args[ "path_1" ] = -1
        else:
            args[ "path_0" ] = 0x00ff & path_mask
            args[ "path_1" ] = (0xff00 & path_mask) >> 8
        path_level_mask, offset = _from_native_uint16( program_image, offset )
        args[ "path_level_0" ] = 0x00ff & path_level_mask
        args[ "path_level_1" ] = (0xff00 & path_level_mask) >> 8

        fatigue, offset = _from_native_uint16( program_image, offset )
        args[ "fatigue" ] = fatigue % 100
        args[ "gem_cost" ] = fatigue // 100

        effect_args[ "raw_area" ], offset \
        = _from_native_uint16( program_image, offset )

        effect_args[ "effect_number" ], offset \
        = _from_native_uint16( program_image, offset )

        effect_args[ "raw_range" ], offset \
        = _from_native_uint16( program_image, offset )

        args[ "precision" ], offset \
        = _from_native_int16( program_image, offset )

        unknowns[ offset ], offset \
        = _from_native_uint32( program_image, offset )

        effect_args[ "raw_argument" ], offset \
        = _from_native_int64( program_image, offset )

        args[ "effects_count" ], offset \
        = _from_native_uint16( program_image, offset )

        effect_args[ "flight_sprite_number" ], offset \
        = _from_native_int16( program_image, offset )
        effect_args[ "flight_sprite_length" ], offset \
        = _from_native_uint16( program_image, offset )

        effect_args[ "explosion_sprite_number" ], offset \
        = _from_native_int16( program_image, offset )
        effect_args[ "explosion_sprite_length" ], offset \
        = _from_native_uint16( program_image, offset )

        unknowns[ offset ], offset \
        = _from_native_uint32( program_image, offset )
        unknowns[ offset ], offset \
        = _from_native_uint16( program_image, offset )

        effect_args[ "modifiers_mask" ], offset \
        = _from_native_int64( program_image, offset )

        args[ "next_spell" ], offset \
        = _from_native_uint16( program_image, offset )

        effect_args[ "sound_number" ], offset \
        = _from_native_uint16( program_image, offset )

        attribute_keys = [ ]
        for i in range( 13 ):
            attribute_key, offset \
            = _from_native_uint32( program_image, offset )
            attribute_keys.append( attribute_key )

        attribute_values = [ ]
        for i in range( 13 ):
            attribute_value, offset \
            = _from_native_uint32( program_image, offset )
            attribute_values.append( attribute_value )

        unknowns[ offset ], offset \
        = _from_native_uint32( program_image, offset )

        attributes = [ ]
        for key, value in zip( attribute_keys, attribute_values ):
            if not key: continue
            attributes.append( _SpellAttribute.from_raw_data(
                spell_number = number,
                attribute_number = key,
                raw_value = value
            ) )
        args[ "attributes" ] = attributes

        args[ "unknown_fields" ] = [
            SpellUnknownField(
                spell_number = number,
                offset = offset, value = value
            )
            for offset, value in unknowns.items( ) if value
        ]

        effect_args[ "object_type" ] = cls.TITLE( )
        args[ "effect" ] = _Effect.from_raw_data( **effect_args )

        return cls( **args )


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
        pformat_config_compact_no_key = pformat_config.clone(
            indent = "", render_title = False,
            render_key_with_object = False,
            render_compactly = True
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

        template = indent + "Research Requirement {{Spl: #school}}"
        args = {
            "school":
            tables[ MagicSchools_DataTable.LABEL( ) ].pformat_table_lookup(
                self.school, tables,
                pformat_config = pformat_config_compact_no_key
            )
        }
        if 0 > self.school:
            template += ": {school}"
        else:
            template += " {{Spl: #researchlevel}}: {school} {level}"
            args[ "level" ] = self.research_level
        output.append( template.format( **args ) )

        for idx in range( 2 ):
            path = eval( "self.path_{idx}".format( idx = idx ) )
            if 0 <= path:
                output.append(
                    indent + "Magic Path #{idx_plus_1} "
                    "{{Spl: #path {idx}}} {{Spl: #pathlevel {idx}}}: "
                    "{path} {level}".format(
                        idx = idx, idx_plus_1 = idx + 1,
                        path
                        = tables[ MagicPaths_DataTable.LABEL( ) ]\
                        .pformat_table_lookup(
                            path, tables,
                            pformat_config = pformat_config_compact_no_key
                        ),
                        level = eval(
                            "self.path_level_{idx}".format( idx = idx )
                        )
                    )
                )

        output.append( self.effect.pformat_object(
            tables, pformat_config = pformat_config_1
        ) )

        output.append(
            indent + "Number of Effects {{Spl: #nreff}}: "
            "{effects_count}".format(
                effects_count = self.effects_count
            )
        )

        if self.precision:
            output.append(
                indent + "Precision {{Spl: #precision}}: {precision}".format(
                    precision = self.precision
                )
            )
        if   self.fatigue:
            output.append(
                indent + "Fatigue {{Spl: #fatiguecost}}: {fatigue}".format(
                    fatigue = self.fatigue
                )
            )
        elif self.gem_cost:
            output.append(
                indent + "Gem Cost {{Spl: #fatiguecost}}: {gem_cost}".format(
                    gem_cost = self.gem_cost
                )
            )

        if self.next_spell:
            output.append(
                indent + "Next Spell {{Spl: #nextspell}}: "
                "{next_spell}".format(
                    next_spell
                    = tables[ Spells_DataTable.LABEL( ) ]\
                    .pformat_table_lookup(
                        self.next_spell, tables,
                        pformat_config = pformat_config_compact
                    )
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

        if self.description:
            output.append( "" )
            text_wrapper = _TextWrapper(
                width = pformat_config.line_width,
                initial_indent = pformat_config_1.indent,
                subsequent_indent = pformat_config_1.indent
            )
            output.extend( text_wrapper.wrap( self.description ) )

        return "\n".join( output ) + "\n"
        

class _Spell_ForeignKey( _DataTableRow ):
    """ Abstraction for spell number as a foreign key. """


    __abstract__    = True


    @_SQLA_declared_attr
    def spell_number( cls ):
        return _SQLA_Column(
            _SQLA_Integer,
            _SQLA_ForeignKey(
                Spell.TABLE_NAME( ) + "." + Spell.KEY_NAME( )
            ),
            primary_key = True
        )


    _KEY_NAME       = "spell_number"


class _SpellAttribute( _Spell_ForeignKey, _Attribute_ForeignKey ):
    

    __tablename__   = "attributes_by_spell"


    attribute       = _SQLA_relationship( _Attribute )


    @classmethod
    def from_raw_data( cls, spell_number, attribute_number, raw_value ):
        """ Creates an instance from a set of raw arguments. """

        attribute = _Attribute.from_raw_data(
            attribute_number = attribute_number,
            object_type = "Spell",
            raw_value = raw_value
        )

        return cls(
            spell_number = spell_number,
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


class SpellUnknownField( _Spell_ForeignKey, _DataTableRow_UnknownField ):
    """ An unknown field of a spell record. """


    __tablename__   = "spell_unknown_fields"


class Spells_DataTable( _DataTable_NamedInteger, _DataTable_ProgramImage ):
    """ A table of spells. """


    _TITLE          = "Spells"
    _LABEL          = "Spells"
    _FILE_NAME_BASE = "spells"
    _ROW_CLASS      = Spell


    _PROGRAM_IMAGE_BASE_OFFSETS = {
        _PLATFORM_LINUX( ): {
            "4.03": 0x6BBAE0, "4.04": 0x8A7560,
        }
    }
    _PROGRAM_IMAGE_BASE_OFFSETS_DESCRIPTIONS_INDEX = {
        _PLATFORM_LINUX( ): {
            "4.03": 0x2D2316, "4.04": 0x348FB3,
        }
    }
    _PROGRAM_IMAGE_BASE_OFFSETS_DESCRIPTIONS = {
        _PLATFORM_LINUX( ): {
            "4.03": 0x2DF8D0, "4.04": 0x34EDE8,
        }
    }


    def postprocess_extracted_table( self, program_image, dominions_version ):
        """ Performs post-processing on an extracted table. """

        # TEMP HACK: Disable until a proper lookup table is found.
        return

        DEBUG           = False

        # TODO: Version this constant.
        NAME_LENGTH     = 36
        # UGLY HACK
        DUPLICATES = {
            "Natural Rain": "Rain",
            "Summon Great Eagles": "Summon Great Eagle",
            "Revive Bishop": "Revive Arch Bishop",
            "Revive Acolyte": "Revive Arch Bishop",
            "Revive Dusk Elder": "Revive Spectator",
            "Improved Cross Breeding": "Cross Breeding",
            "Wrath of the Sepulchre": "Unholy Wrath",
            "Protection of the Sepulchre": "Protection of the Grave",
            "Royal Protection": "Protection of the Grave",
            "Call Sirrush": "Contact Sirrush",
            "Contact Cu Sidhe": "Summon Cu Sidhe",
            "Contact Scorpion Man": "Summon Scorpion Man",
            "Summon Rakshasa Warriors": "Summon Rakshasas",
        }
        UNDESCRIBED = set( [
            "Contact Forest Giant",
            "Bind Beast Bat",
            "Revive Lemur Consul",
            "Revive Lemur Acolyte",
        ] )
        NEXT_INDICES_MISSING = {
            "Fire Flies": 1,
            "King of Elemental Fire": 1,
            "Charge Body": 2,
            "Corpse Man Construction": 1,
            "Clockwork Soldiers": 1,
            "Mechanical Men": 2,
            "Carrion Woods": 3,
            "Bind Beast Bats": 1,
            "Polymorph": 1,
            "Revive Lemur Senator": 1,
            "Spirit Curse": 1,
            "Call Wraith Lord": 1,
            "Ghost Riders": 1,
        }

        # TODO: Setup some proper logging.
        if DEBUG:
            debug_file = open( "TEMP-DEBUG.txt", "w" )

        name_descr_pairs    = { }
        spell_names         = set( )
        for spell in self._table.values( ):
            spell_names.add( spell.name )

        descr_idx_offset    = type( self )._find_table_base_offset(
            program_image, dominions_version,
            "_PROGRAM_IMAGE_BASE_OFFSETS_DESCRIPTIONS_INDEX"
        )
        descrs_offset       = type( self )._find_table_base_offset(
            program_image, dominions_version,
            "_PROGRAM_IMAGE_BASE_OFFSETS_DESCRIPTIONS"
        )

        # TEMP HACK
        descrs_offset_base = descrs_offset
        for number in range( 900 ):
            description, descrs_offset \
            = self._parse_spell_description_from_program_image(
                program_image, descrs_offset
            )
            if DEBUG:
                print( "{number} (Offset: {offset})\n--\n{descr}\n".format(
                    number = number,
                    offset = descrs_offset - descrs_offset_base,
                    descr = description
                ), file = debug_file )
        if DEBUG:
            debug_file.close( )
        return

        descr_count         = 1
        # The number of entries in the descriptions index does not match the
        # number of tabulated spells, all or non-hidden. Hence, an upper bound
        # on the scan is needed in case the termination condition is not met.
        # TODO: Use a versioned constant for the upper bound of the index scan.
        for number in range( 1100 ):

            name, __ \
            = _from_string( program_image, descr_idx_offset, NAME_LENGTH )
            if "no description available" == name: break
            descr_idx_offset += len( name ) + 1
            if name and ":" == name[ 0 ]:
                name = name[ 1 : ]
            if name not in spell_names:
                pass
            # UGLY HACK
            if name in DUPLICATES:
                name_descr_pairs[ name ] \
                = name_descr_pairs[ DUPLICATES[ name ] ] 
                continue
            if name in UNDESCRIBED:
                continue

            while descr_count:
                description, descrs_offset \
                = self._parse_spell_description_from_program_image(
                    program_image, descrs_offset
                )
                descr_count -= 1

            if name in NEXT_INDICES_MISSING:
                descr_count += NEXT_INDICES_MISSING[ name ]
            descr_count += 1

            while description and ":" == description[ 0 ]:
                name_inline = description[ 1 : ]
                # TODO? Validate inline name.
                description, descrs_offset \
                = self._parse_spell_description_from_program_image(
                    program_image, descrs_offset
                )
                name_descr_pairs[ name_inline ] = description

                if DEBUG:
                    print( "{name}\n--\n{descr}\n".format(
                        name = name_inline, descr = description
                    ), file = debug_file )

                description, descrs_offset \
                = self._parse_spell_description_from_program_image(
                    program_image, descrs_offset
                )

            name_descr_pairs[ name ] = description

            if DEBUG:
                print( "{name}\n--\n{descr}\n".format(
                    name = name, descr = description
                ), file = debug_file )

        for number, spell in self._table.items( ):
            description = name_descr_pairs.get( spell.name )
            if description:
                spell.description = description

        if DEBUG:
            debug_file.close( )


    def _parse_spell_description_from_program_image( self,
        program_image, offset
    ):
        """ Parses a spell description from program image. """

        CHUNK_SIZE      = 8

        description = ""
        while True:
            chunk, __ = _from_string( program_image, offset, CHUNK_SIZE )
            description += chunk
            offset += CHUNK_SIZE
            if CHUNK_SIZE != len( chunk ):
                if not chunk and 0 != len( description ) % CHUNK_SIZE:
                    print( description )
                break

        return description, offset


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #
