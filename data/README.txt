

The ascii formats here were created from the SaveSIFT() method.

(Note that sometimes the ascii features occur in a different order.  I
suppose that this is not a bug, but it makes testing a pain sometimes...)


The binary formats here were created from VisualSfM, and they follow
the file format described here:

  http://ccwu.me/vsfm/doc.html

The binary formats should be readable by sift_reader.py

The binary formats are sorted according to scale, so the features
should always be in the same order.  (Unless two features happen to
have exactly the same scale, in which case I suppose that the order
is undefined...)

