
from dotenv import load_dotenv
from flask import Flask, request

import os
import json
import traceback

import leetcode.process 

scraper_app = Flask(__name__)

load_dotenv()

PORT = os.getenv("PORT") or 3000

@scraper_app.route("/", methods = ['GET']) 
def leetcode_scrape():
    response = {}
    response_code = 200

    try:   
        response = leetcode.process.run_scraper(request.args)
        response["status"] = "success"
    
    except Exception as error:
        print(traceback.format_exc())
        print("LOLOLOL", error)
        response["status"] = "error"
        response["message"] = f"{error.args[0]}"
        response_code = error.args[1]

    finally:
        leetcode.process.complete_scrape()
        
        return json.dumps(response, indent=4), response_code

         

scraper_app.run(port=PORT)
