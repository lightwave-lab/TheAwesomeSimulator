===========
The Awsome Simulator Library (version 0.5)
===========

The Awesome Simulator Library (AwSimLib) is an open-source compilation of
tools to disect and analyze physics simulations. In this initial release,
we provide a file-parser for the DF-ISE file format, commonly used in the
Synopsys Sentaurus simulation suite. In addition, we provide a method of
aligning Lumerical FDTD grids with Sentaurus SDevice FEM grids.

Typical usage often looks like this::

    import sys
    sys.path.append('./AwSimLib/') #path to the AwSimLib folder
    from AwSimLib.fileIO import DFISE
    from AwSimLib.sim import grids as grids
    

Authorship
=========
Author: Abhejit Rajagopal <abhejit@umail.ucsb.edu><abhejit@ucla.edu>
Copyright 2014

License
=========
This product is licensed under GNU LGPL Version 3 license.
A copy of the license is provided with this software, in LICENSE.txt.

Credits
=========
The DF-ISE parser was inspired by the Ph.D thesis of Michael Kelzenberg:
<http://thesis.library.caltech.edu/5938/>
<http://thesis.library.caltech.edu/5938/1/mkelzenberg_thesis.pdf>
<http://mkelzenb.caltech.edu/thesis/mk_thesis_appB.pdf>

Although M. Kelzenberg demonstrated a similar method in 2D before (2010),
neither had it been shown for 3D nor had it been generalized to handle any
data-type. Also, this project was implemented in Python (a free software)
as opposed to MATLAB (commercial software).
