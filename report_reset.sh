#!/bin/bash
echo "delete calc file"
rm -f /home/marc/MAD/files/stops_dundalk.calc
echo "removed all area name from database"
echo "DELETE FROM custom_pokestop_area WHERE area = 'dundalk';" | mysql -u  --password="" -D pogo
echo "reloading mapping in mad"
curl http://192.168.50.56:5555/reload
echo "Fininshed mappings loading new area back into database"
perl /home/marc/MAD/files/custom/custom_dundalk.pl
echo "all done new stop added into route"
