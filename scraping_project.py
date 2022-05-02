from socket import gethostbyaddr
from bs4 import BeautifulSoup
import requests, re



def getHTML(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except:
        print("An error occurred while performing Http request: ")
        return ''
    else:
        return response.text
def scrapePage(page_html):
    soup = BeautifulSoup(page_html, "html.parser")

    return soup
def get_all_quotes_on_page(scraped_page):
    #From the html on the page grab all of the quotes on the current page
    page_quotes = [] 

    quote_blocks = scraped_page.select('div.quote') #Quote info are held in divs with a "quote" class
    
    for quote_block in quote_blocks:
        #Get 
        # quote_text = quote_block.select('span.text')[0].get_text()
        # quote_author = quote_block.select('span small.author')[0].get_text()
        # quote_author_bio_link  = quote_block.select("span a")[0]["href"]
        quote_dict = {'text': quote_block.select('span.text')[0].text , 'author': quote_block.select('span small.author')[0].get_text(), 'author_bio_sub_dir': quote_block.select("span a")[0]["href"]}
        page_quotes.append(quote_dict)
  
    return page_quotes

def has_next_button(scraped_page):
    #From the html parse and return boolean for if there is a "Next" button

    return scraped_page.find("li",{"class":"next"})
    
    
def get_next_button_dir(scraped_page):
    #Grab the button's sub directory
    return scraped_page.find("li", {"class":"next"}).find("a")["href"]

def scrape_all_pages():
    base_url = "http://quotes.toscrape.com/"
    page_sub_dir = ''
    quotes = []
    count = 0
    #Grab all the quotes on all of the pages
    while(True):

        #Get the html of the current page
        current_page_html = getHTML(base_url + page_sub_dir)
        #Scrape the page with BS4
        scraped_page = scrapePage(current_page_html)
        # Grab  all the quotes on the current page and add the info (quote, author, author_link) to the quotes list
        quotes.extend(get_all_quotes_on_page(scraped_page))
        count += 1
        # Check if there is a next page button. If there isn't break the loop
        if(not has_next_button(scraped_page)):
            break
        # If there is, grab the sub directory to the next page and adjust the page_sub_dir variable
        else:
            page_sub_dir = get_next_button_dir(scraped_page)

    return quotes

def game_loop():
    guesses = 4
    game = True


    def handle_game_over():
    #Get if the user wants to play again, if
    #Reset the game if needed or break the loop
        if input("Do you want to play again? (y/):") == "y":
            #Resets and return True
            global guesses
            guesses = 4
            quotes.shuffle()
            return True
          
        return False

    #Grab all of the quotes from the website and shuffle them in the list
    quotes = scrape_all_pages()
    quotes.shuffle()


    #Begin the game loop
    while(game):

        #Display the 1st quote and get the user input
        print("Here's a quote:")
        print()
        print(quotes[0]["text"])
        user_guess = input(f"Who said this? Guesses remaining: {guesses}: ")
        
        #If the user is correct tell them congrats and ask if they want to play again. If they do, reshuffle the quotes and update the guesses
        if user_guess.lower() == quotes[0]["author"].lower():
            print("You guessed correctly correctly! Congratulations!")
            if not handle_game_over():
                break
        #If the user isn't correct, update the number of guesses
        else:
            guesses -= 1

            match guesses:
                case 0:
                    print("You're out of guesses! GAME OVER!")
                    handle_game_over()
                case 1:
                    name_letters= quotes[0]["author"]
                    print(f"The author has {len(name_letters)} letters in their name" )
     
        #If they're out of guesses, game over and ask if they want to play against and reset the game
        # 3 guesses left - show a hint with the authors bdate and location
        # 2 guesses left - first letter of author first name and last name
        # 1 guess left - Number of letters in their first name


        











