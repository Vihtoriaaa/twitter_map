## Twitter Map

Twitter_map is an app for generating a map with locations of 50 user's friends.

## Main files

This project contains one module:
- twitter_map.py - its goal is to create map with 50 Twitter friends of the user

## How does it work?

When a user runs the programm, he/she gets a local server ip, and after
clicking on it the browser page opens. Then the user has an opportunity to
enter a Twitter-user's screen name to get followers map. Also bearer token must
be entered too (it is used to get friends list from Twitter). Then after a few
minutes an HTML map generates and the user can open and see it.

This is how the main page looks like. Here the user can input the screen name
of Twitter account he/she wants to get a map of friends of.
![text](menu.png?raw=true "text")

## Result
User gets an HTML map with locations of needed user's 50 Twitter friends
This is a result for screen_name @Cristiano and my bearer token

This is how it looks like with Open street map tile
![text](openstreetmap.png?raw=true "text")
Now with CartoDB Dark Matter tile
![text](cartodbdark_mattermap.png?raw=true "text")
And final with Stamen Toner tile
![text](stamentonermap.png?raw=true "text")