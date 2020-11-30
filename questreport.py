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
import re
import json
import requests
from bs4 import BeautifulSoup

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
use_emoji = config.getboolean('CONFIG','use_emoji')
use_shiny_emoji = config.getboolean('CONFIG','use_shiny_emoji')
use_webhook_name = config.getboolean('CONFIG','use_webhook_name')
use_slim_name = config.getboolean('CONFIG','use_slim_name')
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
mega_energy = config.getboolean('ITEMS','mega_energy')
ar_task = config.getboolean('ITEMS','ar_task')
stardust = config.get('ITEMS','stardust')
encounters = config.getboolean('ITEMS','encounters')
mons = config.get('POKEMON','dex_number')
adtitle = config.get('AD','Ad_Title')
adbody = config.get('AD','Ad_Body')
adthumb = config.get('AD','Ad_Thumbnail')
# CONFIG END

# SPRITES
if args.gif:
 img = 'https://raw.githubusercontent.com/marcb1387/assets/master/pokemon_icon_' #animated
 ext = '.gif' #animated
else:
 img = 'https://raw.githubusercontent.com/whitewillem/PogoAssets/resized/no_border/pokemon_icon_' # Static
 ext = '.png' #Static
 
imgs = 'https://raw.githubusercontent.com/whitewillem/PogoAssets/resized/no_border/pokemon_icon_' # Static
exts = '.png' #Static

imgwn = "https://raw.githubusercontent.com/Debaucus/PAIcons/master/Current%20Shiny/pokemon_icon_" #webhook name shiny

mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host, port=port)
cursor = mariadb_connection.cursor()
shiny_data = requests.get("https://pogoapi.net/api/v1/shiny_pokemon.json").json()
with open(f"names/en.json", "r") as f:
 mon_names = json.load(f)
 
