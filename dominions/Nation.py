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

""" Nations. """


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
    from_native_uint8       as _from_native_uint8,
    from_native_uint16      as _from_native_uint16,
    from_native_int16       as _from_native_int16,
    from_native_uint32      as _from_native_uint32,
    from_native_int32       as _from_native_int32,
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
from dominions.Attribute import (
    Attribute               as _Attribute,
    Attribute_ForeignKey    as _Attribute_ForeignKey,
)


class Nation( _DataTableRow_NamedInteger, _DataTableRow_ProgramImage ):
    """ A nation. """


    __tablename__   = "nations"


    epithet                 = _SQLA_Column( _SQLA_String )
    abbreviation            = _SQLA_Column( _SQLA_String )
    file_name_base          = _SQLA_Column( _SQLA_String )

    # TODO: Add foreign key against monsters table.
    initial_scout           = _SQLA_Column( _SQLA_Integer )
    # TODO: Add foreign key against monsters table.
    initial_leader          = _SQLA_Column( _SQLA_Integer )
    # TODO: Add foreign key against monsters table.
    initial_troops_type_1   = _SQLA_Column( _SQLA_Integer )
    initial_troops_count_1  = _SQLA_Column( _SQLA_Integer )
    # TODO: Add foreign key against monsters table.
    initial_troops_type_2   = _SQLA_Column( _SQLA_Integer )
    initial_troops_count_2  = _SQLA_Column( _SQLA_Integer )

    pretender_types         = _SQLA_relationship( "NationPretenderType" )
    unpretender_types       = _SQLA_relationship( "NationUnpretenderType" )
    fort_leader_types       = _SQLA_relationship( "NationFortLeaderType" )
    fort_troop_types        = _SQLA_relationship( "NationFortTroopType" )
    nonfort_leader_types    = _SQLA_relationship( "NationNonfortLeaderType" )
    nonfort_troop_types     = _SQLA_relationship( "NationNonfortTroopType" )

    attributes              = _SQLA_relationship( "_NationAttribute" )
    unknown_fields          = _SQLA_relationship( "NationUnknownField" )


    _TITLE                      = "Nation"
    _PROGRAM_IMAGE_RECORD_SIZES = {
        "4.03": 1108, "4.04": 1108,
    }


    @classmethod
    def from_program_image(
        cls, program_image, base_offset, number, dominions_version
    ):
        """ Creates an instance from a program image. """

        # TODO: Version these constants.
        NAME_LENGTH             = 36
        EPITHET_LENGTH          = 36
        GROUP_CODE_LENGTH       = 5
        FILE_NAME_BASE_LENGTH   = 63

        offset = base_offset
        
        args = { "number": number }
        unknowns = _OrderedDict( )
        
        args[ "name" ], __ = _from_string( program_image, offset, NAME_LENGTH )
        if "end" == args[ "name" ]: raise StopIteration( )
        offset += NAME_LENGTH

        args[ "epithet" ], __ \
        = _from_string( program_image, offset, EPITHET_LENGTH )
        offset += EPITHET_LENGTH

        args[ "abbreviation" ], __ \
        = _from_string( program_image, offset, GROUP_CODE_LENGTH )
        offset += GROUP_CODE_LENGTH

        args[ "file_name_base" ], __ \
        = _from_string( program_image, offset, FILE_NAME_BASE_LENGTH )
        offset += FILE_NAME_BASE_LENGTH

        # TEMP HACK: For decoding.
        for i in range( 16 ):
            unknowns[ offset - base_offset ], offset \
            = _from_native_uint16( program_image, offset )

        attribute_keys = [ ]
        for i in range( 64 ):
            attribute_key, offset \
            = _from_native_uint32( program_image, offset )
            attribute_keys.append( attribute_key )

        attribute_values = [ ]
        for i in range( 64 ):
            attribute_value, offset \
            = _from_native_int32( program_image, offset )
            attribute_values.append( attribute_value )

