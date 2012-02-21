#!/usr/bin/env python
"""Regex via FSM hopefully!"""
from stringtests import get_is_in_char_set
from stringtests import get_return_True
from regexparsing import parse_regex

def convert_one_to_state_descriptions(char_class, num):
    """Creates lists of transitions for a given char class and num
    char class is a list of chars
    num can be 1, ?, or inf

    >>> convert_one_to_state_descriptions(['a'], 1)
    [[(<function is_in_char_set_['a'] at ...>, 'next')]]
    >>> convert_one_to_state_descriptions(['b'], '?')
    [[(<function is_in_char_set_['b'] at ...>, 'next'), (<function return_True at ...>, 'next')]]
    >>> convert_one_to_state_descriptions(['c'], float('inf'))
    [[(<function is_in_char_set_['c'] at ...>, 'here'), (<function return_True at ...>, 'next')]]
    >>> convert_one_to_state_descriptions(['c', 'd'], float('inf'))
    [[(<function is_in_char_set_['c', 'd'] at ...>, 'here'), (<function return_True at ...>, 'next')]]
    >>> convert_one_to_state_descriptions(['.', 'd'], float('inf'))
    [[(<function is_in_char_set_['.', 'd'] at ...>, 'here'), (<function return_True at ...>, 'next')]]
    """
    descriptions = []
    if num == 1:
        descriptions.append([(get_is_in_char_set(char_class), 'next')])
    elif num == '?':
        descriptions.append([(get_is_in_char_set(char_class), 'next'), (get_return_True(), 'next')])
    elif num == float('inf'):
        descriptions.append([(get_is_in_char_set(char_class), 'here'), (get_return_True(), 'next')])
    else:
        raise Exception('Logic Error!')
    return descriptions

def create_state_machine(l, parent):
    """Creates states for each char class and num
    >>> create_state_machine([[['a'], 1], [['b'], 1]], None)
    [state 0, state 1, finished]
    """
    m = []
    for char_class, num in l:
        m.append(convert_one_to_state_descriptions(char_class, num))

    # make objects from transition sets
    groups_of_states = []
    counter = 0
    for group_of_transition_sets in m:
        inner_list = []
        groups_of_states.append(inner_list)
        for transition_set in group_of_transition_sets:
            state = State(parent, 'state '+str(counter))
            state.transitions = transition_set
            inner_list.append(state)
            counter += 1
    groups_of_states.append([State(parent, 'finished')])

    # remove 'next' and 'here' placeholders
    for group_index, group_of_states in enumerate(groups_of_states):
        for state_index, state in enumerate(group_of_states):
            for transition_index, transition in enumerate(state.transitions):
                if transition[1] == 'here': # this means this very state
                    groups_of_states[group_index][state_index].transitions[transition_index] = (transition[0], groups_of_states[group_index][state_index])
                elif transition[1] == 'next': # this means first state of next group of groups_of_states
                    groups_of_states[group_index][state_index].transitions[transition_index] = (transition[0], groups_of_states[group_index+1][0])
                else:
                    pass
    # flattening
    states = [state for group in groups_of_states for state in group]
    return states

class State(object):
    """Represents a state of a finite state machine, meaning transitions"""
    def __init__(self, parent, name=None):
        self.parent = parent
        self.name = name or 'unnamed'
        self.transitions = []
    def __repr__(self):
        return str(self.name)
    def find_working_transitions(self, s, i):
        """Returns list of state to try next and new string index"""
        working = []
        for transition in self.transitions:
            result = transition[0](s, i)
            if type(result) == bool and result == False:
                pass
            elif type(result) == int:
                working.append((transition[1], result))
        return working


