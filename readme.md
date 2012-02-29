state machine Regex matcher
---------------------------

TODO

 * Turn the NFA into a DFA!
   * hopefully making this faster than builtin python regex engine for pathological expressions
 * add parens to allow character concatenation, like this: a(bc)+d
   * state engine generator is ready for this, would just have to add to parser
