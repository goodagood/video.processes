# -*- coding: utf-8 -*- 
# # perl 
use 5.12.4;

my $vfile_name = '/home/za/Videos/materials/216/videos_for_your_cat_crickets.mp4';

my $ffcmd = "ffprobe $vfile_name 2>&1 | grep Duration";

my $out = `$ffcmd`;

say $out;
