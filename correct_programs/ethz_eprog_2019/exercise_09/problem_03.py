"""
Parse the file containing the list of bonus flying miles.

Here is an example:

.. code-block::

    Michaela Meier
    LX326 05.12.2016 ECONOMY
    LX317 10.01.2017 ECONOMY
    A3851 12.05.2017 BUSINESS
    LX8 12.10.2017 FIRST 4433
    .
    Stefan Oliver Schmid
    LX4150 19.10.2017 BUSINESS 6404
    .

The list consists of blocks. Each block begins with the name of the flier. The name
is then followed by the list of flights. For each flight, the flight number, the flight
date (in ``dd.mm.yyyy``), the class of the flight ("ECONOMY", "BUSINESS", "FIRST")
are given. If it is an inter-continental flight, the number of miles follows
the class of flight.

If no miles are given, you can assume a "flat-rate" of 125 miles. The miles flown in
"BUSINESS" are counted double and the miles in "FIRST" triple, respectively.

Output the number of miles per person.

For the aforementioned example:

.. code-block::

    Michaela Meier: 13799
    Stefan Oliver Schmid: 12808
"""
