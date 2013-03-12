# -*- coding: utf-8 -*- 
# # perl 
use File::Find qw(find); 

my @video_suffix = qw(mpg avi wmv mov asx asf flv );

my $src_dir= '/tmp/a5/';

my $mpg_target_dir = '/tmp/a5/';

my $subtitled_dir = '/tmp/s5/';

# ----
my $vfiles = `ls $src_dir`;
#print $vfiles, "\n";

@vfiles = split( /\n/, $vfiles);

foreach(@vfiles){
    my $filename = $_;
    #do_format_transfer($filename);
    #mpg_mv($filename);

    #add_subtitle($filename);

}

sub get_vbitrate{
    #my $duration_line = `ffprobe $full_file_name 2>&1 | grep Duration`;
}

# ----
# 2nd pass, to add subtitles:
$vm_files = `ls $mpg_target_dir`;

#print $vfiles, "\n";

@vm_files = split( /\n/, $vm_files);

foreach(@vm_files){
    my $filename = $_;

    #add_subtitle($filename);
    #do_format_transfer($filename);
    #mpg_mv($filename);

}

sub mpg_mv{

    my $filename = shift @_;
    print "$filename \n" if $filename =~ /mpg$/;
    my @name_parts = split(/\./, $filename);

}

sub do_format_transfer{
    my $filename = shift @_;
    if(not $filename =~ /mpg$/){
        #print "$filename \n";
        my $output_name = $filename;
        $output_name =~ s/\.\w+$/\.mpg/;

        my $full_input_name = $src_dir . $filename;
        my $full_output_name = $mpg_target_dir . $output_name;

        #print "$full_input_name  -->  $full_output_name  \n";

        my $cmd = "ffmpeg -i $full_input_name  -sameq $full_output_name";
        `$cmd`;
        #print "$cmd \n";
    }
}


sub add_subtitle{
    my $filename = shift @_;

    #print "$filename \n";
    my $output_name = $filename;
    $output_name =~ s/(\.\w+)$/-sub\1/;

    # note we use $mpg_target_dir
    my $full_input_name = $mpg_target_dir . $filename;
    my $full_output_name = $subtitled_dir . $output_name;

    #print "$full_input_name  -->  $full_output_name  \n";



=pod
    my $cmd = <<END;
mencoder  $full_input_name -oac copy -ovc lavc -sub /tmp/subc.srt -subcp utf-8 -utf8 -font 'WenQuanYi Micro Hei'    -o $full_output_name
END
=cut

    my $cmd = <<END;
mencoder  $full_input_name -o $full_output_name -oac lavc -ovc lavc -lavcopts autoaspect -sub /tmp/asrt.srt  -utf8 -font 'WenQuanYi Micro Hei'
END

    `$cmd`;
    #print "$cmd \n";
}
