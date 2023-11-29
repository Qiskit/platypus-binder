# This code is part of Qiskit.
#
# (C) Copyright IBM 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""

"""

from typing import Sequence


from qiskit.circuit import  Qubit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import Layout

def permute_sparse_pauli_op(
    operator: SparsePauliOp,
    layout: Layout,
    original_qubits: Sequence[Qubit],
) -> SparsePauliOp:
    """
    Args:
       operator: Operator to be transpiled.
       layout: The layout of the transpiled circuit.
       original_qubits: Qubits that original circuit has.

    Returns:
        The operator for the given layout.
    """
    virtual_bit_map = layout.get_virtual_bits()
    identity = SparsePauliOp("I" * len(virtual_bit_map))
    perm_pattern = [virtual_bit_map[v] for v in original_qubits]
    return identity.compose(operator, qargs=perm_pattern)