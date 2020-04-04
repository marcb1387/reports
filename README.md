# Field Research Report
Discord Python Report that will post Research for Pokemon Go. For use with MAD Scanner. 

DO NOT INSTALL ON SAME ENVIRONMENT AS SCANNER.


**Optional Pokemon Filter**

Pokemon filters can be in an area.ini file or config.ini file. Takes 3 digit pokedex numbers to display only those pokemon. If left empty all pokemon encounters will be displayed. An area.ini file will surpass the config.ini file for any settings including a blank dex_number list. If this is not needed it can be commented out in the area.ini file for the config.ini values to be used.

**config.ini File Edits**

You can edit the config.ini file to pick which items you would want in your report with true/false statements. You can also adjust the stardust for research. Stardust amounts will show anything Greater then and equal to the amount you enter. 

```
[CONFIG]
DiscordQ=WEBHOOK_URL_FIELD_RESEARCH
DiscordR=WEBHOOK_URL_ROCKET_LEADERS
Author=POSTING_AUTHOR_NAME
AuthorIMG=https://i.imgur.com/DDZEOj7.png Temporary URL for Icon can be changed  
Areaname=NAME_OF_TEMP_AREA_FILE (can be anything but i would suggest the name of the area)

#Coordinates string of area. First and last coordinate set must be equal/the same one. Format:Latitute and longitude separated by spaces and coordinate pairs separated by , symbol
Area = COORDINATES_OF_AREA 38.95971  -77.10273, 38.95971  -76.92077, 38.84281 -76.91545, 38.84268 -77.08299,38.95971  -77.10273

[DATABASE]
MAD_db_host=HOST_ADRESS_HERE
db_name=DB_NAME_HERE
db_user=DB_USER_HERE
db_pass=DB_PASS_HERE
port=3306 (default but it can be changed)

[ITEMS]
poke_ball=false
great_ball=false
ultra_ball=false
potion=false
super_potion=false
hyper_potion=false
max_potion=true
revive=false
max_revive=true
razz_berry=false
golden_razz_berry=true
pinap_berry=false
silver_pinap_berry=true
nanab_berry=false
dragon_scale=true
kings_rock=true
metal_coat=true
sun_stone=true
up_grade=true
shinnoh_stone=true
unova_stone=true
fast_tm=true
charged_tm=true
rare_candy=true
glacial_lure=true
mossy_lure=true
magnetic_lure=true
stardust=1000
encounters=true

[POKEMON]
dex_number= (delete this text if you want all pokemon) accepts 3 digit Pokedex numbers in any order seprated by a comma. example 001,025,125
```

**Optional Arguments:**

Running without any arguments will run the report with static images and no file/stops checks using the config.ini file information.

-c, --check will check the area for the amount of pokestops vs amount of research tasks before posting and perform a filecheck to see if a report has already ran today. CRON use for running every X amount of minutes to autopost after all stops have scanned for research. Do not use with -s.

-a, --area allows to pass optional area, webhook, areanames or author. If this is not used the config.ini defaults will be used.

-g, --gif will load Animated Gif Sprites for pokemon vs the standard images.

-s, --safe Will perform a file check only to see if a report has already ran today. CRON Use as a fail safe run at a specific time if some stops haven’t reported research. Do no use with -c.

**Example Pokemon, Items and Stradust reports:**

![Iteam_pokemon_example](https://i.imgur.com/oia6W60.png)

![Iteam_item_example](https://i.imgur.com/A3I8L47.png)

![Iteam_stardust_example](https://i.imgur.com/8t9UAMp.png)

# Rocket Report

Used to show where Team rocket leaders are located, Top Link to Counters guide for each leader as well.

**Optional Arguments:**

Running without any arguments will run the report with static images and no file/stops checks using the config.ini file information.

-a, --area allows to pass optional area, webhook, or author. If this is not used the config.ini defaults will be used.

**Example report**

![Iteam_rocket_example](https://i.imgur.com/uIH4JSV.png)

**Requires the Python Modules below:**

https://pypi.org/project/discord-webhook/ 
pip install discord-webhook

https://pypi.org/project/mysql-connector-python/
pip install mysql-connector-python
