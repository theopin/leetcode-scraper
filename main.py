
from dotenv import load_dotenv
from flask import Flask, request

import os
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
        response["status"] = "error"
        response["message"] = f"{error.args[0]}"
        response_code = error.args[1]

    finally:
        leetcode.process.complete_scrape()
        
        return response, response_code

         

scraper_app.run(port=PORT)
