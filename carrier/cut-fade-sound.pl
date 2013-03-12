#!/usr/bin/perl

my $mp3_sound = '/home/za/Videos/materials/sounds/waves_60mins_of_lapping_waves_sleep_video.mp3';

#my $nosound_avi = '/home/za/Videos/materials/bp/screen-cast-web-7m3s12.avi';
my $nosound_avi = '/home/za/Videos/materials/bp/screen-8m3s16.avi';

#my $duration = '00:07:03.12';
my $duration = '00:08:03.16';
#my $seconds = '423.12';
my $seconds = '483.16';

my $result_avi = '/home/za/Videos/materials/bp/avscreen-cast-web-8m3s16-waves1.avi';

my $tmp_cut_mp3 = '/tmp/tmpa.mp3';
my $tmp_faded_mp3 = '/tmp/tmpaf.mp3';

`ffmpeg -y -i $mp3_sound -acodec copy -vn -ss 00:00 -t $duration $tmp_cut_mp3`;

`sox $tmp_cut_mp3 $tmp_faded_mp3 fade 2 $seconds 8`;

`ffmpeg -y -i $tmp_faded_mp3 -i $nosound_avi -acodec copy -vcodec copy -sameq $result_avi`;
