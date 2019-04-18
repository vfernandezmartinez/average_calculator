# Description

  * The CSV is processed while it is being downloaded. It is not stored anywhere.
  * To increase performance, the data is assumed to be in ASCII, thus allowing us to save decoding of UTF-8 data.
  * Data is read in chunks. readline() is not used, which allows us to increase performance.


The implementation imposes the following restriction:

  * Line length cannot be longer than 64 kbytes.

Notes:

  * Since requirements specify that only vanilla Python 3 should be used, no modules such as pandas or numpy were used.

  * The returned line count includes the header line. Therefore, the total number of actual rows in the CSV is this line count - 1.

  * A simple unit test is included to ensure code correctness. To run it:

  * * python3 -m unittest
