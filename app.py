# This is a sample Python script.

#webscrapping project of flipkart
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as bs
import requests
from flask import Flask, app, request, render_template

app = Flask(__name__)


@app.route('/')
def scrap():

    search=input()
    flipkart_url = "https://www.flipkart.com/search?q="
    search_url = flipkart_url + search
    uClient = ureq(search_url)
    flipkartPage = uClient.read()
    uClient.close()
    flipkartBeauty = (bs(flipkartPage, "html.parser"))
    bigBoxes = flipkartBeauty.findAll("div", {"class": '_1AtVbE col-12-12'})
    finalReview = []
    del bigBoxes[0:3]
    for bigBoxe in bigBoxes:
        box = bigBoxe
        try:
            product_link = "https://www.flipkart.com" + (box.div.div.div.a['href'])
            prod_res = requests.get(product_link)
            flipkartBeauty_Product = (bs(prod_res.text, "html.parser"))
            reviews = flipkartBeauty_Product.findAll("div", {"class": '_16PBlm'})
            for review in reviews:
                try:
                    name = review.div.div.findAll("p", {"class": '_2sc7ZR _2V5EHH'})[0].text
                except:
                    name = "no Name"
                try:
                    rating = review.div.div.div.div.text
                except:
                    rating = "no rating"
                try:
                    commentHead = review.div.div.div.p.text
                except:
                    commentHead = "no head"
                try:
                    tag = review.div.div.findAll("div", {"class": ''})
                    custComment = tag[0].div.text
                except:
                    custComment = "no custComment"
                mydict = {"seachString": search, "name": name, "rating": rating, "commentHead": commentHead,
                          "custComment": custComment}
                finalReview.append(mydict)
        except:
            print("no link")
    print(finalReview)
    return render_template('app.html')


# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    app.run(debug=True)
