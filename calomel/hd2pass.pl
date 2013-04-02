# -*- coding: utf-8 -*- 
# # perl 

#my $src_dir= '/home/za/vids/src/';
my $src_dir= '/mnt/sadia/';


#my $subtitled_dir = '/tmp/s5/';
#my $subtitled_dir = '/home/za/vids/subed/';
my $subtitled_dir = '/mnt/subed/';

#my $subtitle = '/home/za/workspace/videos/asrt.srt';
my $subtitle = '/home/ubuntu/workspace/video.processes/asrt.srt';

# ----
my $vfiles = `ls $src_dir`;
#print $vfiles, "\n";

@vfiles = split( /\n/, $vfiles);

foreach(@vfiles){
    my $filename = $_;

    add_subtitle($filename);
    sleep 10;

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

    # Note: I DID NOT drop out sound for sky-lapse videos:

=pod
    my $cmd = <<END;
mencoder  $full_input_name -o $full_output_name -oac lavc -ovc lavc -lavcopts autoaspect -sub $subtitle  -utf8 -font 'WenQuanYi Micro Hei'
END

    `$cmd`;
    #print "$pass1cmd \n". "$pass2cmd \n";
=cut

    my $pass1cmd = "mencoder  $full_input_name -o /dev/null -oac lavc -ovc lavc -lavcopts autoaspect:vpass=1 -sub $subtitle  -utf8 -font 'WenQuanYi Micro Hei' ";

    # br=512 is not allowed in mp2 error:
    #my $pass2cmd = "mencoder  $full_input_name -o $full_output_name -oac lavc -ovc lavc -lavcopts vbitrate=15900:abitrate=512:autoaspect:vpass=2 -sub $subtitle  -utf8 -font 'WenQuanYi Micro Hei' ";

    my $pass2cmd = "mencoder  $full_input_name -o $full_output_name -oac lavc -ovc lavc -lavcopts vbitrate=15900:autoaspect:vpass=2 -sub $subtitle  -utf8 -font 'WenQuanYi Micro Hei' ";

    #`$pass1cmd`;
    #`$pass2cmd`;
    #print "$pass1cmd \n". "$pass2cmd \n";

    my $cmd = "$pass1cmd && $pass2cmd";
    #print $cmd, "\n";
    print "\ndoing: $full_input_name \n--> $full_output_name \n";
    system($cmd);

}
