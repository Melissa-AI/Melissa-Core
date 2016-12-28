# Run this program from the top level directory, one directory up, as
# python -m create_lm

import os
import urllib2
import urllib
from bs4 import BeautifulSoup

# Melissa
try:
    import melissa.actions_db as actions_db
except ImportError:
    import sys
    sys.path.insert(0,
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import melissa.actions_db as actions_db
    del sys.path[0]

# Poster
import poster.encode as encode
from poster.streaminghttp import register_openers


def get_language_model():
    print 'Retrieving the language model.'

    # Register the streaming http handlers with urllib2
    register_openers()

    data1 = encode.MultipartParam("formtype", "simple")
    data2 = encode.MultipartParam.from_file(
        "corpus", "./data/model/phrase_list.txt")
    datagen, headers = encode.multipart_encode([data1, data2])

    # Create the Request object
    request = urllib2.Request(
        "http://www.speech.cs.cmu.edu/cgi-bin/tools/lmtool/run", datagen, headers)
    # Do the request, and get the response
    data = urllib2.urlopen(request).read()

    # Get all the anchors.
    soup = BeautifulSoup(data, "html.parser")
    anchors = soup.find_all('a')

    # Get the base name and its numeric part.
    base = os.path.basename(anchors[0]['href'])
    num_part = os.path.splitext(base)[0][3:]

    # Get the url less the base name.
    url = anchors[0]['href']
    url_dir = url[:-len(base)]

    # Construct the url for LM download.
    dic = url_dir + num_part + '.dic'
    lm = url_dir + num_part + '.lm'

    # Download and save the LM.
    urllib.urlretrieve(dic, './data/model/lm/sphinx.dic')
    urllib.urlretrieve(lm, './data/model/lm/sphinx.lm')
    print 'Created ./data/model/lm/sphinx.dic and ./data/model/lm/sphinx.lm'


def create_phrase_list():
    queries = ()
    with open('./data/model/user_queries.txt', 'r') as f:
        queries = [line.rstrip().lower() for line in f]

    sql = "SELECT word_group " \
        + "FROM word_groups " \
        + "ORDER BY word_group"

    actions_db.cur.execute(sql)
    word_groups = actions_db.cur.fetchall()
    word_groups = [x[0].lower() for x in word_groups]  # flatten list of tuples

    # combine the text queries and the mysql word groups.
    queries.extend(word_groups)
    queries_set = set(queries)
    if '' in queries_set:
        queries_set.remove('')

    with open('./data/model/phrase_list.txt', 'w') as f:
        f.write("\n".join(sorted(queries_set)))


def main():
    create_phrase_list()
    get_language_model()

main()