#Pokemon
def quest_mon():
 query = ("SELECT DISTINCT quest_pokemon_id,quest_pokemon_form_id,quest_pokemon_costume_id FROM trs_quest inner join pokestop on trs_quest.GUID = pokestop.pokestop_id where DATE(FROM_UNIXTIME(trs_quest.quest_timestamp)) = CURDATE() and quest_reward_type = 7 and quest_type NOT like 46 and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude)) order by trs_quest.quest_pokemon_id;")
 cursor.execute(query)
 name = cursor.fetchall()
 res =[tuple(str(ele) for ele in sub) for sub in name]
 for mon in res:
     monquery = ("select CONVERT(pokestop.name USING UTF8MB4) as pokestopname,pokestop.latitude,pokestop.longitude,quest_task from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where DATE(FROM_UNIXTIME(trs_quest.quest_timestamp)) = CURDATE() and quest_reward_type = 7 and quest_pokemon_id ="+mon[0]+" and quest_type NOT like 46 and quest_pokemon_form_id like '%"+mon[1]+"%' and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
     cursor.execute(monquery)
     monname = cursor.fetchall()
     monres =[tuple(str(ele) for ele in sub) for sub in monname]
     mon_name=mon_names.get(str(mon[0]), "")
     mon3d = "{:03d}".format(int(mon[0]))
     form2d = "{:02d}".format(int(mon[1]))
     shiny = ""
     if str(mon[0]) in shiny_data:
      if shiny_data.get(str(mon[0]), {}).get("found_research", True):
       shiny = ":sparkles:"
     if ":sparkles:" in shiny:
      print (mon_name+" Shiny? YES")
     else: print (mon_name+" Shiny? NO")
     snum = ""
     if int(mon[0]) == 327:
      url = 'https://leekduck.com/research/'
      reqs = requests.get(url)
      soup = BeautifulSoup(reqs.content, 'html.parser')
      s = soup.find_all('p')[2].get_text()
      snumm = re.sub("[^0-9]", "", s)
      snum = snumm+" "
     alolan = ""
     if int(mon[1]) in [46, 74, 64, 56, 52, 60, 68]:
      alolan = "(Alolan) " 
     taskquery = ("select CONVERT(pokestop.name USING UTF8MB4) as pokestopname,pokestop.latitude,pokestop.longitude,quest_task from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where DATE(FROM_UNIXTIME(trs_quest.quest_timestamp)) = CURDATE() and quest_reward_type = 7 and quest_pokemon_id ="+mon[0]+" and quest_type NOT like 46 and quest_pokemon_form_id like '%"+mon[1]+"%' and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
     cursor.execute(taskquery)
     taskname = cursor.fetchall()
     taskres =[tuple(str(ele) for ele in sub) for sub in taskname]
     task3 =[]
     for task in taskres:
      task3 += [task[3]]
     result = all(elem == task3[0] for elem in task3)
     if result:
         if mons:
          for dex in mons.split(','):
           if dex == mon3d:
              print ("Research Task Is The Same "+mon_name)
              #convert data into string
              monres.sort()
              webhook = DiscordWebhook(url=webhookurl)
              # create embed object for webhook 
              research = ''
              for stop in monres: 
               research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+'\n')
               if len(research)> 1900:
                print ("larger then 2048 breaking up")
                print (mon_name+" Length:", len(research))
                if use_webhook_name: 
                 embed = DiscordEmbed(title=shiny+' Research Task: '+stop[3]+shiny, description=research, color=16777011)
                 webhook.username = mon_name+" "+alolan+snum+'Field Research'
                 url=imgwn+mon3d+'_'+form2d+ext
                 r = requests.head(url)
                 if r.status_code == requests.codes.ok:
                  webhook.avatar_url = imgwn+mon3d+'_'+form2d+exts
                 else:
                  webhook.avatar_url = img+mon3d+'_'+form2d+ext
                elif use_slim_name:
                 embed = DiscordEmbed(title= shiny+mon_name+" "+alolan+snum+': '+stop[3]+shiny, description=research, color=16777011)
                else:
                 embed = DiscordEmbed(title= shiny+mon_name+" "+alolan+snum+'Field Research'+shiny, description=research, color=16777011)
                 embed.set_author(name='Research Task: '+stop[3])
                if use_emoji:embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
                if use_shiny_emoji:
                 url=imgwn+mon3d+'_'+form2d+ext
                 r = requests.head(url)
                 if r.status_code == requests.codes.ok:
                  embed.set_thumbnail(url=imgwn+mon3d+'_'+form2d+ext)
                 else:
                  embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
                if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
                #add embed object to webhook
                webhook.add_embed(embed)
                webhook.execute()
                research = ''
                webhook.remove_embed(0)
                time.sleep(2)
              print (mon_name+" Length:", len(research))
              if use_webhook_name: 
               embed = DiscordEmbed(title=shiny+' Research Task: '+stop[3]+shiny, description=research, color=16777011)
               webhook.username = mon_name+" "+alolan+snum+'Field Research'
               url=imgwn+mon3d+'_'+form2d+ext
               r = requests.head(url)
               if r.status_code == requests.codes.ok:
                webhook.avatar_url = imgwn+mon3d+'_'+form2d+exts
               else:
                webhook.avatar_url = img+mon3d+'_'+form2d+ext
              elif use_slim_name:
               embed = DiscordEmbed(title= shiny+mon_name+" "+alolan+snum+': '+stop[3]+shiny, description=research, color=16777011)
              else:
               embed = DiscordEmbed(title= shiny+mon_name+" "+alolan+snum+'Field Research'+shiny, description=research, color=16777011)
               embed.set_author(name='Research Task: '+stop[3])
              if use_emoji:embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
              if use_shiny_emoji:
               url=imgwn+mon3d+'_'+form2d+ext
               r = requests.head(url)
               if r.status_code == requests.codes.ok:embed.set_thumbnail(url=imgwn+mon3d+'_'+form2d+ext)
               else:embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
              if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
              #add embed object to webhook
              webhook.add_embed(embed)
              webhook.execute()
              research = ''
              webhook.remove_embed(0)
              time.sleep(2)
         else:
              print ("Research Task Is The Same "+mon_name)
              #convert data into string
              monres.sort()
              webhook = DiscordWebhook(url=webhookurl)
              # create embed object for webhook 
              research = ''
              for stop in monres: 
               research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+'\n')
               if len(research)> 1900:
                print ("larger then 2048 breaking up")
                print (mon_name+" Length:", len(research))
                if use_webhook_name: 
                 webhook.username = mon_name+" "+alolan+snum+'Field Research'
                 embed = DiscordEmbed(title=shiny+' Research Task: '+stop[3]+shiny, description=research, color=16777011)
                 url=imgwn+mon3d+'_'+form2d+ext
                 r = requests.head(url)
                 if r.status_code == requests.codes.ok:
                  webhook.avatar_url = imgwn+mon3d+'_'+form2d+exts
                 else:
                  webhook.avatar_url = img+mon3d+'_'+form2d+ext
                elif use_slim_name:
                 embed = DiscordEmbed(title= shiny+mon_name+" "+alolan+snum+': '+stop[3]+shiny, description=research, color=16777011)
                else:
                 embed = DiscordEmbed(title= shiny+mon_name+" "+alolan+snum+'Field Research'+shiny, description=research, color=16777011)
                 embed.set_author(name='Research Task: '+stop[3])
                if use_emoji: embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
                if use_shiny_emoji:
                 url=imgwn+mon3d+'_'+form2d+ext
                 r = requests.head(url)
                 if r.status_code == requests.codes.ok:embed.set_thumbnail(url=imgwn+mon3d+'_'+form2d+ext)
                 else:embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
                if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
                #add embed object to webhook
                webhook.add_embed(embed)
                webhook.execute()
                research = ''
                webhook.remove_embed(0)
                time.sleep(2)
              print (mon_name+" Length:", len(research))
              if use_webhook_name: 
               webhook.username = mon_name+" "+alolan+snum+'Field Research'
               embed = DiscordEmbed(title=shiny+' Research Task: '+stop[3]+shiny, description=research, color=16777011)
               url=imgwn+mon3d+'_'+form2d+ext
               r = requests.head(url)
               if r.status_code == requests.codes.ok:
                webhook.avatar_url = imgwn+mon3d+'_'+form2d+exts
               else:
                  webhook.avatar_url = img+mon3d+'_'+form2d+ext
              elif use_slim_name:
               embed = DiscordEmbed(title= shiny+mon_name+" "+alolan+snum+': '+stop[3]+shiny, description=research, color=16777011)
              else:
               embed = DiscordEmbed(title= shiny+mon_name+" "+alolan+snum+'Field Research'+shiny, description=research, color=16777011)
               embed.set_author(name='Research Task: '+stop[3])
              if use_emoji: embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
              if use_shiny_emoji:
               url=imgwn+mon3d+'_'+form2d+ext
               r = requests.head(url)
               if r.status_code == requests.codes.ok:embed.set_thumbnail(url=imgwn+mon3d+'_'+form2d+ext)
               else:embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
              if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
              #add embed object to webhook
              webhook.add_embed(embed)
              webhook.execute()
              research = ''
              time.sleep(2)
     else:
         if mons:
          for dex in mons.split(','):
           if dex == mon3d:
              print ("Research Task Is The Different "+mon_name)
              #convert data into string
              monname.sort(key = operator.itemgetter(3, 0))
              monres =[tuple(str(ele) for ele in sub) for sub in monname]
              webhook = DiscordWebhook(url=webhookurl)
              # create embed object for webhook 
              research = ''
              for stop in monres: 
                research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+' '+stop[3]+'\n')
                if len(research)> 1900:
                 print ("larger then 2048 breaking up")
                 print (mon_name+" Length:", len(research))
                 if use_webhook_name: 
                  webhook.username = mon_name+" "+alolan+snum+'Field Research'
                  embed = DiscordEmbed( description=research, color=16777011)
                  url=imgwn+mon3d+'_'+form2d+ext
                  r = requests.head(url)
                  if r.status_code == requests.codes.ok:
                   webhook.avatar_url = imgwn+mon3d+'_'+form2d+exts
                  else:
                   webhook.avatar_url = img+mon3d+'_'+form2d+ext
                 else:
                  embed = DiscordEmbed(title= shiny+mon_name+" "+alolan+snum+'Field Research'+shiny, description=research, color=16777011)
                  webhook.avatar_url = img+mon3d+'_'+form2d+ext
                 if use_emoji: embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
                 if use_shiny_emoji:
                  url=imgwn+mon3d+'_'+form2d+ext
                  r = requests.head(url)
                  if r.status_code == requests.codes.ok:embed.set_thumbnail(url=imgwn+mon3d+'_'+form2d+ext)
                  else:embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
                 if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
                 #add embed object to webhook
                 webhook.add_embed(embed)
                 webhook.execute()
                 research = ''
                 webhook.remove_embed(0)
                 time.sleep(2)
              print (mon_name+" Length:", len(research))
              if use_webhook_name: 
               webhook.username = mon_name+" "+alolan+snum+'Field Research'
               embed = DiscordEmbed( description=research, color=16777011)
               url=imgwn+mon3d+'_'+form2d+ext
               r = requests.head(url)
               if r.status_code == requests.codes.ok:
                webhook.avatar_url = imgwn+mon3d+'_'+form2d+exts
               else:
                webhook.avatar_url = img+mon3d+'_'+form2d+ext
              else:
               embed = DiscordEmbed(title= shiny+mon_name+" "+alolan+snum+'Field Research'+shiny, description=research, color=16777011)
              if use_emoji: embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
              if use_shiny_emoji:
               url=imgwn+mon3d+'_'+form2d+ext
               r = requests.head(url)
               if r.status_code == requests.codes.ok:embed.set_thumbnail(url=imgwn+mon3d+'_'+form2d+ext)
               else:embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
              if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
              #add embed object to webhook
              webhook.add_embed(embed)
              webhook.execute()
              research = ''
              time.sleep(2)
         else:
              print ("Research Task Is The Different "+mon_name)
              #convert data into string
              monname.sort(key = operator.itemgetter(3, 0))
              monres =[tuple(str(ele) for ele in sub) for sub in monname]
              webhook = DiscordWebhook(url=webhookurl)
              # create embed object for webhook 
              research = ''
              for stop in monres: 
               research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+' '+stop[3]+'\n')
               if len(research)> 1900:
                print ("larger then 2048 breaking up")
                print (mon_name+" Length:", len(research))
                if use_webhook_name: 
                 webhook.username = mon_name+" "+alolan+snum+'Field Research'
                 embed = DiscordEmbed( description=research, color=16777011)
                 url=imgwn+mon3d+'_'+form2d+ext
                 r = requests.head(url)
                 if r.status_code == requests.codes.ok:
                  webhook.avatar_url = imgwn+mon3d+'_'+form2d+exts
                 else:
                  webhook.avatar_url = img+mon3d+'_'+form2d+ext
                else:
                 embed = DiscordEmbed(title= shiny+mon_name+" "+alolan+snum+'Field Research'+shiny, description=research, color=16777011)
                if use_emoji: embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
                if use_shiny_emoji:
                 url=imgwn+mon3d+'_'+form2d+ext
                 r = requests.head(url)
                 if r.status_code == requests.codes.ok:embed.set_thumbnail(url=imgwn+mon3d+'_'+form2d+ext)
                 else:embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
                if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
                #add embed object to webhook
                webhook.add_embed(embed)
                webhook.execute()
                research = ''
                webhook.remove_embed(0)
                time.sleep(2)
              print (mon_name+" Length:", len(research))
              if use_webhook_name: 
               webhook.username = mon_name+" "+alolan+snum+'Field Research'
               embed = DiscordEmbed( description=research, color=16777011)
               url=imgwn+mon3d+'_'+form2d+ext
               r = requests.head(url)
               if r.status_code == requests.codes.ok:
                webhook.avatar_url = imgwn+mon3d+'_'+form2d+exts
               else:
                webhook.avatar_url = img+mon3d+'_'+form2d+ext
              else:
               embed = DiscordEmbed(title= shiny+mon_name+" "+alolan+snum+'Field Research'+shiny, description=research, color=16777011)
              if use_emoji: embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
              if use_shiny_emoji:
               url=imgwn+mon3d+'_'+form2d+ext
               r = requests.head(url)
               if r.status_code == requests.codes.ok:embed.set_thumbnail(url=imgwn+mon3d+'_'+form2d+ext)
               else:embed.set_thumbnail(url=img+mon3d+'_'+form2d+ext)
              if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
              #add embed object to webhook
              webhook.add_embed(embed)
              webhook.execute()
              research = ''
              time.sleep(2)
#items
def quest_item(itemid,item,sprite):
 mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host,port=port)
 cursor = mariadb_connection.cursor()
 query = ("select CONVERT(pokestop.name USING UTF8MB4) as pokestopname,pokestop.latitude,pokestop.longitude,trs_quest.quest_task,trs_quest.quest_item_amount from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where DATE(FROM_UNIXTIME(trs_quest.quest_timestamp)) = CURDATE() and quest_item_id = "+itemid+" and quest_type NOT like 46 and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
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
       research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+ '- Amount: '+stop[4]+'\n')
       if len(research)> 1900:
        print ("larger then 2048 breaking up")
        print (item+" Length:", len(research))
        if use_webhook_name:
         embed = DiscordEmbed(description=research, color=4390656)        
         webhook.username = item+' Field Research'
         webhook.avatar_url = sprite
         embed.set_author(name='Research Task: '+stop[3])
        elif use_slim_name:
         embed = DiscordEmbed(title= item+': '+stop[3], description=research, color=4390656)
        else:
         embed = DiscordEmbed(title= item+' Field Research', description=research, color=4390656)
         embed.set_author(name='Research Task: '+stop[3])
        if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
        if use_emoji: embed.set_thumbnail(url=sprite) 
        webhook.add_embed(embed)
        webhook.execute()
        research = ''
        webhook.remove_embed(0)
        time.sleep(2)
      print (item+" Length:", len(research))    
      if use_webhook_name:
       embed = DiscordEmbed(description=research, color=4390656)        
       webhook.username = item+' Field Research'
       webhook.avatar_url = sprite
       embed.set_author(name='Research Task: '+stop[3])
      elif use_slim_name:
       embed = DiscordEmbed(title= item+': '+stop[3], description=research, color=4390656)
      else:
       embed = DiscordEmbed(title= item+' Field Research', description=research, color=4390656)
       embed.set_author(name='Research Task: '+stop[3])
      if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
      if use_emoji: embed.set_thumbnail(url=sprite) 
      webhook.add_embed(embed)
      webhook.execute()
      research = ''
      time.sleep(2)
  else:
      print ("Research Task Is Different "+item)
      name.sort(key = operator.itemgetter(3,0))
      res =[tuple(str(ele) for ele in sub) for sub in name]
      for stop in res: 
       research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+' '+stop[3]+' - Amount: '+stop[4]+'\n')
       if len(research)> 1900:
        print ("larger then 2048 breaking up")
        print (item+" Length:", len(research))
        #add embed object to webhook
        if use_webhook_name:
         embed = DiscordEmbed(description=research, color=4390656)        
         webhook.username = item+' Field Research'
         webhook.avatar_url = sprite
        else:
         embed = DiscordEmbed(title= item+' Field Research', description=research, color=4390656)
        if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
        if use_emoji: embed.set_thumbnail(url=sprite)
        webhook.add_embed(embed)
        webhook.execute()
        research = ''
        webhook.remove_embed(0)
        time.sleep(2)
      print (item+" Length:", len(research))
      
      #add embed object to webhook
      if use_webhook_name:
       embed = DiscordEmbed(description=research, color=4390656)        
       webhook.username = item+' Field Research'
       webhook.avatar_url = sprite
      else:
       embed = DiscordEmbed(title= item+' Field Research', description=research, color=4390656)
      if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
      if use_emoji: embed.set_thumbnail(url=sprite) 
      webhook.add_embed(embed)
      webhook.execute()
      research = ''
      time.sleep(2)
#AR Stops
def ar_stops(item,sprite):
 mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host,port=port)
 cursor = mariadb_connection.cursor()
 query = ("select CONVERT(pokestop.name USING UTF8MB4) as pokestopname,pokestop.latitude,pokestop.longitude,trs_quest.quest_task from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where DATE(FROM_UNIXTIME(trs_quest.quest_timestamp)) = CURDATE() and quest_type = 46 and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
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
        if use_webhook_name:
         embed = DiscordEmbed(description=research, color=15105570)        
         webhook.username = item+' Field Research'
         webhook.avatar_url = sprite
         embed.set_author(name='Research Task: '+stop[3])
        elif use_slim_name:
         embed = DiscordEmbed(title= item+': '+stop[3], description=research, color=15105570)
        else:
         embed = DiscordEmbed(title= item+' Field Research', description=research, color=15105570)
         embed.set_author(name='Research Task: '+stop[3])
        if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
        if use_emoji: embed.set_thumbnail(url=sprite) 
        webhook.add_embed(embed)
        webhook.execute()
        research = ''
        webhook.remove_embed(0)
        time.sleep(2)
      print (item+" Length:", len(research))    
      if use_webhook_name:
       embed = DiscordEmbed(description=research, color=15105570)        
       webhook.username = item+' Field Research'
       webhook.avatar_url = sprite
       embed.set_author(name='Research Task: '+stop[3])
      elif use_slim_name:
       embed = DiscordEmbed(title= item+': '+stop[3], description=research, color=15105570)
      else:
       embed = DiscordEmbed(title= item+' Field Research', description=research, color=15105570)
       embed.set_author(name='Research Task: '+stop[3])
      if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
      if use_emoji: embed.set_thumbnail(url=sprite) 
      webhook.add_embed(embed)
      webhook.execute()
      research = ''
      time.sleep(2)
  else:
      print ("Research Task Is Different "+item)
      name.sort(key = operator.itemgetter(3,0))
      res =[tuple(str(ele) for ele in sub) for sub in name]
      for stop in res: 
       research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+' '+stop[3]+'\n')
       if len(research)> 1900:
        print ("larger then 2048 breaking up")
        print (item+" Length:", len(research))
        #add embed object to webhook
        if use_webhook_name:
         embed = DiscordEmbed(description=research, color=15105570)        
         webhook.username = item+' Field Research'
         webhook.avatar_url = sprite
        else:
         embed = DiscordEmbed(title= item+' Field Research', description=research, color=15105570)
        if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
        if use_emoji: embed.set_thumbnail(url=sprite)
        webhook.add_embed(embed)
        webhook.execute()
        research = ''
        webhook.remove_embed(0)
        time.sleep(2)
      print (item+" Length:", len(research))
      
      #add embed object to webhook
      if use_webhook_name:
       embed = DiscordEmbed(description=research, color=15105570)        
       webhook.username = item+' Field Research'
       webhook.avatar_url = sprite
      else:
       embed = DiscordEmbed(title= item+' Field Research', description=research, color=15105570)
      if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
      if use_emoji: embed.set_thumbnail(url=sprite) 
      webhook.add_embed(embed)
      webhook.execute()
      research = ''
      time.sleep(2)
