from .config import get_db_con, FNT_POOL, QUERIES, FNT_QUERIES


def fetch_one_row(query_name, params={}):
    if query_name in QUERIES:
        query = QUERIES[query_name]
        con = get_db_con()
    if query_name in FNT_QUERIES:
        query = FNT_QUERIES[query_name]
        con = FNT_POOL.acquire()
    cur = con.cursor()
    cur.execute(query, params)
    row = cur.fetchone()
    if row:
        desc = cur.description
        column_names = [col[0] for col in desc]
        row = dict(zip(column_names, row))
    con.close()
    return row


def fetch_multiple_rows(query_name, params={}):
    if query_name in QUERIES:
        query = QUERIES[query_name]
        con = get_db_con()
    if query_name in FNT_QUERIES:
        query = FNT_QUERIES[query_name]
        con = FNT_POOL.acquire()
    cur = con.cursor()
    cur.execute(query, params)
    desc = cur.description
    column_names = [col[0].lower() for col in desc]
    data = [dict(zip(column_names, row))
            for row in cur.fetchall()]
    con.close()
    return data
