{ a :} =>pop

{ a : a a } =>dup

{ a b : b a } =>swap

{ a fn : fn execute a } =>dip

{ n : n 1 + } =>inc

{ list : 0 list nth } =>first

{ fn bool :
  {:} fn bool if
} =>when

{ fn pred :
  {: fn execute fn pred while } pred dip swap when
} =>while # Depends on the first element on the stack

{ start end list :
  [] start
  {:
    =index
    index list nth swap append
    index inc
  } {: dup end < } while
  pop
} =>slice

{ list fn :
  0
  {:
    =index
    index list nth fn execute
    index inc
  } {: dup list length < } while
  pop
} =>for

{ list fn :
  []
  list { item :
    item fn execute swap append
  } for
} =>map

{ list fn :
  []
  list { item :
    {: item swap append } item fn execute when
  } for
} =>filter

{ list fn :
  list first
  1 list length list slice
  { item :
    item fn execute
  } for
} =>reduce
