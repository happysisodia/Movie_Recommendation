import requests
import re
import pandas as pd
import numpy as np
import time
import io
from bs4 import BeautifulSoup 

imdb       = []
data_final = []

def extract():
    # Genres of the movies for which the movies will be pulled
    # GENRES = ['action']
    GENRES = ['action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'war',
			  'drama', 'family', 'fantasy','history', 'horror', 
			  'music', 'musical', 'mystery', 'romance', 'sci-fi', 'sport', 'thriller','western']	

	# Upper Limit - How many movies should be pulled at max 
    upper_limit = 500000

    for genre in GENRES:
        movie_count_total = setMovieCountTotal(genre)

        # get number of pages, 50 items per page
        num_pages = int(movie_count_total / 50)
        print ('Genre:\t\t' + genre)
        print ('Num Pages:\t' + str(num_pages))
        print ()

        movie_index = 1

        for i in range(0, num_pages):
		
            url = getUrl(movie_index, genre)

            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            movies_article = soup.find(class_ = 'article')
            movies_list = movies_article.findAll('div', {'class': 'lister-item mode-advanced'})


            for movie in movies_list:
                stripInfo(movie, genre)
			


            if movie_index < upper_limit:
                movie_index += 50
            else:
                break

def getUrl(_movie_count, _genre):
    if (_genre == 'documentary'):
        return ('https://www.imdb.com/search/title/?genres=documentary&start=' + str(_movie_count) + 
                '&explore=genres&ref_=adv_nxt')
    else:
        return ('https://www.imdb.com/search/title/?title_type=feature&genres=' + _genre + '&start=' + 
                str(_movie_count) + '&explore=genres&ref_=adv_nxt')


# find and calculate the number of pages to iterate through based on the number of films in the list
def setMovieCountTotal(_g):
    url_temp = getUrl(1, _g)
    page = requests.get(url_temp)
    soup = BeautifulSoup(page.content, 'html.parser')
    temp = soup.find(class_='desc')

    temp = temp.span.get_text().split()[2]
    temp = temp.replace(',', '')
    print ('total movies: ' + temp)
    return int(temp)


def stripInfo(_movie, _genre):

    movie_id = _movie.find(class_ = 'ribbonize').get('data-tconst')
	
    title = _movie.find(class_ = 'lister-item-header')
    if not(title == None):
        title = title.a.get_text()

    classification = _movie.find(class_='certificate')
    if not(classification == None):
        classification = classification.get_text()

    runtime = _movie.find(class_='runtime')
    if not(runtime == None):
        runtime = runtime.get_text().split()[0]

    year = _movie.find(class_='lister-item-year text-muted unbold')
    if not(year == None):
        year = year.get_text()[-5:-1]

        # make sure the text gather is in the YYYY format, otherwise set to None
        if not(re.search('[0-9][0-9][0-9][0-9]', year)):
            year = None

    rating = _movie.find(class_='inline-block ratings-imdb-rating')
    if not(rating == None):
        rating = rating.get_text().strip()

    metascore = _movie.find(class_='inline-block ratings-metascore')
    if not(metascore == None):
        metascore = metascore.get_text().split()[0]
    
    data = {"ID": movie_id,
			"movie_title": title,
            "class": classification, 
            "year": year,
            "runtime": runtime ,
            "rating": rating,
            "meta": metascore}
    imdb.append(data)	


