from .config import get_db_con, FNT_POOL, QUERIES, FNT_QUERIES


def create_row(query_name,  params={}):
    if query_name in QUERIES:
        query = QUERIES[query_name]
        con = get_db_con()
    if query_name in FNT_QUERIES:
        query = FNT_QUERIES[query_name]
        con = FNT_POOL.acquire()
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()
    id = cur.lastrowid
    con.close()
    return id

def execute_sql(query, params={}):
    con = get_db_con()    
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()
    id = cur.lastrowid
    con.close()
    return id    
