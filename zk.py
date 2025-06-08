import os

dir_list = os.listdir("CSVs")
maxFiles = 2

print(dir_list)

rev_dir_list = dir_list

rev_dir_list.reverse()

for i, file in enumerate(rev_dir_list):
    if i > maxFiles-2:
        os.remove(f"CSVs/{file}")
