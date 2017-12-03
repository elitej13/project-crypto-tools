# About Crypto tools

This program comes with two main tools.

****************************************RSA****************************************

The first tool includes the ability to generate RSA keys based on user input.
It can then attempt to crack the key using a simple brute force algorithm.
This algorithm is timed and can be given a max time to give up upon reaching.
Of course it will be faster if there is no time constraint to check against each
frame.

The algorithm can also be spread across multiple threads based on user
input. The maximum thread count that is currently implemented is 64. In theory
having n more threads makes the algorithm n times faster, but of course this
assumes a bit about your own computers hardware. So the increase of speed may
diminish beyond a certain thread count.

****************************************Hill****************************************

The Hill cipher portion of the program is divided into two sections: encrypt and
decrypt. For encryption the user inputs a message and presses enter to validate
and potentially pad it with spaces. Then the user must pick a block size (n) to
break up the message into. An nxn key matrix of random numbers from 0 to 89 is
then generated and multiplied by each block of the message. The resulting vectors
are then converted back into an ascii string and printed along with the key.

For decryption a message is entered followed by the key that was used to encrypted
the message. The formatting of the key is that of column major and is critical to
get correct. It is also important to only use numbers.

A 3x3 matrix would look like:
[1,2,3],[4,5,6],[7,8,9]
Where each section denoted by square brackets is a column vector. And inside of
each vector contains the entries of the matrix from top to bottom. This same format
can be used for any sized square matrix.

Upon entering the key the inverse mod of the key is calculated and multiplied by
each block of the message to give the decrypted message. Both the decrypted message
and the inverse mod of the key matrix are then printed to screen.

# Libraries
The GUI was all built on top of a library called Kivy which is free, easy to use,
and can be found at:
https://kivy.org/

Most of the complex math operations were done using a library sympy. Sympy is
free and can be found at:
https://sympy.org

# Math
For more information on the math used in this project consider visiting
https://simple.wikipedia.org/wiki/RSA_(algorithm)
or
https://en.wikipedia.org/wiki/Hill_cipher

# Source Code
This project was made in python and the code for which can be found online at the
git repository:
https://github.com/elitej13/project-crypto-tools

# License
This project uses an MIT license which can be found in the same folder as this document or in the git repo.