def Movie_extract(df_movie_final):

    num_range = df_movie_final.shape[0]
    for i in range(0,num_range):
    
        url = "https://www.imdb.com/title/" + df_movie_final.ID[i]
        Id = df_movie_final.ID[i]
    
        #intialize variables
        poster      = ''
        budget      = ''
        genre       = '' 
        Director    = ''
        language    = ''
        Keywords    = '' 
        tagl        = ''
        mpaac       = ''
        budget      = ''
        evenue     = ''
        description = ''
        Actors      = ''
        writer      = ''
        ratingCount = ''
        company     = ''
        genres      = []
    

        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')

        # Poster Link
        poster = soup.find('div',{'class': 'poster'})
        if not(poster == None):   
           poster = poster.find('img')
           poster = poster.get('src')

        # Movie Summary 
        for i in soup.find_all('div',{'class': 'summary_text'}):
            i = i.text
            description = i.strip()

        #Director , writer and actors of the movie
        plot_summaryDirector = soup.find('div',{'class': 'plot_summary'})
        Director = []
        Actors   = []
        writer   = [] 
        if not(plot_summaryDirector == None):
            for i in plot_summaryDirector.find_all('div',{'class': 'credit_summary_item'}):
                i = i.text
                i = i.strip()
                if "Director:" in i:
                    Director = i[10:]
                    Director = Director.split(',')
                    Director = Director
                elif "Directors:" in i:
                    Director = i[11:]
                    Director = Director.split(',')
                    Director = Director
                elif "Writer:" in i:
                    writer = i[8:]
                    writer = writer.split(',')
                    writer = writer
                elif "Writers:" in i:
                    writer = i[9:]
                    writer = writer.split(',')
                    writer = writer
                elif "Stars:" in i:
                    Actors = i[6:]
                    Actors = Actors.split('|')
                    Actors = Actors[0:]
                    s      = ([s.strip() for s in Actors])
                    Actors =([x for x in s if x])

        # rating Count of the movie 
        ratingCount = soup.find("span", {"itemprop" : "ratingCount"})
        if not(ratingCount == None):
            ratingCount = ratingCount.string
    
        #language list
        txtblock = soup.find('div',{'id': 'titleDetails'}) 
        if not(txtblock == None):
            for i in txtblock.find_all('div',{'class': 'txt-block'}):
                i = i.text
                i = i.strip()
                if "Language:" in i:
                    language = i.split()
                    language = language[1:]
                    s        = ([s.strip('|') for s in language])
                    language =([x for x in s if x])

        text1 = soup.find('div',{'id': 'titleStoryLine'})

        # keywords of the movie
        if not(text1 == None):    
            for i in text1.find_all('div',{'class': 'see-more inline canwrap'}):
                i = i.text
                i = i.strip()
                if "Keywords:" in i:
                    Keywords = i.split('|')
                    Keywords = Keywords[1:]
                    s        = ([s.strip() for s in Keywords])
                    Keywords =([x for x in s if x])	
                elif "Genres:" in i:
                    genres = i.split(':')
                    genres = genres[1:]
                    s = ([s.strip() for s in genres])
                    genres = ([x for x in s if x])	
                    genre = genres

        #tagline of the movie and motion picture Rating 
        if not(text1 == None):
            for i in text1.find_all('div',{'class': 'txt-block'}):
                i = i.text
                i = i.strip()
                if "Taglines" in i:
                    tagl = i
                    tagl = tagl[10:]
                elif "MPAA" in i:
                    mpaac = i.split('|')
                    mpaac = mpaac[0:]


        text2 = soup.find('div',{'id': 'titleDetails'})

        # Budget , Revenue and the production company of the movie
        if not(text2 == None):
            for i in text2.find_all('div',{'class': 'txt-block'}):
                i = i.text
                i = i.strip()
                if "Budget:" in i:
                    budget = i.split(':')
                    budget = budget[1:]
                    s      = ([s.strip() for s in budget])
                    budget =([x for x in s if x])
                elif "Cumulative Worldwide Gross" in i: 
                    revenue = i.split(':')
                    revenue = revenue[1:]
                elif "Production Co" in i:
                    company = i.split(':')
                    company = company[1:]
                    s       = ([s.strip() for s in company])
                    company =([x for x in s if x])	


        data1 = {
            "ID"                : Id,
            "Poster"            : poster,
            "Genre"             : genre,    
           "Director"          : Director,
            "Language"          : language,
            "Keywords"          : Keywords,
            "Tagline"           : tagl,
            "MPAA"              : mpaac,
            "Budget"            : budget,
            "revenue"           : revenue,
            "Summary"           : description,
            "Actors"            : Actors,
            "writer"            : writer,
            "No_of_Votes"       : ratingCount,
            "Production_Company": company
        }
        data_final.append(data1)


if __name__ == '__main__':

    extract()

    movie_ini = pd.DataFrame(imdb)
    movie_ini.to_csv('data_ini.csv',index=False)

    
    Movie_extract(movie_data)
    movie_ext = pd.DataFrame(data_final)
    movie_ext.to_csv('data_ext.csv',index=False)

    movie_data = pd.merge(movie_ini, movie_ext, on="ID")
    movie_data.to_csv('data_movie.csv',index=False)


    
