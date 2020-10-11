import DatabaseService
import pandas as pd 
import DataPipeline

ratings = pd.read_csv('./data/ratings.csv').iloc[:500]
links = pd.read_csv('./data/links.csv').iloc[:500]
movies = pd.read_csv('./data/movies_metadata.csv').iloc[:500]
_credits = pd.read_csv('./data/credits.csv').iloc[:500]
keywords = pd.read_csv('./data/keywords.csv').iloc[:500]


#accepts a panda data frame type that follows the schema of the csv.
dataPipeline = DataPipeline.DataPipeline(Links=links, Ratings=ratings, Movies=movies, Keywords=keywords, Credits=_credits)


dataPipeline.insertData()