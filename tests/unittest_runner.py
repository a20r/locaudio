#!/usr/bin/env python
import os
import re
import sys
import shutil
import subprocess


__author__ = "Christopher Choi <chutsu@gmail.com>"


# SETTINGS
keep_unittest_logs = False
unittests_bin_dir = "tests"
unittests_log_dir = "unittests_log"
unittests_file_pattern = "^test_[a-zA-Z0-9_]*.*$"

cmd_dict = {
    "sh": "bash",
    "py": "python"
}

class TC:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def print_stdout(unittest_output_fp):
    # open unittest stdout log file
    unittest_output = open(unittest_output_fp, 'r')
    output_content = unittest_output.read()
    unittest_output.close()

    # print unittest stdout
    print("-" * 79)
    print(output_content)
    print("-" * 79)


def get_files(path, pattern):
    file_list = []

    for root, directory, files in os.walk(path):
        for f in files:
            if re.match(pattern, f):
                file_list.append(os.path.join(root, f))

    return file_list


if __name__ == "__main__":
    orig_cwd = os.getcwd()

    # make log dir if not already exist
    if not os.path.exists(unittests_log_dir):
        os.mkdir(unittests_log_dir)

    # gather all unittests
    file_list = os.listdir(unittests_bin_dir)
    unittests = get_files(unittests_bin_dir, unittests_file_pattern)

    # execute all unittests
    error = False
    return_val = 0
    for unittest in unittests:
        # execute unittest
        try:
            print "UNITTEST [{0}] {1}Starting{2}".format(unittest, TC.OKBLUE, TC.ENDC)
            print("UNITTEST [{0}] ".format(unittest)),
            unittest_output_fp = os.path.join(
                orig_cwd,
                unittests_log_dir,
                os.path.basename(unittest) + ".log"
            )
            unittest_output = open(unittest_output_fp, 'w')

            return_val = subprocess.check_call(
                [cmd_dict[unittest.split(".")[-1]], "./{0}".format(unittest)],
                stdout=unittest_output,
                stderr=unittest_output
            )
            unittest_output.close()
            print("{0}PASSED!{1}".format(TC.OKGREEN, TC.ENDC))

        except:
            unittest_output.close()
            print("{0}FAILED!{1}".format(TC.FAIL, TC.ENDC))
            print_stdout(unittest_output_fp)
            error = True

    os.chdir(orig_cwd)
    # keep unittest stdout dir?
    if keep_unittest_logs is False:
        shutil.rmtree(unittests_log_dir)

    if error is True:
        sys.exit(-1)
    else:
        sys.exit(0)