#        unknowns[ offset - base_offset ], offset \
#        = _from_native_uint32( program_image, offset )

        # 90 troop type slots at end

        args[ "fort_troop_types" ] = [ ]
        for slot_idx in range( 90 ):
            monster_number, offset \
            = _from_native_int32( program_image, offset )
            if 0 >= monster_number: break
            troop_type = NationFortTroopType(
                nation_number = number, monster_number = monster_number
            )
            args[ "fort_troop_types" ].append( troop_type )

        if -2 == monster_number:
            args[ "fort_leader_types" ] = [ ]
            for slot_idx in range( slot_idx, 89 ):
                monster_number, offset \
                = _from_native_int32( program_image, offset )
                if 0 >= monster_number: break
                troop_type = NationFortLeaderType(
                    nation_number = number, monster_number = monster_number
                )
                args[ "fort_leader_types" ].append( troop_type )

        if -3 == monster_number:
            args[ "nonfort_troop_types" ] = [ ]
            for slot_idx in range( slot_idx, 89 ):
                monster_number, offset \
                = _from_native_int32( program_image, offset )
                if 0 >= monster_number: break
                troop_type = NationNonfortTroopType(
                    nation_number = number, monster_number = monster_number
                )
                args[ "nonfort_troop_types" ].append( troop_type )

        if -4 == monster_number:
            args[ "nonfort_leader_types" ] = [ ]
            for slot_idx in range( slot_idx, 89 ):
                monster_number, offset \
                = _from_native_int32( program_image, offset )
                if 0 >= monster_number: break
                troop_type = NationNonfortLeaderType(
                    nation_number = number, monster_number = monster_number
                )
                args[ "nonfort_leader_types" ].append( troop_type )

        if -1 == monster_number:
            args[ "pretender_types" ] = [ ]
            args[ "unpretender_types" ] = [ ]
            monster_numbers = set( )
            for slot_idx in range( slot_idx, 89 ):
                monster_number, offset \
                = _from_native_int32( program_image, offset )
                if monster_number in monster_numbers:
                    continue
                else:
                    monster_numbers.add( monster_number )
                if -1 == monster_number: break
                if 0 == monster_number: continue
                if 0 < monster_number:
                    troop_type = NationPretenderType(
                        nation_number = number,
                        monster_number = monster_number
                    )
                    args[ "pretender_types" ].append( troop_type )
                else:
                    troop_type = NationUnpretenderType(
                        nation_number = number,
                        monster_number = -monster_number
                    )
                    args[ "unpretender_types" ].append( troop_type )

        # Note: Should not have any non-zero values.
        for slot_idx in range( slot_idx, 89):
            unknowns[ offset - base_offset ], offset \
            = _from_native_int32( program_image, offset )

        attributes = [ ]
        for key, value in zip( attribute_keys, attribute_values ):
            if not key: continue
            attributes.append( _NationAttribute.from_raw_data(
                nation_number = number,
                attribute_number = key,
                raw_value = value
            ) )
        args[ "attributes" ] = attributes

        args[ "unknown_fields" ] = [
            NationUnknownField(
                nation_number = number,
                offset = offset, value = value
            )
            for offset, value in unknowns.items( ) if value
        ]

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

        if self.epithet:
            output.append( indent + "Epithet: {epithet}".format(
                epithet = self.epithet
            ) )
        if self.abbreviation:
            output.append( indent + "Abbreviation: {abbreviation}".format(
                abbreviation = self.abbreviation
            ) )
        if self.file_name_base:
            output.append( indent + "File Name Base: {file_name_base}".format(
                file_name_base = self.file_name_base
            ) )

        if self.initial_scout:
            # TODO: Fill out via table lookup.
            output.append(
                indent + "Initial Scout {{#startscout}}: "
                "{initial_scout}".format(
                    initial_scout = self.initial_scout
                )
            )
        if self.initial_leader:
            # TODO: Fill out via table lookup.
            output.append(
                indent + "Initial Leader {{#startcom}}: "
                "{initial_leader}".format(
                    initial_leader = self.initial_leader
                )
            )
            # TODO: Fill out via table lookup.
            output.append(
                indent + "Initial Troops (Type I) {{#startunittype1}}: "
                "{initial_troops_type} "
                "(Count {{#startunitnbs1}}: {initial_troops_count})".format(
                    initial_troops_type = self.initial_troops_type_1,
                    initial_troops_count = self.initial_troops_count_1
                )
            )
            # TODO: Fill out via table lookup.
            output.append(
                indent + "Initial Troops (Type II) {{#startunittype2}}: "
                "{initial_troops_type} "
                "(Count {{#startunitnbs2}}: {initial_troops_count})".format(
                    initial_troops_type = self.initial_troops_type_2,
                    initial_troops_count = self.initial_troops_count_2
                )
            )

        indent_1 = indent + 4 * " "

        if self.unpretender_types:
            output.append( indent + "Excluded Pretenders {#delgod}" )
            for troop_type in self.unpretender_types:
                # TODO: Fill out via table lookup.
                output.append( indent_1 + str( troop_type.monster_number ) )
        if self.pretender_types:
            output.append( indent + "Pretenders {#addgod}" )
            for troop_type in self.pretender_types:
                # TODO: Fill out via table lookup.
                output.append( indent_1 + str( troop_type.monster_number ) )
        if self.fort_leader_types:
            output.append(
                indent + "Recruitable Leaders (Fortification) {#addreccom}"
            )
            for troop_type in self.fort_leader_types:
                # TODO: Fill out via table lookup.
                output.append( indent_1 + str( troop_type.monster_number ) )
        if self.fort_troop_types:
            output.append(
                indent + "Recruitable Troops (Fortification) {#addrecunit}"
            )
            for troop_type in self.fort_troop_types:
                # TODO: Fill out via table lookup.
                output.append( indent_1 + str( troop_type.monster_number ) )
        if self.nonfort_leader_types:
            output.append(
                indent + "Recruitable Leaders (Foreign) {#addforeigncom}"
            )
            for troop_type in self.nonfort_leader_types:
                # TODO: Fill out via table lookup.
                output.append( indent_1 + str( troop_type.monster_number ) )
        if self.nonfort_troop_types:
            output.append(
                indent + "Recruitable Troops (Foreign) {#addforeignunit}"
            )
            for troop_type in self.nonfort_troop_types:
                # TODO: Fill out via table lookup.
                output.append( indent_1 + str( troop_type.monster_number ) )

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
        

