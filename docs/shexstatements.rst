shexstatements package
======================

It's also possible to use ``shexstatements`` in Python programs. This page gives a complete detail of the different modules that can be used in the programs.

In our first example, we take a look at the method ``generate_shex_from_csv``, which takes as input a CSV file containing shexstatements and a delimiter. In this example, we use "," as a delimiter.

::

  from shexstatements.shexfromcsv import CSV

  shex = CSV.generate_shex_from_csv("language.csv", delim=",")
  print(shex)

In our second example, we use a data string consisting of shexstatements and make use of the function ``generate_shex_from_data_string``. Note here, that we use "|" as a delimiter.
::

  from shexstatements.shexfromcsv import CSV 
  
  shexstatements="""
  wd|<http://www.wikidata.org/entity/>
  wdt|<http://www.wikidata.org/prop/direct/>
  xsd|<http://www.w3.org/2001/XMLSchema#>
  
  @language|wdt:P31|wd:Q34770|# instance of a language
  @language|wdt:P1705|LITERAL|# native name
  @language|wdt:P17|.|+|# spoken in country
  @language|wdt:P2989|.|+|# grammatical cases
  @language|wdt:P282|.|+|# writing system
  @language|wdt:P1098|.|+|# speakers
  @language|wdt:P1999|.|*|# UNESCO language status
  @language|wdt:P2341|.|+|# indigenous to
  """
  
  shex = CSV.generate_shex_from_data_string(shexstatements) 
  print(shex)


Submodules
----------


shexstatements.shexfromcsv
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: shexstatements.shexfromcsv
   :members:

shexstatements.shexjfromcsv
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: shexstatements.shexjfromcsv
   :members:

shexstatements.shexfromapplprofilecsv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: shexstatements.shexfromapplprofilecsv
   :members:


shexstatements.errors
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: shexstatements.errors
   :members:
