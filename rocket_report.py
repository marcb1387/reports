from discord_webhook import DiscordWebhook, DiscordEmbed
import mysql.connector as mariadb
import time



area = ''
webhookurl = 'https://discordapp.com/api/'
user = ''
passwd = ''
database = ''
host = ''
author = ''


#Rocket Leaders - Standard
def rocket(leader,lname,sprite,guide):
 mariadb_connection = mariadb.connect(user=user, password=passwd, database=database, host=host)
 cursor = mariadb_connection.cursor()
 query = ("select CONVERT(pokestop.name USING UTF8MB4) as pokestopname,pokestop.latitude,pokestop.longitude from pokestop WHERE incident_grunt_type = "+leader+" and ST_CONTAINS(ST_GEOMFROMTEXT('POLYGON(("+area+"))'), point(pokestop.latitude, pokestop.longitude))")
 cursor.execute(query)
 name = cursor.fetchall()
 
 if not name:
  print ("Leader not Found: "+lname)
 else:
  #convert data into string
  res =[tuple(str(ele) for ele in sub) for sub in name]
  webhook = DiscordWebhook(url=webhookurl)
  # create embed object for webhook 
  research = ''
  for stop in res: 
   research += ('['+stop[0]+'](''https://www.google.com/maps/search/?api=1&query='''+stop[1]+','+stop[2]+')'+'\n')
   if len(research)> 1900:
    print ("larger then 2048 breaking up")
    print (lname+" Length:", len(research))
    webhook.username = lname
    webhook.avatar_url=sprite
    embed = DiscordEmbed(title= 'Leader: '+lname, description=research, color=3158064)
    embed.set_thumbnail(url=sprite)
    embed.set_footer(text='Leader Locations by: '+author)
    embed.set_author(name=lname+' Counters Guide', url=guide)
    #add embed object to webhook
    webhook.add_embed(embed)
    webhook.execute()
    research = ''
    webhook.remove_embed(0)
    time.sleep(2)
  
  print (lname+" Length:", len(research))
  webhook.username = lname
  webhook.avatar_url=sprite
  embed = DiscordEmbed(title= 'Leader: '+lname, description=research, color=3158064)
  embed.set_thumbnail(url=sprite)
  embed.set_footer(text='Leader Locations by: '+author)
  embed.set_author(name=lname+' Counters Guide', url=guide)
  #add embed object to webhook
  webhook.add_embed(embed)
  webhook.execute()
  research = ''
  time.sleep(2)
  


rocket("41","Cliff","https://i.imgur.com/foAB0mG.png","https://pokemongohub.net/post/guide/rocket-leader-cliff-counters/")
rocket("42","Arlo","https://i.imgur.com/T7YOeVe.png","https://pokemongohub.net/post/guide/rocket-leader-arlo-counters/")
rocket("43","Sierra","https://i.imgur.com/skMP1PB.png","https://pokemongohub.net/post/guide/rocket-leader-sierra-counters/")
rocket("44","Giovanni","https://i.imgur.com/uUNF3ST.png","https://pokemongohub.net/post/guide/rocket-boss-giovanni-counters/")
