from geoalchemy2.functions import GenericFunction

# Taken from the Skylines opensource project
# https://github.com/skylines-project/skylines/blob/master/skylines/lib/sql.py

class _ST_Intersects(GenericFunction):
    """
    ST_Intersects without index search
    """
    name = '_ST_Intersects'
    type = None


class _ST_Contains(GenericFunction):
    """
    ST_Contains without index search
    """
    name = '_ST_Contains'
    type = None


def query_to_sql(query):
    """
    Convert a sqlalchemy query to raw SQL.
    https://stackoverflow.com/questions/4617291/how-do-i-get-a-raw-compiled-sql-query-from-a-sqlalchemy-expression
    """

    from psycopg2.extensions import adapt as sql_escape

    statement = query.statement.compile(dialect=query.session.bind.dialect)
    dialect = query.session.bind.dialect

    enc = dialect.encoding
    params = {}

    for k, v in statement.params.iteritems():
        if isinstance(v, unicode):
            v = v.encode(enc)
        params[k] = sql_escape(v)

    return (statement.string.encode(enc) % params).decode(enc)
