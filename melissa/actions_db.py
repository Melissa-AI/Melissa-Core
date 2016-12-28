import importlib
import pkgutil
import sqlite3
import sys
import os

# Melissa
import profile

con = 0
cur = 0
modules = {}


def create_actions_db(con, cur):

    try:
        cur.executescript("""
            CREATE TABLE synonyms (
              synonym varchar(50) PRIMARY KEY,
              word varchar(50)
            );

            CREATE TABLE words (
              word varchar(50),
              word_group varchar(255),
              word_order integer
            );

            CREATE INDEX word_index ON words (word);

            CREATE TABLE word_groups (
              word_group varchar(255),
              function varchar(255),
              word_count integer
            );

            CREATE INDEX word_group_index ON word_groups (word_group);

            CREATE TABLE functions (
              function varchar(255) PRIMARY KEY,
              priority integer
            );

            CREATE TABLE expression (
              word varchar(50) PRIMARY KEY,
              word_order integer
            );
            """)
        con.commit()

    except sqlite3.Error as err:
        print "Error %s:" % err.args[0]
        sys.exit(1)

    return True


def insert_words(con, cur, name, words, priority):

    # Jasper format, each word in list is a word_group
    if isinstance(words, type([])):  # if words is a list

        function_name = name + ' ' + 'handle'
        try:
            cur.execute(
                "INSERT INTO functions (function, priority) "
                + "values ('{fn}',{p})"
                .format(fn=function_name, p=priority))

        except sqlite3.Error as err:
            print "Error %s:" % err.args[0]
            sys.exit(1)

        for word in words:
            word = word.lower()
            cur.execute(
                "INSERT INTO words (word, word_group, word_order) "
                + "values ('{w}','{wg}',{seq})"
                .format(w=word, wg=word, seq=0))

            cur.execute(
                "INSERT INTO word_groups "
                + "(word_group, function, word_count) "
                + "values ('{wg}','{fn}',{cnt})"
                .format(wg=word, fn=function_name, cnt=1))

        con.commit()

    # Melissa format, dictionary of function name
    # and list of word match groups (lists)
    elif isinstance(words, type({})):  # if words is a dictionary

        for function_name, fields in words.iteritems():

            function_name = name + ' ' + function_name
            priority = fields['priority'] if 'priority' in fields \
                else 0
            try:
                cur.execute(
                    "INSERT INTO functions (function, priority) "
                    + "values ('{fn}',{p})"
                    .format(fn=function_name, p=priority))

            except sqlite3.Error as err:
                print "Error %s:" % err.args[0]
                sys.exit(1)

            for group in fields['groups']:
                if isinstance(group, type('')):

                    word = group.lower()

                    cur.execute(
                        "INSERT INTO word_groups "
                        + "(word_group, function, word_count) "
                        + "values ('{wg}','{fn}',{cnt})"
                        .format(wg=word, fn=function_name, cnt=1))

                    cur.execute(
                        "INSERT INTO words "
                        + "(word, word_group, word_order) "
                        + "values ('{w}','{wg}',{seq})"
                        .format(w=word, wg=word, seq=0))

                elif isinstance(group, type([])):
                    word_group_string = (' '.join(group)).lower()

                    cur.execute(
                        "INSERT INTO word_groups "
                        + "(word_group, function, word_count) "
                        + "values ('{wg}','{fn}',{cnt})"
                        .format(wg=word_group_string,
                                fn=function_name, cnt=len(group)))

                    for order in range(0, len(group)):

                        word = group[order].lower()
                        cur.execute(
                            "INSERT INTO words "
                            + "(word, word_group, word_order) "
                            + "values ('{w}','{wg}',{seq})"
                            .format(w=word, wg=word_group_string,
                                    seq=order))
        con.commit()

    else:
        print "Invalid WORDS type '%s' for module %s"\
            % (type(words), name)


def assemble_actions_db():
    global con, cur, modules
    try:
        if profile.data['actions_db_file'] != ':memory:' \
                and os.path.exists(profile.data['actions_db_file']):
            os.remove(profile.data['actions_db_file'])

        con = sqlite3.connect(
            profile.data['actions_db_file'],
            check_same_thread=False)
        con.text_factory = sqlite3.OptimizedUnicode
        cur = con.cursor()

    except sqlite3.Error as e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    if create_actions_db(con, cur):
        print 'Successfully Created ' + profile.data['actions_db_file']

    package = importlib.import_module(profile.data['modules'])
    for finder, name, _ in pkgutil.walk_packages(package.__path__):
        print 'Loading module ' + name
        try:
            loader = finder.find_module(name)
            mod = loader.load_module(name)

        except:
            print "Skipped module '%s' due to an error." % name

        else:
            priority = mod.PRIORITY if hasattr(mod, 'PRIORITY') else 0

            if hasattr(mod, 'WORDS'):
                insert_words(con, cur, name, mod.WORDS, priority)
                modules[name] = mod

            else:
                print 'WARNING: Module will not be used.'
                print '    WORDS not found for module ' + name

    # con.close()

if con == 0:
    assemble_actions_db()
