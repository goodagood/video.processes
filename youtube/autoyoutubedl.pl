#!/usr/bin/perl

# wget all videos listed in a file

#my $vlist_filename = "/home/ubuntu/tmp/yhb";
my $vlist_filename = "yhb";
#my $vlist_filename = "/tmp/th";

open(my $vlist, "<$vlist_filename") || die "Can not open $vlist_filename \n";

my $ii = 0;

while(<$vlist>){
	#print $_ if $_ !~ /^\s*$/;
	if( $_ !~ /^\s*$/ ){
		my $url = $_;
		print "$ii to get: $url \n";
		#`perl ygv.pl $url`;
        #`myyoutube-dl.sh  $url`;

        #`youtube-dl  -o '%(title)s_%(autonumber)s.%(ext)s'  --restrict-filenames $url`;
        `youtube-dl  -o '%(title)s.%(ext)s'  --restrict-filenames $url`;

		sleep 5;
		$ii ++;
	}
}
