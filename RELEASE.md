# v0.8 (in progress)
===============================================================================
*

# v0.7
===============================================================================
* Support more than one input CSV files on the command line
* Support option to run web application from the command line (`--run`)
* Update documentation
* Prepare `pip` first release

# v0.6
===============================================================================
* Move cli argument parsing to `shexstatements` folder 
* Move web application program to `shexstatements` folder
* Prepare configuration for a `pip` package

# v0.5 
===============================================================================
* API for shexstatements
  * JSON input array with two parameters
  * ShEx as json output array
* Support CSV file upload (web interface)
* Add API documentation

# v0.4 
===============================================================================
* Web interface
  * Add support for online generation of ShEx
  * Use of Flask
* New features
  * Support IMPORT
  * Allow # in nodenames
  * Add >< for CLOSED
  * Add ++ for EXTRA
  * Support code coverage
  * Add Github actions to test package
* Update documentation
  * Update web interface documentation
  * Update README with demo links
  * Update About section
  * Add CSS and images
  * Add documentation for coverage
  * Add command for reporting code coverage
  * Add link to Software Heritage
* Bugs
  * Resolve shift-reduce conflict
  * Update unit tests
  * Remove Python 3.5
* Examples
  * Add hospital (Malayalam) example 
  * Add examples on dataset, API and sparql endpoints

# v0.3
===============================================================================
* documentation for ShExStatements
  * Installation and working with Python virtualenv 
* Comments can have special characters (,.)
* Support for additional forms of cardinality
  * ?: one or more values
  * m,: m or more values
* Support negative statements
* Suport for case-insentive node kinds
  * Literal, BNode, NonLiteral, IRI
* Support for types in third column
  * values starting with @@ considered as types

# v0.2
===============================================================================

* Support for specifying CSV header
  * --skipheader or -s option in shexstatement.sh
  * skipheader function argument in CSV.generate_shex_from_csv
* Support generation of ShExJ from CSV files 
  * --shexj or -j option in shexstatement.sh
* Supports input in the form of Application Profile
  * --applicationprofile or -ap option in shexstatement.sh
* Handling cardinality values of the form (in addition to +,\*)
  * number
  * number,number

# v0.1
===============================================================================
* Support generation of ShEx from CSV files 
* Support for prefixes, keywords like EXTRA, CLOSED etc. 
