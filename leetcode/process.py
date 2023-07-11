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

    upper_limit = min(params["offset"] + 1 + params["limit"] , len(synthesized_problems))
    for i in range(params["offset"] + 1, len(synthesized_problems)):
            try:
                if(len(scraped_data_list) == upper_limit):
                    break

                scraped_data = scraper.scrape_question(i, synthesized_problems[i])

                set_delay(params, i)
                
                if (check_common_topics(params["topics"], scraped_data["details"]["topics"])):
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

    new_params["offset"] = params.get("offset", default=-1, type=int)
    new_params["limit"] = params.get("limit", default=0, type=int)
    new_params["difficulty"] = params.get("difficulty", default=0, type=int)
    new_params["topics"] = params.get("topics", default="", type=str).strip(" ").split(",")

    return new_params

def set_delay(params, i):
    if (i != params["offset"] + 1) and ((i - params["offset"] - 1) % 30 == 0):
        print(f"30 Questions scraped! Sleeping 20s\n")
        time.sleep(20)
    else:
        print(f"Sleeping 1 secs\n")
        time.sleep(1)

def check_common_topics(selected_topics, scraped_question_topics):
    if selected_topics == [""]:
        return True
    
    return any(i in selected_topics for i in scraped_question_topics)

def complete_scrape():
    scraper.quit_web_driver()

