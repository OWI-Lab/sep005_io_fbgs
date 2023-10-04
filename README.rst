SEP005 FBGS io
-----------------------

Basic package to import data collected from FBGS data compliant with
SDyPy format for timeseries as proposed in SEP005.

Using the package
------------------

    .. code-block:: python

        from sep005_io_fbgs import read_fbgs

        file_path = # Path to the tdms file of interest
        signals = read_fbgs(file_path)

Acknowledgements
----------------
This package was developed in the framework of the
`Interreg Smart Circular Bridge project
<https://vb.nweurope.eu/projects/project-search/smart-circular-bridge-scb-for-pedestrians-and-cyclists-in-a-circular-built-environment/>`_