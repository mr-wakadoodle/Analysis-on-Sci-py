import os
import re
import csv

count = 0
dir_name = os.path.dirname(os.path.realpath(__file__))

output_file = open('part2_output.csv', "a+", newline='')
writer = csv.writer(output_file)
writer.writerow(['File', 'No of assertions'])

for root, dirs, files in os.walk(dir_name, topdown=True):
    dirs[:] = [d for d in dirs if d not in 'build']
    for file in files:
        assertion_count = 0
        if re.match('^test_.*\.py$', file):
            count += 1
            final_path = os.path.join(root, file)
            with open(final_path, "r+") as file_ptr:
                data = file_ptr.readlines()
                for line in data:
                    assertion_count += len(re.findall(r'\bassert_[a-zA-Z0_]*\(', line))
            writer.writerow([file, str(assertion_count)])


output_file.write('Total number of test.py files : ' + str(count))
output_file.close()

