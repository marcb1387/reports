# Field Research Report
Discord Python Report that will post Reseach for Pokemon Go. For use with MAD Scanner. 

DO NOT INSTALL ON SAME ENVIRONMENT AS SCANNER.

Will post all Pokemon encounters, Stardust over 1000 and Rare Items. 

Please edit the config.ini file

```
[CONFIG]
DiscordURL=URL_STRING_HERE
Author=POSTING_AUTHOR_NAME
Areaname=NAME_OF_TEMP_AREA_FILE

#Coordinates string of area. First and last coordinate set must be equal. Format:Latitute and longitude separated by spaces and coordinate pairs separated by , symbol
Area = COORDINATES_OF_AREA 38.95971  -77.10273, 38.95971  -76.92077, 38.84281 -76.91545, 38.84268 -77.08299,38.95971  -77.10273

[DATABASE]
MAD_db_host=HOST_ADRESS_HERE
db_name=DB_NAME_HERE
db_user=DB_USER_HERE
db_pass=DB_PASS_HERE
```

**Optional Arguments:**

Running without any arguments will run the report with static images and no file/stops checks using the config.ini file information.

-c, --check will check the area for the amount of pokestops vs amount of research tasks before posting and perform a filecheck to see if a report has already ran today. CRON use for running every X amount of minutes to autopost after all stops have scanned for research. Do not use with -s.

-a, --area allows to pass optional area, webhook, areanames or author. If this is not used the config.ini defults will be used.

-g, --gif will load Animated Gif Sprites for pokemon vs the standard images.

-s, --safe Will perform a file check only to see if a report has already ran today. CRON Use as a fail safe run at a specific time if some stops havent reported research. Do no use with -c.

**Example Pokemon, Items and Stradust reports:**

![Iteam_pokemon_example](https://i.imgur.com/oia6W60.png)

![Iteam_item_example](https://i.imgur.com/A3I8L47.png)

![Iteam_stardust_example](https://i.imgur.com/8t9UAMp.png)

# Rocket Report

Used to show where Team rocket leaders are located, Top Link to Counters guide for each leader as well.

**Example report**

![Iteam_rocket_example](https://i.imgur.com/uIH4JSV.png)

Requires the Python Modules below: 

https://pypi.org/project/discord-webhook/ 
pip install discord-webhook

https://pypi.org/project/mysql-connector-python/
pip install mysql-connector-python
