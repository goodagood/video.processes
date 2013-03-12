#!/usr/bin/perl

my $file = '/home/za/Videos/materials/carrier/s7/rites_of_passage1sub.avi';

my $outmp3 = '/home/za/Videos/materials/carrier/s7/aaritsub.mp3';
my $outvideo = '/home/za/Videos/materials/carrier/s7/aaritsub.avi';

# extract sound, libmp3lame works for me:
`ffmpeg -i $file -vn -acodec libmp3lame  $outmp3`;

`ffmpeg -i $file -an -vcodec copy $outvideo`;
