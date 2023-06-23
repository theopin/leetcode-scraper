
import colorama
from colorama import Back, Fore

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time

import tracker 
import driver
import api
import scraper
import format



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

            
            # Sleep for 25 for each problem and 30s after every 30 problems
            if (i - prev_extracted_questions) % 30 == 0:
                print(f"Sleeping 2 mins\n")
                time.sleep(120)
            else:
                print(f"Sleeping 5 secs\n")
                time.sleep(5)



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

        data = scraper.scrape_question(web_driver.page_source)

        data["question_id"] = frontend_question_id
        data["title"] = question_title
        data["difficulty_index"] = difficulty
        data["difficulty"] = difficulty_level
        data["url"] = url

        markdown_content = format.convert_to_markdown(data)
        print(markdown_content)

        
        # Update upto which the problem is downloaded
        tracker.update_tracker('tracker.conf', question_num)
        
        print(f"Successfully extracted problem " 
            + Fore.BLACK + Back.YELLOW + f"#{question_num}"
            + Fore.RESET + Back.RESET + "\n")

    except Exception as e:
        print(Back.RED + f"Failed to extract problem " 
                + Fore.BLACK + Back.YELLOW + f"#{question_num}")
        print(Back.RED + "Reason: "+ f"{e}")
        web_driver.quit()
        exit(0)



if __name__ == "__main__":
    main()