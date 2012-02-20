#!/usr/bin/env python
"""Regex via FSM hopefully!"""
import sys

def get_is_char(c):
    """Creates function that checks to see if character is a char
    Returns the new index of the string we're at if True, else False
    >>> get_is_char('a')('abc', 0)
    1
    >>> get_is_char('b')('abc', 0)
    False
    >>> get_is_char('a').func_name
    'is_char_a'
    >>> get_is_char('b')('abc', 1)
    2
    >>> get_is_char('a')('abc', 3)
    False
    """
    def output_function(s, index):
        try:
            char_in_question = s[index]
        except IndexError:
            return False
        if c == char_in_question:
            return index+1
        else:
            return False
    output_function.func_name = 'is_char_'+c
    def new_repr(self):
        return '<function '+self.func_name+'>'
    output_function.__repr__ = new_repr
    return output_function

def get_is_in_char_set(l):
    """Creates function that checks to see if char is in char set
    Returns the new index of the string we're at if True, else False

    >>> get_is_in_char_set(['a', 'b', 'c'])('abc', 0)
    1
    >>> get_is_in_char_set(['b', 'c'])('abc', 0)
    False
    >>> get_is_in_char_set(['a']).func_name
    "is_in_char_set_['a']"
    >>> get_is_in_char_set(['b'])('abc', 3)
    False
    >>> get_is_in_char_set(['c'])('abc', 2)
    3
    >>> get_is_in_char_set(['c', '.'])('aaa', 0)
    1
    >>> get_is_in_char_set(['.'])('aaa', 0)
    1
    """
    def output_function(s, index):
        try:
            char_in_question = s[index]
        except IndexError:
            #print 'out of string! returning false'
            return False
        #print 'checking if', s[index], 'in', l
        if '.' in l:
            #print 'yep!'
            return index + 1
        if char_in_question in l:
            #print 'yep!'
            return index + 1
        else:
            #print 'nope!'
            return False
    output_function.func_name = 'is_in_char_set_'+str(l)
    def new_repr(self):
        return '<function '+self.func_name+'>'
    output_function.__repr__ = new_repr
    return output_function

def get_return_True():
    """Returns the current index (nothing consumed) unconditionally

    >>> get_return_True()('asdf', 0)
    0
    """
    def return_True(s, index):
        return index
    def new_repr(self):
        return '<function '+self.func_name+'>'
    return_True.__repr__ = new_repr
    return return_True

def group_classes(l):
    """groups char classes together
    >>> group_classes(list('a[bc]d'))
    ['a', ['b', 'c'], 'd']
    >>> group_classes(list('abc'))
    ['a', 'b', 'c']
    >>> group_classes(list('a[bc]{}d'))
    ['a', ['b', 'c'], '{', '}', 'd']
    """
    while True:
        try:
            left_index = l.index('[')
        except ValueError:
            if ']' in l:
                raise ValueError('too many ]\'s in list')
            return l
        right_index = l.index(']')
        chars_in_class = l[left_index+1:right_index]
        l.insert(left_index, chars_in_class)
        for i in range(left_index-1, right_index):
            l.pop(left_index + 1)

def associate_modifiers(l):
    """creates tuples of (class, num_times)
    >>> associate_modifiers(list('abc'))
    [(['a'], [1]), (['b'], [1]), (['c'], [1])]
    >>> associate_modifiers(['a', ['b', 'c'], 'd'])
    [(['a'], [1]), (['b', 'c'], [1]), (['d'], [1])]
    >>> associate_modifiers(['a', ['b', 'c'], '{', '1', ',', '6', '}', 'd'])
    [(['a'], [1]), (['b', 'c'], [1, 6]), (['d'], [1])]
    >>> associate_modifiers(['a', 'b', '+', 'd', '*'])
    [(['a'], [1]), (['b'], [1]), (['b'], inf), (['d'], inf)]
    """
    new_l = []
    need_number = False
    while True:
        try:
            popped_char = l.pop(0)
        except IndexError:
            if type(new_l[-1]) == tuple:
                pass
            else:
                new_l[-1] = (new_l[-1], [1])
            return new_l
        if type(popped_char) == list:
            if need_number:
                new_l[-1] = (new_l[-1], [1])
            new_l.append(popped_char)
            need_number = True
        elif popped_char == '{':
            num_spec_chars = []
            while True:
                lookahead_popped_char = l.pop(0)
                if lookahead_popped_char == '}':
                    nums_in_num_spec = [int(x) for x in ''.join(num_spec_chars).split(',')]
                    if len(nums_in_num_spec) == 1:
                        nums = nums_in_num_spec[0]
                    elif len(nums_in_num_spec) == 2:
                        nums = [nums_in_num_spec[0], nums_in_num_spec[1]]
                    else:
                        raise Exception("Logic Error: more than two nums in {}?")
                    new_l[-1] = (new_l[-1], nums)
                    need_number = False
                    break
                else:
                    num_spec_chars.append(lookahead_popped_char)
        elif popped_char == '*':
            new_l[-1] = (new_l[-1], float('inf'))
            need_number = False
        elif popped_char == '?':
            new_l[-1] = (new_l[-1], [0, 1])
            need_number = False
        elif popped_char == '+':
            new_l[-1] = (new_l[-1], [1])
            new_l.append((new_l[-1][0], float('inf')))
            need_number = False
        else:
            if need_number:
                new_l[-1] = (new_l[-1], [1])
            new_l.append([popped_char])
            need_number = True

