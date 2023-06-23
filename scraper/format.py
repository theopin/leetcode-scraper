"""
    Utility functions to keep track of upto which problems have been downloaded so that we can continue from 
    that problem if downloading of questions stop halfway 
"""

def convert_to_markdown(data):
    markdown = f"## {data['title']} "
    markdown += f"[#{data['question_id']}](" + f"{data['url']}" + ") "   

    difficulty = data['difficulty']

    chip_color = '#ff0000'  # Red
    if difficulty == 'Easy':
        chip_color = '#00ff00'  # Green
    elif difficulty == 'Medium':
        chip_color = '#ffff00'  # Yellow

    markdown += f'\n\n<span style="display: inline-block; padding: 3px 10px; border-radius: 20px; background-color: {chip_color}; color: #333; font-size: 14px; margin-right: 5px; max-width: 200px;">{difficulty}</span>'
    
    markdown += f"\n\n<b>Topics:</b> {', '.join(data['topics'])}\n\n"

    content = data['content']
    markdown += f"### Description\n\n{content['description']}\n\n"

    markdown += "### Examples\n\n"
    for example in content['examples']:
        markdown += "<pre>\n"
        markdown += f"<b>Input:</b> {example['input']}\n\n"
        markdown += f"<b>Output:</b> {example['output']}\n"
        if 'explanation' in example:
            markdown += f"\n<b>Explanation:</b> {example['explanation']}\n"
        markdown += "</pre>\n\n"

    markdown += "### Constraints\n\n"
    for constraint in content['constraints']:
        markdown += f"- {constraint}\n"

    if(content['follow_up'] != ''):
        markdown += f"\n<b>Follow-up:</b> {content['follow_up']}\n\n"

    markdown += "### Proposed Solution - Python"  + "\n\n"
    markdown += "<pre>" + "# Python solution code here"
    markdown += "</pre>\n\n"

    markdown += "### Proposed Solution - Java" + "\n\n"
    markdown += "<pre>" + "// Java solution code here"
    markdown += "</pre>\n\n"

    markdown += "### Solution Explanation\n\n"
    markdown += "Explain the approach and reasoning behind the proposed solution. Add any additional details or insights related to the problem."
    markdown += "\n\n"

    markdown += "### Complexity Analysis\n\n"
    markdown += "- Time complexity: Please input the time complexity of the solution and an explanation for your choice."
    markdown += "\n\n"

    return markdown


