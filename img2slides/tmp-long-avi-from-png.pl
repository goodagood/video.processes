#!/usr/bin/perl

my $slide_interval = 10;

my $duration = `soxi -d $mp3_sound`;
#my $duration = '00:07:03.12';

#my $seconds = `soxi -D $mp3_sound`;
#my $seconds = '10800';
my $seconds = '108';

my $result_avi = '/home/za/Videos/materials/slidesffmpeg/avfoo.avi';

=pod
my $tmp_cut_mp3 = '/tmp/tmpa.mp3';
my $tmp_faded_mp3 = '/tmp/tmpaf.mp3';
=cut

my $number_of_slides = int($seconds/$slide_interval) + 1;

my $ls = `ls i*.png`;
my @files = split(/\n/; $ls);
my $cat_list = "";
my $j = 0;
for(my $i=0; $i<$number_of_slides; $i++){
    $cat_list = $cat_list . "  $files[$j]";
    $j = 0 if $j == $#files;

}

print $cat_list, "\n";

=pod
`ffmpeg -y -f image2pipe -i $mp3_sound -acodec copy -vn -ss 00:00 -t $duration $tmp_cut_mp3`;

`ffmpeg -y -i $mp3_sound -acodec copy -vn -ss 00:00 -t $duration $tmp_cut_mp3`;

`sox $tmp_cut_mp3 $tmp_faded_mp3 fade 2 $seconds 8`;

`ffmpeg -y -i $tmp_faded_mp3 -i $nosound_avi -acodec copy -vcodec copy -sameq $result_avi`;
=cut
