#!/usr/bin/perl
use 5.10.0;

## Note the BOM, it will make REGEX fail
## Put at least one empty line at the beginning of the subtitle file.
#
my $src_subtitle = '/tmp/fsrt';
#my $src_subtitle = '/tmp/asrt.srt';
#my $src_subtitle = '/tmp/se.srt';
#my $src_subtitle = '/home/za/Videos/materials/carrier/csub/srt7.srt';

my $out_subtitle = '/tmp/sf.srt';
#my $out_subtitle = '/home/za/Videos/materials/carrier/csub/srt7.srt';

my $number_pat = '[\r\n]\s*[\r\n]+(\d+)\s*[\r\n]';

open(my $srt_src, $src_subtitle) or die "can't open $src_subtitle! \n";
my $subtitle_text = join("", <$srt_src>);
close($srt_src);

#print $subtitle_text;

## split the file (in $subtitle_text) to pieces, perl is good at this
## split by empty lines
my @parts = split /[\r\n]\s*[\r\n]+/, $subtitle_text;

#print join("\n--\n", @parts), "\n";

my $arranged = "";
my $i = 1;

## Finally, perl show it power.
my $new_text = "";
foreach $part (@parts){
    next if $part =~ /^[\r\n\s\D]*$/;
    ($part =~ s/^[\r\n\s]*\d+\s*[\r\n]+/\n$i\n/) or $part = "\n$i\n" . $part;
    $new_text = $new_text . $part . "\n";
    $i ++;
}

#my $new_text = join("\n", @parts);

open(my $outfile, ">$out_subtitle") or die "can't open $src_subtitle! \n";
print $outfile  $new_text;
close($srt_src);

=pod

=cut
