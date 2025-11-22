"""
This file extends some of the mutation functions and the PrimitiveSet class
from the DEAP evolutionary computing framework's gp.py file which is released
under the GNU LESSER GENERAL PUBLIC LICENSE version 3, 29 June 2007
"""

import random
import sys
from collections import defaultdict
from deap import tools, base, gp, creator

class Condition(gp.Terminal):
    
    def __init__(self, terminal, symbolic, ret):
        super(Condition, self).__init__(terminal, symbolic, ret)

class Action(gp.Terminal):
    
    def __init__(self, terminal, symbolic, ret):
        super(Action, self).__init__(terminal, symbolic, ret)

class PrimitiveSetExtended(gp.PrimitiveSet):
    """
    Extends DEAP's PrimitveSet class to be able to distinguish
    between different types of behaviour tree nodes so that we
    can control the ratio of condition nodes vs action nodes
    """

    def __init__(self, names, in_types):
        self.conditions = defaultdict(list)
        self.actions = defaultdict(list)
        self.conditions_count = 0
        self.actions_count = 0
        super(PrimitiveSetExtended, self).__init__(names, in_types)

    def _add(self, prim):
        def addType(dict_, ret_type):
            if ret_type not in dict_:
                new_list = []
                for type_, list_, in dict_.items():
                    if issubclass(type_, ret_type):
                        for item in list_:
                            if item not in new_list:
                                new_list.append(item)
                dict_[ret_type] = new_list
        
        addType(self.primitives, prim.ret)
        addType(self.terminals, prim.ret)
        addType(self.conditions, prim.ret)
        addType(self.actions, prim.ret)
        
        self.mapping[prim.name] = prim
        
        if isinstance(prim, gp.Primitive):
            for type_ in prim.args:
                addType(self.primitives, type_)
                addType(self.terminals, type_)
            dict_ = self.primitives
        elif isinstance(prim, Condition):
            dict_ = self.conditions
        elif isinstance(prim, Action):
            dict_ = self.actions
        
        for type_ in dict_:
            if issubclass(prim.ret, type_):
                dict_[type_].append(prim)

    def addCondition(self, condition, name=None):
        
        symbolic = False
        
        if name is None and callable(condition):
            name = condition.__name__
        
        assert name not in self.context, "\nname "+name+" is not unique\n"
        
        if name is not None:
            self.context[name] = condition
            condition = name
            symbolic = True
        elif condition in (True, False):
            self.context[str(condition)] = condition
        
        prim = Condition(condition, symbolic, gp.__type__)
        self._add(prim)
        self.conditions_count += 1
        
    def addAction(self, action, name=None):
        
        symbolic = False
        
        if name is None and callable(action):
            name = action.__name__
        
        assert name not in self.context, "\nname "+name+" is not unique\n"
        
        if name is not None:
            self.context[name] = action
            action = name
            symbolic = True
        elif action in (True, False):
            self.context[str(action)] = action
        
        prim = Action(action, symbolic, gp.__type__)
        self._add(prim)
        self.actions_count += 1

def genEmpty(pset, min_, max_, type_=None):
    """
    For big mad robot repo
    """
    return []

def genFull(pset, min_, max_, type_=None):
    """
    From DEAP
    """

    def condition(height, depth):
        return depth == height

    return generate(pset, min_, max_, condition, type_)
   
def generate(pset, min_, max_, condition, type_=None):
    """
    Chooses the type of terminal node (condition or action)
    with equal probability before selecting a specific node
    """
    if type_ is None:
        type_ = pset.ret
    expr = []
    height = random.randint(min_, max_)
    stack = [(0, type_)]
    while len(stack) != 0:
        depth, type_ = stack.pop()
        if condition(height, depth):
            try:
                node_type = random.choice([pset.conditions[type_], pset.actions[type_]])
                term = random.choice(node_type)
            except IndexError:
                _, _, traceback = sys.exc_info()
                raise IndexError("The gp.generate function tried to add "
                                 "a terminal of type '%s', but there is "
                                 "none available." % (type_,)).with_traceback(traceback)
            # if type(term) is MetaEphemeral:
                # term = term()
            expr.append(term)
        else:
            try:
                prim = random.choice(pset.primitives[type_])
            except IndexError:
                _, _, traceback = sys.exc_info()
                raise IndexError("The gp.generate function tried to add "
                                 "a primitive of type '%s', but there is "
                                 "none available." % (type_,)).with_traceback(traceback)
            expr.append(prim)
            for arg in reversed(prim.args):
                stack.append((depth + 1, arg))
    return expr

def mutUniform(individual, expr, pset):
    """
    From DEAP
    """
    index = random.randrange(len(individual))
    slice_ = individual.searchSubtree(index)
    type_ = individual[index].ret
    individual[slice_] = expr(pset=pset, type_=type_)
    return individual,

def mutNodeReplacement(individual, pset):
    """
    Chooses the type of terminal node (condition or action)
    with equal probability before selecting a specific node
    """
    if len(individual) < 2:
        return individual,

    index = random.randrange(1, len(individual))
    node = individual[index]

    if node.arity == 0:  # Terminal
        node_type = random.choice([pset.conditions[node.ret], pset.actions[node.ret]])
        term = random.choice(node_type)
        individual[index] = term
    else:  # Primitive
        prims = [p for p in pset.primitives[node.ret] if p.args == node.args]
        individual[index] = random.choice(prims)

    return individual,

def mutShrink(individual):
    """
    From DEAP
    """
    # We don't want to "shrink" the root
    if len(individual) < 3 or individual.height <= 1:
        return individual,

    iprims = []
    for i, node in enumerate(individual[1:], 1):
        if isinstance(node, gp.Primitive) and node.ret in node.args:
            iprims.append((i, node))

    if len(iprims) != 0:
        index, prim = random.choice(iprims)
        arg_idx = random.choice([i for i, type_ in enumerate(prim.args) if type_ == prim.ret])
        rindex = index + 1
        for _ in range(arg_idx + 1):
            rslice = individual.searchSubtree(rindex)
            subtree = individual[rslice]
            rindex += len(subtree)

        slice_ = individual.searchSubtree(index)
        individual[slice_] = subtree

    return individual,

