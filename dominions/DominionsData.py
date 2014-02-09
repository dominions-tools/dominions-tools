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

""" Abstraction layer for Dominions data. """


__docformat__ = "reStructuredText"


from collections import (
    OrderedDict             as _OrderedDict,
)
import functools        as _functools

import os               as _os
from os.path import (
    extsep                  as _path_extsep,
    join                    as _path_join,
    exists                  as _path_exists,
    isdir                   as _path_is_directory,
)
import mmap             as _mmap

from sqlalchemy.orm import (
    sessionmaker            as _SQLA_sessionmaker,
)

from dominions.utils import (
    database_session_scope  as _database_session_scope,
    DominionsVersion        as _DominionsVersion,
    PrettyFormatConfig      as _PrettyFormatConfig,
)
from dominions.DataTable import (
    DataTableRow            as _DataTableRow,
)
from dominions.constants_tables import (
    AttributeKeys_DataTable,
    Sounds_DataTable,
    MonsterTags_DataTable,
    MagicSchools_DataTable,
    MagicPaths_DataTable,
    AnonymousProvinceEvents_DataTable,
    SpecialUniqueSummons_DataTable,
    TerrainSpecificSummons_DataTable,
    OtherPlanes_DataTable,
    MapTerrainTypes_DataTable,
)
from dominions.Nation import (
    Nations_DataTable,
)
from dominions.Armor import (
    ArmorTypes_DataTable,
    ArmorProtectionZones_DataTable,
    Armors_DataTable,
)
from dominions.Effect import (
    EffectsInfo_DataTable,
    EffectModifierBits_DataTable,
    FlightSprites_DataTable,
    ExplosionSprites_DataTable,
    SpecialDamageTypes_DataTable,
    Buffs1Types_DataTable,
    Buffs2Types_DataTable,
    Enchantments_DataTable,
)
from dominions.Weapon import (
    Weapons_DataTable,
)
from dominions.Spell import (
    Spells_DataTable,
)


class DominionsData( object ):
    """ Supreme binder for all Dominions data. """


    _TABLE_TYPES                = [
        AttributeKeys_DataTable,
        Sounds_DataTable,
        ArmorTypes_DataTable,
        ArmorProtectionZones_DataTable,
        EffectsInfo_DataTable,
        EffectModifierBits_DataTable,
        FlightSprites_DataTable,
        ExplosionSprites_DataTable,
        SpecialDamageTypes_DataTable,
        Buffs1Types_DataTable,
        Buffs2Types_DataTable,
        MonsterTags_DataTable,
        MagicSchools_DataTable,
        MagicPaths_DataTable,
        Enchantments_DataTable,
        AnonymousProvinceEvents_DataTable,
        SpecialUniqueSummons_DataTable,
        TerrainSpecificSummons_DataTable,
        OtherPlanes_DataTable,
        MapTerrainTypes_DataTable,
        Nations_DataTable,
        Armors_DataTable,
        Weapons_DataTable,
        Spells_DataTable,
    ]
    _LOADABLE_TABLE_TYPES       = list( filter(
        lambda ttype: hasattr( ttype, "from_csv_file" ),
        _TABLE_TYPES
    ) )
    _EXTRACTABLE_TABLE_TYPES    = list( filter(
        lambda ttype: hasattr( ttype, "from_program_image" ),
        _TABLE_TYPES
    ) )


    _dominions_version  = None
    _tables             = None


    @classmethod
    def from_database( cls, db_engine ):
        """ Instantiates from a databse. """

        tables = _OrderedDict( )

        # TODO: Implement.


    @classmethod
    def from_program_and_data_files(
        cls, program_path, constants_path_base
    ):
        """ Instantiates from a Dominions executable
            and supporting data files. """

        tables = _OrderedDict( )

        with open( program_path, "rb" ) as program_file:
            with _mmap.mmap(
                program_file.fileno( ), 0, prot = _mmap.PROT_READ
            ) as program_image:

                dominions_version \
                = _DominionsVersion.from_program_image( program_image )

                # Load tables of constants from CSV files.
                for table_type in cls._LOADABLE_TABLE_TYPES:
                    table = table_type.from_csv_file(
                        _path_join(
                            constants_path_base,
                              table_type.FILE_NAME_BASE( )
                            + _path_extsep + "csv"
                        ),
                        dominions_version
                    )
                    tables[ table_type.LABEL( ) ] = table

                # Extract other tables from the Dominions executable.
                for table_type in cls._EXTRACTABLE_TABLE_TYPES:
                    table = table_type.from_program_image(
                        program_image, dominions_version
                    )
                    tables[ table_type.LABEL( ) ] = table

                # TODO: Implement other extractions.

                self = cls( dominions_version, tables )

        return self


    def __init__( self, dominions_version, tables ):
        
        self._dominions_version     = dominions_version
        self._tables                = tables


    def persist_in_database( self, db_engine ):
        """ Persists all loaded data in a database. """

        # Refresh the database prior to persisting objects.
        _DataTableRow.metadata.drop_all( bind = db_engine )
        _DataTableRow.metadata.create_all( bind = db_engine )

        for table in self._tables.values( ):
            table.persist_in_database( db_engine )

        Session = _SQLA_sessionmaker( bind = db_engine )

        with _database_session_scope( Session ) as session:
            # TODO: Persist other data in database.
            pass


    def pprint( self,
        dump_files_path = None, pformat_config = _PrettyFormatConfig( )
    ):
        """ Dumps all loaded data to stdout or to files in a directory. """

        if not _path_exists( dump_files_path ):
            _os.mkdir( dump_files_path, 0o700 )
        else:
            if not _path_is_directory( dump_files_path ):
                raise IOError( "Not a directory: {0}".format(
                    dump_files_path
                ) )
            if not _os.access(
                dump_files_path, _os.R_OK | _os.W_OK | _os.X_OK
            ):
                raise IOError( "Could not access directory: {0}".format(
                    dump_files_path
                ) )

        tables = self._tables
        for table in tables.values( ):
            if None is dump_files_path:
                table.pprint( tables, pformat_config )
            else:
                dump_file_path = _path_join(
                    dump_files_path,
                    table.FILE_NAME_BASE( ) + _path_extsep + "txt"
                )
                with open( dump_file_path, "w" ) as dump_file:
                    stream_print \
                    = _functools.partial( print, file = dump_file )
                    table.pprint( tables, pformat_config, stream_print )


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #
