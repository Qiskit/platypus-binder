# This code is a derivative work of the Qiskit Optimization Module
# -----------------------------------------------------------------

# This code is part of Qiskit.
#
# (C) Copyright IBM 2021, 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
This is a module for working with Quadratic Programs. 

To run a Quadratic Program on a quantum computer we need to convert all 
constraints into pentalites and this module contains the tools to help achieve 
this

"""

from .quadratic_program import QuadraticProgram
from .exceptions import QuadraticProgramError


__all__ = ["QuadraticProgram", "QuadraticProgramError"]