class _Nation_ForeignKey( _DataTableRow ):
    """ Abstraction for nation number as a foreign key. """


    __abstract__    = True


    @_SQLA_declared_attr
    def nation_number( cls ):
        return _SQLA_Column(
            _SQLA_Integer,
            _SQLA_ForeignKey(
                Nation.TABLE_NAME( ) + "." + Nation.KEY_NAME( )
            ),
            primary_key = True
        )


    _KEY_NAME       = "nation_number"


# TODO: Inherit from Monster_ForeignKey.
class _NationTroopType( _Nation_ForeignKey ):
    """ A recruitable troop type of a nation. """


    __abstract__    = True


    @_SQLA_declared_attr
    def monster_number( cls ):
        return _SQLA_Column( _SQLA_Integer, primary_key = True )


class NationFortTroopType( _NationTroopType ):
    """ A recruitable troop type of a nation. """

    
    __tablename__   = "fort_troop_types_by_nation"


class NationNonfortTroopType( _NationTroopType ):
    """ A recruitable troop type of a nation. """

    
    __tablename__   = "nonfort_troop_types_by_nation"


class NationFortLeaderType( _NationTroopType ):
    """ A recruitable troop type of a nation. """

    
    __tablename__   = "fort_leader_types_by_nation"


class NationNonfortLeaderType( _NationTroopType ):
    """ A recruitable troop type of a nation. """

    
    __tablename__   = "nonfort_leader_types_by_nation"


class NationPretenderType( _NationTroopType ):
    """ A recruitable troop type of a nation. """

    
    __tablename__   = "pretender_types_by_nation"


class NationUnpretenderType( _NationTroopType ):
    """ A recruitable troop type of a nation. """

    
    __tablename__   = "unpretender_types_by_nation"


class _NationAttribute( _Nation_ForeignKey, _Attribute_ForeignKey ):
    

    __tablename__   = "attributes_by_nation"


    attribute       = _SQLA_relationship( _Attribute )


    @classmethod
    def from_raw_data( cls, nation_number, attribute_number, raw_value ):
        """ Creates an instance from a set of raw arguments. """

        attribute = _Attribute.from_raw_data(
            attribute_number = attribute_number,
            object_type = "Nation",
            raw_value = raw_value
        )

        return cls(
            nation_number = nation_number,
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


class NationUnknownField( _Nation_ForeignKey, _DataTableRow_UnknownField ):
    """ An unknown field of a nation record. """


    __tablename__   = "nation_unknown_fields"


class Nations_DataTable( _DataTable_NamedInteger, _DataTable_ProgramImage ):
    """ A table of nations. """


    _TITLE          = "Nations"
    _LABEL          = "Nations"
    _FILE_NAME_BASE = "nations"
    _ROW_CLASS      = Nation


    _PROGRAM_IMAGE_BASE_OFFSETS = {
        _PLATFORM_LINUX( ): {
            "4.03": 0x6739A0, "4.04": 0x82CEA0,
        }
    }


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #
