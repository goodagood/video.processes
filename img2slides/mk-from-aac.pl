#!/usr/bin/perl

#my $mp3_sound = '/home/za/Videos/materials/sounds/nature_sound_16_the_most_relaxing_sounds.mp3';
my $mp3_sound = '/home/za/Music/sound-tracks/battleship_2012_entire_soundtrack.m4a';
#my $mp3_sound = '/home/za/Music/sound-tracks/battleship_2012_entire_soundtrack.mp3';

#my $nosound_avi = '/home/za/Videos/materials/bp/screen-cast-web-7m3s12.avi';
#my $nosound_avi = '/home/za/Videos/materials/slidesffmpeg/r10f05-1h16m20s.avi';
#my $nosound_avi = '/home/za/Videos/materials/slidesffmpeg/r10f15-3h48m45s.avi';
#my $nosound_avi = '/home/za/Videos/materials/slidesffmpeg/r10f10-2h32m30s.avi';
my $nosound_avi = '/home/za/Videos/materials/slidesffmpeg/r10f15.avi';

my $duration = `soxi -d $mp3_sound`;
# remove newlines:
$duration =~ s/\n//g;
$duration = '01:14:12.98';

my $seconds = `soxi -D $mp3_sound`;
# remove newlines:
$seconds =~ s/\n//g;
#my $seconds = '423.12';

my $tmp_cut_avi = '/tmp/avicut.avi';
my $result_avi = '/home/za/Videos/materials/slidesffmpeg/battleship2012-st-slides15.avi';
my $result_flv = '/home/za/Videos/materials/slidesffmpeg/battleship2012-st-slides15.flv';


my $cmd = "ffmpeg -y -i $nosound_avi -an -vcodec copy -ss 00:00 -t $duration $tmp_cut_avi";
#print $cmd, "\n";
`$cmd`;
$cmd = "ffmpeg -y -i $tmp_cut_avi  -i $mp3_sound -acodec copy -vcodec copy -shortest $result_avi";
`$cmd`;
#print $cmd, "\n";

#`ffmpeg -y -i $result_avi -vcodec mpeg4 -acodec libmp3lame -ab 132k $result_flv`;
`ffmpeg -y -i $result_avi -ab 132k  $result_flv`;


=pod
`ffmpeg -y -f image2pipe -i $mp3_sound -acodec copy -vn -ss 00:00 -t $duration $tmp_cut_mp3`;

`ffmpeg -y -i $mp3_sound -acodec copy -vn -ss 00:00 -t $duration $tmp_cut_mp3`;

`sox $tmp_cut_mp3 $tmp_faded_mp3 fade 2 $seconds 8`;

`ffmpeg -y -i $tmp_faded_mp3 -i $nosound_avi -acodec copy -vcodec copy -sameq $result_avi`;
=cut
