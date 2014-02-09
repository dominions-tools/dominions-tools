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
    Provides a wide assortment of useful modules. The modules cover these
    areas:
        
        * :py:mod:`utility functions <.utils>`
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division                as _FUTURE_division,
    absolute_import         as _FUTURE_absolute_import,
    print_function          as _FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


import sys
import collections


# Get Python version.
PythonVersion = collections.namedtuple(
    "PythonVersion", "flavor major minor"
)
if (3 == sys.version_info[ 0 ]) and (3 <= sys.version_info[ 1 ]):
    python_version = PythonVersion(
        sys.implementation.name,
        sys.version_info.major, sys.version_info.minor
    )
else:
    # Note: Access 'version_info' members by index rather than name for 
    #       Python 2.6 compatibility.
    python_version = PythonVersion(
        sys.subversion[ 0 ], sys.version_info[ 0 ], sys.version_info[ 1 ]
    )


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #
