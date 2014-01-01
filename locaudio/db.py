
import rethinkdb as r
import fingerprint


"""

DB Structure:
    [
        {
            name: <String>,
            fingerprint: <List[Int]>,
            distance: <Float>,
            spl: <Float>
        },
        .
        .
        .
    ]

"""


# Connection Information
HOST = "localhost"
PORT = 28015
DB = "reference"


# Table Names
FINGERPRINT_TABLE = "fingerprints"


# Primary Keys
FINGERPRINT_PRIMARY_KEY = "name"


def create(conn):
    """

    Creates tables in the database and initializes the primary and secondary
    keys

    @param conn Connection object

    """

    r.db_create(DB).run(conn)

    r.db(DB).table_create(
        FINGERPRINT_TABLE,
        primary_key=FINGERPRINT_PRIMARY_KEY
    ).run(conn)


def init():
    """

    Initializes the RethinkDB database

    """

    conn = r.connect()
    if not DB in r.db_list().run(conn):
        create(conn)
        return True
    else:
        return False


def get_best_matching_print(f_in):
    conn = r.connect(host=HOST, port=PORT, db=DB)

    table = list(r.table(FINGERPRINT_TABLE).run(conn))

    if len(table) == 0:
        raise LookupError("Database is empty")

    conf_list = map(
        lambda info: {
            "conf": fingerprint.get_similarity(f_in, info["fingerprint"]),
            "name": info["name"]
        }, table
    )

    best_match = max(conf_list, key=lambda ct: ct["conf"])
    return best_match["name"], best_match["conf"]


def get_reference_data(ref_name):
    conn = r.connect(host=HOST, port=PORT, db=DB)
    ref_data = r.table(FINGERPRINT_TABLE).get(ref_name).run(conn)

    try:
        return ref_data["distance"], ref_data["spl"]
    except KeyError:
        raise LookupError("Database does not have the requested reference")


def insert_reference(name, f_ref, r_ref, l_ref):
    conn = r.connect(host=HOST, port=PORT, db=DB)

    ret_obj = r.table(FINGERPRINT_TABLE).insert(
        {
            "name": name,
            "fingerprint": f_ref,
            "distance": r_ref,
            "spl": l_ref
        }
    ).run(conn)

    return ret_obj

