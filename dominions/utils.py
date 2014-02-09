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

"""
    A collection of utility functions.
"""


__docformat__ = "reStructuredText"


import struct           as _struct

from contextlib import (
    contextmanager          as _contextmanager,
)


def from_byte( raw_bytes, offset ):
    """ Returns a single byte from an array of bytes. """
    return raw_bytes[ offset ], offset + 1


def from_native_uint8( raw_bytes, offset ):
    """ Reads a native 8-bit unsigned integer from an array of bytes. """
    return _struct.unpack_from( "=B", raw_bytes, offset )[ 0 ], offset + 1


def from_native_int8( raw_bytes, offset ):
    """ Reads a native 8-bit signed integer from an array of bytes. """
    return _struct.unpack_from( "=b", raw_bytes, offset )[ 0 ], offset + 1


def from_native_uint16( raw_bytes, offset ):
    """ Reads a native-Endian 16-bit unsigned integer 
	from an array of bytes. """
    return _struct.unpack_from( "=H", raw_bytes, offset )[ 0 ], offset + 2


def from_native_int16( raw_bytes, offset ):
    """ Reads a native-Endian 16-bit signed integer 
	from an array of bytes. """
    return _struct.unpack_from( "=h", raw_bytes, offset )[ 0 ], offset + 2


def from_native_uint32( raw_bytes, offset ):
    """ Reads a native-Endian 32-bit unsigned integer 
	from an array of bytes. """
    return _struct.unpack_from( "=I", raw_bytes, offset )[ 0 ], offset + 4


def from_native_int32( raw_bytes, offset ):
    """ Reads a native-Endian 32-bit signed integer 
	from an array of bytes. """
    return _struct.unpack_from( "=i", raw_bytes, offset )[ 0 ], offset + 4


def from_native_uint64( raw_bytes, offset ):
    """ Reads a native-Endian 64-bit unsigned integer 
	from an array of bytes. """
    return _struct.unpack_from( "=Q", raw_bytes, offset )[ 0 ], offset + 8


def from_native_int64( raw_bytes, offset ):
    """ Reads a native-Endian 64-bit signed integer 
	from an array of bytes. """
    return _struct.unpack_from( "=q", raw_bytes, offset )[ 0 ], offset + 8


def from_string( raw_bytes, offset, count = 0 ):
    """ Converts a sequence of NUL-terminated bytes to a Python string. """

    s_out = ""
    i = 0

    while True:
        c = raw_bytes[ offset + i ]
        if 0 == c: break
        s_out += chr( c )
        i += 1
        if count and (i == count): break

    return s_out, i


@_contextmanager
def database_session_scope( Session ):
    """ Provides a transactional scope around a series of operations. """

    session = Session( )
    try:
        yield session
        session.commit( )
    except:
        session.rollback( )
        raise
    finally:
        session.close( )


# Dominions Platforms
def PLATFORM_LINUX( ):     return "Linux"
def PLATFORM_MACOSX( ):    return "MacOS X"
def PLATFORM_WINDOWS( ):   return "Windows"


class DominionsVersion( object ):
    """ Dominions version with comparison for ordering. """

    import re               as _re


    _RE_SPLIT_VERSION   = _re.compile( r"^(\d{1})\.(\d{2})(\w?)$" )


    _platform           = None
    _version            = None


    @classmethod
    def from_program_image( cls, program_image ):
        """ Create an instance, using data gathered from the image
            of a Dominions executable, if possible. """

        if   "version 4.01" == from_string( program_image, 0x255686, 12 )[ 0 ]:
            platform, version = PLATFORM_LINUX( ), "4.01"
        elif "version 4.03" == from_string( program_image, 0x256372, 12 )[ 0 ]:
            platform, version = PLATFORM_LINUX( ), "4.03"
        elif "version 4.04" == from_string( program_image, 0x2336A5, 12 )[ 0 ]:
            platform, version = PLATFORM_LINUX( ), "4.04"
        else:
            raise LookupError( "Could not determine Dominions version." )
        
        return cls( platform, version )


    def __lt__( self, dominions_version ):
        """ Returns True if this Dominions version is
            less than another one. """

        return 0 > self._compare_version( dominions_version )


    def __gt__( self, dominions_version ):
        """ Returns True if this Dominions version is
            greater than another one. """

        return 0 < self._compare_version( dominions_version )


    def __eq__( self, dominions_version ):
        """ Returns True if this Dominions version is
            equal to another one. """

        return 0 == self._compare_version( dominions_version )


    def _compare_version( self, dominions_version ):
        """ Compares this Dominions version with another one,
            returning -1 if the other version is greater, 
            0 if the versions are equivalent, 
            and 1 if this version is greater. """

        this = self._RE_SPLIT_VERSION.findall( self._version )[ 0 ]
        that = self._RE_SPLIT_VERSION.findall( dominions_version.version )[ 0 ]
        result = list( filter( None, map(
            lambda x, y: (x > y) - (x < y), this, that
        ) ) )

        return result[ 0 ] if result else 0


    def __init__( self, platform, version ):
        
        super( DominionsVersion, self ).__init__( )
        self._platform = platform
        self._version = version


    @property
    def platform( self ):
        """ Operating system on which Dominions runs. """

        return self._platform


    @property
    def version( self ):
        """ Version string of Dominions. """

        return self._version


