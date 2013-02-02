# -*- coding: utf-8 -*- 
# # perl 
use File::Find qw(find); 

my @video_suffix = qw(mpg avi wmv mov asx asf flv );

my $src_dir= '/tmp/fun164/';

my $mpg_target_dir = '/tmp/mpgb/';

my $vfiles = `ls $src_dir`;

#print $vfiles, "\n";

my @vfiles = split( /\n/, $vfiles);

foreach(@vfiles){
    my $filename = $_;
    do_format_transfer($filename);
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
