
BoardGameGeek Top2000 Boardgames Analysis
________________________________________________________________________


Purpose

The goal of this project was to be able to properly analyze all the relevant metrics of the best boargames found on BoardGameGeek.com to see what games would better fit the condition of a specific gaming night, where number of players and preference about the theme and the weight of the game are often already determined.


Strategy

The mentioned goal was achieved with the creation of a table in the "Useful" worksheet of the FinalGamesAnalysis.xlsx workbook, where through filtering and sorting, one can easily create a list of games that satisfy the required conditions.
In the workbook a bounch of other calculation are performed in various sheet, leading to other interesting insight of the 02/2023 boardgaming scene.


Tools and implementation

The data about the Top2000 boardgames in the said table comes from the BoardGameGeek.com rankings, and was collected through the use of both the python web-scraping framework Scrapy and the BoardGameGeek XML API.
Scrapy allowed to crawl and parse the ranking pages with a Spider, collecting the IDnumber information that would than be necessary to request the game stats through the XML API.

The request to this API was nontheless a Scrapy Request, and the response was queried with css and xpaths selectors, retrieving the needed informations and storing them in various instances of defined Items, one of each type for each boardgame. The prevision of multiple type of Items was necessary as the boargames presented different numbers of data entries from each other (e.g. the community votes for the playability at any player count), so that a relational database with multiple tables was needed for the storage (in this example each Item would represent a single "numpvotes" table row, in which the votes relative to a specific game and a specific player count would be stored, having as a result multiple rows per game).

The scraping process ended with the creation of a Pipeline system that allowed to store the Items in the right one of four tables (boardgames, numpvotes, types and categories) in a MySQL locally hosted database.

Finally, the database was imported to Excel through the use of the ODBC interface. The data from the different tables was then convieniently unified using the VLOOKUP excel function.


________________________________________________________________________


Hope everything was clear, don't esitate to contact me at francesco.frusone@gmail.com for more information or even just to talk about the challenges and solutions found building this project.

Have an excellent rest of your day, Francesco.