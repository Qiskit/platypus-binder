# This code is part of Qiskit.
#
# (C) Copyright IBM 2023
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Default Workflow for transforming a Quadradic Program with 
Constraints to a Quadratic Program without constraints (QUBO form)

"""
from .fulqrum import Workflow


from ..quadratic_program.passes import (InequalityToEquality,
                                      IntegerToBinary,
                                      LinearEqualityToPenalty,
                                      LinearInequalityToPenalty,
                                      MaximizeToMinimize,
                                      EvaluateProgramSolution,
                                      UnrollQUBOVariables
                                     )

def QuadraticProgramConverter():
    return Workflow([InequalityToEquality(), # Transformation
                     IntegerToBinary(), # Transformation
                     LinearEqualityToPenalty(), # Transformation
                     LinearInequalityToPenalty(), # Transformation
                     MaximizeToMinimize(), # Transformation
                    ], name='quadratic-converter')


def QuadraticProgramPostprocess(qubo, quadratic_transformer):
    return Workflow([EvaluateProgramSolution(qubo),
                     UnrollQUBOVariables(quadratic_transformer),
                    ], name='quadratic-postprocess')