

from util import on_import
import atexit
import jpype
import math
import json


jvm_path = "/System/Library/Frameworks/JavaVM.framework/JavaVM"


def surround_jvm(func):
    def _inner(*args, **kwargs):
        if not jpype.isJVMStarted():
            jpype.startJVM(jvm_path)

        ret_val = func(*args, **kwargs)

        return ret_val
    return _inner


def load_fingerprint_from_file(filename):
    with open(filename) as f:
        print_dict = json.loads(f.read())
        return ReferencePrint(
            print_dict["fingerprint"],
            print_dict["radius"],
            print_dict["sound_pressure_level"]
        )


#@atexit.register
def destroy_env():
    if jpype.isJVMStarted():
        jpype.shutdownJVM()


@surround_jvm
def get_similarity(f_1, f_2):
    Jfingerprint = jpype.JPackage("com").musicg.fingerprint
    com_obj = Jfingerprint.FingerprintSimilarityComputer(f_1, f_2)
    sim_obj = com_obj.getFingerprintsSimilarity()
    sim = sim_obj.getSimilarity()
    if math.isnan(sim):
        return 0.5
    else:
        return sim


@surround_jvm
def get_fingerprint(wav_path):
    Jwave = jpype.JPackage("com").musicg.wave
    wv = Jwave.Wave(wav_path)
    return list(wv.getFingerprint())


class ReferencePrint(object):

    def __init__(self, fingerprint, radius, spl):
        self.fingerprint = fingerprint
        self.radius = radius
        self.spl = spl

