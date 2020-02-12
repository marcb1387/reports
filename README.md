# Field Research Report
Discord Python Report that will post Reseach for Pokemon Go. For use with MAD Scanner. 

DO NOT INSTALL ON SAME ENVIRONMENT AS SCANNER.

Will post all Pokemon encounters, Stardust over 1000 and Rare Items. 

Please edit the config.ini file

```
area = '38.95971  -77.10273, 38.95971  -76.92077, 38.84281 -76.91545, 38.84268 -77.08299,38.95971  -77.10273' 
Cordinates of geofence for research, first and last corrdinates must be the same

webhookurl = 'WEBHOOK URL'

user = 'Database username'

passwd = 'Database password'

database = 'Scanner Databse Name'

host = 'Database IP address'

author = 'Name that will appear in footer of embed, Research by __________'
```
Example Pokemon, Items and Stradust reports 

![Iteam_pokemon_example](https://i.imgur.com/oia6W60.png)

![Iteam_item_example](https://i.imgur.com/A3I8L47.png)

![Iteam_stardust_example](https://i.imgur.com/8t9UAMp.png)

# Rocket Report

Used to show where Team rocket leaders are located, Top Link to Counters guide for each leader as well.

Example report

![Iteam_rocket_example](https://i.imgur.com/uIH4JSV.png)

Requires the Python Modules below: 

https://pypi.org/project/discord-webhook/ 
pip install discord-webhook

https://pypi.org/project/mysql-connector-python/
pip install mysql-connector-python
