from discord_webhook import DiscordWebhook, DiscordEmbed
import mysql.connector as mariadb
import time
import datetime
import os
from os import path
import configparser
import argparse
import csv
import operator

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--area",default="config.ini", help="Area config file to use")
parser.add_argument("-c", "--check",action="store_true", help="Check to make sure amount of stops and task is the same before posting")
parser.add_argument("-g", "--gif",action="store_true", help="Use Animated Gif Pokemon Sprites")
parser.add_argument("-s", "--safe",action="store_true", help="Dose no stop vs task check only a file check as a filesafe run")
args = parser.parse_args()
areafile = args.area


# CONFIG
config = configparser.ConfigParser()
config.read(['config.ini',areafile])
webhookurl = config.get('CONFIG', 'DiscordQ')
area = config.get('CONFIG', 'Area')
areaname = config.get('CONFIG', 'Areaname')
author = config.get('CONFIG', 'Author')
footerimg = config.get ('CONFIG', 'AuthorIMG')
host = config.get('DATABASE', 'MAD_db_host')
database = config.get('DATABASE', 'db_name')
port = config.get('DATABASE', 'port')
user = config.get('DATABASE', 'db_user')
passwd = config.get('DATABASE', 'db_pass')
poke_ball = config.getboolean('ITEMS','poke_ball')
great_ball = config.getboolean('ITEMS','great_ball')
ultra_ball = config.getboolean('ITEMS','ultra_ball')
potion = config.getboolean('ITEMS','potion')
super_potion = config.getboolean('ITEMS','super_potion')
hyper_potion = config.getboolean('ITEMS','hyper_potion')
max_potion = config.getboolean('ITEMS','max_potion')
revive = config.getboolean('ITEMS','revive')
max_revive = config.getboolean('ITEMS','max_revive')
razz_berry = config.getboolean('ITEMS','razz_berry')
golden_razz_berry = config.getboolean('ITEMS','golden_razz_berry')
pinap_berry = config.getboolean('ITEMS','pinap_berry')
silver_pinap_berry = config.getboolean('ITEMS','silver_pinap_berry')
nanab_berry = config.getboolean('ITEMS','nanab_berry')
dragon_scale = config.getboolean('ITEMS','dragon_scale')
kings_rock = config.getboolean('ITEMS','kings_rock')
metal_coat = config.getboolean('ITEMS','metal_coat')
sun_stone = config.getboolean('ITEMS','sun_stone')
up_grade = config.getboolean('ITEMS','up_grade')
shinnoh_stone = config.getboolean('ITEMS','shinnoh_stone')
unova_stone = config.getboolean('ITEMS','unova_stone')
fast_tm = config.getboolean('ITEMS','fast_tm')
charged_tm = config.getboolean('ITEMS','charged_tm')
rare_candy = config.getboolean('ITEMS','rare_candy')
glacial_lure = config.getboolean('ITEMS','glacial_lure')
mossy_lure = config.getboolean('ITEMS','mossy_lure')
magnetic_lure = config.getboolean('ITEMS','magnetic_lure')
stardust = config.get('ITEMS','stardust')
encounters = config.getboolean('ITEMS','encounters')
mons = config.get('POKEMON','dex_number')
# CONFIG END

# SPRITES
if args.gif:
 img = 'https://raw.githubusercontent.com/marcb1387/assets/master/pokemon_icon_' #animated
 ext = '.gif' #animated
else:
 img = 'https://raw.githubusercontent.com/whitewillem/PogoAssets/resized/no_border/pokemon_icon_' # Static
 ext = '.png' #Static
 
