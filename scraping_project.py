from socket import gethostbyaddr
from bs4 import BeautifulSoup
import requests, re, random



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


def get_author_birth_info(quote_dict):
    #Send request to author's bio page
    #Scrap the bio page

    base_url = "http://quotes.toscrape.com/"
    scraped_page = scrapePage(getHTML(base_url + quote_dict["author_bio_sub_dir"]))
    #Extract the birthinfo
    author_birth_info = scraped_page.find("span", {"class":"author-born-date"}).text +" "+  scraped_page.find("span", {"class":"author-born-location"}).text
    return author_birth_info


def game_loop():
    guesses = 4
    game = True


    def handle_game_over():
    #Get if the user wants to play again, if
    #Reset the game if needed or break the loop
        if input("Do you want to play again? (y/n):") == "y":
            #Resets and return True
            nonlocal guesses
            guesses = 4
            random.shuffle(quotes)
            return True

        return False

    #Grab all of the quotes from the website and shuffle them in the list
    quotes = scrape_all_pages()
    random.shuffle(quotes)

    print(quotes)
    #Begin the game loop
    while(game):

        #Display the 1st quote and get the user input
        print()
        print("Quote:")
        print()
        print(quotes[0]["text"])
        user_guess = input(f"Who said this? Guesses remaining: {guesses}: ")
        print()
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
                    game = handle_game_over()
                case 1:
                    name_letters= re.sub("\W", "", quotes[0]["author"])
                    print(f"The author has {len(name_letters)} letters in their name" )
                case 2:
                    first_name, *other_names = quotes[0]["author"].split(" ")
                    print(f"The author's name begins with {first_name[0]} and their last name begins with {other_names[0][0]}" )
                case 3:
                    print(f"Here's some info about the author's birth: {get_author_birth_info(quotes[0])}") 
                case _:
                    raise ValueError
     
        #If they're out of guesses, game over and ask if they want to play against and reset the game
        # 3 guesses left - show a hint with the authors bdate and location
        # 2 guesses left - first letter of author first name and last name
        # 1 guess left - Number of letters in their first name


        
game_loop()










