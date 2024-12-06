# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


# pylint: disable=line-too-long
''' Accretive objects.

Provides the base class for objects with accretive attributes. Once an
attribute is set on an instance, it cannot be reassigned or deleted.

The implementation uses a special dictionary type for attribute storage that
enforces the accretive behavior. This makes it suitable as a base class for:

* Configuration objects
* Plugin interfaces
* Immutable data containers
* Objects requiring attribute stability

>>> from accretive import Object
>>> obj = Object( )
>>> obj.x = 1  # Add new instance attribute
>>> obj.y = 2  # Add another instance attribute
>>> obj.x = 3  # Attempt modification
Traceback (most recent call last):
    ...
accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'x'.
'''
# pylint: enable=line-too-long


from . import __
from . import classes as _classes


class _Dictionary(
    __.CoreDictionary[ __.H, __.V ], metaclass = _classes.Class
): pass


class Object:
    ''' Accretive objects. '''

    __slots__ = ( '__dict__', )

    def __init__( self, *posargs: __.a.Any, **nomargs: __.a.Any ) -> None:
        super( ).__setattr__( '__dict__', _Dictionary( ) )
        # Pass all arguments down MRO chain without consuming any.
        super( ).__init__( *posargs, **nomargs )

    def __repr__( self ) -> str:
        return "{fqname}( )".format( fqname = __.calculate_fqname( self ) )

    def __delattr__( self, name: str ) -> None:
        from .exceptions import AttributeImmutabilityError
        raise AttributeImmutabilityError( name )

    def __setattr__( self, name: str, value: __.a.Any ) -> None:
        if hasattr( self, name ):
            from .exceptions import AttributeImmutabilityError
            raise AttributeImmutabilityError( name )
        super( ).__setattr__( name, value )

Object.__doc__ = __.generate_docstring(
    Object, 'instance attributes accretion' )
