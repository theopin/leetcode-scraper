
from dotenv import load_dotenv

import time
import os

import api
import scraper

load_dotenv()

LEETCODE_URL = os.getenv("LEETCODE_URL")
PORT = os.getenv("PORT")

scraper.create_web_driver()

# Get the last problem number we stopped at from our previous download (if any) 
question_start_index = 1 

def main():
    problem_json = api.obtain_problem_json()
    synthesized_problems = api.synthesize_problem_json(problem_json)    

    for i in range(question_start_index - 1, len(synthesized_problems)):

        question_api_data = api.format_question_api_data(synthesized_problems[i], LEETCODE_URL)

        scraped_data = scraper.scrape_question(i, question_api_data)

                
        # Sleep for 25 for each problem and 30s after every 30 problems
        if (i != question_start_index) and ((i - question_start_index) % 30 == 0):
            print(f"30 Questions scraped! Sleeping 20s\n")
            time.sleep(20)
        else:
            print(f"Sleeping 1 secs\n")
            time.sleep(1)

    scraper.quit_web_driver()

if __name__ == "__main__":
    main()