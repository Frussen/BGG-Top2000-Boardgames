import scrapy
from BGG.items import boardgame
from BGG.items import boardgameType
from BGG.items import boardgameCategory
from BGG.items import playerCountVotes


topLinks = []
i = 1

class RankSpider(scrapy.Spider):
    name = "ranks"

    def start_requests(self):
        url = 'https://boardgamegeek.com/browse/boardgame'
        yield scrapy.Request(url, callback=self.parseRanks)  
        #url = 'https://boardgamegeek.com/browse/boardgame/page/20'
        #yield scrapy.Request(url, callback=self.pRanks)


    def pRanks(self, response):
    
        with open('G.html', "w", encoding="utf-8") as f:
            f.write(
                f'{response.text}'
            )



    def parseRanks(self, response):

        for row in response.css('tr#row_'):

            #take links to the bgg page of games that are in rank from their thumbnail
            link = row.css('td.collection_thumbnail a::attr(href)').get()   #e.g. /boardgame/174430/gloomhaven

            topLinks.append(link)

        next = response.xpath('//a[@title="next page"]/@href').get()
        next_rankspage = response.urljoin(next)

        global i
        if(i<20):
            yield scrapy.Request(url=next_rankspage, callback=self.parseRanks)
            i+=1
            
        else:

            for link_end in topLinks:

                game_page = response.urljoin(link_end)
                id_number = link_end.split("/")[2]
                game_xml = 'https://api.geekdo.com/xmlapi/boardgame/' + id_number + '?&stats=1'
                yield scrapy.Request(game_page, callback=self.parse_gamepage, meta={'gamexml':game_xml})




    def parse_gamepage(self, response):

        gamexml = response.meta['gamexml']
        description = response.xpath("//meta[@name='description']/@content").get()
        if(len(description)>100):
            description = 'No short description, only long one'
        
        yield scrapy.Request(gamexml, callback=self.parse_xml, meta={'shortdescription':description})
        



    def parse_xml (self, response):

        idnumber = response.url.split("/")[-1].split("?")[0]


        typeitem = boardgameType()
        gametypes = response.css('boardgamesubdomain::text').getall()
        ntypes = len(gametypes)

        for type in gametypes:
            typeitem['idnumber'] = idnumber
            typeitem['type'] = type
            yield typeitem



        categoryitem = boardgameCategory()
        gamecategories = response.css('boardgamecategory::text').getall()
        ncategories = len(gamecategories)

        for category in gamecategories:
            categoryitem['idnumber'] = idnumber
            categoryitem['category'] = category
            yield categoryitem



        numpvotesitem = playerCountVotes()
        allpossiblenump = response.css('results::attr(numplayers)').getall()
        numpoptions = len(allpossiblenump)
        results = ['best', 'recommended', 'not recommended']

        for nump in allpossiblenump:
            strvotes = response.css(f'results[numplayers="{nump}"] result::attr(numvotes)').getall()
            votes = []
            for n in strvotes:
                votes.append(int(n))
            mostvotes = max(votes)
            totalvotes = sum(votes)
            indexmax = votes.index(mostvotes)
            if(totalvotes):
                percentage = mostvotes / totalvotes
            else:
                percentage = 0

            numpvotesitem['idnumber'] = idnumber
            numpvotesitem['nump'] = nump
            numpvotesitem['best'] = votes[0]
            numpvotesitem['recommended'] = votes[1]
            numpvotesitem['notrecommended'] = votes[2]
            numpvotesitem['result'] = results[indexmax]
            numpvotesitem['withpercentage'] = percentage

            yield numpvotesitem
          


        item = boardgame()
        item['idnumber'] = idnumber
        item['name'] = response.css('name[primary=true]::text').get()
        item['position'] = response.xpath('//rank[@name="boardgame"]/@value').get()
        item['bayesaverage'] = response.xpath('//bayesaverage/text()').get()
        item['average'] = response.xpath('//average/text()').get()
        item['usersrated'] = response.xpath('//usersrated/text()').get()
        item['averageweight'] = response.xpath('//averageweight/text()').get()
        item['numweights'] = response.xpath('//numweights/text()').get()
        item['owned'] = response.xpath('//owned/text()').get()
        item['yearpublished'] = response.css('yearpublished::text').get()
        item['minplayers'] =  response.css('minplayers::text').get()
        item['maxplayers'] = response.css('maxplayers::text').get()
        item['playingtime'] = response.css('playingtime::text').get()
        item['age'] = response.css('age::text').get()
        item['boardgamedesigner'] = response.css('boardgamedesigner::text').get()
        description = response.css('description::text').get()
        item['description'] = description[0:9998]
        item['polltotalvotes'] = response.xpath("//poll[@name='suggested_numplayers']/@totalvotes").get()
        item['shortdescription'] = response.meta['shortdescription']
        item['numberoftypes'] = ntypes
        item['numberofcategories'] = ncategories
        item['npossibleplayercount'] = numpoptions

        yield item




