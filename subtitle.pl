# -*- coding: utf-8 -*- 
# # perl 
use File::Find qw(find); 

=pod
Add subtitles to all files in '$src_dir', the produced files will be in
in '$subtitled_dir'

This is same as 'sub_pcm.pl' and 'psubtitle.pl', but simplified the 
command line options for 'mencoder'.

This use 
    -oac lavc
to add subtitle to .flv files, tested on FLV files.

The subtitle file is currently '/home/za/tmp/suba.srt'.
=cut


#my $src_dir= '/tmp/a2/';
my $src_dir= '/home/za/Videos/materials/216/';
my $subtitled_dir = '/tmp/s2/';
my $subtitle_srt_file = '/tmp/asrt.srt';
#my $subtitle_srt_file = '/home/za/Videos/materials/carrier/subtitle.srt';
#my $subtitle_srt_file = '/home/za/workspace/videos/suba.srt';

# finished settings.
# ------------------

my $vfiles = `ls $src_dir`;

#print $vfiles, "\n";

my @vfiles = split( /\n/, $vfiles);

foreach(@vfiles){
    my $filename = $_;
    add_subtitle($filename);

}


sub add_subtitle{
    my $filename = shift @_;

    #print "$filename \n";
    my $output_name = $filename;
    $output_name =~ s/\.(\w+)$/sub\.\1/;

    my $full_input_name = $src_dir . $filename;
    my $full_output_name = $subtitled_dir . $output_name;

    #print "$full_input_name  -->  $full_output_name  \n";


=pod
    my $cmd = <<END;
    mencoder  $full_input_name -oac pcm -ovc lavc -sub /tmp/subc.srt -subcp utf-8 -utf8 -font 'WenQuanYi Micro Hei'    -o $full_output_name
END
=cut

    my $cmd = <<END;
mencoder  $full_input_name -o $full_output_name -oac lavc -ovc lavc -lavcopts autoaspect -sub $subtitle_srt_file -utf8 -font 'WenQuanYi Micro Hei'
END


    `$cmd`;
    #print "$cmd \n";
}
