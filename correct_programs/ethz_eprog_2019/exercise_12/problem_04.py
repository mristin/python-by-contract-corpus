"""
Analyze the words of a text.

We consider not only the content of a word as string, but also its position in the text.
A word can appear in multiple locations in the text. (We consider inflections as
different words: "go" and "goes" are considered two different words.)

We define an order of the words. A word ``x`` is smaller than a word ``y`` if the
difference between the first and last occurrence of ``x`` is smaller than the
corresponding difference for ``y``.

Provide a function to extract words from a text.

Provide a function ``top`` to return the largest ``n`` words based on the aforementioned
order.

"""
