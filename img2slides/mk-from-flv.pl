#!/usr/bin/perl

my $flv_input = '/home/za/Videos/materials/sounds/two_hours_of_rain_and_thunder_on_the_lake.flv';

#my $nosound_avi = '/home/za/Videos/materials/slidesffmpeg/r10f05.avi';
my $nosound_avi = '/home/za/Videos/materials/slidesffmpeg/r10f15.avi';

my $ab = '256k';

my $result_flv = '/home/za/Videos/materials/slidesffmpeg/two-hours-rain-thunder-on-lake-mp3_256.flv';

my $result_avi = '/tmp/av.avi';

my $mp3_sound = '/tmp/m.mp3';

my $duration = `soxi -d $mp3_sound`;
# remove newlines:
$duration =~ s/\n//g;

my $seconds = `soxi -D $mp3_sound`;
$seconds =~ s/\n//g;

my $tmp_cut_avi = '/tmp/avicut.avi';

## Get MP3 from FLV:
`ffmpeg -y -i $flv_input -vn -ab 256k $mp3_sound`;

## Cut no-sound video with sound track length
my $cmd = "ffmpeg -y -i $nosound_avi -an -vcodec copy -ss 00:00 -t $duration $tmp_cut_avi";
#print $cmd, "\n";
`$cmd`;

## Merge sound and video
$cmd = "ffmpeg -y -i $tmp_cut_avi  -i $mp3_sound -acodec copy -vcodec copy -shortest $result_avi";
`$cmd`;
#print $cmd, "\n";

## transfer to FLV
`ffmpeg -y -i $result_avi  -ab $ab $result_flv`;


