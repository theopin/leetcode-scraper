"""
    Utility functions to keep track of upto which problems have been downloaded so that we can continue from 
    that problem if downloading of questions stop halfway 
"""

import bs4

import driver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

web_driver = None

def create_web_driver():
    global web_driver
    web_driver = driver.create_driver()

def quit_web_driver():
    global web_driver
    web_driver.quit()


def scrape_question(question_num, question_api_data):
    print(f"Fetching problem " + f"#{question_num}")

    try:
        web_driver.get(question_api_data["url"])

        # Wait 30 secs or until div with class '_1l1MA' appears
        WebDriverWait(web_driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "_1l1MA"))
        )

        scraped_data = format_scraped_question(web_driver.page_source, question_api_data)

        print(f"Successfully extracted problem " + f"#{question_num}\n")

        return scraped_data

        

    except Exception as e:
        print(f"Failed to extract problem "+ f"#{question_num}")
        print("Reason: "+ f"{e}")
        web_driver.quit()
        exit(0)


# Tracks the questions we have already downloaded
def format_scraped_question(page_source, question_api_data):

    soup = bs4.BeautifulSoup(page_source, "html.parser")

    # Retrieve question content
    content = soup.find("div", class_="_1l1MA")
    
    # Get list of topics related to the problem. For example: Dynamic programming, Greedy, String etc...
    topics = []
    for topic in soup.find_all("a", {"class": "mr-4 rounded-xl py-1 px-2 text-xs transition-colors text-label-2 dark:text-dark-label-2 hover:text-label-2 dark:hover:text-dark-label-2 bg-fill-3 dark:bg-dark-fill-3 hover:bg-fill-2 dark:hover:bg-dark-fill-2"}):
        topics.append(topic.findAll(string=True)[0])
        
    scraped_data = {
        "content": convert_content_to_json(soup, content),
        "topics": topics
    }

    scraped_data.update(question_api_data)
    
    return scraped_data


def convert_content_to_json(soup, content):
    # Extract description
    description = ""
    description_set = content.find_all('p')

    for i in range(0, len(description_set)):
        if(description_set[i].text.strip() == ""):
            break
        description += description_set[i].text.replace('\xa0', " ") + "\n\n"
    description = description.rstrip()

    # Extract examples
    examples = []
    example_tags = content.find_all("pre")

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

    # Extract constraints
    constraints = []
    constraint_tags = content.find('strong', text='Constraints:').find_next('ul').find_all('li')

    for constraint_tag in constraint_tags:
        constraints.append(constraint_tag.text.replace('\xa0', " ").strip())

    # Extract follow-up
    follow_up = ''
    follow_up_div = content.find('strong', text='Follow-up: ')
    if follow_up_div:
        follow_up_siblings = follow_up_div.next_siblings
        for sibling in follow_up_siblings:
            follow_up += sibling.text.strip()
            follow_up += " "
        follow_up = follow_up.rstrip()

    return {
        'description': description,
        'examples': examples,
        'constraints': constraints,
        'follow_up': follow_up
    }
