#!/usr/bin/env python
"""Functions for parsing a regular expression into tuples of character
classes
"""
import sys
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

def lprint(l):
    print_list_no_quotes(l)
    sys.stderr.write('\n')

def parse_regex(expression):
    """Turns regex string into tuple pairs of char class and modifier"""
    return expand_multiple_nums(associate_modifiers(group_classes(list(expression))))

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
