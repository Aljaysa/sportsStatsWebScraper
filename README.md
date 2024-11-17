# sportsStatsWebScraper
Scrapes stats from sports websites, uploads them to a database and then produces visualizations off of the data. Visualizations are sent from a web server to a client web browser and then displayed.

This project contains the following parts:
Baseball Stats Web Scraper (Python & SQL)
•	Used Beautiful Soup 4.4 Python library to compile data from baseball-reference.com and upload it to a database file using SQL
•	Used proper programming practices referenced in the book Code Complete such as classes performing one purpose only, classes having no more dependencies than needed, creating methods that are scalable and have parameters that change based on predictable variations in the baseball-reference.com URLs rather than relying on hard-coded values
 
Website Displaying Baseball Stats Visualizations (HTML & CSS) 
•	Used HTML and CSS to create an interactive website where specific stat parameters can be specified before the corresponding graph (generated with Matplotlib) is displayed  
•	Used both Flexbox and Grid display methods in CSS

Client to Server Data Transfer (JavaScript & Python) 
•	Used Python Flask to create a web server as well as the Fetch API to fetch from the web server the graph visualizations, the HTML and CSS files into the client’s JavaScript file



To Run the project:
1. Run webServer.py which can be found in the root directory of the project. This starts up the web server
2. search http://localhost:8000 in browser in order to request from the web server the HTML file to then show the website to the client
