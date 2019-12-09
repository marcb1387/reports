#!/usr/bin/perl

use WWW::Mechanize;
use JSON qw( decode_json );
use JSON qw( encode_json );
use DBI;

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
@months = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
@days = qw(Sun Mon Tue Wed Thu Fri Sat Sun);
# Change intro line here
my $introline='{"content":"***Dundalk Quest Report for:' . $days[$wday] . ' ' . $months[$mon] . ' ' . $mday .'***"}';
# CHange to put Webhook Url in single quotes
my $webhookurl = 'https://discordapp.com/api/webhooks/';
my $discordClient = WWW::Mechanize->new();
my $clientConnected = eval { $discordClient->post( $webhookurl, 'Content-Type' => 'application/json', Content => $introline ); };
# Change db name, username, password as necessary
$dbh2 = DBI->connect('DBI:mysql:pogo;host=localhost', '', ''
             ) || die "Could not connect to database: $DBI::errstr";


sub list_quest { 
    my @list = @_;
    my $query = "select CONVERT(pokestop.name USING ascii) as pokestopname,pokestop.latitude,pokestop.longitude from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID inner join custom_pokestop_area on pokestop.pokestop_id = custom_pokestop_area.pokestop_id where quest_pokemon_id = " . @list[0] . " and DATE(FROM_UNIXTIME(trs_quest.quest_timestamp)) = CURDATE() and custom_pokestop_area.area = 'dundalk'";
    $sth2 = $dbh2->prepare($query);
    $sth2->execute();
    $numrows = $sth2->rows;
    if ($sth2->rows) {
        my $jsonpost = '{"content":"'. @list[1] . ' Quests**__\n';
        my $postsize = 16;
        for (my $i=0; $i < $numrows; $i++) { 
           my @row = $sth2->fetchrow_array();
           $jsonpost .= '['.@row[0].'](<https://www.google.com/maps/search/?api=1&query='.@row[1].','.@row[2].'>)\n';
           $postsize = $postsize + length($jsonpost);
           if ($postsize > 1950) {
             $jsonpost .= '"}';
             print "posting to discord becuse we are at $postsize\n$jsonpost\n";
             my $clientConnected = eval { $discordClient->post( $webhookurl, 'Content-Type' => 'application/json', Content => $jsonpost ); };
             $jsonpost = '{"content":"';
             $postsize = 0;
             sleep 15;
           }
        }
        $jsonpost .= '"}';
        print $jsonpost;
        my $clientConnected = eval { $discordClient->post( $webhookurl, 'Content-Type' => 'application/json', Content => $jsonpost ); };
        sleep 15;
    }

}

sub list_item_quest {
    my @list = @_;
    my $query = "select CONVERT(pokestop.name USING ascii) as pokestopname,pokestop.latitude,pokestop.longitude,trs_quest.quest_task,trs_quest.quest_item_amount,trs_quest.quest_item_id from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID inner join custom_pokestop_area on pokestop.pokestop_id = custom_pokestop_area.pokestop_id where quest_item_id = " . @list[0] . " and DATE(FROM_UNIXTIME(trs_quest.quest_timestamp)) = CURDATE() and custom_pokestop_area.area = 'dundalk'";
    $sth2 = $dbh2->prepare($query);
    $sth2->execute();
    $numrows = $sth2->rows;
    if ($sth2->rows) {
        my $jsonpost = '{"content":"'. @list[1] . ' Quests**__\n';
        my $postsize = 16;
        for (my $i=0; $i < $numrows; $i++) {
           my @row = $sth2->fetchrow_array();
           $jsonpost .= '['.@row[0].'](<https://www.google.com/maps/search/?api=1&query='.@row[1].','.@row[2].'>) - '.@row[3].' - Amount:'.@row[4].'\n';
           $postsize = $postsize + length($jsonpost);
           if ($postsize > 1950) {
             $jsonpost .= '"}';
             print "posting to discord becuse we are at $postsize\n$jsonpost\n";
             my $clientConnected = eval { $discordClient->post( $webhookurl, 'Content-Type' => 'application/json', Content => $jsonpost ); };
             $jsonpost = '{"content":"';
             $postsize = 0;
             sleep 15;
           }
        }
        $jsonpost .= '"}';
        print $jsonpost;
        my $clientConnected = eval { $discordClient->post( $webhookurl, 'Content-Type' => 'application/json', Content => $jsonpost ); };
        sleep 15;
    }

}

sub list_item_stardust {
    my @list = @_;
    my $query = "select CONVERT(pokestop.name USING ascii) as pokestopname,pokestop.latitude,pokestop.longitude,trs_quest.quest_task,if(trs_quest.quest_stardust>999,trs_quest.quest_stardust, null) from pokestop inner join trs_quest on pokestop.pokestop_id = trs_quest.GUID inner join custom_pokestop_area on pokestop.pokestop_id = custom_pokestop_area.pokestop_id where quest_pokemon_id = " . @list[0] . " and DATE(FROM_UNIXTIME(trs_quest.quest_timestamp)) = CURDATE() and if(trs_quest.quest_stardust>999,trs_quest.quest_stardust, null) is not null and custom_pokestop_area.area = 'dundalk'";
	$sth2 = $dbh2->prepare($query);
    $sth2->execute();
    $numrows = $sth2->rows;
    if ($sth2->rows) {
        my $jsonpost = '{"content":"'. @list[1] . ' Quests**__\n';
        my $postsize = 16;
        for (my $i=0; $i < $numrows; $i++) {
           my @row = $sth2->fetchrow_array();
           $jsonpost .= '['.@row[0].'](<https://www.google.com/maps/search/?api=1&query='.@row[1].','.@row[2].'>) - '.@row[3].' - Amount:'.@row[4].'\n';
           $postsize = $postsize + length($jsonpost);
           if ($postsize > 1950) {
             $jsonpost .= '"}';
             print "posting to discord becuse we are at $postsize\n$jsonpost\n";
             my $clientConnected = eval { $discordClient->post( $webhookurl, 'Content-Type' => 'application/json', Content => $jsonpost ); };
             $jsonpost = '{"content":"';
             $postsize = 0;
             sleep 15;
           }
        }
        $jsonpost .= '"}';
        print $jsonpost;
        my $clientConnected = eval { $discordClient->post( $webhookurl, 'Content-Type' => 'application/json', Content => $jsonpost ); };
        sleep 15;
    }

}



