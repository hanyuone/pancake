{ a b : a b mod zero? } =>multiple?

{ n :
  2 n range { item : item print, n item multiple? } filter empty?
} =>prime?

31 prime? print