def expand_multiple_nums(l):
    """Turns tuple (char class, {3, 5}) into 5 states

    >>> expand_multiple_nums([(['a', 'b'], [2, 3])])
    [(['a', 'b'], 1), (['a', 'b'], 1), (['a', 'b'], '?')]
    """
    new_l = []
    for char_class, nums in l:
        if nums == float('inf'):
            new_l.extend([(char_class, float('inf'))])
        elif len(nums) == 1:
            new_l.extend([(char_class, 1) for i in range(nums[0])])
        elif len(nums) == 2:
            new_l.extend([(char_class, 1) for i in range(nums[0])])
            new_l.extend([(char_class, '?') for i in range(nums[1] - nums[0])])
        else:
            raise Exception('Logic Error')
    return new_l

def convert_one_to_state_descriptions(char_class, num):
    """Creats states for a given char class and num
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

def create_state_machine(l):
    """Creates states for each char class and num"""
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
            state = State('state '+str(counter))
            state.transitions = transition_set
            inner_list.append(state)
            counter += 1
    groups_of_states.append([State('finished')])

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
    def __init__(self, name=None):
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

    def search(self, s, initial_index, allow_finish_early=False):
        """Populates yet_to_try, commences trying, return True if found"""
        yet_to_try = self.find_working_transitions(s, initial_index)
        #print 'transitions to try:', yet_to_try
        while True:
            try:
                state, index = yet_to_try.pop(0)
            except IndexError:
                #print 'nothing left to try! return False'
                return False
            if state.name == 'finished':
                #print 'found finished!'
                if len(s) == index or allow_finish_early:
                    return True
                else:
                    return False
            if state.search(s, index, allow_finish_early=allow_finish_early):
                #print 'exiting branch that worked!'
                return True
            #print 'exiting branch that didn\'t work'

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
    """
    def __init__(self, expression):
        self.expression = expression
        self.states = self.parse_regex(expression)
        self.search_states = None

    def __repr__(self):
        return '<parsed regex for "'+self.expression+'">'

    def parse_regex(self, expression):
        """Turns regex string into states of DFM"""
        l = list(expression)
        l = group_classes(l)
        l = associate_modifiers(l)
        l = expand_multiple_nums(l)
        states = create_state_machine(l)
        return states

    def match(self, s):
        """Returns true if string matches"""
        return self.states[0].search(s, 0)

    def search(self, s):
        """Returns true if string anywhere in file
        >>> [Regex('abc').search(x) for x in ['abc', '  abc  ', 'axabxabcx', 'xabcx', 'xaxbxc']]
        [True, True, True, True, False]
        """
        if not self.search_states:
            self.search_states = self.parse_regex('.*'+self.expression)
        return self.search_states[0].search(s, 0, allow_finish_early=True)

def demo_parse_regex(expression):
    """Turns regex string into states of DFM"""
    print expression
    l = list(expression)
    lprint(l)
    l = group_classes(l)
    lprint(l)
    l = associate_modifiers(l)
    lprint(l)
    l = expand_multiple_nums(l)
    lprint(l)
    states = create_state_machine(l)
    print states
    return states

def traverse_state_machine(states, s):
    pass

def lprint(l):
    print_list_no_quotes(l)
    sys.stderr.write('\n')

def print_list_no_quotes(l):
    sys.stderr.write('[')
    first = True
    for x in l:
        if first:
            first = False
        else:
            sys.stderr.write(' ')
        if type(x) == list:
            print_list_no_quotes(x)
        elif type(x) == tuple:
            print_list_no_quotes(x)
        else:
            sys.stderr.write(str(x))
    sys.stderr.write(']')

def test():
    p = 'asd?'
    print 'pattern:', p
    r = Regex(p)
    for s in ['asd', 'asdd', 'asdf', 'abd', 'as']:
        print s, r.match(s)

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)

    r = Regex('abc')
    #r.search('abc')
    #r.search('abc ')
    r.search('xabcx')

    #demo_parse_regex('[ab]cd')
    #demo_parse_regex('as{3,6}df[eg]+dfp*d.')
    #states = demo_parse_regex('asd?')
    #s = states[0]

