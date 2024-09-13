import base64
import json
import time

import requests


def create_repository(token, user, name, desc):
    url = f"https://api.github.com/user/repos"
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"token {token}"}
    data = {"name": name, "description": desc}
    response = requests.post(url=url, headers=headers, json=data)
    if response.status_code == 201:
        return name
    else:
        return None


def update_repository(token, user, repo, file_paths):
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"token {token}"}

    # creating a blob for each individual file to be committed
    def create_blob(file_path):
        # get the contents of the file
        with open(f"./saved_code/{file_path}", "rb") as file:
            file_contents = file.read()
        # encode the contents of the file
        encoded_contents = base64.b64encode(file_contents).decode()
        blob_data = {
            "content": encoded_contents,
            "encoding": "base64"
        }
        time.sleep(0.5)
        blob_response = requests.post(f"https://api.github.com/repos/{user}/{repo}/git/blobs", headers=headers, json=blob_data)

        # returning the SHA of the blob
        sha = blob_response.json()["sha"]

        return file_path, sha

    def create_tree(files_and_blobshas_2):
        tree_data = {"tree": []}
        for i in files_and_blobshas_2:
            data = {
                "path": i[0],
                "mode": "100644",
                "type": "blob",
                "sha": i[1]
            }
            tree_data["tree"].append(data)
        time.sleep(0.5)
        tree_response = requests.post(f"https://api.github.com/repos/{user}/{repo}/git/trees", headers=headers, json=tree_data)
        sha = tree_response.json()["sha"]

        return sha

    def create_commit(tree_sha_2, latest_commit_sha_2):
        commit_data = {
            "message": "adding codeforces solutions",
            "tree": tree_sha_2,
            "parents": [latest_commit_sha_2]
        }

        time.sleep(0.5)
        commit_response = requests.post(f"https://api.github.com/repos/{user}/{repo}/git/commits", headers=headers, json=commit_data)
        commit_sha = commit_response.json()["sha"]
        return commit_sha

    def update_reference(commit_sha_2):
        update_ref_data = {"sha": commit_sha}
        update_ref_response = requests.post(f"https://api.github.com/repos/{user}/{repo}/git/refs/heads/main", headers=headers, json=update_ref_data)
        return update_ref_response.status_code

    # getting the SHA of the latest commit
    response = requests.get(url=f"https://api.github.com/repos/{user}/{repo}/branches/main")
    latest_commit_sha = response.json()["commit"]["sha"]

    # getting a list of file names and their associated blob SHAs
    files_and_blobshas = []
    for fp in file_paths:
        files_and_blobshas.append(create_blob(fp))

    # creating a tree referencing the blob SHAs from the list
    tree_sha = create_tree(files_and_blobshas)

    # creating a commit
    commit_sha = create_commit(tree_sha, latest_commit_sha)

    # updating reference of latest commit
    status = update_reference(commit_sha)
    if status == 200:
        print("Successfully committed all files to GitHub")
    else:
        print("Failed to commit files to GitHub")