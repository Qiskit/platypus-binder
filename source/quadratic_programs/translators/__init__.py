# This code is a derivative work of the Qiskit Optimization 
# and Qiskit Nature Module
# --------------------------------------------------------------------------

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
Translator functions

1. DOCPLEX.MP (IBM Decision Optimization - Mathematical Programming Module) 
    -> QuadraticProgram
2. QuadraticProgram 
    -> Qiskit Operator in Sparse Pauli Formn (Quantum)

3. QCSchema 
    -> Fermi Operator 
4. Fermi Operator 
    -> Qiskit Operator in Sparse Pauli Formn (Quantum)

"""

from .docplex_mp_to_qp import docplex_mp_to_qp
from .qubo_to_sparse_pauli_op import qubo_to_sparse_pauli_op

__all__ = [
    "docplex_mp_to_qp", "qubo_to_sparse_pauli_op"
]
