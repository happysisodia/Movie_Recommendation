<h1> My Movie Recommendation Website </h1>

<h2> Objective </h2>
Build a content based movie recommendation system and make an API using django and deploy it on the cloud. </br> </br>

Recommendation system are everywhere. Almost every major tech company has applied them in some form. Some of the best example are 'Youtube', 'Netflix', 'Spotify' etc. In this Project, I will create a Recommendation site and host it on Heroku. I took up this project as finding a good movie is one of the most classical problem that many of us face on a day to day basis(especially in this pandemic). Thus this recommendation system based on machine learning or deep learning to find movies that users are most likely to enjoy! </br>

<h2> Contents:</h2>
<ul>
  <li> Extracting the data </li>
  <li> Cleaning the data </li>
  <li> exploratory data analysis (EDA) </li>
  <li> Building a Content based Recommendation system </li>
  <li> Build a REST API using Django </li>
  <li> Test it on the local System host </li>
  <li> Deploy it on Heroku - API goes online </li>
</ul>

<h2> Dataset</h2>

To Source data, we often rely on SQL and NoSQL databases, API's or ready made CSV dataset. The Problem is one can not always find a dataset on your topic, databases are not kept current and API are either expensive or have usage limit. Therefore I decided to extract the data from the IMDb website instead of using the other pre-cleaned datasets from Kaggle or other website. </br>
Since I wanted to collect the information of as many movies as possible. I tried identifying efficient ways of obtaining the data. On investigation of the IMDb website, I found an advance search option that displaying all the movies belonging to a particular 'Genre'. It contains some of the information that I needed to make an recommendation model. More importantly, I was able to extract IMDb movie ID which could be further used to extract all the available information of the movie.  </br>
Thus using the Url - 'https://www.imdb.com/search/title/?title_type=feature&genres=' + _genre + '&start=' + str(_movie_count) + '&explore=genres&ref_=adv_nxt' and looping through all the pages (number of movies/50) I was able to collect the following information from the extract : 
<ul>
  <li> IMDb ID </li>
  <li> Movie Name </li>
  <li> Classification - Certification of the movie </li>
  <li> Year           - The year movie was released </li>
  <li> Runtime        - The length of the movie in minutes </li>
  <li> IMDb           - The average of the rating of the movie by people </li>
  <li> Metascore      - Movie rating as give on the metascore website </li>
</ul>  
</br>

The Genres for which the above information was collected are - "action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'war','drama', 'family', 'fantasy', 'history', 'horror','sport', 'western','music', 'musical', 'mystery', 'romance', 'sci-fi',  'thriller". The total number of non-duplicate movies after collecting the above mentioned information is '112540' with movies as old as from '1900' to movie with release date in '2027'(Discussed in detail  in the EDA). </br>
 
For this I deciced to further restrict the movies to a year range of 1980 to 2020 which reduced the number of movies to 67055. Now Though the information collected above was enough for doing an EDA, it was not enough for creating the recommendation system I had in mind. So to collect more information, I queried the IMDb using the 'Movie Id' and the </br> url = "https://www.imdb.com/title/" + 'Movie_id' for all the 67055 movies and collected the following information. 
<ul>
  <li> Genre            - genres of the movies </li>
  <li> Director         - Director of the movie</li>
  <li> Language         - Languages the movie is available in  </li>
  <li> Keywords         - Tags assigned to the movie </li>
  <li> Tagline          - Tagline of the movie</li>
  <li> MPAA             - Motion Picture Rating</li>
  <li> Budget           - Budger of the movie</li>
  <li> Revenue          - total earnings of the movie (till yet)</li>
  <li> Summary          - Bried description of the movie</li>
  <li> Actors           - Actors in the movie</li>
  <li> Writer           - Writer of the movie</li>
  <li> Votes            - Number of votes for the movie on the IMDb website</li>
  <li> Production House - the Production company that made the movie</li>
</ul>

Thus After Combining both the datasets on 'ID' , I had a datasets of 67055 Movies with 20 attributes. 

 
 
