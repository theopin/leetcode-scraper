"""
    Utility functions to keep track of upto which problems have been downloaded so that we can continue from 
    that problem if downloading of questions stop halfway 
"""

import bs4


# Tracks the questions we have already downloaded
def scrape_question(html):

    soup = bs4.BeautifulSoup(html, "html.parser")

    # Retrieve question content
    content = soup.find("div", class_="_1l1MA")
    
    # Get list of topics related to the problem. For example: Dynamic programming, Greedy, String etc...
    topics = []
    for topic in soup.find_all("a", {"class": "mr-4 rounded-xl py-1 px-2 text-xs transition-colors text-label-2 dark:text-dark-label-2 hover:text-label-2 dark:hover:text-dark-label-2 bg-fill-3 dark:bg-dark-fill-3 hover:bg-fill-2 dark:hover:bg-dark-fill-2"}):
        topics.append(topic.findAll(string=True)[0])
        
    db_entry = {
        "content": convert_content_to_json(soup, content),
        "topics": topics
    }
    

    print(db_entry) # TODO: Convert to markdown and append to file
    return db_entry


def convert_content_to_json(soup, content):

    # Extract description
    description = content.find('p').text.replace('\xa0', " ")

    # Extract examples
    examples = []
    example_tags = content.find('strong', text='Input:')

    for example_tag in example_tags:
        #print("example",example_tag.find_next('pre').children)
        print("input", example_tag.next.text)
        #print("output", example_tag.find_next('pre'))
        example = {
            'input': example_tag.next.text.strip('input').strip(),
            'output': example_tag.next.next.next.next.text.strip('output').strip()
        }
        explanation_tag = example_tag.find_next('strong', class_='example')
    
        if explanation_tag and explanation_tag.name == 'strong':
            example['explanation'] = explanation_tag.find_next('pre').text.strip()
    
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
