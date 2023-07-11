
from dotenv import load_dotenv
from flask import Flask, request


import time
import os

import api
import scraper

scraper_app = Flask(__name__)

load_dotenv()

LEETCODE_URL = os.getenv("LEETCODE_URL") or "https://leetcode.com/problems/"
PORT = os.getenv("PORT") or 3000




@scraper_app.route("/", methods = ['GET']) 
def run_scrape_operation():
    
    
    question_start_index = int(request.headers["index"])
    question_quantity = int(request.headers["quantity"])


    scraper.create_web_driver()

    problem_json = api.obtain_problem_json()
    synthesized_problems = api.synthesize_problem_json(problem_json, LEETCODE_URL)    

    scraped_data_list = []

    upper_limit = min(question_start_index + question_quantity, len(synthesized_problems))
    for i in range(question_start_index, upper_limit):
        try:
            scraped_data = scraper.scrape_question(i, synthesized_problems[i])

                    
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
            "questions": scraped_data_list,
            "count": len(scraped_data_list)
        }
    }
    


scraper_app.run(port=PORT)
