# -*- coding: utf-8 -*- 
# # perl 
use File::Find qw(find); 

=pod
This use 
    -oac pcm
to subtitle .flv files.
=cut


my $src_dir= '/tmp/a22/';
my $subtitled_dir = '/tmp/s22/';

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
        $output_name =~ s/\.(\w+)$/_sub\.\1/;

        my $full_input_name = $src_dir . $filename;
        my $full_output_name = $subtitled_dir . $output_name;

        #print "$full_input_name  -->  $full_output_name  \n";



        my $cmd = <<END;
        mencoder  $full_input_name -oac pcm -ovc lavc -sub /tmp/subc.srt -subcp utf-8 -utf8 -font 'WenQuanYi Micro Hei'    -o $full_output_name
END
        `$cmd`;
        #print "$cmd \n";
}
