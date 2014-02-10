
import rethinkdb as r
import fingerprint
import config

from multiprocessing import Pool


"""

DB Structure:
    [
        {
            name: <String>,
            class: <String>,
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
SAMPLE_CLASS = "Chicken"


# Table Names
FINGERPRINT_TABLE = "fingerprints"


# Primary Keys
FINGERPRINT_PRIMARY_KEY = "name"


# Secondary Keys
FINGERPRINT_SECONDARY_KEY = "class"


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

    r.db(DB).table(FINGERPRINT_TABLE).index_create(
        FINGERPRINT_SECONDARY_KEY
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
        insert_reference(
            SAMPLE_NAME,
            f_print,
            SAMPLE_R_REF,
            SAMPLE_L_REF,
            SAMPLE_CLASS
        )
        return True
    else:
        return False


class SimilarityFunction:

    def __init__(self, f_check):
        self.f_check = f_check


    def __call__(self, db_dict):
        return {
            "conf": fingerprint.get_similarity(
                self.f_check, db_dict["fingerprint"]
            ),
            "name": db_dict["name"],
            "class": db_dict["class"]
        }


def determine_sound_class(conf_list):

    class_conf_dict = dict()
    class_count_dict = dict()

    for db_dict in conf_list:
        if not db_dict["class"] in class_conf_dict.keys():
            class_conf_dict[db_dict["class"]] = 0.0
            class_count_dict[db_dict["class"]] = 0

        class_conf_dict[db_dict["class"]] += db_dict["conf"]
        class_count_dict[db_dict["class"]] += 1

    best_match = max(
        class_conf_dict.items(),
        key=lambda ct: ct[1] / float(class_count_dict[ct[0]])
    )

    return best_match[0]


def get_best_matching_print(f_in):
    """

    Given an input fingerprint, this function iterates through the database
    and returns the most similar fingerprint and the corresponding confidence

    @param f_in Input fingerprint

    @return A tuple with the most similar fingerprint and corresponding
    confidence.

    """

    p_pool = Pool(processes=4)

    try:
        conn = r.connect(host=HOST, port=PORT, db=DB)

        table = list(r.table(FINGERPRINT_TABLE).run(conn))

        if len(table) == 0:
            raise LookupError("Database is empty")

        map_func = SimilarityFunction(f_in)
        conf_list = p_pool.map(map_func, table)

        best_match = max(conf_list, key=lambda ct: ct["conf"])
        sound_class = determine_sound_class(conf_list)

        return best_match["name"], sound_class, best_match["conf"]
    finally:
        p_pool.terminate()


def get_class_reference_data(class_name):
    conn = r.connect(host=HOST, port=PORT, db=DB)
    ref_list = list(r.table(FINGERPRINT_TABLE).get_all(
        class_name, index=FINGERPRINT_SECONDARY_KEY
    ).run(conn))


    avg_distance = 0.0
    avg_spl = 0.0
    for ref_data in ref_list:
        avg_distance += ref_data["distance"]
        avg_spl += ref_data["spl"]

    len_ref_list = float(len(list(ref_list)))
    return avg_distance / len_ref_list, avg_spl / len_ref_list


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


def insert_reference(name, f_ref, r_ref, l_ref, class_ref):
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
            "spl": l_ref,
            "class": class_ref
        }
    ).run(conn)

    return ret_obj

