#!/usr/bin/perl
use DBI;
$dbh2 = DBI->connect('DBI:mysql:pogo;host=localhost', '', ''
             ) || die "Could not connect to database: $DBI::errstr";
$count=0;
open(ROUTE,'/home/marc/MAD/files/stops_dundalk.calc');
foreach $line (<ROUTE>) {
    @coords = split(",",$line);
    my $query = "select pokestop_id from pokestop where latitude = '@coords[0]' and longitude = '@coords[1]'";
    $sth2 = $dbh2->prepare($query);
    $sth2->execute();
    if($sth2->rows) {
        my @row = $sth2->fetchrow_array();
        print "@row[0]\n";
        $count++;
        my $query = "insert into custom_pokestop_area values ('@row[0]','dundalk')";
        $sth3 = $dbh2->prepare($query);
        $sth3->execute();
        $sth3->finish();
    }
}
close(ROUTE);
print "Count: $count\n";
$dbh2->disconnect();