class PrettyFormatConfig( object ):
    """ Configuration for the various pretty-formatters in use. """


    _DEFAULTS = {
        "indent": "", "line_width": 79,
        "key_format": "s",
        "render_title": True, "render_key_with_object": True,
        "render_compactly": False, "suppress_unknowns": False
    }


    def __init__( self, **kwargs ):
        
        attrs_DICT = self._DEFAULTS.copy( )
        attrs_DICT.update( kwargs )
        for key, value in attrs_DICT.items( ):
            setter_name = "_set_" + key
            if hasattr( self, setter_name ):
                getattr( self, setter_name )( value )
        

    def clone( self, **kwargs ):
        """ Returns a clone of the calling instance,
            selectively altering properties of the clone as desired. """

        attrs_DICT = { k: getattr( self, k ) for k in self._DEFAULTS.keys( ) }
        attrs_DICT.update( kwargs )
        return PrettyFormatConfig( **attrs_DICT )


    def _get_indent( self ): return self._indent
    def _set_indent( self, indent ): self._indent = indent
    indent = property(
        fget = _get_indent, fset = _set_indent,
        doc = """ Indentation string. """
    )


    def _get_line_width( self ): return self._line_width
    def _set_line_width( self, line_width ): self._line_width = line_width
    line_width = property(
        fget = _get_line_width, fset = _set_line_width,
        doc = """ Line width. """
    )


    def _get_key_format( self ): return self._key_format
    def _set_key_format( self, key_format ): self._key_format = key_format
    key_format = property(
        fget = _get_key_format, fset = _set_key_format,
        doc = """ Key format. """
    )


    def _get_render_title( self ): return self._render_title
    def _set_render_title( self, render_title ):
        self._render_title = render_title
    render_title = property(
        fget = _get_render_title, fset = _set_render_title,
        doc = """ Render title? """
    )


    def _get_render_key_with_object( self ):
        return self._render_key_with_object
    def _set_render_key_with_object( self, render_key_with_object ):
        self._render_key_with_object = render_key_with_object
    render_key_with_object = property(
        fget = _get_render_key_with_object, fset = _set_render_key_with_object,
        doc = """ Render key with object? """
    )


    def _get_render_compactly( self ): return self._render_compactly
    def _set_render_compactly( self, render_compactly ):
        self._render_compactly = render_compactly
    render_compactly = property(
        fget = _get_render_compactly, fset = _set_render_compactly,
        doc = """ Render compactly? """
    )


    def _get_suppress_unknowns( self ): return self._suppress_unknowns
    def _set_suppress_unknowns( self, suppress_unknowns ):
        self._suppress_unknowns = suppress_unknowns
    suppress_unknowns = property(
        fget = _get_suppress_unknowns, fset = _set_suppress_unknowns,
        doc = """ Suppress unknowns? """
    )


def pprint_bit_names_table(
        bit_names_table, stream_print = print, pre_ws = "\t"
):
    """ Nicely prints pairs of bitmask values and their names
        from the given mask table. """

    for bit, bit_name in bit_names_table.items( ):
        stream_print( pre_ws + "{bit:20d}: {bit_name}".format(
            bit = bit, bit_name = bit_name
        ) )


def pprint_bitmask( mask, title, mask_bits_table, stream_print = print ):
    """ Nicely prints the bitwise interpretation of a mask value. """

    if not mask: return
    if -1 == mask:
        stream_print( "{title}: -1".format( title = title ) )
        return

    if 0 > mask: mask = -mask
    bits_info = [
        "{bit_name} [{bit}]".format( bit_name = bit_name, bit = bit )
        for bit, bit_name in mask_bits_table.items( ) if bit & mask
    ]
    stream_print( "{title}: {bits_info} [Total: {mask}]".format(
        title = title, bits_info = ", ".join( bits_info ), mask = mask,
    ) )


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #
