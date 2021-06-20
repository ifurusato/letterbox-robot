*****************************************************************************
Letterbox-Robot: The operating system for a robot that resides in a letterbox
*****************************************************************************

This provides a *Robot Operating System* (ROS) for a Raspberry Pi based robot
written in Python 3, whose prototype hardware implementations is a fixed-location
robot that resides in a letterbox.

The hardware consists of a PIR sensor and an HT0740 Switch controlling a 12v
power supply to toggle a 2.5 meter strip of white LEDs, to light the garden path.


.. image:: https://service.robots.org.nz/wiki/attach/LBR01/LetterboxRobot2778.jpg
   :width: 1200px
   :align: center
   :height: 676px
   :alt: The LBR01 Robot

More information can be found on the New Zealand Personal Robotic Group (NZPRG) Blog at:

* `Facilius Est Multa Facere Quam Diu <https://robots.org.nz/2020/04/24/facilius-est/>`

and the NZPRG wiki at:

* `LBR01 Robot <https://service.robots.org.nz/wiki/Wiki.jsp?page=LBR01>`

This project is part of the *New Zealand Personal Robotics (NZPRG)* "Robot
Operating System" — not to be confused with other "ROS" projects. 


Features
********

* `Behaviour-Based System (BBS) <https://en.wikipedia.org/wiki/Behavior-based_robotics>`
* `Subsumption Architecture <https://en.wikipedia.org/wiki/Subsumption_architecture>` [#f1]_
* Configuration via YAML file
* written in Python 3

.. [#f1] Uses finite state machines, an asynchronous message queue, an arbitrator and controller for task prioritisation.


Status
******

This project should currently be considered a "**Technology Preview**".

The project is still in an early prototyping stage.

The project is being exposed publicly so that those interested can follow its
progress. At such a time when the ROS is generally useable this status section
will be updated accordingly.


Installation
************

The project requires installation of a number of support libraries. In order to
begin you'll need Python3 (at least 3.8) and pip3.

The setup.py script performs a standard library installation. You can also use::

    sudo pip3 install -e .


Support & Liability
*******************

This project comes with no promise of support or liability. Use at your own risk.


Further Information
*******************

For more information check out the `NZPRG Blog <https://robots.org.nz/>` and
`NZPRG Wiki <https://service.robots.org.nz/wiki/>`.

Please note that the documentation in the code will likely be more current
than this README file, so please consult it for the "canonical" information.


Execution
*********

To force the Raspberry Pi to prioritise execution of the python operating
system, use the 'chrt' command, e.g.::

    % chrt -f 5 python3 ./fusion_test.py



Copyright & License
*******************

All contents (including software, documentation and images) Copyright 2020-2021
by Murray Altheim. All rights reserved.

This file is part of the Robot Operating System project, released under the MIT License.

Software and documentation are distributed under the MIT License, see LICENSE
file included with project.

