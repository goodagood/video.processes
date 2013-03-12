#!/usr/bin/perl
#
#my $src_subtitle = '/tmp/se.srt';
my $src_subtitle = '/home/za/Videos/materials/carrier/s3secrets/srt3.srt';

my $enough = 11;

=pod
=cut

my $time_line_pat = '.*(\d+):(\d+):(\d+)[^-]+-->\s*(\d+):(\d+):(\d+).*';



open(my $srt_src, $src_subtitle) or die "can't open $src_subtitle! \n";
#my $subtitle_text = join("", <$srt_src>);

my $cnt = 0;
my @s = ();
my @e = ();
my @t = ();

foreach $line (<$srt_src>){
    if($line =~ /$time_line_pat/g){
        #print $line if $line =~ /$time_line_pat/g;
        #print join(":", ($1,$2,$3,$4,$5,$6)), "--\n";
        #my $line =~ /$time_line_pat/g;

        my $h1 = $1;
        my $m1 = $2;
        my $s1 = $3;
        my $h2 = $4;
        my $m2 = $5;
        my $s2 = $6;

        $s[$cnt] = hms2seconds($h1,$m1,$s1);
        $e[$cnt] = hms2seconds($h2,$m2,$s2);
        $t[$cnt] = 0;
        $cnt = $cnt +1;

    }
}
close($srt_src);

for(my $i=0; $i < scalar(@s); $i++){

    next if $i == 0;
    $t[$i] = $s[$i] - $e[$i-1];

    if($t[$i] > $enough){
        print join("  ", ($s[$i],  $e[$i],  $t[$i], seconds2hms($s[$i]), seconds2hms($e[$i]))), "\n";
    }
}


sub hms2seconds{
        my $hour = shift @_;
        my $minute = shift @_;
        my $second = shift @_;

        my $seconds = (($hour * 60) + $minute) * 60 + $second;
        return $seconds;
}

sub seconds2hms{
    my $seconds = shift @_;

    my $s = $seconds % 60;

    my $ms = int($seconds / 60);
    my $m = $ms % 60;
    my $h = int($ms / 60);
    return "$h:$m:$s";
}

=pod
#print $subtitle_text;

## match all time tags
my @time_lines = $subtitle_text =~ /$time_line_pat/g;

print join(", ", @time_lines), "\n";

foreach $time_tag (@time_lines){
    my $new_time = shift_time($time_tag, $delta_time);
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
    my @hms = split ( /:/, $time_tag);
    #print '@hms: ', join(":", @hms), "\n";

    my $hour   = $hms[0];
    my $minute = $hms[1];
    my $second = $hms[2];

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
    #print $time_tag, '  ', $new_time, "\n";

    return $new_time;
}

=cut
