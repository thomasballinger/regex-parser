#!/usr/bin/env python
"""Functions which generate functions that check a string at an index,
returning the advanced index if match"""

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

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
