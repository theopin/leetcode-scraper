"""
    Utility functions to keep track of upto which problems have been downloaded so that we can continue from 
    that problem if downloading of questions stop halfway 
"""
import requests
import json


# Leetcode API URL to get json of problems on algorithms categories
ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"
LEETCODE_URL_BASE = "https://leetcode.com/problems/"


# Tracks the questions we have already downloaded
def obtain_problem_json():
    algorithm_problems_content = requests.get(ALGORITHMS_ENDPOINT_URL).content
    return json.loads(algorithm_problems_content)


 # Creates a list to store questions partial information retrieved from API
def synthesize_problem_json(problem_json, isToSort=True):
    synthesized_problems = []
    for child in problem_json["stat_status_pairs"]:

        # Currently we are only processing free problems
        if not child["paid_only"]:
            question_api_data = {
                "id": child["stat"]["question_id"],
                "title": child["stat"]["question__title"],
                "difficulty_index": child["difficulty"]["level"],
                "url": LEETCODE_URL_BASE + child["stat"]["question__title_slug"],
                "total_acs": child["stat"]["total_acs"]
            }

            synthesized_problems.append(question_api_data)
    
    if isToSort:
        # Sort by difficulty follwed by problem id in ascending order
        synthesized_problems = sorted(synthesized_problems, key=lambda x: (x["difficulty_index"], x["id"]))

    return synthesized_problems

