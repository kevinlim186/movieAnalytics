import config
import pymysql
from datetime import datetime
import pandas as pd

class Database():
    
    def __init__(self):
        self.myDB = pymysql.connect(host=config.config['host'], port=int(config.config['port']), user=config.config['dbuser'], passwd=config.config['dbpassword'], db=config.config['database'],
        autocommit=True,local_infile=True);

        self.cHandler = self.myDB.cursor()
    
    
    def insertCast(self, name, movieID, character_, gender):
        sql = '''
            insert into Cast_ (name, movieID, character_, gender )
            values (%s, %s, %s, %s)
            '''

        try:
            self.cHandler.execute(sql, (str(name), str(movieID), str(character_), str(gender)))
        except Exception as e: 
            pass

    def insertCrew(self, name, movieID, department,gender):
        sql = '''
            insert into Crew (name, movieID, department,gender)
            values (%s, %s, %s, %s)
            '''

        try:
            self.cHandler.execute(sql, (str(name), str(movieID), str(department),str(gender)))
        
        except Exception as e: 
            pass

    def insertGenre(self, name, movieID):
        sql = '''
            insert into Genre (name, movieID)
            values (%s, %s)
            '''

        try:
            self.cHandler.execute(sql, (str(name), str(movieID)))
        except Exception as e: 
            pass
        
    def insertKeywords(self, name, movieID):
        sql = '''
            insert into Keywords (name, movieID)
            values (%s, %s)
            '''

        try:
            self.cHandler.execute(sql, (str(name), str(movieID)))
        except Exception as e: 
            pass

    def insertLanguage(self, name, movieID):
        sql = '''
            insert into Language (name, movieID)
            values (%s, %s)
            '''

        try:
            self.cHandler.execute(sql, (str(name), str(movieID)))
        except Exception as e: 
            pass

    def insertLinks(self, movieID, imdbID, tmdbID):
        sql = '''
            insert into Links (movieID,imdbID,tmdbID)
            values (%s, %s, %s)
            '''

        try:
            self.cHandler.execute(sql, (str(movieID), str(imdbID), str(tmdbID)))
        except Exception as e: 
            pass

    def insertProductionCountry(self, name, movieID):
        sql = '''
            insert into ProductionCountry (name, movieID)
            values (%s, %s)
            '''

        try:
            self.cHandler.execute(sql,(str(name), str(movieID)) )
        except Exception as e: 
            pass

    def insertProductionCompany(self, name, movieID):
        sql = '''
            insert into ProductionCompany (name, movieID)
            values (%s, %s)
            '''

        try:
            self.cHandler.execute(sql, (str(name), str(movieID)))
        except Exception as e: 
            pass

    def insertRatings(self, userID, movieID, rating ,timestamp):
        sql = '''
            insert into Ratings (userID, movieID, rating, timestamp)
            values (%s, %s, %s, %s)
            '''

        try:
            self.cHandler.execute(sql,  (str(userID), str(movieID), str(rating) ,str(timestamp)))
        except Exception as e: 
            pass

    def insertMovie(self, adult,belongs_to_collection, budget, homepage, id,original_title,overview, popularity, poster_path, release_date, revenue, runtime, status, tagline, title, video, vote_average, vote_count):
        sql = '''
            insert into Movie (adult,belongs_to_collection, budget, homepage, id,original_title,overview, popularity, poster_path, release_date, revenue, runtime, status, tagline, title, video, vote_average, vote_count)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

        try:
            self.cHandler.execute(sql, (str(adult),
            str(belongs_to_collection), 
            str(budget), 
            str(homepage), 
            str(id),
            str(original_title),
            str(overview), 
            str(popularity), 
            str(poster_path), 
            str(release_date), 
            str(revenue), 
            str(runtime), 
            str(status), 
            str(tagline), 
            str(title), 
            str(video), 
            str(vote_average), 
            str(vote_count)))
        except Exception as e: 
            pass

