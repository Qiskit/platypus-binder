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
QUBO workflow
"""
import numpy as np
from . validation import validate_output_type
from quadratic_programs.workflows.fulqrum import PropertySet


class UnrollQUBOVariables():
    """Unroll QUBO variables to their original definitions
    """
    def __init__(self, workflow):
        self.workflow = workflow
        self.input_types = (tuple, )
        self.output_types = (np.ndarray, )
        self.property_set = PropertySet()

    @validate_output_type
    def run(self, solution):
        x = np.fromiter(solution[1], dtype=int)
        for converter in self.workflow.blocks[::-1]:
            x = converter.interpret(x)
        return x
