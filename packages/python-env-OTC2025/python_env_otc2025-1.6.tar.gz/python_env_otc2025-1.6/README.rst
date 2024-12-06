During the interactive lectures of the OTC 2025 shore-based course, you will
need to install tools and libraries for reading, processing and visualizing
data.

To make sure all students get the same environment, a bundle containing
SEAScope [1]_, Python 3.12.6 and additional material required by some lectures has
been created.


Installation
============

To install the software bundle:

1. Locate a disk/partition with the most free space on your computer (software
   itself does not take much space, but data used during the lectures will
   require several gigabytes)

2. Create a new directory on that disk/partition, all the software and data
   used during the course will be stored in that directory.

   Note that moving the directory elsewhere or renaming it will create
   problems, so choose wisely (using a short and meaningful name such as
   ``otc25`` is recommended).

   This directory will be referred to as the "OTC directory" in the upcoming
   instructions.

3. The next steps depend on your operating system:

   **Linux**

   * Download https://ftp.odl.bzh/odl/events/otc25/software/linux-otc25-bundle.sh

   * Save the file in the OTC directory

   * Open your file browser (or a terminal) and go to the OTC directory, then
     double-click on the bundle file (or execute it from the terminal).

   +------------------------------------------------------------------------+
   | Depending on the web browser used to download the bundle, you may have |
   | to make the file executable before double-clicking on it (either using |
   | your file browser or by running the ``chmod +x linux-otc25-bundle.sh`` |
   | command in a terminal.                                                 |
   +------------------------------------------------------------------------+

   **Windows**

   * Download https://ftp.odl.bzh/odl/events/otc25/software/windows-otc25-bundle.bat

   * Save the file in the OTC directory

   * Open your file browser (or a terminal) and go to the OTC directory,
     then double-click on the bundle file (or execute it from the
     terminal).

   +---------------------------------------------------------------+
   | Windows might issue a warning regarding the execution of the  |
   | file, click on the "More info" link so Windows will display a |
   | button allowing you execute the file anyway.                  |
   +---------------------------------------------------------------+

   **macOS**

   * Install SEAScope using the instructions available on https://seascope.oceandatalab.com/macos.html

   * Open a terminal

   * Move to the OTC directory using the ``cd`` command

   * Execute the following command:

     .. code:: bash

        curl -fsSL https://ftp.odl.bzh/odl/events/otc25/software/macos_get-otc25.sh | sh


4. The installation of the bundle will start and will take several minutes.

   A message is displayed at the end of the installation process, explaining
   how to start SEAScope and a new terminal already set up for the training
   course.

Verification
============

The software bundle includes a small tool to check that the environment is
correctly installed.

To perform this check:

1. Using a file browser, go to the OTC directory

2. Start SEAScope:

   **Linux**

   * Go to the ``seascope`` sub-directory

   * Double-click on the ``seascope`` file

   **Windows**

   * Go to the ``seascope`` sub-directory

   * Double-click on the ``SEAScope`` shortcut

   **macOS**

   * Click on the SEAScope application

   The SEAScope viewer will start and display a globe.

   Keep the viewer running, it will be used in the next steps.

4. In your file browser, go back to the OTC directory, there should be a file
   named ``Terminal.sh`` (Linux), ``Terminal.bat`` (Windows) or ``Terminal``
   (macOS).

   Double-click on that file (or execute it) to open a terminal.

5. In the terminal, type:

   .. code:: bash

      otc2025-check-environment

   It might take some time depending on your computer but at the end it should
   open a Jupyter notebook in your web browser, and the "OTC" letters should
   appear on the globe in the SEAScope viewer.

   Please follow the instructions mentioned in the notebook to determine
   whether or not the tests were successful.

   Each notebook cell can be executed by pressing Shift+Enter or by clicking on
   the button with a "Play" symbol (▶).

6. Close the notebook in your web browser. You can also stop the SEAScope
   viewer and close your terminal.

   You're ready for the interactive lectures! :)

Additional information
======================

+-----------------------------------------------------------------------------+
| The OTC environment installed with the bundle scripts are independent from  |
| your operating system and should not require any admin permissions.         |
+-----------------------------------------------------------------------------+

+-----------------------------------------------------------------------------+
| The bundle scripts modify some Python packages to make them compatible with |
| Python 3.12.                                                                |
+-----------------------------------------------------------------------------+


.. [1] on macOS SEAScope must be installed separately