list_quest(1,"__**Bulbasaur");
list_quest(4,"__**Charmander");
list_quest(7,"__**Squirtle");
list_quest(9,"__**Blastoise");
list_quest(16,"__**Pidgey");
list_quest(27,"__**Sandshrew");
list_quest(29,"__**Nidoran");
list_quest(30,"__**Nidorina");
list_quest(31,"__**Nidoqueen");
list_quest(32,"__**Nidoran");
list_quest(33,"__**Nidorino");
list_quest(34,"__**Nidoking");
list_quest(37,"__**Vulpix");
list_quest(41,"__**Ditto");
list_quest(56,"__**Mankey");
list_quest(58,"__**Growlithe");
list_quest(59,"__**Arcanine");
list_quest(60,"__**Poliwag");
list_quest(66,"__**Machop");
list_quest(70,"__**Weepinbell");
list_quest(72,"__**Tentacool");
list_quest(73,"__**Tentacruel");
list_quest(74,"__**Geodude");
list_quest(77,"__**Ponyta");
list_quest(81,"__**Magnemite");
list_quest(84,"__**Doduo");
list_quest(85,"__**Dodrio");
list_quest(86,"__**Seel");
list_quest(88,"__**Grimer");
list_quest(92,"__**Gastly");
list_quest(95,"__**Onix");
list_quest(96,"__**Drowzee");
list_quest(100,"__**Voltorb");
list_quest(102,"__**Exeggcute");
list_quest(103,"__**Exeggutor");
list_quest(104,"__**Cubone");
list_quest(113,"__**Chansey");
list_quest(121,"__**Starmie");
list_quest(124,"__**Jynx");
list_quest(125,"__**Electabuzz");
list_quest(126,"__**Magmar");
list_quest(129,"__**Magikarp");
list_quest(131,"__**Lapras");
list_quest(133,"__**Eevee");
list_quest(138,"__**Omanyte");
list_quest(140,"__**Kabuto");
list_quest(142,"__**Aerodactyl");
list_quest(147,"__**Dratini");
list_quest(191,"__**Sunkern");
list_quest(220,"__**Swinub");
list_quest(209,"__**Snubbull");
list_quest(215,"__**Sneasel");
list_quest(216,"__**Teddiursa");
list_quest(227,"__**Skarmory");
list_quest(228,"__**Houndour");
list_quest(246,"__**Larvitar");
list_quest(252,"__**Treecko");
list_quest(261,"__**Poochyena");
list_quest(286,"__**Breloom");
list_quest(287,"__**Slakoth");
list_quest(294,"__**Loudred");
list_quest(296,"__**Makuhita");
list_quest(302,"__**Sableye");
list_quest(307,"__**Meditite");
list_quest(310,"__**Manectric");
list_quest(311,"__**Plusle");
list_quest(312,"__**Minun");
list_quest(317,"__**Swalot");
list_quest(325,"__**Spoink");
list_quest(327,"__**Spinda 1");
list_quest(335,"__**Zangoose");
list_quest(336,"__**Seviper");
list_quest(345,"__**Lileep");
list_quest(347,"__**Anorith");
list_quest(353,"__**Shuppet");
list_quest(359,"__**Absol");
list_quest(361,"__**Snorunt");
list_quest(366,"__**Clamperl");
list_quest(399,"__**Bidoof");
list_quest(408,"__**Cranidos");
list_quest(410,"__**Shieldon");
list_quest(425,"__**Drifloon");
list_quest(427,"__**Buneary");
list_quest(436,"__**Bronzor");
list_quest(562,"__**Yamask");
list_quest(607,"__**Litwick");
list_quest(622,"__**Golett");
list_item_quest(202,"__**<:maxrevive:630142298105053184> Max Revive");
list_item_quest(502,"__**<:glacial:652307147874631691> Glacial Lure");
list_item_quest(503,"__**<:moss:652307147715248151> Mossy Lure");
list_item_quest(504,"__**<:magnetic:652307147811455027> Magnetic Lure");
list_item_quest(706,"__**<:golden:606100739408003082> Golden Razz");
list_item_quest(708,"__**<:silver:606100695304765441> Silver Pinap");
list_item_quest(1101,"__**<:sunstone:652307147966906388> Sun Stone");
list_item_quest(1102,"__**<:kingrock:652307147920637977> Kings Rock");
list_item_quest(1103,"__**<:metalcoat:652307147673305139> Metal Coat");
list_item_quest(1104,"__**<:dragonscale:652307147908055060> Dragon Scale");
list_item_quest(1105,"__**<:upgrade:652307147757191181> Up-Grade");
list_item_quest(1106,"__**<:sinnohstone:630142661478842408> Sinnoh Stone");
list_item_quest(1107,"__**<:unova:652307148050530353> Unova Stone");
list_item_quest(1201,"__**<:fast:652307147547213835> Fast TM");
list_item_quest(1202,"__**<:charged:652307147576836109> Charged TM");
list_item_quest(1301,"__**<:rare:606100716217696266> Rare Candy");
list_item_stardust(0,"__**<:stardust:630142766243905556> Stardust"); 





$dbh2->disconnect();