#Pokemon
def quest_mon(monid,mon,shiny,typeid,formid):
 mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host, port=port)
 cursor = mariadb_connection.cursor()
 query = ("select CONVERT(pokestop.name USING UTF8MB4) as pokestopname,pokestop.latitude,pokestop.longitude,quest_task from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where quest_pokemon_id ="+monid+" and quest_pokemon_form_id ="+typeid+" and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
 cursor.execute(query)
 name = cursor.fetchall()
 res =[tuple(str(ele) for ele in sub) for sub in name]
 
 task3 =[]
 for task in res:
  task3 += [task[3]]
 result = all(elem == task3[0] for elem in task3)
 if result:
     if mons:
      for dex in mons.split(','):
       if dex == monid:
         mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host, port=port)
         cursor = mariadb_connection.cursor()
         query = ("select CONVERT(pokestop.name USING UTF8MB4) as pokestopname,pokestop.latitude,pokestop.longitude,quest_task from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where quest_pokemon_id ="+monid+" and quest_pokemon_form_id ="+typeid+" and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
         cursor.execute(query)
         name = cursor.fetchall()
         
         if not name:
          print ("no quests for "+mon)
         else:
          print ("Research Task Is The Same "+mon)
          #convert data into string
          res =[tuple(str(ele) for ele in sub) for sub in name]
          res.sort()
          webhook = DiscordWebhook(url=webhookurl)
          # create embed object for webhook 
          research = ''
          for stop in res: 
           research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+'\n')
           if len(research)> 1900:
            print ("larger then 2048 breaking up")
            print (mon+" Length:", len(research))
            embed = DiscordEmbed(title= shiny+mon+' Field Research'+shiny, description=research, color=16777011)
            embed.set_thumbnail(url=img+monid+'_'+formid+ext)
            embed.set_footer(text='Research by '+author, icon_url=footerimg)
            embed.set_author(name='Research Task: '+stop[3])
            #add embed object to webhook
            webhook.add_embed(embed)
            webhook.execute()
            research = ''
            webhook.remove_embed(0)
            time.sleep(2)
          
          print (mon+" Length:", len(research))
          embed = DiscordEmbed(title= shiny+mon+' Field Research'+shiny, description=research, color=16777011)
          embed.set_thumbnail(url=img+monid+'_'+formid+ext)
          embed.set_footer(text='Research by '+author, icon_url=footerimg)
          embed.set_author(name='Research Task: '+stop[3])
          #add embed object to webhook
          webhook.add_embed(embed)
          webhook.execute()
          research = ''
          time.sleep(2)
     else:
         mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host, port=port)
         cursor = mariadb_connection.cursor()
         query = ("select CONVERT(pokestop.name USING UTF8MB4) as pokestopname,pokestop.latitude,pokestop.longitude,quest_task from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where quest_pokemon_id ="+monid+" and quest_pokemon_form_id ="+typeid+" and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
         cursor.execute(query)
         name = cursor.fetchall()
         
         if not name:
          print ("no quests for "+mon)
         else:
          print ("Research Task Is The Same "+mon)
          #convert data into string
          res =[tuple(str(ele) for ele in sub) for sub in name]
          res.sort()
          webhook = DiscordWebhook(url=webhookurl)
          # create embed object for webhook 
          research = ''
          for stop in res: 
           research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+'\n')
           if len(research)> 1900:
            print ("larger then 2048 breaking up")
            print (mon+" Length:", len(research))
            embed = DiscordEmbed(title= shiny+mon+' Field Research'+shiny, description=research, color=16777011)
            embed.set_thumbnail(url=img+monid+'_'+formid+ext)
            embed.set_footer(text='Research by '+author, icon_url=footerimg)
            embed.set_author(name='Research Task: '+stop[3])
            #add embed object to webhook
            webhook.add_embed(embed)
            webhook.execute()
            research = ''
            webhook.remove_embed(0)
            time.sleep(2)
          
          print (mon+" Length:", len(research))
          embed = DiscordEmbed(title= shiny+mon+' Field Research'+shiny, description=research, color=16777011)
          embed.set_thumbnail(url=img+monid+'_'+formid+ext)
          embed.set_footer(text='Research by '+author, icon_url=footerimg)
          embed.set_author(name='Research Task: '+stop[3])
          #add embed object to webhook
          webhook.add_embed(embed)
          webhook.execute()
          research = ''
          time.sleep(2)
 else:
     if mons:
      for dex in mons.split(','):
       if dex == monid:
         mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host, port=port)
         cursor = mariadb_connection.cursor()
         query = ("select CONVERT(pokestop.name USING UTF8MB4) as pokestopname,pokestop.latitude,pokestop.longitude,quest_task from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where quest_pokemon_id ="+monid+" and quest_pokemon_form_id ="+typeid+" and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
         cursor.execute(query)
         name = cursor.fetchall()
         
         if not name:
          print ("no quests for "+mon)
         else:
          print ("Research Task Is The Different "+mon)
          #convert data into string
          name.sort(key = operator.itemgetter(3, 0))
          res =[tuple(str(ele) for ele in sub) for sub in name]
          webhook = DiscordWebhook(url=webhookurl)
          # create embed object for webhook 
          research = ''
          for stop in res: 
           research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+' '+stop[3]+'\n')
           if len(research)> 1900:
            print ("larger then 2048 breaking up")
            print (mon+" Length:", len(research))
            embed = DiscordEmbed(title= shiny+mon+' Field Research'+shiny, description=research, color=16777011)
            embed.set_thumbnail(url=img+monid+'_'+formid+ext)
            embed.set_footer(text='Research by '+author, icon_url=footerimg)
            #add embed object to webhook
            webhook.add_embed(embed)
            webhook.execute()
            research = ''
            webhook.remove_embed(0)
            time.sleep(2)
          
          print (mon+" Length:", len(research))
          embed = DiscordEmbed(title= shiny+mon+' Field Research'+shiny, description=research, color=16777011)
          embed.set_thumbnail(url=img+monid+'_'+formid+ext)
          embed.set_footer(text='Research by '+author, icon_url=footerimg)
          #add embed object to webhook
          webhook.add_embed(embed)
          webhook.execute()
          research = ''
          time.sleep(2)
     else:
         mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host, port=port)
         cursor = mariadb_connection.cursor()
         query = ("select CONVERT(pokestop.name USING UTF8MB4) as pokestopname,pokestop.latitude,pokestop.longitude,quest_task from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where quest_pokemon_id ="+monid+" and quest_pokemon_form_id ="+typeid+" and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
         cursor.execute(query)
         name = cursor.fetchall()
         
         if not name:
          print ("no quests for "+mon)
         else:
          print ("Research Task Is The Different "+mon)
          #convert data into string
          name.sort(key = operator.itemgetter(3, 0))
          res =[tuple(str(ele) for ele in sub) for sub in name]
          webhook = DiscordWebhook(url=webhookurl)
          # create embed object for webhook 
          research = ''
          for stop in res: 
           research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+' '+stop[3]+'\n')
           if len(research)> 1900:
            print ("larger then 2048 breaking up")
            print (mon+" Length:", len(research))
            embed = DiscordEmbed(title= shiny+mon+' Field Research'+shiny, description=research, color=16777011)
            embed.set_thumbnail(url=img+monid+'_'+formid+ext)
            embed.set_footer(text='Research by '+author, icon_url=footerimg)
            #add embed object to webhook
            webhook.add_embed(embed)
            webhook.execute()
            research = ''
            webhook.remove_embed(0)
            time.sleep(2)
          
          print (mon+" Length:", len(research))
          embed = DiscordEmbed(title= shiny+mon+' Field Research'+shiny, description=research, color=16777011)
          embed.set_thumbnail(url=img+monid+'_'+formid+ext)
          embed.set_footer(text='Research by '+author, icon_url=footerimg)
          #add embed object to webhook
          webhook.add_embed(embed)
          webhook.execute()
          research = ''
          time.sleep(2)   
