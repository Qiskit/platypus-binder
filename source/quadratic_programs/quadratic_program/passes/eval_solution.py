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

from qiskit.result import QuasiDistribution

from .validation import validate_output_type
from quadratic_programs.workflows.fulqrum import PropertySet, LazyEval


class EvaluateProgramSolution:
    """Evaluate solutions
    """
    def __init__(self, program=None):
        self.program = program
        self.input_types = (QuasiDistribution, )
        self.output_types = (tuple, )
        self.property_set = PropertySet()

    @validate_output_type
    def run(self, dist):
        if self.program is None:
            self.program = self.property_set['qubo-transformer']['final_output']
        if isinstance(self.program, LazyEval):
            self.program = self.program.lazyeval_return()
        best_val = np.inf
        best_bits = None
        for bitstring in dist.binary_probabilities():
            temp = evaluate_quadratic_program(bitstring, self.program)
            if temp < best_val:
                best_val = temp
                best_bits = bitstring
        best_bits = best_bits[::-1]
        out = (best_val, np.fromiter(best_bits, int))
        return out


def evaluate_quadratic_program(bitstring, program):
    constant = program.objective.constant
    linear_elements = program.objective.linear.to_dict()
    quadratic_elements = program.objective._quadratic.to_dict()

    # Flip string so 0th bit is 0th array element for easy math
    x = np.fromiter(list(bitstring[::-1]), dtype=int)
    
    sum = constant
    for element, val in linear_elements.items():
        sum += x[element] * val
    for element, val in quadratic_elements.items():
        sum += x[element[0]] * val * x[element[1]]
    return sum
