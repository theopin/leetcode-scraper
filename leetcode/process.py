import time

import leetcode.api as api
import leetcode.scraper as scraper



def run_scraper(params):
    response = {}
    params = process_params(params)

    scraper.create_web_driver()

    problem_json = api.obtain_problem_json()
    synthesized_problems = api.synthesize_problem_json(problem_json, params)   

    scraped_data_list = []

    upper_limit = min(params["index"] + params["quantity"] , len(synthesized_problems))
    for i in range(params["index"] , upper_limit):
            try:
                scraped_data = scraper.scrape_question(i, synthesized_problems[i])

                            
                if (i != params["index"]) and ((i - params["index"]) % 30 == 0):
                    print(f"30 Questions scraped! Sleeping 20s\n")
                    time.sleep(20)
                else:
                    print(f"Sleeping 1 secs\n")
                    time.sleep(1)
                    
                scraped_data_list.append(scraped_data)
            except Exception:
                raise Exception("Unable to scrape question", 502)

    response["data"] = {
                "questions": scraped_data_list,
                "count": len(scraped_data_list)
        }
    
    complete_scrape()
    
    return response

def process_params(params):
    new_params = {}

    new_params["index"] = params.get("index", default=None, type=int)
    new_params["quantity"] = params.get("quantity", default=None, type=int)
    new_params["difficulty"] = params.get("difficulty", default=0, type=int)

    if not (new_params["index"] and (new_params["quantity"])):
        raise Exception("Invalid index and quantity specified", 400)

    return new_params


def complete_scrape():
    scraper.quit_web_driver()

