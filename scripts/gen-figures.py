import matplotlib.pyplot as plt
import numpy as np
import csv
import os

## Years Vs Test Files added

data_modification = {}

with open('../output/part4_output.csv','r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] == 'Test File Path':
            continue
        data_modification[row[2][0:4]] = data_modification.get(row[2][0:4], 0) + 1
file.close()

y1 = np.array(list(data_modification.values()))
years_label = list(data_modification.keys())

plt.barh(years_label, y1)
plt.title('Years vs Test Files Added')
plt.xlabel('Number of Test Files Added')
plt.ylabel('Years')
plt.show()

## Most and Least Modified Test Files

file_modification = {}

with open('../output/part4_output.csv','r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] == 'Test File Path':
            continue
        file_modification[row[0]] = file_modification.get(row[0], 0) + int(row[3])
file.close()

top_five = sorted(file_modification.items(), key=lambda x:x[1], reverse=True)
top_test_file = [i[0][i[0].rindex('\\')+1:] for i in top_five[0:5]]
top_test_file_modif_count = [i[1] for i in top_five[0:5]]


low_five = sorted(file_modification.items(), key=lambda x:x[1])
low_test_file = [i[0][i[0].rindex('\\')+1:] for i in low_five[0:5]]
low_test_file_modif_count = [i[1] for i in low_five[0:5]]


plt.barh(top_test_file, top_test_file_modif_count)
plt.title('Top 5 Most Modified Files')
plt.xlabel('Modification Count')
plt.ylabel('Test Files')
plt.show()

plt.barh(low_test_file, low_test_file_modif_count)
plt.xticks([0,1])
plt.title('Top 5 Least Modified Files')
plt.xlabel('Modification Count')
plt.ylabel('Test Files')
plt.show()


###############################################################
###Top 5 files with most assertions

cur_path = os.path.dirname(__file__)
new_path = os.path.relpath('../output/part2_output.csv', cur_path)

assertions_count = {}
with open(new_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] == 'File' or row[0].__contains__('Total'):
            continue
        path = row[0].split("\\")
        assertions_count[path[len(path)-1]] = int(row[1])
file.close()

top_five = sorted(assertions_count.items(), key=lambda x:x[1], reverse=True)
top_files = [i[0] for i in top_five[0:5]]
top_assertions = [i[1] for i in top_five[0:5]]


plt.barh(top_files, top_assertions)
plt.title('Top 5 Files with most Assertions')
plt.xlabel('No of Assertions')
plt.ylabel('Test File')
plt.show()

#############################################################
###Top 5 files with highest coverage

new_path = os.path.relpath('../output/coverage.csv', cur_path)

coverage_count = {}

plt.close()

with open(new_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] == 'Module' or row[0].__contains__('Total')\
                or row[6] in coverage_count.values():
            continue
        path = row[0].split("/")
        coverage_count[path[len(path)-1]] = row[6]

file.close()

top_5 = sorted(coverage_count.items(), key=lambda x: x[1], reverse=True)
print(top_5)
top_file = list(reversed([i[0] for i in top_5[0:5]]))
top_cov = list(reversed([i[1] for i in top_5[0:5]]))

plt.bar(top_file, top_cov)
plt.title('Top 5 Files with highest coverage')
plt.xlabel('Coverage %')
plt.ylabel('Test File')
plt.show()


###############################################################
#Top 5 files with most branches

branch_count = {}

plt.close()

with open(new_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] == 'Module' or row[0].__contains__('Total')\
                or row[6] in branch_count.values():
            continue
        path = row[0].split("/")
        branch_count[path[len(path) - 1] + "-" + row[6]] = int(row[4])

file.close()

top_5 = sorted(branch_count.items(), key=lambda x:x[1], reverse=True)
top_file = [i[0] for i in top_5[0:5]]
top_branch = [i[1] for i in top_5[0:5]]

plt.barh(top_file, top_branch)
plt.title('Top 5 Files with highest branches')
plt.xlabel('Branch count')
plt.ylabel('Test File')
plt.show()


#############################################################

# Coverage above 80 and below 80.

coverage_count = {"+90": 0, "+80": 0, "+70": 0, "others": 0}

plt.close()

with open(new_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] == 'Module' or row[0].__contains__('Total') \
                or row[6] in coverage_count.values():
            continue
        percentage = int(row[6].split("%")[0])

        if percentage >= 90:
            coverage_count["+90"] += 1
        elif percentage >= 80:
            coverage_count["+80"] += 1
        elif percentage >= 70:
            coverage_count["+70"] += 1
        else:
            coverage_count["others"] += 1

file.close()
font = {'family': 'Arial',
        'weight': 'normal',
        'size': 12,
        }
plt.title('Percentage distribution of code coverage', y = -0.1, fontdict=font)
plt.pie(coverage_count.values(), labels=coverage_count.keys(), autopct='%1.0f%%', pctdistance=0.7, labeldistance=1.08, textprops=font)
plt.show()

###########################################################
# Part 3 Figures

data = {}


with open('../output/part3_output.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] == "File" or row[0].startswith("Total"):
            continue
        data[row[0]] = [int(row[1]), int(row[2])]

file.close()

# Files vs assertions
files = []
assertions = []
for keys, values in data.items():
    if int(values[0]) != 0:
        if keys.split("/")[-1] in files:
            files.append(keys.split("/")[-2] + "/" + keys.split("/")[-1])
        else:
            files.append(keys.split("/")[-1])
        assertions.append(values[0])

plt.barh(files, assertions)
plt.title('Files vs Assertions')
plt.xlabel('File Name')
plt.ylabel('Number of Assertions')
plt.ylim(bottom=0)
plt.show()


files = []
debug = []
for keys, values in data.items():
    if int(values[1]) != 0:
        if keys.split("/")[-1] in files:
            files.append(keys.split("/")[-2] + "/" + keys.split("/")[-1])
        else:
            files.append(keys.split("/")[-1])
        debug.append(values[1])


plt.barh(files, debug)
plt.title('Files vs Debugs')
plt.xlabel('File Name')
plt.ylabel('Number of Debugs')
plt.ylim(bottom=0)
plt.show()

