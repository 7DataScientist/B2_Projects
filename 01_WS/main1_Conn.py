from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
from urllib .request import urlopen as urReq
import logging
import requests
# import pandas as pd
from datetime import datetime

import mysql.connector as conn

# Custom Packages
from db_connect import create_db, create_table, insert_table


# Creating connection object
mydb = conn.connect(host = "localhost",user = "root",password = "admin123", database = "Flip")
print(mydb)

cursor = mydb.cursor()

dataBaseName = "Flip"
customer_comments = "Cust_Comm"

# create_db(cursor,dataBaseName)
# create_table(cursor,customer_comments)


# fileName = datetime.now().strftime('main_%H_%M_%S_%d_%m_%Y.log')
logging.basicConfig(filename="main1.log", level = logging.INFO, format=" %(asctime)s %(levelname)s %(name)s %(message)s")

app = Flask(__name__, template_folder='templates')

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

            response.close()
            
            beautified_html = bs(data_flipcart,"html.parser") 

            beautified_all_phones = beautified_html.find("div",{"class":"_1YokD2 _3Mn1Gg"})
            beautiful_ph = beautified_all_phones.find("a",{"class":"_1fQZEK"})
            # logging.info(beautiful_ph)
            
            beautiful_ph_link = beautiful_ph.get("href")
            
            beautiful_ph_site = flipkart_url + beautiful_ph_link
        
            
            product6 = requests.get(beautiful_ph_site)

            product6_page = bs(product6.text,'html.parser')
            commentboxes = product6_page.find_all("div",{"class":"_16PBlm"})
            
            reviews = []
            
            for commentsB in commentboxes:
            
                # price = product6_page.find('div',{'class':'_30jeq3 _16Jk6d'}).text
                
                try:
                    # comments = commentsB.div.div.find_all('div',{'class':''})
                    # custComment = comments[0].div.text
                    comments = commentsB.div.div.find('div',{'class':''}).text
                    custComment = comments
                except:
                    print("No comments found")
                
                try:
                    # name = commentsB.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                    name = commentsB.div.div.find("p",{"class":"_2sc7ZR _2V5EHH"}).text
                    
                except:
                    print('Name Information Not available')
                    
                
                mydict = {"Comment":custComment,'Name':name}
                reviews.append(mydict)
            
                logging.info(reviews)
            
            # insert_table(cursor=cursor,tb_name=customer_comments,lst=reviews)
            # mydb.commit
            
            insert_query = "INSERT INTO Cust_Comm(Comments,Customer_Name) VALUES( %(Comment)s, %(Name)s);"
            cursor.executemany(insert_query, reviews)
            mydb.commit  
            
            
            return render_template('results.html', reviews1=reviews[0:(len(reviews)-1)])
            # return render_template('results.html', reviews1=reviews[0:len(reviews)])
            
        except:
            return render_template('Issue in the code check')
            
    else:
        return render_template('index.html')
    
    
 


if __name__ == '__main__':
   app.run(debug=True)