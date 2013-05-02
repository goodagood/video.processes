# -*- coding: utf-8 -*- 
# # perl 
use warnings;
use strict;


my $basedir = '/media/my/';

find_dirs($basedir);


sub find_dirs{
    my $base = shift;

    if(!$base){
        return;
    }

    my $abs_path = find_waiting_dir($base);
    while( $abs_path ){
        print $abs_path . "  -- going to do youtubedl.\n"; 
        system("cd $abs_path && perl autoyoutubedl.pl");
        $abs_path = find_waiting_dir($base);

    }

}


sub find_waiting_dir{
    my $base = shift;

    opendir(my $mydir, $base) or die $!;
    my $file = readdir($mydir)
    while( $file ){
        next unless(-d $base.$file);
        next if($file =~ /^\.+$/);
        #print $file . "\n";

        my $abs_path = $base . $file;
        if( is_waiting_dir($abs_path) == 1){
            print $abs_path . "  -- going to do youtubedl.\n"; 
            return $abs_path;
        }else{
            print "This is not todo dir: $abs_path \n";
        }


    }
    close($mydir);
    return 0;
}


sub is_waiting_dir{
    my $dir = shift;
    #print "\$dir : $dir \n";

    my $yhb = 0;
    my $video_file = 0;

    $yhb = 1 if (-f "$dir/yhb");

    my $filenames = `ls $dir`;
    
    #print $filenames . "\n";
    #return 1;

    if( $yhb != 1){
        return 0;
    }

    if ( has_video($filenames) == 0){
        return 1;
    }

    return 0;
}


sub has_video{
    my $filenames = shift;
    return 1 if ($filenames =~ /\bwebm\b/);
    return 1 if ($filenames =~ /\bmp4\b/);
    return 1 if ($filenames =~ /\bflv\b/);
    return 0;
}

