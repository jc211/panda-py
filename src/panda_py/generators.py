"""
Control library for the Panda robot. The general workflow
is to instantiate a controller and hand it over to the
:py:class:`panda_py.Panda` class for execution using the
function :py:func:`panda_py.Panda.start_controller`.
"""

# pylint: disable=no-name-in-module
from ._core import JointMotionGenerator, Generator, CartesianMotionGenerator
                    
