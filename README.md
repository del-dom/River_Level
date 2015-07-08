# River_Level

This is a quick and dirty script I made to monitor the flood state of the Lansing Mi, river trail. I use the river trail daily
for commuting and was tired of not knowing if I needed to reroute due to flooding. So, this script scrapes data from 
the National Weather Service. It then parses the HTML, and checks if the rivers are at flood state anywhere along the trail.
If, they are flooded or partially flooded it sends myself and a few friends an e-mail telling us that it is flooded. I have set this up to run as a
scheduled task at 7am and 4pm.

I realize I should probably have employed OOP principles for the 3 rivers. But, I was doing this fast and programmatic was simple
to do. I may rework it to work with objects in the future.
