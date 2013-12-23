

from util import on_import
import atexit
import jpype
import math


jvm_path = "/System/Library/Frameworks/JavaVM.framework/JavaVM"
Jfingerprint = None


@on_import
def setup_env():
    if jpype.isJVMStarted():
        return

    jpype.startJVM(jvm_path)

    global Jfingerprint


@atexit.register
def destroy_env():
    jpype.shutdownJVM()


def get_similarity(f_1, f_2):

    Jfingerprint = jpype.JPackage("com").musicg.fingerprint
    com_obj = Jfingerprint.FingerprintSimilarityComputer(f_1, f_2)
    sim_obj = com_obj.getFingerprintsSimilarity()
    sim = sim_obj.getSimilarity()
    if math.isnan(sim):
        print sim
        return 0.5
    else:
        return sim


class ReferencePrint(object):

    def __init__(self, fingerprint, radius, spl):
        self.fingerprint = fingerprint
        self.radius = radius
        self.spl = spl

