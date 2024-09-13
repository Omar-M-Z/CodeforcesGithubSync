from bs4 import BeautifulSoup
import requests

def download_submissions(cf_handle):
    response = requests.get(f"https://codeforces.com/api/user.status?handle={cf_handle}&from=1")

    if response.status_code != 200:
        print("Hmm . . . seems like something went wrong. Please try again later.")
        return

    submissions = response.json()["result"]
    for s in submissions:
        if s["verdict"] == "OK":
            submission_id = s["id"]
            contest_id = s["contestId"]
            problem = str(contest_id) + s["problem"]["index"]
            language = s["programmingLanguage"]
            get_code(contest_id, problem, submission_id, language)


def get_code(contest, problem, submission_id):
    url = f"https://codeforces.com/contest/{contest}/submission/{submission_id}"
    page_to_scrape = requests.get(url)
    print(page_to_scrape.text)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    lines = soup.find("pre")

    file_ext = "txt"
    # TODO: change file extension based on language

    file = open(f"saved_code/{problem}.{file_ext}", "w")
    file.write(lines.text)
    file.close()

