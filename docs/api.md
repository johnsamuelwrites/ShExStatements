ShExStatements API
------------------

### Operations

ShExStatements has also a public API that can be easily accessible both
on a local installation as well as on the public interface. It has one
operation that takes as input a JSON array with two elements as given
below:

-   delimiter
-   CSV (every line should be terminated by \\n)

It returns a JSON array with one element containing the ShEx (shape
expression).

### Example JSON input

Take for example the file `tvseries.json` (also present in
`examples/api/tvseries.json`). It is an array with two elements.


    [
    "|",
    "wd|<http://www.wikidata.org/entity/>|||\n
    wdt|<http://www.wikidata.org/prop/direct/>|||\n
    xsd|<http://www.w3.org/2001/XMLSchema#>|||\n
    \n
    @tvseries|wdt:P31|wd:Q5398426|# instance of a tvseries\n
    @tvseries|wdt:P136|@genre|*|# genre\n
    @tvseries|wdt:P495|.|+|#country of origin\n
    @tvseries|wdt:P57|.|+|#director\n
    @tvseries|wdt:P58|.|+|#screenwriter\n
    @genre|wdt:P31|wd:Q201658,wd:Q15961987|#instance of genre\n"
    ]

Calling ShExStatements API
--------------------------

Following is the way to call the ShExStatements API


    $ curl -s http://127.0.0.1:5000/ -X POST -H "Accept: application/json"  --data  @examples/api/tvseries.json |sed 's/\\n/\n/g'

or


    $ curl -s https://shexstatements.toolforge.org/ -X POST -H "Accept: application/json"  --data  @examples/api/tvseries.json |sed 's/\\n/\n/g'

### Example JSON output response

It gives the following output. For the output, the above command makes
use of `sed`.


    "PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    start = @<tvseries>
    <tvseries> {
      wdt:P31 [ wd:Q5398426  ] ;# instance of a tvseries
      wdt:P136 @<genre>* ;# genre
      wdt:P495 . ;#country of origin
      wdt:P57 . ;#director
      wdt:P58 . ;#screenwriter
    }
    <genre> {
      wdt:P31 [ wd:Q201658 wd:Q15961987  ] ;#instance of genre
    }
    "
