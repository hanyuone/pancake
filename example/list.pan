1 6 range =sample

1 5 sample slice print
0 5 range print
sample { item : item print } for
sample reverse print
sample { n : n 1 + } map print
sample { n : n 3 > } filter print
sample { a b : a b + } reduce print

sample
  { n : n 2 mod zero? } filter
  { n : n n * } map
  { a b : a b + } reduce
  print
