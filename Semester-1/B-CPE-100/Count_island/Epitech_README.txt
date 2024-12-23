# How to test your count_island function easily

Simply build your C files with the given main.o file.
For instance: gcc -o count_island *.c main.o

This object file  includes a main function that does the necessary magic to read a map given as parameter, convert it to a char** that is passed to your count_island function.

You can use it like so:
./count_island foo.txt

It will display the map that is the result of your function.

!!! You can see in the given map, `foo.txt`, that the first line contains a number.
It is the number of lines of the map. It is only used by our main function and will not be contained in your function's parameter. !!!
