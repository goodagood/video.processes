# -*- coding: utf-8 -*- 
# # perl 
use File::Find qw(find); 

#my $src_dir= '/home/za/Videos/materials/223b/';
#my $src_dir= '/home/za/Videos/materials/sky-time-lapse224/';
my $src_dir= '/tmp/tla/';

my $subtitled_dir = '/tmp/s3/';

my $subtitle = '/tmp/asrt.srt';

# ----
my $vfiles = `ls $src_dir`;
#print $vfiles, "\n";

@vfiles = split( /\n/, $vfiles);

foreach(@vfiles){
    my $filename = $_;

    add_subtitle($filename);

}



sub add_subtitle{
    my $filename = shift @_;

    #print "$filename \n";
    my $output_name = $filename;
    # add '-sub' suffix to output file name:
    #$output_name =~ s/(\.\w+)$/-sub\1/;

    # note we use $src_dir
    my $full_input_name = $src_dir . $filename;
    my $full_output_name = $subtitled_dir . $output_name;

    #print "$full_input_name  -->  $full_output_name  \n";

    # Note: I drop out sound for sky-lapse videos:

=pod
    my $cmd = <<END;
mencoder  $full_input_name -o $full_output_name -oac lavc -ovc lavc -lavcopts autoaspect -sub $subtitle  -utf8 -font 'WenQuanYi Micro Hei'
END

    `$cmd`;
    #print "$pass1cmd \n". "$pass2cmd \n";
=cut

    my $pass1cmd = <<END;
mencoder  $full_input_name -o /dev/null -nosound -ovc lavc -lavcopts autoaspect:vpass=1 -sub $subtitle  -utf8 -font 'WenQuanYi Micro Hei'
END

    my $pass2cmd = <<END;
mencoder  $full_input_name -o $full_output_name -nosound -ovc lavc -lavcopts vbitrate=8800:autoaspect:vpass=2 -sub $subtitle  -utf8 -font 'WenQuanYi Micro Hei'
END

    `$pass1cmd`;
    `$pass2cmd`;
    #print "$pass1cmd \n". "$pass2cmd \n";

}