#mega energy
def mega_item(itemid,item,sprite):
 mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host,port=port)
 cursor = mariadb_connection.cursor()
 query = ("select CONVERT(pokestop.name USING UTF8MB4) as pokestopname,pokestop.latitude,pokestop.longitude,trs_quest.quest_task,trs_quest.quest_item_amount,trs_quest.quest_pokemon_id from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where DATE(FROM_UNIXTIME(trs_quest.quest_timestamp)) = CURDATE() and quest_reward_type = 12 and quest_pokemon_id = "+itemid+" and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
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
       research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+' - Amount: '+stop[4]+'\n')
       if len(research)> 1900:
        print ("larger then 2048 breaking up")
        print (item+" Length:", len(research))
        if use_webhook_name:
         embed = DiscordEmbed(description=research, color=1752220)        
         webhook.username = item+' Field Research'
         webhook.avatar_url = sprite
         embed.set_author(name='Research Task: '+stop[3])
        elif use_slim_name:
         embed = DiscordEmbed(title= item+': '+stop[3], description=research, color=1752220)
        else:
         embed = DiscordEmbed(title= item+' Field Research', description=research, color=1752220)
         embed.set_author(name='Research Task: '+stop[3])
        if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
        if use_emoji: embed.set_thumbnail(url=sprite) 
        webhook.add_embed(embed)
        webhook.execute()
        research = ''
        webhook.remove_embed(0)
        time.sleep(2)
      print (item+" Length:", len(research))    
      if use_webhook_name:
       embed = DiscordEmbed(description=research, color=1752220)        
       webhook.username = item+' Field Research'
       webhook.avatar_url = sprite
       embed.set_author(name='Research Task: '+stop[3])
      elif use_slim_name:
       embed = DiscordEmbed(title= item+': '+stop[3], description=research, color=1752220)
      else:
       embed = DiscordEmbed(title= item+' Field Research', description=research, color=1752220)
       embed.set_author(name='Research Task: '+stop[3])
      if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
      if use_emoji: embed.set_thumbnail(url=sprite) 
      webhook.add_embed(embed)
      webhook.execute()
      research = ''
      time.sleep(2)
  else:
      print ("Research Task Is Different "+item)
      name.sort(key = operator.itemgetter(3,0))
      res =[tuple(str(ele) for ele in sub) for sub in name]
      for stop in res: 
       research += ('['+stop[0]+'](''https://maps.google.com/?q='''+stop[1]+','+stop[2]+')'+' '+stop[3]+' - Amount: '+stop[4]+'\n')
       if len(research)> 1900:
        print ("larger then 2048 breaking up")
        print (item+" Length:", len(research))
        #add embed object to webhook
        if use_webhook_name:
         embed = DiscordEmbed(description=research, color=1752220)        
         webhook.username = item+' Field Research'
         webhook.avatar_url = sprite
        else:
         embed = DiscordEmbed(title= item+' Field Research', description=research, color=1752220)
        if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
        if use_emoji: embed.set_thumbnail(url=sprite)
        webhook.add_embed(embed)
        webhook.execute()
        research = ''
        webhook.remove_embed(0)
        time.sleep(2)
      print (item+" Length:", len(research))
      
      #add embed object to webhook
      if use_webhook_name:
       embed = DiscordEmbed(description=research, color=1752220)        
       webhook.username = item+' Field Research'
       webhook.avatar_url = sprite
      else:
       embed = DiscordEmbed(title= item+' Field Research', description=research, color=1752220)
      if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
      if use_emoji: embed.set_thumbnail(url=sprite) 
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
    if use_webhook_name:
     embed = DiscordEmbed(description=research, color=16711931)
     webhook.username = item+' Field Research'
     webhook.avatar_url = sprite
    else:
     embed = DiscordEmbed(title= item+' Field Research', description=research, color=16711931)
     if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
    if use_emoji:  embed.set_thumbnail(url=sprite)
    #add embed object to webhook
    webhook.add_embed(embed)
    webhook.execute()
    research = ''
    webhook.remove_embed(0)
    time.sleep(2)
  print (item+" Length:", len(research))
  if use_webhook_name:
   embed = DiscordEmbed(description=research, color=16711931)
   webhook.username = item+' Field Research'
   webhook.avatar_url = sprite
  else:
   embed = DiscordEmbed(title= item+' Field Research', description=research, color=16711931)
  if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
  if use_emoji:  embed.set_thumbnail(url=sprite)
  #add embed object to webhook
  webhook.add_embed(embed)
  webhook.execute()
  research = ''
  time.sleep(2)

