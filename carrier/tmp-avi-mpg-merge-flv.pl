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
my $afile = '/home/za/Videos/materials/carrier/s3secrets/av0111.avi';
my $bfile = '/home/za/Videos/materials/carrier/s3secrets/avad1.avi';
my $cfile = '/home/za/Videos/materials/carrier/s3secrets/av0358.avi';
my $dfile = '/home/za/Videos/materials/carrier/s3secrets/avad2.avi';

my $mafile = '/tmp/av0111.mpg';
my $mbfile = '/tmp/avad1.mpg';
my $mcfile = '/tmp/av0358.mpg';
my $mdfile = '/tmp/avad2.mpg';

my $out_mpg = '/tmp/out.mpg';
my $out_avi = '/tmp/out.avi';
my $out_flv = '/tmp/out.flv';

my @all_avis = ($afile, $bfile, $cfile, $dfile);
my @all_mpgs = ($mafile, $mbfile, $mcfile, $mdfile);

for(my $i=0; $i<4; $i++){
    my $cmd = "ffmpeg -y -i $all_avis[$i] -sameq $all_mpgs[$i]";
    `$cmd`;
    #print $cmd . "\n";

}

`cat $mafile $mbfile $mcfile $mdfile > $out_mpg`;


`ffmpeg -y -i $out_mpg  -sameq $out_avi`;
`ffmpeg -y -i $out_mpg  -sameq $out_flv`;




=pod
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
=cut