#Items
def quest_item(itemid,item,sprite):
 mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host,port=port)
 cursor = mariadb_connection.cursor()
 query = ("select CONVERT(pokestop.name USING UTF8MB4) as pokestopname,pokestop.latitude,pokestop.longitude,trs_quest.quest_task,trs_quest.quest_item_amount from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where quest_item_id = "+itemid+" and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
 cursor.execute(query)
 name = cursor.fetchall()
 
 if not name:
  print ("no quests for "+item)
 else:
  #convert data into string
  res =[tuple(str(ele) for ele in sub) for sub in name]
  
  res.sort()
  webhook = DiscordWebhook(url=webhookurl)
  # create embed object for webhook
  research = ''
  task3 =[]
  for task in res:
   task3 += [task[3]]
  result = all(elem == task3[0] for elem in task3)
  if result:
      print ("Research Task Is The Same "+item)
      for stop in res: 
       research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+'\n')
       if len(research)> 1900:
        print ("larger then 2048 breaking up")
        print (item+" Length:", len(research))
        embed = DiscordEmbed(title= item+' Field Research', description=research, color=4390656)
        embed.set_author(name='Research Task: '+stop[3])
        embed.set_footer(text='Research by '+author, icon_url=footerimg)
        embed.set_thumbnail(url=sprite) 
        #add embed object to webhook
        webhook.add_embed(embed)
        webhook.execute()
        research = ''
        webhook.remove_embed(0)
        time.sleep(2)
      print (item+" Length:", len(research))
      embed = DiscordEmbed(title= item+' Field Research', description=research, color=4390656)
      embed.set_author(name='Research Task: '+stop[3])
      embed.set_footer(text='Research by '+author, icon_url=footerimg)
      embed.set_thumbnail(url=sprite) 
      #add embed object to webhook
      webhook.add_embed(embed)
      webhook.execute()
      research = ''
      time.sleep(2)
  else:
      print ("Research Task Is Different "+item)
      for stop in res: 
       research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+' '+stop[3]+' - Amount: '+stop[4]+'\n')
       if len(research)> 1900:
        print ("larger then 2048 breaking up")
        print (item+" Length:", len(research))
        embed = DiscordEmbed(title= item+' Field Research', description=research, color=4390656)
        embed.set_footer(text='Research by '+author, icon_url=footerimg)
        embed.set_thumbnail(url=sprite) 
        #add embed object to webhook
        webhook.add_embed(embed)
        webhook.execute()
        research = ''
        webhook.remove_embed(0)
        time.sleep(2)
      print (item+" Length:", len(research))
      embed = DiscordEmbed(title= item+' Field Research', description=research, color=4390656)
      embed.set_footer(text='Research by '+author, icon_url=footerimg)
      embed.set_thumbnail(url=sprite) 
      #add embed object to webhook
      webhook.add_embed(embed)
      webhook.execute()
      research = ''
      time.sleep(2)

