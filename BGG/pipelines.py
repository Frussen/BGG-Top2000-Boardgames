# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from BGG.items import boardgame
from BGG.items import boardgameType
from BGG.items import boardgameCategory
from BGG.items import playerCountVotes

class BoardgamesPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'Berlin27ff!',
            database = 'BGGP'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
            
        ## Create Boardgames table if none exists
        self.cur.execute("""
        CREATE TABLE Boardgames(

            idnumber int,
            name varchar(100),
            position int,
            bayesaverage float,
            average float,
            usersrated int,
            averageweight float,
            numweights int,
            owned int,
            yearpublished int,
            minplayers int,
            maxplayers int,
            playingtime int,
            age int,
            boardgamedesigner varchar(100),
            description varchar(10000),
            polltotalvotes int,
            shortdescription varchar(100),
            numberoftypes int,
            numberofcategories int,
            npossibleplayercount int,

            PRIMARY KEY (idnumber)     
        )
        """)

        self.cur.execute("""
        CREATE TABLE Types(
            idnumber int,
            type varchar(100)
        )
        """)

        self.cur.execute("""
        CREATE TABLE Categories(
            idnumber int,
            category varchar(100)
        )
        """)

        self.cur.execute("""
        CREATE TABLE Numpvotes(
            idnumber int,
            nump varchar(100),
            best int,
            recommended int,
            notrecommended int,
            result varchar(100),
            withpercentage float
        )
        """)


    def process_item(self, item, spider):
        ## Define insert statement
        if isinstance(item, boardgame):
            self.cur.execute(""" insert into Boardgames (idnumber, name, position, bayesaverage, average, usersrated, averageweight, numweights, owned, yearpublished, minplayers, maxplayers, playingtime, age, boardgamedesigner, description, polltotalvotes, shortdescription, numberoftypes, numberofcategories, npossibleplayercount) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
                item['idnumber'],
                item['name'],
                item['position'],
                item['bayesaverage'],
                item['average'],
                item['usersrated'],
                item['averageweight'],
                item['numweights'],
                item['owned'],
                item['yearpublished'],
                item['minplayers'],
                item['maxplayers'],
                item['playingtime'],
                item['age'],
                item['boardgamedesigner'],
                item['description'],
                item['polltotalvotes'],
                item['shortdescription'],
                item['numberoftypes'],
                item['numberofcategories'],
                item['npossibleplayercount']
            ))


        if isinstance(item, boardgameType):
            self.cur.execute("insert into Types (idnumber, type) values (%s,%s)", (
                item['idnumber'],
                item['type']
            ))

        if isinstance(item, boardgameCategory):
            self.cur.execute("insert into Categories (idnumber, category) values (%s,%s)", (
                item['idnumber'],
                item['category']
            ))

        if isinstance(item, playerCountVotes):
            self.cur.execute("insert into Numpvotes (idnumber, nump, best, recommended, notrecommended, result, withpercentage) values (%s,%s,%s,%s,%s,%s,%s)", (
                item['idnumber'],
                item['nump'],
                item['best'],
                item['recommended'],
                item['notrecommended'],
                item['result'],
                item['withpercentage']
            ))


        ## Execute insert of data into database
        self.conn.commit()

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
