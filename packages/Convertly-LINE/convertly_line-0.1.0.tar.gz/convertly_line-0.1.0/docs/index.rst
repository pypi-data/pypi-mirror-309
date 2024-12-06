.. converter documentation master file, created by
   sphinx-quickstart on Tue Nov  5 15:45:57 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Convertly_LINE - Documentation
==========================
.. toctree::
   :maxdepth: 2
   :caption: Contents:

Welcome to **Convertly_LINE**, the powerful unit conversion library that allows you to easily convert between various units, currencies, and time zones. This library is designed to provide accurate, fast, and reliable conversions across a wide range of categories.

Current Version: 1.0.0  
Future updates will introduce more categories and improved functionalities.

Installation
------------

To get started with **Convertly_LINE**, simply install it via `pip`:

.. code-block:: bash

    pip install convertly_line

Features
--------

- **Unit Conversion**: Convert between units of measurement, including length, weight, and temperature in both the **International System of Units (SI)** and **Imperial (Anglosajón)** systems.
- **Currency Conversion**: Convert between various global currencies (divisas) with up-to-date exchange rates.
- **Time Zone Conversion**: Get the current or a specified time in any location worldwide, making it easy to manage time differences between different time zones.
- Simple and intuitive interface for performing conversions.
- Easy to extend and update with new conversion categories.

Functions of the library
________________________

.. autosummary::
   :toctree: generated/

   convertly_line.measure_convertor
   convertly_line.convert_temperature
   convertly_line.UnitConverter
   convertly_line.UnitConverter.convert
   convertly_line.UnitConverter.to_base
   convertly_line.UnitConverter.from_base
   convertly_line.time_zones
   convertly_line.convert_currency

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
