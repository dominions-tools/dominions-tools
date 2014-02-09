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

""" Data tables. """


__docformat__ = "reStructuredText"


from collections import (
    namedtuple              as _namedtuple,
    OrderedDict             as _OrderedDict,
)

import csv              as _csv

from sqlalchemy.ext.declarative import (
    declarative_base        as _SQLA_declarative_base,
)
from sqlalchemy import (
    Column                  as _SQLA_Column,
    ForeignKey              as _SQLA_ForeignKey,
    Integer                 as _SQLA_Integer,
    String                  as _SQLA_String,
)
from sqlalchemy.ext.declarative import (
    declared_attr           as _SQLA_declared_attr,
)
from sqlalchemy.orm import (
    sessionmaker            as _SQLA_sessionmaker,
)


from dominions.utils import (
    database_session_scope  as _database_session_scope,
    DominionsVersion        as _DominionsVersion,
    PrettyFormatConfig      as _PrettyFormatConfig,
)


class DataTableRow( _SQLA_declarative_base( ) ):
    """ A generic table row. """


    __abstract__    = True


    _TITLE          = None
    _KEY_NAME       = None
    _KEY_FORMAT     = "s"


    @classmethod
    def TITLE( cls ):
        """ Returns the title of the object class. """

        return cls._TITLE


    @classmethod
    def TABLE_NAME( cls ):
        """ Returns the name of the corresponding database table. """

        return cls.__tablename__


    @classmethod
    def KEY_NAME( cls ):
        """ Returns the name of the primary key 
            on the corresponding database table. """

        return cls._KEY_NAME


    def pprint_row( self,
        tables, pformat_config = _PrettyFormatConfig( ), stream_print = print
    ):
        """ Prints a nicely-formatted table row to an output stream. """

        stream_print( self.pformat_row( tables, pformat_config ) )


    def pformat_row( self, tables, pformat_config = _PrettyFormatConfig( ) ):
        """ Nicely formats the table row for display. """

        pformat_config_row = pformat_config.clone(
            indent = "", render_title = False, render_key_with_object = False
        )
        return (pformat_config.indent + "{key}: {value}").format(
            key = self.pformat_key( tables, pformat_config_row ),
            value = self.pformat_object( tables, pformat_config_row )
        )


    def pprint_key( self,
        tables, pformat_config = _PrettyFormatConfig( ), stream_print = print
    ):
        """ Prints a nicely-formatted row key to an output stream. """

        stream_print( self.pformat_key( tables, pformat_config ) )


    def pformat_key( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the row key for display. """

        return ("{key:" + pformat_config.key_format + "}").format(
            key = getattr( self, self._KEY_NAME )
        )


    def pprint_object( self,
        tables, pformat_config = _PrettyFormatConfig( ), stream_print = print
    ):
        """ Prints a nicely-formatted object to an output stream. """

        stream_print( self.pformat_object( tables, pformat_config ) )


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        template = "{value}"
        args = {
            "value":
            self._pformat_object( tables, pformat_config = pformat_config )
        }

        if pformat_config.render_title:
            template = "{title}: " + template
            args[ "title" ] = self._TITLE

        if pformat_config.render_key_with_object:
            template += " [{key}]"
            args[ "key" ] = self.pformat_key(
                tables,
                pformat_config = pformat_config.clone(
                    key_format = self._KEY_FORMAT
                )
            )

        template = pformat_config.indent + template

        return template.format( **args )


    def _pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display.
            (Internal version - override as necessary.) """

        return str( self )


class DataTable( object ):
    """ A generic table. """


    _TITLE                  = None
    _LABEL                  = None
    _FILE_NAME_BASE         = None
    _ROW_CLASS              = None

    _dominions_version      = None
    _table                  = None


    @classmethod
    def TITLE( cls ):
        """ Returns the table title. """

        return cls._TITLE


    @classmethod
    def LABEL( cls ):
        """ Returns the table label. """

        return cls._LABEL


    @classmethod
    def FILE_NAME_BASE( cls ):
        """ Returns the base file name associated with the table. """

        return cls._FILE_NAME_BASE


    @classmethod
    def ROW_CLASS( cls ):
        """ Returns the class corresponding to a table row. """

        return cls._ROW_CLASS


    def __init__( self, table ):
        
        super( DataTable, self ).__init__( )
        self._table = table


    def persist_in_database( self, db_engine ):
        """ Persists all rows in database tables. """

        Session = _SQLA_sessionmaker( bind = db_engine )

        with _database_session_scope( Session ) as session:
            self._persist_in_database( session )


    def _persist_in_database( self, session ):
        """ Persists all rows in database tables.
            (Internal version to be overriden as necessary.) """

        session.add_all( self._table.values( ) )


    def pprint( self,
        tables, pformat_config = _PrettyFormatConfig( ), stream_print = print
    ):
        """ Prints a nicely-formatted table to an output stream. """

        stream_print( self.pformat( tables, pformat_config ) )


    def pformat( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats table for display. """

        indent = pformat_config.indent
        line_width = pformat_config.line_width

        output_format = \
        (indent + "\n{{title:-^{line_width}}}\n\n{{table_rows}}\n").format(
            line_width = line_width - len( indent )
        )

        return output_format.format(
            title = "  Table: {0}  ".format( self._TITLE ),
            table_rows = self.pformat_table_rows( tables, pformat_config )
        )


    def pprint_table_rows( self,
        tables, pformat_config = _PrettyFormatConfig( ), stream_print = print
    ):
        """ Nicely formats and prints the table rows to an output stream. """

        stream_print( self.pformat_table_rows( tables, pformat_config ) )


    def pformat_table_rows( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the table rows for display. """

        pformat_config_row = pformat_config.clone(
            key_format = self._generated_key_format( )
        )
        return "\n".join( [
            row.pformat_row( tables, pformat_config = pformat_config_row )
            for row in self._table.values( )
        ] )


    def pformat_table_lookup( self,
        key, tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats a table lookup for display. """

        return self._table[ key ].pformat_object(
            tables, pformat_config = pformat_config
        )


class DataTable_CSV( DataTable ):
    """ A generic table which can be loaded from CSV data. """


    @classmethod
    def from_csv_file( cls, file_path, dominions_version ):
        """ Create an instance from a CSV file. """

        with open( file_path, "r" ) as csv_file:
            self = cls.from_csv( csv_file, dominions_version )

        return self


    @classmethod
    def from_csv( cls, istream, dominions_version ):
        """ Creates an instance from a stream of CSV rows. """

        sniffer = _csv.Sniffer( )
        if not sniffer.has_header( istream.read( 1024 ) ):
            raise IOError( "Invalid CSV input stream." )
        istream.seek( 0 )
        dialect = sniffer.sniff( istream.read( 1024 ) )
        istream.seek( 0 )

        table = _OrderedDict( )
        platform = dominions_version.platform

        csv = _csv.DictReader( istream, dialect = dialect )
        for row in csv:

            # Exclude rows which are tagged for a version of Dominions
            # greater than the targeted version.
            if "dominions_version" in row:
                row_dominions_version \
                = _DominionsVersion( platform, row[ "dominions_version" ] )
                if row_dominions_version > dominions_version: continue

            # Add new table entry or update table entry from CSV row.
            # Note: Newer versions of a row are expected to be encountered
            #       later than earlier versions of it.
            table[ cls._ROW_CLASS.key_from_dict( row ) ] \
            = cls._ROW_CLASS.from_dict( row )

        return cls( table )


class DataTableRow_ProgramImage( object ):
    """ A mixin to provide support for common activities
        pertaining to table rows and program images in memory. """


    _PROGRAM_IMAGE_RECORD_SIZES = None


    @classmethod
    def PROGRAM_IMAGE_RECORD_SIZE( cls, dominions_version ):
        """ Returns the size of a record within the program image. """

        return cls._PROGRAM_IMAGE_RECORD_SIZES[ dominions_version.version ]


class DataTable_ProgramImage( DataTable ):
    """ A generic table which can be loaded from a program image. """


    @classmethod
    def from_program_image( cls, program_image, dominions_version ):
        """ Creates an instance from a program image in memory. """

        base_offset = cls._find_table_base_offset(
            program_image, dominions_version
        )

        self = cls._from_program_image(
            program_image, base_offset, dominions_version
        )

        self.postprocess_extracted_table( program_image, dominions_version )

        return self


    # TODO: Implement sniffer rather than rely on hard-coded constants.
    @classmethod
    def _find_table_base_offset( cls,
        program_image, dominions_version,
        offsets_table_name = "_PROGRAM_IMAGE_BASE_OFFSETS"
    ):
        """ Finds and returns the base offset of the table 
            within the program image for the given Dominions version. """

        platform        = dominions_version.platform
        version         = dominions_version.version

        base_offset = None
        base_offsets_by_platform \
        = getattr( cls, offsets_table_name ).get( platform )
        if base_offsets_by_platform:
            base_offset = base_offsets_by_platform.get( version )

        if None is base_offset:
            raise LookupError(
                "Unable to find base offset of table for this Dominions "
                "{version} on {platform}.".format(
                    platform = platform, version = version
                )
            )

        return base_offset


    @classmethod
    def _from_program_image(
        cls, program_image, base_offset, dominions_version
    ):
        """ Extracts the table from a program image.
            (Internal version - override as needed.) """

        RECORD_SIZE \
        = cls._ROW_CLASS.PROGRAM_IMAGE_RECORD_SIZE( dominions_version )

        table       = _OrderedDict( )
        offset      = base_offset
        number      = 0

        try:
            while True:

                table[ number ] = cls._ROW_CLASS.from_program_image(
                    program_image, offset, number, dominions_version
                )

                number += 1
                offset += RECORD_SIZE

        except StopIteration as exc: pass

        return cls( table )


    def postprocess_extracted_table( self, program_image, dominions_version ):
        """ Performs post-processing on an extracted table.
            (Empty implementation - override as needed.) """

        pass


class DataTableRow_NamedInteger( DataTableRow ):
    """ A generic table row, naming an integer value. """


    __abstract__    = True


    _KEY_NAME       = "number"
    _KEY_FORMAT     = "d"


    number          = _SQLA_Column( _SQLA_Integer, primary_key = True )
    name            = _SQLA_Column( _SQLA_String )


    @classmethod
    def from_dict( cls, attributes_dict ):
        """ Creates an instance from an attributes dictionary. """

        return cls(
            number = cls.key_from_dict( attributes_dict ),
            name = attributes_dict[ "name" ]
        )


    @classmethod
    def key_from_dict( cls, attributes_dict ):
        """ Returns value of primary key from an attributes dictionary. """

        return int( attributes_dict[ cls._KEY_NAME ] )


    def _pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object data for display. """

        return self.name


class DataTable_NamedInteger( DataTable ):
    """ A generic table with named integer values. """


    def __init__( self, table ):
        
        super( DataTable_NamedInteger, self ).__init__( table )
        self._calculate_key_width( )


    def _calculate_key_width( self ):
        """ Calculates the pad width for justified display formats
            of the table keys. """

        self._key_width = len( str( max( self._table.keys( ) ) ) )


    def _generated_key_format( self ):
        """ Generates a format string for application to row keys
            in a tabular display. """

        return "{key_width}d".format( key_width = self._key_width )


class DataTableRow_NamedBits( DataTableRow ):
    """ A generic table row representing a named bit in a bitmask. """


    __abstract__    = True


    _KEY_NAME       = "bit_value"
    _KEY_FORMAT     = "d"


    bit_value       = _SQLA_Column( _SQLA_Integer, primary_key = True )
    bit_name        = _SQLA_Column( _SQLA_String )


    @classmethod
    def from_dict( cls, attributes_dict ):
        """ Creates an instance from an attributes dictionary. """

        return cls(
            bit_value = cls.key_from_dict( attributes_dict ),
            bit_name = attributes_dict[ "bit_name" ]
        )


    @classmethod
    def key_from_dict( cls, attributes_dict ):
        """ Returns value of primary key from an attributes dictionary. """

        return int( attributes_dict[ cls._KEY_NAME ] )


    def _pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object data for display. """

        return self.bit_name


class DataTable_NamedBits( DataTable_NamedInteger ):
    """ A generic table representing a bit mask with named positions. """


    def pformat_table_lookup( self,
        key, tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats a table lookup for display. """

        pformat_config_row = pformat_config.clone( )
        if pformat_config.render_title:
            pformat_config_row.indent = pformat_config.indent + " " * 4
            pformat_config_row.render_title = False

        template = "{values}"
        args = {
            "values": 
            "\n".join( [
                row.pformat_object(
                    tables, pformat_config = pformat_config_row
                )
                for row in self._table.values( )
                if key & row.bit_value
            ] )
        }

        if pformat_config.render_title:
            args[ "title" ] = self._TITLE
            if pformat_config.render_key_with_object:
                template = "{title} [Total: {key}]:\n" + template
                args[ "key" ] = key
            else:
                template = "{title}:\n" + template

        return template.format( **args )


class DataTableRow_UnknownField( DataTableRow ):
    """ A generic table row representing an unknown field. """


    __abstract__    = True


    @_SQLA_declared_attr
    def offset( cls ):
        return _SQLA_Column( _SQLA_Integer, primary_key = True )
    value           = _SQLA_Column( _SQLA_Integer )


    _KEY_NAME       = "offset"


    def pformat_object( self,
        tables, pformat_config = _PrettyFormatConfig( )
    ):
        """ Nicely formats the object for display. """

        template = "<Unknown> [Offset: {offset}]: {value}"
        args = {
            "offset": self.offset, "value": self.value
        }

        template = pformat_config.indent + template

        return template.format( **args )


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #
