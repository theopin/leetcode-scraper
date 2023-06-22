"""
    Utility functions to keep track of upto which problems have been downloaded so that we can continue from 
    that problem if downloading of questions stop halfway 
"""
import requests
import json


# Leetcode API URL to get json of problems on algorithms categories
ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"


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

            synthesized_problems.append((difficulty, frontend_question_id, question__title_slug, question__title, difficulty_level))
    
    if isToSort:
        # Sort by difficulty follwed by problem id in ascending order
        synthesized_problems = sorted(synthesized_problems, key=lambda x: (x[0], x[1]))

    return synthesized_problems