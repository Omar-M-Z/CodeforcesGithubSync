from authorize_github import device_flow_authorization
from get_submissions import download_submissions
from manage_repository import create_repository, update_repository
from os import listdir

token = device_flow_authorization()
print("Your token: " + str(token))
user = input("Enter GitHub username: ")
repo_name = input("Enter repository name: ")
desc = input("Enter repository description: ")
create_repository(token, user, repo_name, desc)

# download submissions to the saved code repository
cf_handle = input("Enter Codeforces Handle: ")
download_submissions(cf_handle)

# commit and push code to repository
create_repository(token, repo_name, "Codeforces solutions")
file_paths = [f for f in listdir("./saved_code")]
update_repository(token, user, repo_name, file_paths)

