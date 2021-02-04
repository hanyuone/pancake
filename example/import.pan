[ "inc" "map-fn" ] "./example/list.pan" require

0 =index
{ n : n inc } [ 1 2 3 4 5 ] map-fn execute print
