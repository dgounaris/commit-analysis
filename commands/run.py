import os
import csv
import random
from typing import Optional

from commands import show


def execute_run(max_path_level: int, commanddir: str, outputdir: str, filename: str):
    commit_hashes = os.popen('git log --pretty=format:"%H"').read().splitlines()
    all_file_changes = dict()
    for idx, commit_hash in enumerate(commit_hashes):
        file_changes = os.popen('git diff-tree --no-commit-id --name-only -r ' + commit_hash).read().splitlines()
        file_changes = dict.fromkeys(filter(
            lambda item: item is not None, [normalize_path(it, commanddir, max_path_level) for it in file_changes])
        )
        for file_change in file_changes:
            all_file_changes[file_change] = all_file_changes.get(file_change) \
                if all_file_changes.get(file_change) is not None else dict()
            for file_change_inner in file_changes:
                all_file_changes[file_change][file_change_inner] = \
                    (all_file_changes.get(file_change).get(file_change_inner)
                     if all_file_changes.get(file_change).get(file_change_inner) is not None else 0) + 1
        print("Commit " + str(idx) + " of " + str(len(commit_hashes)) + " processed")
    # at this point, optimizations for files that have been deleted or renamed can be added to improve visualization
    all_files_lookup = list(all_file_changes.keys())
    all_files_lookup.sort()
    all_file_changes_matrix = [[0 for i in range(len(all_files_lookup))] for i in range(len(all_files_lookup))]
    for primary_index, file_name in enumerate(all_files_lookup):
        for secondary_index, file_name_inner in enumerate(all_files_lookup):
            all_file_changes_matrix[primary_index][secondary_index] = \
                all_file_changes.get(file_name).get(file_name_inner) \
                if all_file_changes.get(file_name).get(file_name_inner) is not None else 0

    with open(os.path.join(outputdir, filename), 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow([''] + all_files_lookup)
        for file_lookup_index, file_lookup in enumerate(all_files_lookup):
            writer.writerow([file_lookup] + [str(it) for it in all_file_changes_matrix[file_lookup_index]])

    show.execute_show(outputdir, filename)


def normalize_path(path: str, commanddir: str, max_level: int) -> Optional[str]:
    if not os.path.abspath(path).startswith(os.path.abspath(commanddir)):
        return None
    path = os.path.normpath(path)
    path_list = path.split(os.sep)
    if len(path_list) == 1:
        return path
    elif max_level == -1:
        return os.sep.join(path_list[:-1])
    elif len(path_list) > max_level:
        return os.sep.join(it for it in path_list[:max_level])
    else:
        return os.sep.join(path_list[:-1])
