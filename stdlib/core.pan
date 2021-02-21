# STACK MANIPULATION (inspiration from Factor)

{ a :} =>pop

{ a : a a } =>dup

{ a b : b a } =>swap

{ a fn : fn exec a } =>dip

# CONTROL FLOW

{ fn bool :
  {:} fn bool if
} =>when

{ fn bool :
  fn {:} bool if
} =>unless

# NOTE: function depends on the first element in the stack only,
#       any elements besides the top one are ignored
{ fn pred :
  {: fn exec fn pred while } pred dip swap when
} =>while

{ fn pred :
  {: fn exec fn pred until } pred dip swap unless
} =>until

# MATHS OPERATIONS

{ n : n 1 + } =>inc

{ n : n 1 - } =>dec

{ n : n 0 eq } =>zero?

{ n : n 0 > } =>pos?

{ n : n 0 < } =>neg?

# ARRAY MANIPULATION

{ list : 0 list nth } =>first

{ start end list :
  [] start
  {:
    =index
    index list nth swap append
    index inc
  } {: dup end < } while
  pop
} =>slice

{ start end :
  [] start
  {:
    =index
    index swap append
    index inc
  } {: dup end < } while
  pop
} =>range

{ list fn :
  0
  {:
    =index
    index list nth fn exec
    index inc
  } {: dup list length < } while
  pop
} =>for

{ list :
  [] list length dec
  {:
    =index
    index list nth swap append
    index dec
  } {: dup neg? } until
  pop
} =>reverse

# HIGHER-ORDER FUNCTIONS

{ list fn :
  []
  list { item :
    item fn exec swap append
  } for
} =>map

{ list fn :
  []
  list { item :
    {: item swap append } item fn exec when
  } for
} =>filter

{ list fn :
  list first
  1 list length list slice
  { item :
    item fn exec
  } for
} =>reduce
