777533779
312320716
*****
Comments:
Our evaluation function is built by various criteria. Each one of them is given a weight according to their importance
to achieve success. We decided to use the strategy where the tile with the greater value is in the corner and
is followed by other tiles sorted in descending order. In order to achieve this, we decided to assign a bonus point to
the state in which we start the first line with the max tile in the corner, followed by the second, the third, and the
fourth max tile in descending order.

In addition to the bonus point, we also gave weight to the sum of all the numbers in the board, the number of free
tiles, and the max tile.

