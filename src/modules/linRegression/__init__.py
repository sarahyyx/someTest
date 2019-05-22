'''Simple Linear Regression Module

This model takes in x and y numpy arrays from the data directory and uses the data to fit a linear regression model, which is plotted on a scatter plot.
The same x array is then passed through the model to generate a fitted linear regression line, which is plotted on the same plot. 

Before you Begin
================

Make sure that the configuration files are properly set, as mentioned in the Specifcations 
section. Also, [add any other housekeeping that needs to be done before starting the module]. 

Details of Operation
====================

[
Over here, you should provide as much information as possible for what the modules does. 
You should mention the data sources that the module uses, and important operations that
the module performs.
]
Data sources: 
 - x, y are found in the someTest/data directory, and are both numpy arrays
 Important operations:
  - Fits x and y data into a linear regression model
  - Passes x data into the model to obtain predictions of the y value

Results
=======

[
You want to describe the results of running this module. This would include instances of
the database that the module updates, as well as any other files that the module creates. 
]
A plot.png showing the plotted results will be created in the data folder.

Specifications:
===============

Specifications for running the module is described below. Note that all the json files
unless otherwise specified will be placed in the folder ``config`` in the main project
folder.

Specifications for the database:
--------------------------------

[
Note the tables within the various databases that will be affected by this module.
]

Specifications for ``modules.json``
-----------------------------------

Make sure that the ``execute`` statement within the modules file is set to True. 

.. code-block:: python
    :emphasize-lines: 3

    "moduleName" : "module1",
    "path"       : "modules/module1/module1.py",
    "execute"    : true,
    "description": "",
    "owner"      : ""


Specification for [any other files]
-----------------------------------

[
Make sure that you specify all the other files whose parameters will need to be
changed. 
]

'''