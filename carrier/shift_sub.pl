#!/usr/bin/perl
#
#my $src_subtitle = '/tmp/sd.srt';
my $src_subtitle = '/home/za/Videos/materials/carrier/s3secrets/srt3.srt';

my $out_subtitle = '/tmp/se.srt';
my $delta_time = -4;
my $delta_micro_seconds = -444;

open(my $srt_src, $src_subtitle) or die "can't open $src_subtitle! \n";
my $subtitle_text = join("", <$srt_src>);
close($srt_src);

#print $subtitle_text;

## match all time tags
my @time_tags = $subtitle_text =~ /\d+:\d+:\d+,\d{1,3}/g;

#print join(", ", @time_tags), "\n";

foreach $time_tag (@time_tags){
    my $new_time = shift_time($time_tag, $delta_time);
    $new_time = shift_micro_seconds($new_time, $delta_micro_seconds);
    $subtitle_text =~ s/$time_tag/$new_time/ ;
}

open(my $outfile, ">$out_subtitle") or die "can't open $src_subtitle! \n";
print $outfile  $subtitle_text;
close($srt_src);
#print $subtitle_text;

sub shift_time{
    my $time_tag = shift @_;
    my $delta = shift @_;

    ## You must put pattern as the first parameter:
    my @hms = split ( /:|,/, $time_tag);
    #print '@hms: ', join(":", @hms), "\n";

    my $hour   = $hms[0];
    my $minute = $hms[1];
    my $second = $hms[2];
    my $micro_seconds = $hms[3];

    $second = $second + $delta;

    if ($second >= 60) {
        $second = $second -60;
        $minute = $minute + 1;
    }
    if ($second <  0) {
        $second = $second +60;
        $minute = $minute - 1;
    }

    ## do minute, and we care not hours
    if ($minute >= 60) {
        $minute = $minute -60;
        $hour = $hour + 1;
    }
    if ($minute <  0){
        $minute = $minute +60;
        $hour = $hour - 1;
    }

    #print $time_tag, '  ', $delta, "\n";
    my $new_time = join(":", ($hour, $minute, $second));
    $new_time = $new_time . ",$micro_seconds";
    #print $time_tag, '  ', $new_time, "\n";

    return $new_time;
}

=pod
=cut

sub shift_micro_seconds{
    my $time_tag = shift @_;
    my $delta_micro_seconds = shift @_;

    ## You must put pattern as the first parameter:
    my @hms = split ( /:|,/, $time_tag);
    #print '@hms: ', join(":", @hms), "\n";

    my $hour   = $hms[0];
    my $minute = $hms[1];
    my $second = $hms[2];
    my $micro_seconds = $hms[3];

    $micro_seconds = $micro_seconds + $delta_micro_seconds;

    if ($micro_seconds >= 1000) {
        $micro_seconds = $micro_seconds -1000;
        $second = $second + 1;
    }
    if ($micro_seconds <  0) {
        $micro_seconds = $micro_seconds + 1000;
        $second = $second - 1;
    }


    ## do seconds
    if ($second >= 60) {
        $second = $second -60;
        $minute = $minute + 1;
    }
    if ($second <  0) {
        $second = $second +60;
        $minute = $minute - 1;
    }

    ## do minute,     
    if ($minute >= 60) {
        $minute = $minute -60;
        $hour = $hour + 1;
    }
    if ($minute <  0){
        $minute = $minute +60;
        $hour = $hour - 1;
    }

    ## and we care not hours, it can be 999 hours,
    ## but do make it right by hand if it becomes -1 hour

    #print $time_tag, '  ', $delta_micro_seconds, "\n";
    my $new_time = join(":", ($hour, $minute, $second));
    $new_time = $new_time . ",$micro_seconds";
    #print $time_tag, ' -->  ', $new_time, "\n";

    return $new_time;
}
