"""
    Utility functions to keep track of upto which problems have been downloaded so that we can continue from 
    that problem if downloading of questions stop halfway 
"""

import bs4


# Tracks the questions we have already downloaded
def scrape_question(html):

    soup = bs4.BeautifulSoup(html, "html.parser")

    # Retrieve question content
    content = soup.find("div", {"class": "_1l1MA"})
    
    # Get list of topics related to the problem. For example: Dynamic programming, Greedy, String etc...
    topics = []
    for topic in soup.find_all("a", {"class": "mr-4 rounded-xl py-1 px-2 text-xs transition-colors text-label-2 dark:text-dark-label-2 hover:text-label-2 dark:hover:text-dark-label-2 bg-fill-3 dark:bg-dark-fill-3 hover:bg-fill-2 dark:hover:bg-dark-fill-2"}):
        topics.append(topic.findAll(string=True)[0])
        
    db_entry = {
        "content": content,
        "topics": topics
    }
    

    print(db_entry) # TODO: Convert to markdown and append to file
    return db_entry
