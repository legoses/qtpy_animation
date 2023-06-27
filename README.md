# README
In its current iteration, this is pretty rough, but it should provide enough functionality for basic animations. <br>

Before using, make sure you have circuit python installed. <br>
Currently, this only works for 14x4 displays. <br>
<br>
In order to use this, do not clone directly to the qtpy storage. These devices have a very small amount of storage, and space should be saved where possible.<br>
Instead, clone to your computers hard drive, and copy which ever library directly to the qtpy. Each library can be used on their own and do not require any dependencies.<br><br>
Animation.py makes it simple to create basic animations and works well with adafruits library to control the board, however it is heavier to run and may not work well on all boards. <br>
If that is the case, display.py may work better. It does not require any additional libraries, and can handle functions such as brightness and writing to the display.

![Label Guide](images/segmentLabels1.png)

See code.py for examples and further explanations.
