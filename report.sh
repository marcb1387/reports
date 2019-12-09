#!/bin/bash
now=$(date +"%m_%d_%Y")
yesterday=$(date -d "yesterday" '+%m_%d_%Y')
T1=$(mysql -u -p -D pogo -se "select count(*) from trs_quest inner join custom_pokestop_area on trs_quest.GUID = custom_pokestop_area.pokestop_id and DATE(FROM_UNIXTIME(quest_timestamp)) = CURDATE() and custom_pokestop_area.area = 'dundalk'")
T2=$(mysql -u -p -D pogo -se "select (char_length(routefile) - char_length(REPLACE(routefile, '\"', ''))) div 2 from settings_routecalc where routecalc_id = '12'")
            if [ "$T1" = "$T2" ]; then
                echo value is true
                if [ ! -f /home/marc/report/temp/dundalk_$now.temp ]; then
                  echo file dose not exist RUNNING SCRIPT
                  touch /home/marc/report/temp/dundalk_$now.temp
                  perl /home/marc/report/questreport_dundalk.pl
                  rm  /home/marc/report/temp/dundalk_$yesterday.temp
                else
                  echo file exists exiting
                fi
            else
                echo Research still running
            fi