def ad():
 if not adbody:
  print ("no Ad to Display")
 else:
  print ("Ad found")
  webhook = DiscordWebhook(url=webhookurl)
  # create embed object for webhook
  adbodydecode = bytes(adbody, "utf-8").decode("unicode_escape")
  embed = DiscordEmbed(title=adtitle, description=adbodydecode, color=16711931)
  if author: embed.set_footer(text='Research by '+author, icon_url=footerimg)
  embed.set_thumbnail(url=adthumb) 
  #add embed object to webhook
  webhook.add_embed(embed)
  webhook.execute()
  research = ''
  webhook.remove_embed(0)
  time.sleep(2)
 
#Pokeomon, Items, Stardust, Megas
def stuff():
    if encounters:
        quest_mon()
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
    if mega_energy:
        mega_item('3','Venusaur Mega Energy','https://raw.githubusercontent.com/marcb1387/assets/master/energy.png')
        mega_item('6','Charizard Mega Energy','https://raw.githubusercontent.com/marcb1387/assets/master/energy.png')
        mega_item('9','Blastoise Mega Energy','https://raw.githubusercontent.com/marcb1387/assets/master/energy.png')
        mega_item('15','Beedrill Mega Energy','https://raw.githubusercontent.com/marcb1387/assets/master/energy.png')
    if ar_task:
        ar_stops('AR','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/decrypted_assets/png/tx_tutorial_arDataSurround.png')
    if int(stardust) > 199:
        quest_stardust('0', 'Stardust Over ' + stardust + '','https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/static_assets/png/stardust_painted.png')

 
now = (datetime.date.today())
today = now.strftime("%m_%d_%Y")
yday = (now - datetime.timedelta(days=1))
yesterday = yday.strftime("%m_%d_%Y")

mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host, port=port)
cursor = mariadb_connection.cursor()
quests = ("select count(*) from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID where DATE(FROM_UNIXTIME(trs_quest.quest_timestamp)) = CURDATE() and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
stops = ("select count(*) from pokestop where ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
cursor.execute(quests)
qcount = cursor.fetchall()
cursor.execute(stops)
scount = cursor.fetchall()
my_path = os.path.abspath(os.path.dirname(__file__))
dir = os.path.join(my_path, "./temp/")

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
   ad()
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
  ad()
  if os.path.isfile(dir+areaname+'_'+yesterday+'.temp'):
   os.remove(dir+areaname+'_'+yesterday+'.temp')
else:
 print("No checks running report")  
 stuff()
 ad()
