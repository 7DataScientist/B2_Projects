from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
from urllib .request import urlopen as urReq
import logging
import requests
import pandas as pd
from datetime import datetime


fileName = datetime.now().strftime('main_%H_%M_%S_%d_%m_%Y.log')

logging.basicConfig(filename=fileName, level = logging.INFO, format=" %(asctime)s %(levelname)s %(name)s %(message)s")

app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route("/review", methods = ['POST', 'GET'])
def results():
    
    if request.method == "POST":
        try:
            
            searchString = request.form['content'].replace(" ","")
            print(searchString)
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            response = urReq(flipkart_url)
            data_flipcart = response.read()
            # logging.info(data_flipcart)
            # print(data_flipcart)
            response.close()
            
            beautified_html = bs(data_flipcart,"html.parser") 
            # logging.info(beautified_html)
            # print(beautified_html)
            
            beautified_all_phones = beautified_html.find("div",{"class":"_1YokD2 _3Mn1Gg"})
            beautiful_ph = beautified_all_phones.find("a",{"class":"_1fQZEK"})
            # logging.info(beautiful_ph)
            
            beautiful_ph_link = beautiful_ph.get("href")
            
            beautiful_ph_site = flipkart_url + beautiful_ph_link
            
            # bs = bs(beautiful_ph_site,'html.parser')
            # logging.info(bs)
            
            product6 = requests.get(beautiful_ph_site)
            # prod6_test = product6.text
            # logging.info(prod6_test)
            
            product6_page = bs(product6.text,'html.parser')
            
            # variant_p = product6_page.find_all("div",{"class":"_1AtVbE col-12-12"})
            
            price = product6_page.find('div',{'class':'_30jeq3 _16Jk6d'}).text
            
            comments = product6_page.find_all('div',{'class':'t-ZTKy'})
            
            name = product6_page.find_all('p',{'class':'_2sc7ZR _2V5EHH'})
            
            comment_h = product6_page.find_all('p',{'class':'_2-N8zT'})
            
            data1 = []

            for i in comments:
                i = i.text
                data1.append(i)
            
            data2 = []
            
            for i in comment_h:
                i = i.text
                data2.append(i)
               
            data3 = []
             
            for i in name:
                i = i.text
                data3.append(i)
            
            # Saving it in a DataFrame    
            df_c = pd.DataFrame(data1, columns = ['Comment'])
            df_c["Comment_Header"] = [i.text for i in comment_h]
            df_c["Price"] = price
            df_c["Name"] = [i.text for i in name]
            
            dic = df_c.to_dict()
            
            print(dic)
            logging.info(dic)
            
            
        except:
            pass
        
        
        
        return render_template('results.html')
    
    else:
        return render_template('index.html')



if __name__ == '__main__':
   app.run(debug=True)