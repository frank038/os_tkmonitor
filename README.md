THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY. Anyone can use and modified it for any purpose. Just remember the author.

<big>Os_tkmonitor</big>
by frank38

A simple system monitor in Python3/Tkinter.

This program is written using Python3 and Tkinter. The only external additional module required is psutil.

This program shows some infos about the PC. Among them, about CPU and GPU. About the GPU: at the moment only the Nvidia GPUs are supported (because I own one), but other vendors can be added easily: empty module are provided.

How to use: just type in the terminal 'python3 os_tkmonitor.py' or double click on it.
In this case, no GPU infos are shown. To get them, type 'python3 os_tkmonitor.py 1 nvidia (or nouveau or amdpro or radeon or intel)' where 1 is the update interval of the cpu infos.

The tab CPU shows some infos about the cpu: usage, frequencies and temperature per physical core.

Please, whatch the pictures for a better explanation.
