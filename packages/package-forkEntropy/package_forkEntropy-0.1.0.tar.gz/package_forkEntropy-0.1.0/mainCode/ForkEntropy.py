'''
  导包区
'''
from functools import reduce
import json
import numpy as np

def extract_numbers(text):
    cleaned_text = text.replace('@', '').strip()
    parts = cleaned_text.split()
    num = 0
    for part in parts:
        if ',' in part:
            numbers = part.split(',')
            if len(numbers) >= 2:
                num += int(numbers[1].strip())
    return num

def _calculate_process(re, rpCommitInfo):
    files_column = set()
    commits = re.commits
    authors = list(re.author)
    all_commit_one_seg = []
    all_author_one_seg = []
    for k, commit_ in enumerate(commits):
        all_commit_one_seg.append(commit_)
        all_author_one_seg.append(authors[k])
        for files in commit_:
            try:
                files_column.update(set(files['files']["new_path"]))
            except Exception as e:
                for file_ in files['files']:
                    files_column.update(set(file_["new_path"]))

    if len(all_commit_one_seg)==0 or len(all_author_one_seg)==0 or len(files_column)==0:
        return 0,0,0

    files_dict = {file: num for num, file in enumerate(files_column)}
    users_column = list(set(re.author))
    users_dict = {owner: num for num, owner in enumerate(users_column)}
    matrix = np.zeros([len(users_column), len(files_column)], dtype=np.float64)
    file_len = len(files_column)
    for num, commits in enumerate(all_commit_one_seg):
        for con in commits:
            files = con["files"]["new_path"]
            owner = all_author_one_seg[num]
            if con["id"] not in list(rpCommitInfo.keys()):
               continue
            else:
               changes = rpCommitInfo[con["id"]] 
            owner_id = users_dict[owner]
            for index , file in enumerate(files):
                file_id = files_dict[file]
                changed_line = extract_numbers(changes[index]['diff'])
                matrix[owner_id][file_id] = changed_line
                
    # A process of calculation performed using only matrices
    fork_div_sum = 0
    tmp_sum_ls = []
    for i in range(len(users_column)):
        tmp_sum = 0
        for j in range(len(users_column)):
            norm_ = np.linalg.norm(matrix[i] - matrix[j], ord=1, axis=0)
            gamma = 1/file_len
            tmp = 1 - np.exp(-gamma * norm_)
            fork_div_sum += tmp
            tmp_sum += norm_
        tmp_sum_ls.append({'index':i,'value':tmp_sum})
    tmp_sum_ls.sort(key=lambda x: x['value'])
    if len(matrix) > 0 and len(users_column) > 0:
        fork_div = (1 + 1 / (2 * len(matrix))) / np.power(len(users_column), 2)
        fork_div = fork_div * fork_div_sum # Normalizaiton
        return len(matrix[0]),len(matrix),fork_div
    else:
        fork_div = 0 
        return 0,0,0

def load_commitInfo_to_json(saveRepoName):
    with open(saveRepoName, 'rb') as f:
          con = json.load(f)
    return con