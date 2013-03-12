#!/usr/bin/perl

#my $mp3_sound = '/home/za/Videos/materials/sounds/nature_sound_16_the_most_relaxing_sounds.mp3';
#my $mp3_sound = '/home/za/Music/sound-tracks/battleship_2012_entire_soundtrack.m4a';
my $mp3_sound = '/home/za/Videos/materials/sounds/relaxing_sounds_of_nature_desert_wind.mp3';

#my $nosound_avi = '/home/za/Videos/materials/bp/screen-cast-web-7m3s12.avi';
#my $nosound_avi = '/home/za/Videos/materials/slidesffmpeg/r10f15.avi';
my $nosound_avi = '/home/za/Videos/materials/slidesffmpeg/r10f05.avi';

my $ab = '256k';

my $result_avi = '/tmp/av.avi';
my $result_flv = '/home/za/Videos/materials/slidesffmpeg/relaxing-desert-wind-8m-mp3_256.flv';

my $duration = `soxi -d $mp3_sound`;
# remove newlines:
$duration =~ s/\n//g;
#$duration = '01:14:12.98';

my $seconds = `soxi -D $mp3_sound`;
# remove newlines:
$seconds =~ s/\n//g;
#my $seconds = '423.12';

my $tmp_cut_avi = '/tmp/avicut.avi';

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
#`ffmpeg -y -i $result_avi -ab 132k  $result_flv`;


