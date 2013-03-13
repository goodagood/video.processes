#!/usr/bin/perl

# wget all videos listed in a file

my $vlist_filename = "yhb";
#my $vlist_filename = "/tmp/th";

open(my $vlist, "<$vlist_filename") || die "Can not open $vlist_filename \n";

while(<$vlist>){
	#print $_ if $_ !~ /^\s*$/;
	if( $_ !~ /^\s*$/ ){
		my $url = $_;
		print "\n to get: $url \n";
		`perl ygv.pl $url`;
		sleep 5;
	}
}
