# Field Research/Team Rocket Leaders Report
Discord Report that will post Research and Rocket Leaders for Pokemon Go. For use with MAD Scanner. 

Discord support channel https://discord.gg/bbvqeBQ

**Optional Pokemon Filter**

Pokemon filters can be in an area.ini file or config.ini file. Takes 3 digit pokedex numbers to display only those pokemon. If left empty all pokemon encounters will be displayed. An area.ini file will surpass the config.ini file for any settings including a blank dex_number list. If this is not needed it can be commented out in the area.ini file for the config.ini values to be used.

**config.ini File Edits**

You can edit the config.ini file to pick which items you would want in your report with true/false statements. You can also adjust the stardust for research. Stardust amounts will show anything Greater then and equal to the amount you enter.

A Community Ad can be added to the end of the report see below for example. This will accept any text and Discord markdown for links/formatting for up to 2048 characters. If you do not wish to have an ad you can leave the ```Ad_Body``` blank and none will be added. This is effective in both Quest and Rocket leaders reports. If you have different Areas you can enter seprate Ad's for each area by entering the [AD] config into you area.ini file.

```
[CONFIG]
DiscordQ=WEBHOOK_URL_FIELD_RESEARCH
DiscordR=WEBHOOK_URL_ROCKET_LEADERS
Author=POSTING_AUTHOR_NAME (optional Research BY:_______ footer) leave empty for no footer
AuthorIMG=https://i.imgur.com/DDZEOj7.png Temporary URL for Icon can be changed  
Areaname=NAME_OF_TEMP_AREA_FILE (can be anything but i would suggest the name of the area)

#Emojis and formatting of the post
use_emoji=true
use_slim_name=false
use_webhook_name=false

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
mega_energy=true
ar_task=true
stardust=1000
encounters=true

[POKEMON]
dex_number= (delete this text if you want all pokemon) accepts 3 digit Pokedex numbers in any order seprated by a comma. example 001,025,125

[AD]
Ad_Title = Pokemon Master
Ad_Body = These Quests Brought to you by the Pomemon Masters [Please donate to get cool stuff](http://example.com)
Ad_Thumbnail = https://i.imgur.com/DDZEOj7.png Temporary URL for thumbnail can be removed 
```
**Formatting Examples**

First image - Emoji and all option turned off

Second image - emoji turned on

Third image - emoji and webhook name turned on

Fourth image - emoji and slim name turned on

Webhook name will override slim name if turned on

![Format_example](https://i.imgur.com/wCnA3BC.png)



**Optional Arguments:**

Running without any arguments will run the report with static images and no file/stops checks using the config.ini file information.

-c, --check will check the area for the amount of pokestops vs amount of research tasks before posting and perform a filecheck to see if a report has already ran today. CRON use for running every X amount of minutes to autopost after all stops have scanned for research. Do not use with -s.

-a, --area allows to pass optional area, webhook, areanames or author. If this is not used the config.ini defaults will be used.

-g, --gif will load Animated Gif Sprites for pokemon vs the standard images.

-s, --safe Will perform a file check only to see if a report has already ran today. CRON Use as a fail safe run at a specific time if some stops haven’t reported research. Do no use with -c.

**Example Pokemon, Items, Stradust reports, and Community Ad:**

![Iteam_pokemon_example](https://i.imgur.com/oia6W60.png)

![Iteam_item_example](https://i.imgur.com/A3I8L47.png)

![Iteam_stardust_example](https://i.imgur.com/8t9UAMp.png)

![Community Ad_example](https://i.imgur.com/xZnJk6h.png)

# Rocket Report

Used to show where Team rocket leaders are located, Top Link to Counters guide for each leader as well.

**Optional Arguments:**

Running without any arguments will run the report with static images and no file/stops checks using the config.ini file information.

-a, --area allows to pass optional area, webhook, or author. If this is not used the config.ini defaults will be used.

**Example report**

![Iteam_rocket_example](https://i.imgur.com/uIH4JSV.png)

**Requires the Python Modules below:**

https://pypi.org/project/discord-webhook/ 
pip3 install discord-webhook

https://pypi.org/project/mysql-connector-python/
pip3 install mysql-connector-python

https://pypi.org/project/beautifulsoup4/
pip3 install beautifulsoup4 

**If you appreciate this tool please consider buying me a Coffee/Beer/Pizza :D**

<a href="https://www.buymeacoffee.com/harambe1387" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" ></a>
