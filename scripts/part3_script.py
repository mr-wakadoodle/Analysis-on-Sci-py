import os
import re
import csv


def getDebugs(path):
    numberOfDebugs = 0
    with open(path, "r+") as file_ptr:
        data = file_ptr.readlines()
        for line in data:

            # PDB - Python Debugger
            numberOfDebugs += len(re.findall(r'(?i).*pdb\.run\(.*', line))

            # Logging module - logging.debug()
            numberOfDebugs += len(re.findall(r'(?i).*\.debug\(.*', line))

            # Logging Module - logging.log
            numberOfDebugs += len(re.findall(r'(?i).*\.log\(.*', line))

            # Log module log.err()
            numberOfDebugs += len(re.findall(r'(?i).*\.err\(.*', line))

    return numberOfDebugs


def getAsserts(path):
    numberOfAsserts = 0
    with open(path, "r+") as file_ptr:
        data = file_ptr.readlines()
        for line in data:
            numberOfAsserts += len(re.findall(r'\bassert_[a-zA-Z0_]*\(', line))

    return numberOfAsserts


if __name__ == "__main__":
    totalAsserts = 0

    totalDebugs = 0
    # Getting the directory of the project
    root_dir_name = os.path.dirname(os.path.realpath(__file__))

    # scipy is the production directory of the SCIPY module
    production_directory = os.path.join(root_dir_name, 'scipy')

    print(production_directory)

    output_file = open('part3.csv', "a+", newline='')
    writer = csv.writer(output_file)
    writer.writerow(['File', 'Number of Assert Statements',
                    'Number of Debug Statements'])
    dirs = []
    for root, dirs, files in os.walk(production_directory, topdown=True):
        # print(dirs)
        # Ignoring the Test directories
        dirs[:] = [d for d in dirs if d not in ['tests', 'test']]
        for file in files:
            numberOfAsserts = 0
            numberOfDebugs = 0
            if file.split(".")[-1] == "py":
                numberOfAsserts = getAsserts(os.path.join(root, file))
                numberOfDebugs = getDebugs(os.path.join(root, file))
                totalAsserts += numberOfAsserts
                totalDebugs += numberOfDebugs

            if numberOfAsserts > 0 or numberOfDebugs > 0:
                writer.writerow([os.path.join(root, file), str(
                    numberOfAsserts), str(numberOfDebugs)])

    output_file.write('Total number of Assertions: ' + str(totalAsserts))
    output_file.write('\nTotal number of Debugs: ' + str(totalDebugs))
    output_file.close()
