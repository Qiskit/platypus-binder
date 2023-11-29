# This code is part of a Qiskit project.
#
# (C) Copyright IBM 2018, 2023.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Fulqrum
"""
import copy


class PropertySet(dict):
    """A default dictionary-like object"""
    def __missing__(self, key):
        return None

class Workflow:
    def __init__(self, blocks, name='', store_final_output=False, strict_validation=True):
        self.blocks = blocks
        self.stages = {}
        self.name = name
        self.store_final_output = store_final_output
        self.input_types = None
        self.output_types = None
        self.strict_validation = strict_validation
        self._validate_passes()
        self.property_set = PropertySet()

    def _validate_passes(self):
        self.input_types = self.blocks[0].input_types
        input_types = self.blocks[0].input_types
        for _, individual_pass in enumerate(self.blocks):
            # If the pass is itself a CompositeWorkflow then run its validation
            if isinstance(individual_pass, Workflow):
                if individual_pass.name in self.stages:
                    raise Exception(f'Duplicate stage name {individual_pass.name}')
                self.stages[individual_pass.name] = individual_pass
                individual_pass._validate_passes()
                continue
            temp_input_types = individual_pass.input_types
            # Look to see if there is overlap between last passes outputs
            # and this passes inputs
            input_overlap = set(input_types).intersection(set(temp_input_types))
            # If no overlap, bad news
            if not input_overlap:
                raise Exception(f"{temp_input_types} not compatible with {input_types}")
            # If partial overlap, then can only weakly validate the workflow, raise
            # unless explicitly disabled
            if len(input_overlap) != len(temp_input_types) and self.strict_validation:
                diffs = set(input_types).difference(set(temp_input_types))
                raise Exception(f"Possible inputs {diffs} not valid for this pass")
            input_types = individual_pass.output_types
        self.output_types = individual_pass.output_types
    
    def run(self, input):
        temp = copy.deepcopy(input)
        working_props = self.property_set
        for individual_pass in self.blocks:
            individual_pass.property_set = working_props
            temp = individual_pass.run(temp)
            if isinstance(individual_pass, Workflow):
                if individual_pass.store_final_output:
                    working_props[individual_pass.name] = {"final_output": temp}
        if self.store_final_output:
             working_props[self.name] = {"final_output": temp}
        return temp


class LazyEval:
    def __init__(self, object, keys):
        if not isinstance(keys, tuple):
            keys = tuple(keys)
        self.object = object
        self.keys = keys
        self.evaled_object = None
    def __getattr__(self, attr):
        if self.evaled_object:
            return getattr(self.evaled_object, attr)
        self.lazyeval_return()
    def lazyeval_return(self):
        res = self.object
        for key in self.keys:
            res = res.get(key)
        self.evaled_object = res
        return res
