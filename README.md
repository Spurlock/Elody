# Elody

### What is this?

#### Elody is a tool for ranking your favorite albums.

It basically shows you a series of 1-vs-1 matches and asks you to pick which album you like better. It uses a variation of the [Elo rating system](https://en.wikipedia.org/wiki/Elo_rating_system) to assign scores to your albums based on how well they do against one another. Over time, you get a very solid and empirical list of how your albums stack up.

#### Elody is a personal project

In the sense that I don't expect anyone but me to ever want to use it. I made it because I like the idea of having a very trustworthy way of knowing where the various albums in my collection stand (which I can use to get better results from recommendation engines). But most people probably wouldn't want to put in the kind of time it takes to get good results out of Elody, and don't have such a ridiculous desire for precision anyway. 

Keeping in mind that this project was built to be used by me and me alone helps explain a lot of otherwise odd stuff about it.

### Using the app

#### How do I get data into Elody?

I use Elody in conjunction with [Rate Your Music](https://rateyourmusic.com/). RYM has functionality for exporting your data as a CSV file, and Elody can ingest that data to seed the database. From there, I use Django Admin to add in new artists and albums as my collection grows.

#### What do I do once I have the data in?

Start doing matches! Matches in the sense of chess matches, not match.com matches. It will take a few rounds of these before anything really starts to take shape. You can look at the index view to see the current leaderboard.

#### What's this "Consistency" thing?

It compares the ratings determined by Elody with the star ratings imported from RYM (or otherwise manually entered). The idea is that you might have an album you think of as "4 stars" that actually does about as well as a typical "3.5 stars" album. That album would have a big score in the "needs fewer stars" column, which is your cue to drop its star score a bit and thereby have more accurate data for recommendation engines.

### Technical Stuff

#### How are matches scored?

Using a variation of the Elo rating system, basically the same way chess players are ranked against one another. This algorithm has lots of nice properties, like that defeating a strong opponent gets you more points than defeating a weak opponent, and that the weight to assign to a particular match can vary through the K factor. Elody sets the K factor for each album equal to **40 - number_of_previous_matches**, with a minimum of 10. So albums move around less as time goes on.

#### How are albums paired up for matches?

First, Elody selects the album it has the least information about (or one of them, if it's a tie). Then it chooses a suitable opponent for that album. If Elody doesn't know much about the first album (it's had very few matches), it can pick just about anything as its opponent. The more Elody learns about the album (and thus, the more certain it can be about it's current score being accurate), the more it will start to prefer closely ranked opponents.

#### What about album art?

Automatically fetches it using Last.fm's API.

### Installation/Requirements

Elody was built on Python 2.7.5, Django 1.7.7, and MySQL. I recommend using Django Admin with it. The front end uses Bootstrap 3.2 and a little bit of jQuery just because I was feeling lazy.

Database config, Django's secret key, and the API key for Last.fm are stored in **environment.py**. You'll want to edit **environment_blank.py** and save it without the "_blank".

If you want to import data from RYM, you'll have to comment out a return statement over in **views.py** that I use to avoid accidentally nuking the database. Also you'll probably have to fix a typo in the headers row of the RYM export CSV (there's an extra space in one of the headers).

### What's next for Elody?

Probably nothing! I've been using it for months and I like it a lot. As I said above, it's a personal project. At this point, the single intended user is entirely satisfied with the product.
