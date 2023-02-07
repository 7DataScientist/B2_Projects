from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
from urllib .request import urlopen as urReq
import logging

logging.basicConfig(filename='main.log', level = logging.INFO, format=" %(asctime)s %(levelname)s %(name)s %(message)s")



app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def index():
    return render_template('index.html')



@app.route("/review", methods = ['POST', 'GET'])
def results():
    
    if request.method == "POST":
        try:
            
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            response = urReq(flipkart_url)
            data_flipcart = response.read()
            logging.info(data_flipcart)
            
        
        except:
            pass
        
        
        
        return render_template('results.html')
    
    else:
        return render_template('index.html')



if __name__ == '__main__':
   app.run(debug=True)