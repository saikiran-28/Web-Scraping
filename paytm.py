from flask import Flask,render_template,request
from bs4 import BeautifulSoup  # parser
import requests  # to get source code
import pandas as pd
import numpy as np
import re
from matplotlib import style
import matplotlib.pyplot as plt
app = Flask(__name__)
@app.route('/')
def home():
   return render_template('home.html')
@app.route('/signin')
def signin():
   return render_template('signin.html')
@app.route('/register')
def register():
   return render_template('register.html')
@app.route('/search')
def search():
   return render_template('search.html')
@app.route('/product',methods=['POST'])
def product():
   if request.method == 'POST':
      pro_name = request.form['pro_name']
      range=request.form['filter']
      name =[]
      price = []
      actual =[]
      dis=[]
      category={'mobiles':'6224','laptops':'6453','shoes':'5048','LED TVs':'24843','Dresses for Women':'5223','Dresses for Men':'12565','Earphones':'78654'}
      def search_paytm():#function 
         if(pro_name in category):
            #url for some specific products since paytm has seperate categories for each product
            url = 'https://paytmmall.com/shop/search?q='+pro_name+'&from=organic&child_site_id=6&site_id=2&category='+category[pro_name]
         else:    
            #url for general search other than the products that are not present in the dictionary 'category'
            url = 'https://paytmmall.com/shop/search?q='+pro_name+'&from=organic&child_site_id=6&site_id=2'

         #to get the html code from the specified url
         s_code = requests.get(url)
         #soup variable consists of the html code
         soup = BeautifulSoup(s_code.text,'html.parser') 
         
         for a in soup.findAll('a', href = True ,attrs = {'class': '_8vVO'}):
            #For extracting name of the product
            name1=a.find('div',attrs = {'class': 'UGUy'}).text.strip() 
            #For extracting price of the product
            price1=a.find('div',attrs = {'class': '_1kMS'}).text.strip()
            #removing ;,' in the text extracted
            price1=re.sub(',','',price1)
            #extracting the actual price of the product
            price2 = a.find('div', attrs ={'class':'dQm2'})
            #the actual price is not present for all the products ,to filter them using the below if and else statement
            if str(type(price2)) == "<class 'NoneType'>":
               price2 =price1
            else:
               price2=price2.text.strip()
               if len(price2.split('-')) == 2 :
                  price2 , disc = price2.split('-')
                  price2=re.sub(',','',price2)
               else:
                  price2=re.sub(',','',price2)
            #typecasting price to integer
            price1=int(price1)
            #typecastinf actual price to integer
            price2=int(price2)
            #calculating discount percentage
            discount1 = ((price2-price1)/price1)*100
            #rounding the discount % value to 2 decimal places
            discount = round(discount1,2)
            #adding the extracted details to the list
            name.append(name1)
            price.append(price1)
            actual.append(price2)
            dis.append(discount)
      
         global df
         global top5
         global rslt_df,min,max

         df = pd.DataFrame(list(zip(name,actual,price,dis)))
         df.columns =['Name','Actual Price','Price','Discount %']
         df.index = np.arange(1, len(df)+1)
         #top5 variable consists of top 5 best deals out of all the avaialble products
         result = df.sort_values('Discount %', ascending = False)
         top5=result.iloc[:5,[0,2,3]]
         #plotting and saving a bar_plot of Name Vs Price
         bar_p= df.iloc[:,[0,2]]
         bar_pl = bar_p.set_index(df.Name.str[:30])
         bar_plot = bar_pl.plot(kind = 'bar', figsize=(15,8))
         plt.savefig('/home/vedha-root/Desktop/pybox/static/images/new_plot.png')
         if(range == 'start'):
            min= 0
            max =10000000
         elif(range == 'a'):
            min=0
            max=10000
         elif(range == 'b'):
            min=10000
            max=20000
         elif(range == 'c'):
            min=20000
            max=30000
         elif(range == 'd'):
            min=30000
            max=40000
         elif(range == 'e'):
            min=40000
            max=50000
         elif(range == 'f'):
            min =50000
            max=10000000
        
         rslt_df = df[(df['Price'] >= min) & (df['Price'] <= max)]
         
  

   search_paytm() 
   return render_template('product.html',df=df,top5=top5,min = min,max = max ,rslt_df = rslt_df, name = 'Product_Name Vs Price', url1 ='/static/images/new_plot.png')
if __name__ == '__main__':
   app.run(debug = True)