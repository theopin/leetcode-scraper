
import colorama
from colorama import Back, Fore

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import markdownify

import tracker 
import driver
import api
import scraper



# Problem URL is of the following format format ALGORITHMS_BASE_URL + question__title_slug
ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"

web_driver = driver.create_driver()

# Initialize Colorama
colorama.init(autoreset=True)

# Get the last problem number we stopped at from our previous download (if any) 
prev_extracted_questions = tracker.read_tracker("tracker.conf")

def main():
    problem_json = api.obtain_problem_json()
    synthesized_problems = api.synthesize_problem_json(problem_json)    

    try:
        for i in range(prev_extracted_questions + 1, len(synthesized_problems)):
            difficulty, frontend_question_id, question__title_slug, question__title, difficulty_level = synthesized_problems[i]
    
            # Forms the url to the leetcode question so that we can access the page and scrape its contents
            url = ALGORITHMS_BASE_URL + question__title_slug

            download_questions(i, url, frontend_question_id, question__title, difficulty, difficulty_level)

    finally:
        # Close the browser after download
        web_driver.quit()



def download_questions(question_num, url, frontend_question_id, question_title, difficulty, difficulty_level):
    print(f"Fetching problem " 
            + Fore.BLACK  + Back.YELLOW + f"#{question_num}" 
            + Fore.RESET  + Back.RESET + " from " 
            + Fore.BLACK +  Back.YELLOW + f"{url}")

    try:
        web_driver.get(url)
        # Wait 30 secs or until div with class '_1l1MA' appears
        WebDriverWait(web_driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "_1l1MA"))
        )

        db_entry = scraper.scrape_question(web_driver.page_source)

        db_entry["question_id"] = frontend_question_id
        db_entry["title"] = question_title
        db_entry["difficulty_index"] = difficulty
        db_entry["difficulty"] = difficulty_level
        
        
        # Update upto which the problem is downloaded
        tracker.update_tracker('track.conf', question_num)
        
        print(f"Successfully extracted problem " 
            + Fore.BLACK + Back.YELLOW + f"#{question_num}"
            + Fore.RESET + Back.RESET + "\n")

    except Exception as e:
        print(Back.RED + f" Failed Writing!!  {e} ")
        web_driver.quit()



if __name__ == "__main__":
    main()