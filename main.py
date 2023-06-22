import json
import bs4
import requests
import colorama
import os
from colorama import Back, Fore

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markdownify


from utils import read_tracker, update_tracker, reset_configuration

# Setup Selenium Webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--log-level=3')                   # Show only fatal errors
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-data-dir=" + ".config/chromium")

driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager().install()), \
                          options=options)

# Initialize Colorama
colorama.init(autoreset=True)



def main():
    # Get the last problem number we stopped at from our previous download (if any) 
    completed_upto = read_tracker("tracker.conf")
    # Leetcode API URL to get json of problems on algorithms categories
    ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"

    # Problem URL is of the following format format ALGORITHMS_BASE_URL + question__title_slug
    ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"

    # Load JSON from API
    algorithms_problems_json = requests.get(ALGORITHMS_ENDPOINT_URL).content
    algorithms_problems_json = json.loads(algorithms_problems_json)
    

    # List to store questions partial information retrieved from API
    questions_data = []
    for child in algorithms_problems_json["stat_status_pairs"]:

        # Currently we are only processing free problems
        if not child["paid_only"]:
            question__title_slug = child["stat"]["question__title_slug"]
            question__title = child["stat"]["question__title"]
            frontend_question_id = child["stat"]["frontend_question_id"]
            difficulty = child["difficulty"]["level"]
            # total_accepted_solutions = child["stat"]["total_acs"]

            # map difficulty integer values to its corresponding string values
            difficulty_level = "hard"
            if difficulty == 1:
                difficulty_level = "easy"
            elif difficulty == 2:
                difficulty_level = "medium"

            questions_data.append((difficulty, frontend_question_id, question__title_slug, question__title, difficulty_level))
            
    # Sort by difficulty follwed by problem id in ascending order
    questions_data = sorted(questions_data, key=lambda x: (x[0], x[1]))


    try:
        print(len(questions_data))
        for i in range(completed_upto + 1, len(questions_data)):
            difficulty, frontend_question_id, question__title_slug, question__title, difficulty_level = questions_data[i]
            completed_upto = read_tracker("tracker.conf")
    
            # Forms the url to the leetcode question so that we can access the page and scrape its contents
            url = ALGORITHMS_BASE_URL + question__title_slug

            download_questions(i, url, frontend_question_id, question__title, difficulty, difficulty_level)

    finally:
        # Close the browser after download
        driver.quit()



def download_questions(question_num, url, frontend_question_id, question__title, difficulty, difficulty_level):

    print(f"Fetching problem " 
            + Fore.BLACK  + Back.YELLOW + f"num {question_num}" 
            + Fore.RESET  + Back.RESET + " with url " 
            + Fore.BLACK +  Back.YELLOW + f"{url}")

    try:
        driver.get(url)
        # Wait 30 secs or until div with class '_1l1MA' appears
        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "_1l1MA"))
        )
        # Get current tab page source
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, "html.parser")

        # Retrieve question content
        content = soup.find("div", {"class": "_1l1MA"})
        
        # Get list of topics related to the problem. For example: Dynamic programming, Greedy, String etc...
        topics = []
        for topic in soup.find_all("a", {"class": "mr-4 rounded-xl py-1 px-2 text-xs transition-colors text-label-2 dark:text-dark-label-2 hover:text-label-2 dark:hover:text-dark-label-2 bg-fill-3 dark:bg-dark-fill-3 hover:bg-fill-2 dark:hover:bg-dark-fill-2"}):
            topics.append(topic.findAll(string=True)[0])
            

        db_entry = { 
            "question_id": frontend_question_id, 
            "title": question__title,
            "difficulty_index": difficulty,
            "difficulty": difficulty_level,
            "related_topics": topics,
            "content": content
            }

        print(db_entry)

        # Update upto which the problem is downloaded
        update_tracker('track.conf', question_num)
        
        print(f"Successfully written problem " 
            + Fore.BLACK + Back.YELLOW + f"num {question_num}"
            + Fore.RESET + Back.RESET + "\n")

    except Exception as e:
        print(Back.RED + f" Failed Writing!!  {e} ")
        driver.quit()



if __name__ == "__main__":
    main()