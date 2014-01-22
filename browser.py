from rdflib import Graph, Literal, URIRef
from flask import request, render_template

# create Flask app
from flask import Flask
app = Flask(__name__)

# configure Flask app
DEBUG = True
app.config.from_object(__name__)

# list of disallowed RDF predicates
DISALLOWED_PREDICATE_NAMES = [
    "isDefinedBy",
    "comment",
    "description",
]

def is_allowed(triple):
    """
    Return True if the triple can be printed in the graph. Disallowed
    triples are ones that relate to themselves, or contain predicates
    that are in DISALLOWED_PREDICATE_NAMES.
    """

    # reject triples with predicates that aren't allowed
    for predicate in DISALLOWED_PREDICATE_NAMES:
        if predicate in triple[1]:
            return False

    # reject self-referring triples, regardless of the relationship
    if triple[0] == triple[2]:
        return False

    return True

def make_readable(element):
    """
    Return a readable version of the passed element.

    For literals, newlines are removed. For URIs with
    fragments, everything before the fragment is removed,
    and all whitespace is removed. For URIs without
    fragments, whitespace is removed, and everything after
    the last slash is removed (if there is no slash, just
    the URI is returned).

    For all other types of elements, no processing is done;
    the element is just returned verbatim.

    Empty results are returned as the string "<None>".
    """

    if isinstance(element, URIRef):

        uri = element
        uri = uri.replace(" ", "")
        uri = uri.replace("\n", "")

        if "#" in uri:
            words = uri.split("#")[-1]

        elif "/" in uri:
            words = uri.split("/")[-1]

        else:
            words = uri

    elif isinstance(element, Literal):
        words = element.replace("\n", "")

    else:
        words = element

    if len(words) == 0:
        return "<None>"

    return words

# views
@app.route('/', methods=['GET'])
def browse():

    triples = []
    uri     = request.args.get("uri", "")

    if uri:

        graph = Graph()

        # populate the graph
        try:
            graph.parse(uri, format="n3")

        # if the input is not in N3, try to get it in XML
        except SyntaxError:
            graph.parse(uri, format="xml")

        # make triples readable, and filter out undesired triples
        triples = [(subj, make_readable(pred), obj) for (subj, pred, obj) in graph]
        triples = filter(is_allowed, triples)

    return render_template('graph.html', uri=uri, triples=triples)

if __name__ == '__main__':
    app.run()
