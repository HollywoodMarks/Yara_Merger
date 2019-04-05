#!/usr/bin/env python
# encoding: utf-8

import os
import shutil
import git

#Delete official repo and clone it to retrieve last yara rules
def update_yara_rule_folder(folders):
	for x in folders:
		shutil.rmtree(x)
	git.Git().clone("https://github.com/Yara-Rules/rules.git")
#	git.Git().clone("https://github.com/mikesxrs/Open-Source-YARA-rules.git")

#Get all Yara files
def get_yara_files(folders):
	all_yara_files = []
	for x in folders:
		for root, directories, filenames in os.walk(x):
			if root == x or root == "rules/Mobile_Malware":
				continue
			for file_name in filenames:
				if file_name == "MALW_TinyShell_Backdoor_gen.yar" or file_name == "RomeoFoxtrot_mod.yara.error":
					continue
				if file_name in all_yara_files:
					continue
				if ".yar" in file_name:
					all_yara_files.append(os.path.join(root, file_name))
	return all_yara_files

#Filter Yara files with import math, imphash function and is__osx rule TODO
def remove_incompatible_imports(files):
	yara_files_filtered = []
	for yara_file in files:
		with open(yara_file, 'r') as fd:
			yara_in_file = fd.read()
			#if not (("import \"math\"" in yara_in_file) or ("import \"cuckoo\"" in yara_in_file) or ("import \"hash\"" in yara_in_file) or ("imphash" in yara_in_file)):
			if not (("import \"math\"" in yara_in_file) or ("import \"cuckoo\"" in yara_in_file) or ("import \"hash\"" in yara_in_file) or ("imphash" in yara_in_file) or ("is__elf" in yara_in_file)):
				yara_files_filtered.append(yara_file)
	return yara_files_filtered

#Remove duplicates
def remove_duplicates(files):
        yara_files_filtered = []
        first_elf = True
        to_delete = False
        for yara_file in files:
                with open(yara_file, 'r') as fd:
                        yara_in_file = fd.readlines()
                        for line in yara_in_file:
                                if line.strip() == "private rule is__elf {":
                                        if first_elf:
                                                first_elf = False
                                        else:
                                                to_delete = True
                                if not to_delete:
                                        yara_files_filtered.append(line)
                                if (not first_elf) and line.strip() == "}":
                                        to_delete = False
                        yara_files_filtered.append("\n")
        return yara_files_filtered

def dump_in_file(all_rules):
	with open("all_yara_rules.yar", 'w') as fd:
		fd.write(''.join(all_rules))

def main():
	root_yara = ["rules"]
	update_yara_rule_folder(root_yara)
	all_yara_files = get_yara_files(root_yara)
	all_yara_filtered_1 = remove_incompatible_imports(all_yara_files)
	all_yara_filtered_2 = remove_duplicates(all_yara_filtered_1)
	dump_in_file(all_yara_filtered_2)

# Main body
if __name__ == '__main__':
	main()
