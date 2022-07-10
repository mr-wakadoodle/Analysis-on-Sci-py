import time
from datetime import datetime
import re
from pydriller import Repository
import csv

modification_count = {}

for commit in Repository('https://github.com/scipy/scipy.git').traverse_commits():
    for modif in commit.modified_files:
        if re.search('test_.*\.py$', str(modif.new_path)):
            if modif.new_path not in modification_count:
                modification_count[modif.new_path] = []
                modification_count[modif.new_path].append(1)
                modification_count[modif.new_path].append(set())
                modification_count[modif.new_path][1].add(commit.hash)
                modification_count[modif.new_path].append([])
                modification_count[modif.new_path][2].append(commit.author_date)
                modification_count[modif.new_path][2].append(commit.committer_date)
            else:
                modification_count[modif.new_path][0] = modification_count[modif.new_path][0] + 1
                modification_count[modif.new_path][1].add(commit.hash)
                modification_count[modif.new_path][2].append(commit.author_date)
                modification_count[modif.new_path][2].append(commit.committer_date)



header = ['Test File Path' ,'Test File', 'Date Added', 'Modification Count', 'Number of People Involved']
with open('E:\PATproject\part4_full_file_path.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for key in modification_count:
        line = [key, key[key.rindex('\\')+1:], min(modification_count[key][2]), modification_count[key][0], len(modification_count[key][1])]
        writer.writerow(line)