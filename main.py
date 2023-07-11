
from dotenv import load_dotenv
from flask import Flask


import time
import os

import api
import scraper

scraper_app = Flask(__name__)

load_dotenv()

LEETCODE_URL = os.getenv("LEETCODE_URL") or "https://leetcode.com/problems/"
PORT = os.getenv("PORT") or 3000

# Get the last problem number we stopped at from our previous download (if any) 
question_start_index = 1 


@scraper_app.route("/") 
def run_scrape_operation():
    scraper.create_web_driver()

    problem_json = api.obtain_problem_json()
    synthesized_problems = api.synthesize_problem_json(problem_json)    

    scraped_data_list = []

    #for i in range(question_start_index - 1, len(synthesized_problems)):
    for i in range(question_start_index - 1, question_start_index + 5):
        try:
            question_api_data = api.format_question_api_data(synthesized_problems[i], LEETCODE_URL)

            scraped_data = scraper.scrape_question(i, question_api_data)

                    
            # Sleep for 25 for each problem and 30s after every 30 problems
            if (i != question_start_index) and ((i - question_start_index) % 30 == 0):
                print(f"30 Questions scraped! Sleeping 20s\n")
                time.sleep(20)
            else:
                print(f"Sleeping 1 secs\n")
                time.sleep(1)
            
            scraped_data_list.append(scraped_data)
        
        except Exception as e:
            scraper.quit_web_driver()
            print(f"Failed to extract problem! ")
            
            return {
                "status" : "error",
                "message" : f"{e}"
            }

    scraper.quit_web_driver()

    return {
        "status": "success",
        "data": {
            "questions": scraped_data_list
        }
    }
    


scraper_app.run(port=PORT)
