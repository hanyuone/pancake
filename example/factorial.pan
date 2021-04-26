{ a : a a } =>dup

{ a : a 1 - } =>dec

{ n :
  {: n, n dec factorial, *, dup, print } {: 1 1 print } 1 n eq, if
} =>factorial

20 factorial
