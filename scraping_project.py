from socket import gethostbyaddr
from bs4 import BeautifulSoup
import requests

base_url = "http://quotes.toscrape.com/"
quotes = []

def getHTML(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except:
        print("An error occurred while performing Http request: ")
        return ''
    else:
        return response.text

def get_all_quotes_on_page(page_html):
    #From the html on the page grab all of the quotes on the current page
    page_quotes = [] 

    soup = BeautifulSoup(page_html, "html.parser")
    quote_blocks = soup.select('div.quote') #Quote info are held in divs with a "quote" class
    
    for quote_block in quote_blocks:
        #Get 
        # quote_text = quote_block.select('span.text')[0].get_text()
        # quote_author = quote_block.select('span small.author')[0].get_text()
        # quote_author_bio_link  = quote_block.select("span a")[0]["href"]
        quote_dict = {'text': quote_block.select('span.text')[0].get_text() , 'author': quote_block.select('span small.author')[0].get_text(), 'author_bio_sub_dir': quote_block.select("span a")[0]["href"]}
        page_quotes.append(quote_dict)
  
    return page_quotes

def has_next_button(page_html):
    #From the html parse and return boolean for if there is a "Next" button
    soup = BeautifulSoup(page_html, "html.parser")
    return soup.find("li",{"class":"next"})
    
    
def get_next_button_dir():
    pass
def scrape_all_pages():
    #Get the html of the base page
    base_page_html = getHTML(base_url)
    # Grab  all the quotes on the initial page and add the info (quote, author, author_link) to the quotes list
    quotes.extend(get_all_quotes_on_page(base_page_html))

    print(has_next_button(html))
    #while there is a next page button grab the info on those pages too
    


scrape_all_pages()



