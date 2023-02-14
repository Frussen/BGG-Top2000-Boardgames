# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class boardgame(scrapy.Item):

    idnumber = scrapy.Field()
    name = scrapy.Field()
    position = scrapy.Field()
    bayesaverage = scrapy.Field()
    average = scrapy.Field()
    usersrated = scrapy.Field()
    averageweight = scrapy.Field()
    numweights = scrapy.Field()
    owned = scrapy.Field()
    yearpublished = scrapy.Field()
    minplayers =  scrapy.Field()
    maxplayers = scrapy.Field()
    playingtime = scrapy.Field()
    age = scrapy.Field()
    boardgamedesigner = scrapy.Field()
    description = scrapy.Field()
    polltotalvotes = scrapy.Field()
    shortdescription = scrapy.Field()
    numberoftypes = scrapy.Field()
    numberofcategories = scrapy.Field()
    npossibleplayercount = scrapy.Field()

    pass



class boardgameType(scrapy.Item):

    idnumber = scrapy.Field()
    type = scrapy.Field()

    pass



class boardgameCategory(scrapy.Item):

    idnumber = scrapy.Field()
    category = scrapy.Field()

    pass



class playerCountVotes(scrapy.Item):

    idnumber = scrapy.Field()
    nump = scrapy.Field()
    best = scrapy.Field()
    recommended = scrapy.Field()
    notrecommended = scrapy.Field()
    result =  scrapy.Field()
    withpercentage = scrapy.Field()

    pass