#!/usr/bin/env python
"""Regex via FSM hopefully!"""
import string

def get_is_char(c):
    """Creates function that checks to see if character is a char
    >>> s = list('abc')
    >>> get_is_char('a')(s)
    True
    >>> s
    ['b', 'c']
    >>> s = list('bc')
    >>> get_is_char('a')(s)
    False
    >>> s
    ['b', 'c']
    """
    def output_function(s):
        first_char = s.pop(0)
        if c == first_char:
            return True
        else:
            s.insert(0, first_char)
            return False
    return output_function

def get_is_in_char_set(l):
    """Creates function that checks to see if char is in char set

    >>> s = list('abc')
    >>> get_is_in_char_set(['a', 'b', 'c'])(s)
    True
    >>> s
    ['b', 'c']
    >>> s = list('abc')
    >>> get_is_in_char_set(['b', 'c'])(s)
    False
    >>> s
    ['a', 'b', 'c']
    """
    def output_function(s):
        first_char = s.pop(0)
        if first_char in l:
            return True
        else:
            s.insert(0, first_char)
            return False
    return output_function

class DFM(object):
    """Not actually what it says on the label"""
    def __init__(self, regex):
        self.regex = regex
        self.populate_states()
        self.states = []

    def populate_states(self):
        tokens = parse_regex(self.regex)

        self.states.append()
        pass

    def __repr__(self):
        return self.regex

    def match(self, s):
        pass


class State(object):
    """Transitions in the order we want to do them"""
    def __repr__(self):
        return self.name

    def __init__(self, check_next, check_self, name=None):
        """Given a thing"""
        self.check_next = check_next
        self.check_self = check_self
        self.name = name
        self.transitions = []

    def try_step_forward(self, s):
        return self.check_next(s)

    def try_step_self(self, s):
        return self.check_self(s)

def State_from_set_num_tuple(t):
    char_set, nums = t

    state = State(get_is_in_char_set(char_set), )


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

    >>> expand_multiple_nums([(['a', 'b'],[2,3])])
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

def parse_regex(expression):
    """turns regex string into states of DFM"""
    l = list(expression)
    print l
    l = group_classes(l)
    print l
    l = associate_modifiers(l)
    print l
    l = expand_multiple_nums(l)
    return l



if __name__ == '__main__':
    import doctest
    doctest.testmod()

    parse_regex('as{1,23}df[23]+dfp*d.')

    import sys
    sys.exit()

    def test():
        # a[bc]d matching into
        # abd
        a = State('state 1')
        b = State('state 2')
        c = State('state 3')
        a.transitions.append((get_is_char('a'), b))
        b.transitions.append((get_is_in_char_set(['b', 'c']), c))
        b.transitions.append((lambda x: True, a))
        c.transitions.append((get_is_char('d'), 'finish'))
        c.transitions.append((lambda x: True, b))

        s = list('abd')
        new_state = a
        while True:
            new_state = new_state.get_transition(s)
            #print 'moving to', new_state
            if new_state == 'finish':
                print 'finished, match!'
                break

    test()
