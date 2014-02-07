
import rethinkdb as r
import fingerprint
import config


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
HOST = config.db_host
PORT = config.db_port
DB = "reference"

# Sample entry information
SAMPLE_PATH = "sounds/Cock.wav"
SAMPLE_R_REF = 1
SAMPLE_L_REF = 65
SAMPLE_NAME = "Cock"


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

    @return Whether the database was reinitialized or not

    """

    conn = r.connect()
    if not DB in r.db_list().run(conn):
        create(conn)
        f_print = fingerprint.get_fingerprint(SAMPLE_PATH)
        insert_reference(SAMPLE_NAME, f_print, SAMPLE_R_REF, SAMPLE_L_REF)
        return True
    else:
        return False


def get_best_matching_print(f_in):
    """

    Given an input fingerprint, this function iterates through the database
    and returns the most similar fingerprint and the corresponding confidence

    @param f_in Input fingerprint

    @return A tuple with the most similar fingerprint and corresponding
    confidence.

    """

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
    """

    Gets the associated meta-data for a reference name

    @param ref_name The name of the reference

    @return A tuple containing the reference distance, the reference sound
    pressure level, and the reference fingerprint

    """

    conn = r.connect(host=HOST, port=PORT, db=DB)
    ref_data = r.table(FINGERPRINT_TABLE).get(ref_name).run(conn)

    try:
        return ref_data["distance"], ref_data["spl"], ref_data["fingerprint"]
    except KeyError:
        raise LookupError("Database does not have the requested reference")


def get_list_of_names():
    """

    Gets the list of sound names from the database

    @return A list of strings of sound names

    """
    conn = r.connect(host=HOST, port=PORT, db=DB)
    names = r.table(FINGERPRINT_TABLE)["name"].run(conn)
    return list(names)


def insert_reference(name, f_ref, r_ref, l_ref):
    """

    Inserts a reference into the database

    @param f_ref The reference fingerprint

    @param r_ref The distance at which the reference data was recorded

    @param l_ref The sound pressure level of the reference data

    @return A RethinkDB insert return structure

    """

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

