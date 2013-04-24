#!/usr/bin/perl

# wget all videos listed in a file

#my $vlist_filename = "/home/ubuntu/tmp/yhb";
my $vlist_filename = "yhb";
my $redo_filename = "fyoutube";
#my $vlist_filename = "/tmp/th";

open(my $vlist, "<$vlist_filename") || die "Can not open $vlist_filename \n";
open(my $redofile, ">>$redo_filename") || die "Can not open $redo_filename \n";

my $ii = 0;
my $output = "";

while(<$vlist>){
    #print $_ if $_ !~ /^\s*$/;
    if( $_ !~ /^\s*$/ ){
        my $url = $_;
        print  `pwd`;
        print "$ii to get: $url \n";
        #`perl ygv.pl $url`;
        #`myyoutube-dl.sh  $url`;

        #$output = system("youtube-dl  -o '%(title)s.%(ext)s'  --restrict-filenames $url");
        $output = `youtube-dl  -o '%(title)s%(autonumber)s.%(ext)s' --write-description  --restrict-filenames $url 2>&1 `;
        print "-----------------\n";
        print $output . "\n";
        if ($output !~ /\[download\]/){
            print "ooo ooo ooo \n";
            print $redofile "$url";
        }

        sleep 35;
        $ii ++;
    }
}

close $redofile;
close $vlist;