class Regex(object):
    """Represents a regex pattern, can test strings

    >>> [Regex('asd?').match(x) for x in ['asd', 'asdd', 'asdf', 'abd', 'as']]
    [True, False, False, False, True]
    >>> [Regex('a*bc').match(x) for x in ['abc', 'bc', 'bbc', 'aabc', 'aadabc', 'aaabc']]
    [True, True, False, True, False, True]
    >>> [Regex('ab+c').match(x) for x in ['abc', 'ac', 'abbc', 'abbbc']]
    [True, False, True, True]
    >>> [Regex('[ab]cd').match(x) for x in ['acd', 'abc', 'bcd', 'ccd', 'abcd']]
    [True, False, True, False, False]
    >>> [Regex('a[bc]+d').match(x) for x in ['abd', 'acd', 'abcd', 'ad', 'abcbcd', 'abbbbcbcbcbcbcccd']]
    [True, True, True, False, True, True]
    >>> [Regex('a[bc]*d').match(x) for x in ['abd', 'ad', 'abcd', 'abcbcbccbd', 'abcebcd', 'abde']]
    [True, True, True, True, False, False]
    >>> [Regex('a.*d').match(x) for x in ['abd', 'ad', 'aasdfasdfd', 'a21.[]3d', 'aasdfd1', 'abde']]
    [True, True, True, True, False, False]
    >>> [Regex('a.+d').match(x) for x in ['abd', 'ad', 'aasdfasdfd', 'a3d', 'aasdfd1', 'abde']]
    [True, False, True, True, False, False]
    >>> [Regex('ab{1,3}c').match(x) for x in ['ac', 'abc', 'abbc', 'abbbc', 'abbbbc']]
    [False, True, True, True, False]
    """
    def __init__(self, expression):
        self.expression = expression
        self.states = self.parse_regex(expression)
        self.search_states = None
        self.method = 'depth-first'

    def __repr__(self):
        return '<parsed regex for "'+self.expression+'">'

    def parse_regex(self, expression):
        """Turns regex string into states of DFM"""
        l = parse_regex(expression)
        states = create_state_machine(l, self)
        return states

    def add_to_yet_to_try(self, items, use_search_states_instead=False):
        if self.method == 'depth-first':
            # then use a stack
            for item in items:
                self.yet_to_try.insert(0, item)
        elif self.method == 'breadth-first':
            # then use a queue
            for item in items:
                self.yet_to_try.append(0, item)

    def get_next_try(self):
        if len(self.yet_to_try) == 0:
            return False
        return self.yet_to_try.pop(0)

    def match(self, s):
        """Returns True if entire string matches pattern
        >>> [Regex('abc').match(x) for x in ['abc', 'xabc', 'abcx', 'ac']]
        [True, False, False, False]
        """
        self.string = s
        self.yet_to_try = [(self.states[0], 0)]
        while True:
            r = self.explore_next_node(allow_finish_early=False)
            if type(r) == bool:
                return r

    def search(self, s):
        """Returns true if string anywhere in file
        >>> [Regex('abc').search(x) for x in ['abc', '  abc  ', 'axabxabcx', 'xabcx', 'xaxbxc']]
        [True, True, True, True, False]
        """
        self.string = s
        if not self.search_states:
            self.search_states = self.parse_regex('.*'+self.expression)
        self.yet_to_try = [(self.search_states[0], 0)]
        while True:
            r = self.explore_next_node(allow_finish_early=True)
            if type(r) == bool:
                return r

    def explore_next_node(self, allow_finish_early=False, use_search_states_instead=False):
        """Finds new moves for a state, adds them to self.yet_to_try.
        A "node" is a (State, string index) combination, as returned from
        State.find_working_transitions"""
        try:
            state, index = self.get_next_try()
        except TypeError:
            return False
        #print 'trying this state:', state, index
        nodes = state.find_working_transitions(self.string, index)
        #print 'found these nodes we should try', nodes
        for state, index in nodes:
            if state.name == 'finished':
                #print 'found finished!'
                if len(self.string) == index or allow_finish_early:
                    return True
                else:
                    pass
        self.add_to_yet_to_try(nodes)


def demo_regex(p, s):
    r1 = Regex(p).match(s)
    r2 = Regex(p).search(s)
    print 'pattern: "'+p+'"'
    if len(s) < 60:
        print 'string:', s
    else:
        print 'string too long to print'
    print 'exact match:', r1
    print 'somewhere:', r2

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)

    from regexparsing import demo_parse_regex
    print 'Regex parsing demo'
    demo_parse_regex('as{3,6}df[eg]+dfp*d.')
    print

    print 'Regex matching demo'
    demo_regex('a.*d', 'aasdfasdfd')

