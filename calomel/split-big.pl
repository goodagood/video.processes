# -*- coding: utf-8 -*- 
# # perl 

my $src_dir= '/home/za/vids/src/';
my $src_dir= '/tmp/pbb/';

my $seconds = 240;


# ----
my $vfiles = `ls $src_dir`;
#print $vfiles, "\n";

@vfiles = split( /\n/, $vfiles);

foreach(@vfiles){
    my $filename = $_;
    my $full_name = $src_dir . $filename;

    `python  /home/za/workspace/videos/calomel/ffmpeg-split.py  -f  $full_name  -s $seconds`;
    `rm $full_name`;
    #add_subtitle($filename);
    sleep 10;

}

