
# do trivial jobs:
# After the youtube links fetched by my another python function, 
# there will be a file '/tmp/fha' contains links and titles of youtube videos.
#
# This routine fetch href(s) from /tmp/fha and make directory in /media/my/, then
# start downloading it with using tool from 'calm...' getyoutubevideo perl scripts.
#
# Command line argument would be the name of the directory in the /media/my/, 
# which will contains video files downloaded.

my $base = '/media/my/';
# dirname is the folder name where we are going to put downloaded files:
my $dirname = $base . $ARGV[0] . '/';
print $dirname. "\n";

#sleep(300);


if(! -e $dirname ){
	print "not exists $dirname, mkdir \n";
	`mkdir $dirname`;
}

`cp /home/ubuntu/workspace/video.processes/youtube/ygv.pl $dirname`;
`cp /home/ubuntu/workspace/video.processes/youtube/autoyoutubedl.pl     $dirname`;


if ( -e '/tmp/fha' ){
	`grep  -P  '^http.+\$'  /tmp/fha  > /tmp/yhb`;
}else{
	print "Not exists /tmp/fha \n";
	exit 1;
}

`mv /tmp/yhb  $dirname`;

 
exit 0;
