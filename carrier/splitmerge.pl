#!/usr/bin/perl
#
## split by time piece: from $start_time with $duration
## Than merge the cut off piece into a+v video file

# from 34:28 - 55:08
#my $start_time = '00:34:28';
#my $duration = '00:20:40';

# for my first 4:10 time piece
#my $start_time = '00:34:28';
#my $duration = '00:04:10';

my $start_time = '00:03:58';
my $duration = '00:05:00';

my $fading_seconds = 3;

#my $file = '/home/za/Videos/materials/carrier/rites_of_passage1sub.avi';

## suppose we have separated audio and video source file
my $afile = '/home/za/Videos/materials/carrier/s3secrets/a.mp3';
my $vfile = '/home/za/Videos/materials/carrier/s3secrets/v.avi';
#my $afile = '/home/za/Videos/materials/carrier/s7/aclip.mp3';
#my $vfile = '/home/za/Videos/materials/carrier/s7/vclip.avi';

## The result file, merged with audio and video:
my $result_file = '/tmp/av0358.avi';
#my $result_file = '/home/za/Videos/materials/carrier/s7/clip3428.avi';

## we split audio and video separately, so we will get 2 middle files:
my $afile_ma = '/tmp/mt.mp3';

my $afile_m = '/tmp/maclip.mp3';
my $vfile_m = '/tmp/mvclip.avi';
#my $afile_m = '/home/za/Videos/materials/carrier/s7/maclip.mp3';
#my $vfile_m = '/home/za/Videos/materials/carrier/s7/mvclip.avi';

# split audio, note this cut a piece audio file from AUDIO file.
`ffmpeg -y -i $afile -vn -acodec copy -ss $start_time -t $duration $afile_ma`;

# fade audio
my $mp3_seconds = `soxi -D $afile_ma`;
`sox $afile_ma $afile_m fade $fading_seconds $mp3_seconds $fading_seconds`;

# split video, note this cut a piece video file from VIDEO file.
`ffmpeg -y -i $vfile -an -vcodec copy -ss $start_time -t $duration $vfile_m`;

# merge audio video
`ffmpeg -y -i $vfile_m -i $afile_m -acodec copy -vcodec copy -sameq $result_file`;

print (join " : ", ($afile_m, $afile_ma, $mp3_seconds)), "\n";