#Stardust
def quest_stardust(itemid,item,sprite):
 mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host, port=port)
 cursor = mariadb_connection.cursor()
 samount = (int(stardust) - 1)
 query = ("select CONVERT(pokestop.name USING UTF8MB4) as pokestopname,pokestop.latitude,pokestop.longitude,trs_quest.quest_task,if(trs_quest.quest_stardust>"+str(samount)+",trs_quest.quest_stardust, null) from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where quest_pokemon_id = "+itemid+" and DATE(FROM_UNIXTIME(trs_quest.quest_timestamp)) = CURDATE() and if(trs_quest.quest_stardust>"+str(samount)+",trs_quest.quest_stardust, null) is not null and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
 cursor.execute(query)
 name = cursor.fetchall()
 
 if not name:
  print ("no quests for "+item)
 else:
  #convert data into string
  name.sort(key = operator.itemgetter(4,3,0))
  res =[tuple(str(ele) for ele in sub) for sub in name]
  webhook = DiscordWebhook(url=webhookurl)
  # create embed object for webhook 
  research = ''
  for stop in res: 
   research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+' '+stop[3]+' - Amount: '+stop[4]+'\n') 
   if len(research)> 1850:
    print ("larger then 2048 breaking up")
    print (item+" Length:", len(research))
    embed = DiscordEmbed(title= item+' Field Research', description=research, color=16711931)
    embed.set_footer(text='Research by '+author, icon_url=footerimg)
    embed.set_thumbnail(url=sprite) 
    #add embed object to webhook
    webhook.add_embed(embed)
    webhook.execute()
    research = ''
    webhook.remove_embed(0)
    time.sleep(2)
  print (item+" Length:", len(research))
  embed = DiscordEmbed(title= item+' Field Research', description=research, color=16711931)
  embed.set_footer(text='Research by '+author, icon_url=footerimg)
  embed.set_thumbnail(url=sprite) 
  #add embed object to webhook
  webhook.add_embed(embed)
  webhook.execute()
  research = ''
  time.sleep(2)

