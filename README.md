rdf-browser
===========

A graphical browser for RDF objects. It takes a URI to some Notation-3 or XML RDF data and displays them as a graph using arbor.js. It's very minimal, very simple, and written in Flask.

To run it locally, execute:

    python browser.py

Then, point your browser to the URI on which it says it started serving (usually `http://127.0.0.1:5000`). Some sample RDF data can be found [here][samples1] and [here][samples2]. An interesting example file to look at is http://www.w3.org/2000/10/swap/test/meet/white.n3.

[samples1]: http://www.bl.uk/bibliographic/datasamples.html
[samples2]: http://www.rdfdata.org/
