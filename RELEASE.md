# v0.3 (in progress)
===============================================================================
* documentation for ShExStatements
  * Installation and working with Python virtualenv 
* Comments can have special characters (,.)
* Support for additional forms of cardinality
  * ?: one or more values
  * m,: m or more values
* Support negative statements

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
