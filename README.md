# ShExStatements
ShExStatements allows the users to generate shape expressions from simple CSV statements, CSV files and Spreadsheet. `shexstatements` can be used from the command line as well as from the web interface.

## Quick start

### Using pip
Set up a virtual environment and install `shexstatements`.

```
$ python3 -m venv .venv
$ source ./.venv/bin/activate
$ pip3 install shexstatements
```

Run the following command with an [example CSV file](https://github.com/johnsamuelwrites/ShExStatements/tree/master/examples/language.csv). The file contains an example description of a language on Wikidata. This file uses comma as a delimiter to separate the values.
```
$ shexstatements.sh examples/language.csv
```
 
## Build from source 
### Terminal
Clone the **ShExStatements** repository.
```
$ git clone https://github.com/johnsamuelwrites/ShExStatements.git 
```

Go to **ShExStatements** directory.
```
$ cd ShExStatements
```

Install modules required by **ShExStatements** (here: installing into a virtual environment).
```
$ python3 -m venv .venv
$ source ./.venv/bin/activate
$ pip3 install .
```

Run the following command with an example CSV file. The file contains an example description of a language on Wikidata. This file uses comma as a delimiter to separate the values.
```
$ ./shexstatements.sh examples/language.csv
```

CSV file can use delimiters like _;_. Take for example, the following command works with a file using semi-colon as a delimiter.

```
$ ./shexstatements.sh examples/languagedelimsemicolon.csv --delim ";"
```

But sometimes, users may like to specify the header. In that case, they can make use of `-s` or `--skipheader` to tell the generator to skip the header (firsrt line of CSV).

```
$ ./shexstatements.sh --skipheader examples/header/languageheader.csv 
```

It is also possible to work with Spreadsheet files like .ods, .xls or .xlsx.
```
$ shexstatements.sh examples/language.ods
```

```
$ shexstatements.sh examples/language.xls
```

```
$ shexstatements.sh examples/language.xlsx
```

In all the above cases, the shape expression generated by **ShExStatements** will look like
```
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
start = @<language>
<language> {
  wdt:P31 [ wd:Q34770  ] ;# instance of a language
  wdt:P1705 LITERAL ;# native name
  wdt:P17 .+ ;# spoken in country
  wdt:P2989 .+ ;# grammatical cases
  wdt:P282 .+ ;# writing system
  wdt:P1098 .+ ;# speakers
  wdt:P1999 .* ;# UNESCO language status
  wdt:P2341 .+ ;# indigenous to
}
```

Use `-j` or `--shexj` to generate ShEx JSON Syntax (ShExJ) instead of default ShEx Compact syntax (ShExC).

```
$ ./shexstatements.sh --shexj examples/language.csv 
```

The output will be similiar to:

```json
{
  "type": "Schema",
  "start": "language",
  "shapes": [
    {
      "type": "Shape",
      "id": "language",
      "expression": {

      }
    }
  ]
}
```
It's also possible to use application profiles of the following form
```
Entity_name,Property,Property_label,Mand,Repeat,Value,Value_type,Annotation
```
and Shape expressions can be generated using the following form
```
$ ./shexstatements.sh -ap --skipheader examples/languageap.csv 
```


## Objectives
* Easily generate shape expressions (ShEx) from CSV files and Spreadsheets
* Simple syntax


## Documentation and examples
A detailed documentation can be found [here](https://github.com/johnsamuelwrites/ShExStatements/tree/master/docs/docs.md). with a number of example CSV files in the [examples](https://github.com/johnsamuelwrites/ShExStatements/tree/master/examples) folder.

## Test cases and coverage
All the test cases can be run in  the following manner
```
$ python3 -m tests.tests
```

Code coverage report can also be generated by running the unit tests using the coverage tool.
```
$ coverage run --source=shexstatements -m unittest tests.test
$ coverage report -m
```

### Web interface
`shexstatements` can also be accessed from a web interface.
Clone the **ShExStatements** repository.
```
$ git clone https://github.com/johnsamuelwrites/ShExStatements.git 
```

Go to **ShExStatements** directory.
```
$ cd ShExStatements
```

Install modules required by **ShExStatements** (here: installing into a virtual environment).
```
$ python3 -m venv .venv
$ source ./.venv/bin/activate
$ pip3 install .
```

Now run the application.
```
$ ./shexstatements.sh -r 
```

Check the URL `http://127.0.0.1:5000/`

## API
ShExStatements also has an API to generate ShEx from CSV and is described [here](https://github.com/johnsamuelwrites/ShExStatements/tree/master/docs/api.md).

## Demonstration
Online demonstrations are also available:

* [https://shexstatements.toolforge.org/](https://shexstatements.toolforge.org/)
* [https://tools.wmflabs.org/shexstatements/](https://tools.wmflabs.org/shexstatements/)

## Author
* John Samuel
* [Contributors](https://github.com/johnsamuelwrites/ShExStatements/graphs/contributors)

## Acknowledgements
* Wikidata Community

## Archives and Releases
* [Zenodo](https://doi.org/10.5281/zenodo.3723870)
* [Software Heritage](https://archive.softwareheritage.org/browse/origin/https://github.com/johnsamuelwrites/ShExStatements/directory/)
* [Release Notes](RELEASE.md)

## Licence
All code are released under GPLv3+ licence. The associated documentation and other content are released under [CC-BY-SA](https://creativecommons.org/licenses/by-sa/4.0/).
