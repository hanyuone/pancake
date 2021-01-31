{ n : n 1 + } =>inc

{ list : 0 list nth } =>first

{ pred fn :
  {:} fn pred if
} =>when

{ pred fn :
  # Essentially a recursive function, checks to see if
  # the predicate returns true once executed, then runs
  # while again with the same predicate and function
  {: fn execute fn pred while } pred execute when
} =>while

{ list fn :
  0 =index
  {:
    index list nth =current
    current fn execute
    index inc =index
  } {: index list length < } while
} =>for

{ list fn :
  [] =result

  { item :
    {: item result append =result } item fn execute when
  } list for

  result
} =>filter

{ list fn :
  [] =result

  { item :
    item fn execute result append =result
  } list for

  result
} =>map

{ n : n 3 > } [ 1 2 3 4 5 ] filter print
