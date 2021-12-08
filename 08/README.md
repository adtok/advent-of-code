

## Recap

I used the following approach for part two:

I used `script.py` to figure out how many segments each code with length 5 intersected with the unique codes to come up with a table. The headers are the digits with unique length, and the rows correspond to the digits with repeating length. The entries in the table are the number of segments that intersect:

```
val |  1   4   7   8 | sum
----+----------------+-----
  2 |  1   2   2   5 |  10
  3 |  2   3   3   5 |  13
  5 |  1   3   2   5 |  11
  0 |  2   3   3   6 |  14
  6 |  1   3   2   6 |  12
  9 |  2   4   3   6 |  15
```

Realizing for each each 5 and 6 segmented code had a unique sum of the number of intersections with the digit codes for their given length, I would be able to derive every code for every input if all the unique codes were present in each input. I quickly verified that was the case and implemented a solution that gathers the codes with unique lengths, checks sum of the intersections of each code that has a repeating length and generates a master key. 