#Pokeomon, Items, Stardust
def stuff():
    if encounters:
        quest_mon('001', 'Bulbasaur', ':sparkles:', '0', '00')
        quest_mon('004', 'Charmander', ':sparkles:', '0', '00')
        quest_mon('007', 'Squirtle', ':sparkles:', '0', '00')
        quest_mon('009', 'Blastoise', ':sparkles:', '0', '00')
        quest_mon('016', 'Pidgey', ':sparkles:', '0', '00')
        quest_mon('025', 'Pikachu', ':sparkles:', '598', '00')
        quest_mon('027', 'Sandshrew', ':sparkles:', '0', '00')
        quest_mon('029', 'Nidoran', ':sparkles:', '0', '00')
        quest_mon('030', 'Nidorina', ':sparkles:', '0', '00')
        quest_mon('031', 'Nidoqueen', ':sparkles:', '0', '00')
        quest_mon('032', 'Nidoran', ':sparkles:', '0', '00')
        quest_mon('033', 'Nidorino', ':sparkles:', '0', '00')
        quest_mon('034', 'Nidoking', ':sparkles:', '0', '00')
        quest_mon('035', 'Clefairy', '', '0', '00')
        quest_mon('037', 'Vulpix', '', '0', '00')
        quest_mon('037', 'Alolan Vulpix', ':sparkles:', '56', '56')
        quest_mon('039', 'Jigglypuff', '', '0', '00')
        quest_mon('041', 'Zubat', ':sparkles:', '157', '00')
        quest_mon('044', 'Gloom', '', '0', '00')
        quest_mon('050', 'Diglett', ':sparkles:', '0', '00')
        quest_mon('052', 'Alolan Meowth', ':sparkles:', '64', '64')
        quest_mon('056', 'Mankey', ':sparkles:', '0', '00')
        quest_mon('058', 'Growlithe', ':sparkles:', '0', '00')
        quest_mon('059', 'Arcanine', ':sparkles:', '0', '00')
        quest_mon('060', 'Poliwag', ':sparkles:', '0', '00')
        quest_mon('066', 'Machop', ':sparkles:', '0', '00')
        quest_mon('070', 'Weepinbell', '', '0', '00')
        quest_mon('072', 'Tentacool', ':sparkles:', '0', '00')
        quest_mon('073', 'Tentacruel', ':sparkles:', '0', '00')
        quest_mon('074', 'Geodude', ':sparkles:', '0', '00')
        quest_mon('077', 'Ponyta', ':sparkles:', '0', '00')
        quest_mon('081', 'Magnemite', ':sparkles:', '0', '00')
        quest_mon('084', 'Doduo', '', '0', '00')
        quest_mon('085', 'Dodrio', '', '0', '00')
        quest_mon('086', 'Seel', ':sparkles:', '0', '00')
        quest_mon('087', 'Dewgong', ':sparkles:', '0', '00')
        quest_mon('088', 'Grimer', ':sparkles:', '0', '00')
        quest_mon('090', 'Shellder', ':sparkles:', '0', '00')
        quest_mon('092', 'Gastly', ':sparkles:', '0', '00')
        quest_mon('095', 'Onix', ':sparkles:', '0', '00')
        quest_mon('096', 'Drowzee', ':sparkles:', '0', '00')
        quest_mon('100', 'Voltorb', '', '0', '00')
        quest_mon('102', 'Exeggcute', '', '0', '00')
        quest_mon('103', 'Exeggutor', '', '0', '00')
        quest_mon('104', 'Cubone', ':sparkles:', '0', '00')
        quest_mon('108', 'Lickitung', '', '0', '00')
        quest_mon('113', 'Chansey', ':sparkles:', '0', '00')
        quest_mon('114', 'Tangela', '', '0', '00')
        quest_mon('121', 'Starmie', '', '0', '00')
        quest_mon('124', 'Jynx', '', '0', '00')
        quest_mon('125', 'Electabuzz', ':sparkles:', '0', '00')
        quest_mon('126', 'Magmar', ':sparkles:', '0', '00')
        quest_mon('127', 'Pinsir', ':sparkles:', '0', '00')
        quest_mon('129', 'Magikarp', ':sparkles:', '0', '00')
        quest_mon('131', 'Lapras', ':sparkles:', '0', '00')
        quest_mon('133', 'Eevee', ':sparkles:', '0', '00')
        quest_mon('138', 'Omanyte', ':sparkles:', '0', '00')
        quest_mon('140', 'Kabuto', ':sparkles:', '0', '00')
        quest_mon('142', 'Aerodactyl', ':sparkles:', '0', '00')
        quest_mon('147', 'Dratini', ':sparkles:', '0', '00')
        quest_mon('183', 'Marill', '', '0', '00')
        quest_mon('185', 'Sudowoodo', ':sparkles:', '0', '00')
        quest_mon('187', 'Hoppip', '', '0', '00')
        quest_mon('191', 'Sunkern', ':sparkles:', '0', '00')
        quest_mon('196', 'Espeon', '', '0', '00')
        quest_mon('197', 'Umbreon', '', '0', '00')
        quest_mon('207', 'Gligar', ':sparkles:', '0', '00')
        quest_mon('209', 'Snubbull', ':sparkles:', '0', '00')
        quest_mon('215', 'Sneasel', ':sparkles:', '797', '00')
        quest_mon('216', 'Teddiursa', '', '0', '00')
        quest_mon('220', 'Swinub', ':sparkles:', '0', '00')
        quest_mon('227', 'Skarmory', ':sparkles:', '0', '00')
        quest_mon('228', 'Houndour', ':sparkles:', '0', '00')
        quest_mon('234', 'Stantler', ':sparkles:', '0', '00')
        quest_mon('246', 'Larvitar', ':sparkles:', '0', '00')
        quest_mon('255', 'Torchic', ':sparkles:', '0', '00')
        quest_mon('252', 'Treecko', ':sparkles:', '0', '00')
        quest_mon('261', 'Poochyena', ':sparkles:', '0', '00')
        quest_mon('270', 'Lotad', ':sparkles:', '0', '00')
        quest_mon('280', 'Ralts', ':sparkles:', '292', '00')
        quest_mon('286', 'Breloom', '', '0', '00')
        quest_mon('287', 'Slakoth', ':sparkles:', '0', '00')
        quest_mon('290', 'Nincada', ':sparkles:', '0', '00')
        quest_mon('294', 'Loudred', '', '0', '00')
        quest_mon('296', 'Makuhita', ':sparkles:', '0', '00')
        quest_mon('302', 'Sableye', ':sparkles:', '0', '00')
        quest_mon('307', 'Meditite', ':sparkles:', '0', '00')
        quest_mon('310', 'Manectric', ':sparkles:', '0', '00')
        quest_mon('311', 'Plusle', ':sparkles:', '0', '00')
        quest_mon('312', 'Minun', ':sparkles:', '0', '00')
        quest_mon('315', 'Roselia', ':sparkles:', '0', '00')
        quest_mon('317', 'Swalot', '', '0', '00')
        quest_mon('325', 'Spoink', ':sparkles:', '0', '00')
        quest_mon('327', 'Spinda Number 7', ':sparkles:', '0', '00')
        quest_mon('335', 'Zangoose', ':sparkles:', '0', '00')
        quest_mon('336', 'Seviper', ':sparkles:', '0', '00')
        quest_mon('345', 'Lileep', ':sparkles:', '0', '00')
        quest_mon('347', 'Anorith', ':sparkles:', '0', '00')
        quest_mon('349', 'Feebas', ':sparkles:', '0', '00')
        quest_mon('353', 'Shuppet', ':sparkles:', '0', '00')
        quest_mon('359', 'Absol', ':sparkles:', '0', '00')
        quest_mon('361', 'Snorunt', ':sparkles:', '0', '00')
        quest_mon('362', 'Glalie', '', '0', '00')
        quest_mon('366', 'Clamperl', ':sparkles:', '0', '00')
        quest_mon('399', 'Bidoof', '', '0', '00')
        quest_mon('408', 'Cranidos', '', '0', '00')
        quest_mon('410', 'Shieldon', '', '0', '00')
        quest_mon('415', 'Combee', '', '0', '00')
        quest_mon('420', 'Cherubi', '', '0', '00')
        quest_mon('421', 'Cherrim', '', '95', '00')
        quest_mon('425', 'Drifloon', ':sparkles:', '0', '00')
        quest_mon('427', 'Buneary', ':sparkles:', '0', '00')
        quest_mon('436', 'Bronzor', ':sparkles:', '0', '00')
        quest_mon('449', 'Hippopotas', ':sparkles:', '0', '00')
        quest_mon('453', 'Croagunk', ':sparkles:', '0', '00')
        quest_mon('459', 'Snover', ':sparkles:', '0', '00')
        quest_mon('562', 'Yamask', ':sparkles:', '0', '00')
        quest_mon('594', 'Alomomola', '', '0', '00')
        quest_mon('607', 'Litwick', '', '0', '00')
        quest_mon('613', 'Cubchoo', '', '0', '00')
        quest_mon('618', 'Stunfisk', '', '0', '00')
        quest_mon('622', 'Golett', '', '0', '00')
    if max_revive:
        quest_item('202', 'Max Revive','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0202.png')
    if glacial_lure:
        quest_item('502', 'Glacial Lure','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/TroyKey_glacial.png')
    if mossy_lure:
        quest_item('503', 'Mossy Lure','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/TroyKey_moss.png')
    if magnetic_lure:
        quest_item('504', 'Magnetic Lure','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/TroyKey_magnetic.png')
    if golden_razz_berry:
        quest_item('706', 'Golden Razz','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0706.png')
    if silver_pinap_berry:
        quest_item('708', 'Silver Pinap','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0707.png')
    if sun_stone:
        quest_item('1101', 'Sun Stone','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Bag_Sun_Stone_Sprite.png')
    if kings_rock:
        quest_item('1102', 'Kings Rock',"https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Bag_King's_Rock_Sprite.png")
    if metal_coat:
        quest_item('1103', 'Metal Coat','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Bag_Metal_Coat_Sprite.png')
    if dragon_scale:
        quest_item('1104', 'Dragon Scale','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Bag_Dragon_Scale_Sprite.png')
    if up_grade:
        quest_item('1105', 'Up-Grade','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Bag_Up-Grade_Sprite.png')
    if shinnoh_stone:
        quest_item('1106', 'Sinnoh Stone','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Bag_Sinnoh_Stone_Sprite.png')
    if unova_stone:
        quest_item('1107', 'Unova Stone','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Bag_Unova_Stone_Sprite.png')
    if fast_tm:
        quest_item('1201', 'Fast TM','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_1201.png')
    if charged_tm:
        quest_item('1202', 'Charged TM','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_1202.png')
    if rare_candy:
        quest_item('1301', 'Rare Candy','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_1301.png')
    if poke_ball:
        quest_item('1', 'Poke Ball','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0001.png')
    if great_ball:
        quest_item('2', 'Great Ball','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0002.png')
    if ultra_ball:
        quest_item('3', 'Ultra Ball','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0003.png')
    if potion:
        quest_item('101', 'Potion','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0101.png')
    if super_potion:
        quest_item('102', 'Super Potion','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0102.png')
    if hyper_potion:
        quest_item('103', 'Hyper Potion','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0103.png')
    if max_potion:
        quest_item('104', 'Max Potion','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0104.png')
    if revive:
        quest_item('201', 'Revive','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0201.png')
    if razz_berry:
        quest_item('701', 'Razz Berry','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0701.png')
    if pinap_berry:
        quest_item('705', 'Pinap Berry','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0705.png')
    if nanab_berry:
        quest_item('703', 'Nanab Berry','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/Item_0703.png')
    if int(stardust) > 199:
        quest_stardust('0', 'Stardust Over ' + stardust + '','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/stardust_painted.png')

 

