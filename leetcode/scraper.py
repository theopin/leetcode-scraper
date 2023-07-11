"""
    Utility functions to keep track of upto which problems have been downloaded so that we can continue from 
    that problem if downloading of questions stop halfway 
"""

import bs4

import commons.driver as driver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

web_driver = None

def create_web_driver():
    global web_driver
    web_driver = driver.create_driver()

def quit_web_driver():
    global web_driver

    if web_driver:
        web_driver.quit()


def scrape_question(question_num, question_api_data):
    print(f"Fetching problem " + f"#{question_num}")


    web_driver.get(question_api_data["url"])

    # Wait 30 secs or until div with class '_1l1MA' appears
    WebDriverWait(web_driver, 30).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "_1l1MA"))
    )

    scraped_data = format_scraped_question(web_driver.page_source, question_api_data)

    print(f"Successfully extracted problem " + f"#{question_num}\n")

    return scraped_data

    


# Tracks the questions we have already downloaded
def format_scraped_question(page_source, question_details):
    soup = bs4.BeautifulSoup(page_source, "html.parser")

    # Retrieve question content
    question_content = soup.find("div", class_="_1l1MA")
    
    # Get list of topics related to the problem. For example: Dynamic programming, Greedy, String etc...
    related_questions = extract_related_questions(soup)
    topics = extract_topics(soup)

    question_details.update({
        "related_questions": related_questions,
        "topics": topics
    })

    scraped_data = {
        "contents": convert_content_to_json(question_content),
        "details": question_details
    }

    return scraped_data

def extract_related_questions(soup):
    related_questions = []
    for related_question in soup.find_all("div", {"class": "flex w-full items-center justify-between py-2"}):
        related_questions.append(related_question.findAll(string=True)[0])
    return related_questions

def extract_topics(soup):
    topics = []
    for topic in soup.find_all("a", {"class": "mr-4 rounded-xl py-1 px-2 text-xs transition-colors text-label-2 dark:text-dark-label-2 hover:text-label-2 dark:hover:text-dark-label-2 bg-fill-3 dark:bg-dark-fill-3 hover:bg-fill-2 dark:hover:bg-dark-fill-2"}):
        topics.append(topic.findAll(string=True)[0])
    return topics


def convert_content_to_json(question_content):
    # Extract description
    description = extract_description(question_content)

    # Extract examples
    examples = extract_examples(question_content)

    # Extract constraints
    constraints = extract_constraints(question_content)

    # Extract follow-up
    follow_up = extract_follow_up(question_content)

    return {
        'description': description,
        'examples': examples,
        'constraints': constraints,
        'follow_up': follow_up
    }

def extract_description(question_content):
    description = ""
    description_set = question_content.find_all('p')

    for i in range(0, len(description_set)):
        if(description_set[i].text.strip() == ""):
            break
        description += description_set[i].text.replace('\xa0', " ") + "\n\n"
    description = description.rstrip()
    return description

def extract_examples(question_content):
    examples = []
    example_tags = question_content.find_all("pre")

    for i in range(0, len(example_tags)):
        if (not example_tags[i].text.startswith("Input")):
            continue
        
        text = example_tags[i].text.split("\n")
        input_text = text[0].strip("Input:").strip()
        output_text = text[1].strip("Output:").strip()
        example = {
            'input': input_text,
            'output': output_text
        }
        if text[2] != '':
            example["explanation"] = text[2].strip("Explanation:").strip()

        examples.append(example)
    return examples

def extract_constraints(question_content):
    constraints = []
    constraint_tags = question_content.find('strong', text='Constraints:').find_next('ul').find_all('li')

    for constraint_tag in constraint_tags:
        constraints.append(constraint_tag.text.replace('\xa0', " ").strip())
    return constraints

def extract_follow_up(question_content):
    follow_up = ''
    follow_up_div = question_content.find('strong', text='Follow-up: ')
    if follow_up_div:
        follow_up_siblings = follow_up_div.next_siblings
        for sibling in follow_up_siblings:
            follow_up += sibling.text.strip()
            follow_up += " "
        follow_up = follow_up.rstrip()
    return follow_up
