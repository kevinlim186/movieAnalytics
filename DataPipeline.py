import pandas as pd
import DatabaseService


class DataPipeline():

    def __init__(self, Links, Ratings, Movies, Keywords, Credits):
        self.database = DatabaseService.Database()
        self.Links = Links
        self.Ratings = Ratings
        self.Movies = Movies
        self.Keywords = Keywords
        self.Credits = Credits

    
    def insertData(self):
        self.preprocessObjects()
        self.insertRatings()
        self.insertLinks()

        #normalize the table
        for index, row in self.Movies.iterrows():
            try:
                genres = pd.DataFrame(columns={'movieID', 'name'})
                genres['name'] = pd.json_normalize(row['genres'])['name']
                genres['movieID'] = row['movieId']
                for i, r in genres.iterrows():
                    self.database.insertGenre(r['name'], r['movieID'])

            except Exception as e:
                pass

            try:
                spoken_languages = pd.DataFrame(columns={'movieID', 'name'})
                spoken_languages['name'] = pd.json_normalize(row['spoken_languages'])['name']
                spoken_languages['movieID'] = row['movieId']
                for i, r in spoken_languages.iterrows():
                    self.database.insertLanguage(r['name'], r['movieID'])
            
            except Exception as e:
                pass

            try:
                production_company= pd.DataFrame(columns={'movieID', 'name'})
                production_company['name'] = pd.json_normalize(row['production_companies'])['name']
                production_company['movieID'] = row['movieId']
                for i, r in production_company.iterrows():
                    self.database.insertProductionCompany(r['name'], r['movieID'])
            
            except Exception as e:
                pass

            try:
                production_countries = pd.DataFrame(columns={'movieID', 'name'})
                production_countries['name'] = pd.json_normalize(row['production_countries'])['name']
                production_countries['movieID'] = row['movieId']
                
                for i, r in production_company.iterrows():
                    self.database.insertProductionCountry(r['name'], r['movieID'])
            except Exception as e:
                pass
            
            try:
                self.database.insertMovie(row['adult'],
                row['belongs_to_collection'],
                row['budget'],
                row['homepage'],
                row['movieId'],
                row['original_title'],
                row['overview'],
                row['popularity'],
                row['poster_path'],
                row['release_date'],
                row['revenue'],
                row['runtime'],
                row['status'],
                row['tagline'],
                row['title'],
                row['video'],
                row['vote_average'],
                row['vote_count'])

            except Exception as e:
                pass


        for index, row in self.Keywords.iterrows():
            try:
                keyword = pd.DataFrame(columns={'movieID', 'name'})
                keyword['name'] = pd.json_normalize(row['keywords'])['name']
                keyword['movieID'] = row['movieId']
                for i, r in keyword.iterrows():
                    self.database.insertKeywords(r['name'], r['movieID'])
            except Exception as e:
                pass

        #normalize cast and crew by using movieID as foreign key
        for index, row in self.Credits.iterrows():
            try:
                cast = pd.DataFrame(columns={'movieID', 'name','character', 'gender'})
                cast[['name','character', 'gender']] = pd.json_normalize(row['cast'])[['name','character', 'gender']]
                cast['movieID'] = row['movieId']
                for i, r in cast.iterrows():
                    self.database.insertCast(r['name'], r['movieID'], r['character'], r['gender'])

            except Exception as e:
                pass

            try:
                crew = pd.DataFrame(columns={'movieID', 'name', 'department', 'gender'})
                crew[['name', 'department', 'gender']] = pd.json_normalize(row['crew'])[['name', 'department', 'gender']]
                crew['movieID'] = row['movieId']
                for i, r in crew.iterrows():
                    self.database.insertCrew(r['name'], r['movieID'], r['department'], r['gender'])

            except Exception as e:
                pass


    def preprocessObjects(self):
        #missing ids are removed
        self.Movies = self.Movies.dropna(subset=['id','imdb_id'])
        self.Links = self.Links.dropna()
        
        #nan field cannot be accepted in the insert command
        self.Movies = self.Movies.fillna('')
        self.Credits = self.Credits.fillna('')
        self.Keywords = self.Keywords.fillna('')
        self.Links = self.Links.fillna('')
        self.Ratings = self.Ratings.fillna('')

        self.Links['movieId'] = self.Links['movieId'].astype(int)
        self.Links['imdbId'] = self.Links['imdbId'].astype(int)
        self.Links['tmdbId'] = self.Links['tmdbId'].astype(int)

        
        self.Movies = self.Movies[self.Movies['id'].str.isnumeric()]
        self.Movies = self.Movies[self.Movies['id'].str.isnumeric()]
        self.Movies['imdb_id'] = self.Movies['imdb_id'].str.replace('tt', '', regex=True).astype(int)
        self.Movies = self.Movies.merge(self.Links,how='inner', left_on='imdb_id', right_on='imdbId', suffixes=['', ''])

        self.Movies['genres'] = self.Movies['genres'].fillna('[]')
        self.Movies['genres'] = self.Movies['genres'].apply(eval)
        self.Movies['spoken_languages'] = self.Movies['spoken_languages'].fillna('[]')
        self.Movies['spoken_languages'] = self.Movies['spoken_languages'].apply(eval)
        self.Movies['production_companies'] = self.Movies['production_companies'].fillna('[]')
        self.Movies['production_companies'] = self.Movies['production_companies'].apply(eval)
        self.Movies['production_countries'] = self.Movies['production_countries'].fillna('[]')
        self.Movies['production_countries'] = self.Movies['production_countries'].apply(eval)

        self.Credits['cast'] = self.Credits['cast'].apply(eval)
        self.Credits['crew'] = self.Credits['crew'].apply(eval)
        self.Credits = self.Credits.merge(self.Links,how='inner', left_on='id', right_on='tmdbId', suffixes=['', ''])


        self.Keywords['keywords'] = self.Keywords['keywords'].apply(eval)
        self.Keywords = self.Keywords.merge(self.Links,how='inner', left_on='id', right_on='tmdbId', suffixes=['', ''])

    def insertRatings(self):
        for index,row in self.Ratings.iterrows():
            self.database.insertRatings(row['userId'], row['movieId'], row['rating'], row['timestamp'])

    def insertLinks(self):
        for index,row in self.Links.iterrows():
            self.database.insertLinks(row['movieId'], row['imdbId'], row['tmdbId'])