now = (datetime.date.today())
today = now.strftime("%m_%d_%Y")
yday = (now - datetime.timedelta(days=1))
yesterday = yday.strftime("%m_%d_%Y")

mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host)
cursor = mariadb_connection.cursor()
quests = ("select count(*) from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where DATE(FROM_UNIXTIME(trs_quest.quest_timestamp)) = CURDATE() and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
stops = ("select count(*) from pokestop where ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
cursor.execute(quests)
qcount = cursor.fetchall()
cursor.execute(stops)
scount = cursor.fetchall()
dir = os.path.expanduser('~/reports/temp/')

if args.check:
 print("Checking Stop and Research Count")
 if scount == qcount:
  print("Counts Match, Checking File...")
  if os.path.isfile(dir+areaname+'_'+today+'.temp'):
   print("File exists, Report ran. EXITING")

  else:
   print("file dose not exist RUNNING REPORT")
   x = open(dir+areaname+'_'+today+'.temp', 'w')
   x.close()
   stuff()
   if os.path.isfile(dir+areaname+'_'+yesterday+'.temp'):
    os.remove(dir+areaname+'_'+yesterday+'.temp')
 else:
  print ("Quests Still Scanning")
  print ("Stop count: ",scount)
  print ("Quest count: ",qcount)
elif args.safe:
 if os.path.isfile(dir+areaname+'_'+today+'.temp'):
  print("File exists, Report ran. EXITING")

 else:
  print("file dose not exist RUNNING REPORT")
  x = open(dir+areaname+'_'+today+'.temp', 'w')
  x.close()
  stuff()
  if os.path.isfile(dir+areaname+'_'+yesterday+'.temp'):
   os.remove(dir+areaname+'_'+yesterday+'.temp')
else:
 print("No checks running report")  
 stuff()
