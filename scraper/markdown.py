"""
    Utility functions to keep track of upto which problems have been downloaded so that we can continue from 
    that problem if downloading of questions stop halfway 
"""

def convert_to_markdown(data):
    markdown = f"## {data['title']}\n\n"

    markdown += f"**Difficulty:** {data['difficulty']}\n\n"
    markdown += f"**Question ID:** {data['question_id']}\n\n"
    markdown += f"**Topics:** {', '.join(data['topics'])}\n\n"

    content = data['content']
    markdown += f"### Description\n\n{content['description']}\n\n"

    markdown += "### Examples\n\n"
    for example in content['examples']:
        markdown += "```\n"
        markdown += f"**Input:** `{example['input']}`\n\n"
        markdown += f"**Output:** `{example['output']}`\n"
        if 'explanation' in example:
            markdown += f"\n**Explanation:** {example['explanation']}\n"
        markdown += "```\n\n"


    markdown += "### Constraints\n\n"
    for constraint in content['constraints']:
        markdown += f"- {constraint}\n"

    markdown += f"\n**Follow-up:** {content['follow_up']}\n\n"

    return markdown


