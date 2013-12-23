

from util import on_import
from collections import namedtuple
import os
import sys
import atexit
import jpype


jvm_path = "/System/Library/Frameworks/JavaVM.framework/JavaVM"
Jfingerprint = None


@on_import
def setup_env():
    jpype.startJVM(jvm_path)

    global Jfingerprint
    Jfingerprint = jpype.JPackage("com").musicg.fingerprint


@atexit.register
def destroy_env():
    jpype.shutdownJVM()


def get_similarity(f_1, f_2):
    com_obj = Jfingerprint.FingerprintSimilarityComputer(f_1, f_2)
    sim_obj = com_obj.getFingerprintsSimilarity()
    sim = sim_obj.getSimilarity()
    if not type(sim) == float:
        print sim
        return 0.5
    else:
        return sim


class ReferencePrint(object):

    def __init__(self, fingerprint, radius, spl):
        self.fingerprint = fingerprint
        self.radius = radius
        self.spl = spl

