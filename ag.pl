# -*- coding: utf-8 -*- 
# # perl 
use File::Find qw(find); 

my @video_suffix = qw(mpg avi wmv mov asx asf flv );

my $src_dir= '/tmp/mpga/';

my $mpg_target_dir = '/tmp/sa/';

my $vfiles = `ls $src_dir`;

#print $vfiles, "\n";

my @vfiles = split( /\n/, $vfiles);

foreach(@vfiles){
    my $filename = $_;
    add_subtitle($filename);

    #do_format_transfer($filename);
    #mpg_mv($filename);

}

sub mpg_mv{

    my $filename = shift @_;
    print "$filename \n" if $filename =~ /mpg$/;
    my @name_parts = split(/\./, $filename);

}

sub add_subtitle{
    my $filename = shift @_;

        #print "$filename \n";
        my $output_name = $filename;
        $output_name =~ s/\.\w+$/\.mpg/;

        my $full_input_name = $src_dir . $filename;
        my $full_output_name = $mpg_target_dir . $output_name;

        #print "$full_input_name  -->  $full_output_name  \n";



        my $cmd = <<END;
        mencoder  $full_input_name -oac copy -ovc lavc -sub /tmp/subc.srt -subcp utf-8 -utf8 -font 'WenQuanYi Micro Hei'    -o $full_output_name
END
        `$cmd`;
        #print "$cmd \n";
}
