#!/usr/bin/perl
#

my $taga = <<END;
1
00:00:31,688 --> 00:00:35,388
上网开会  goodagood.com
END

print dhms2sec(8888), "\n";
print dhms2sec("1:1:1:1"), "\n";



sub dhms2sec {
   my $in = shift;
   $in =~ s/(and|,|:)//g;
   $in =~ s/(\w+)s/\1/g;
   my %y = reverse split(/\s+/,$in);
   return ($y{'second'}) +
          ($y{'minute'} * 60) +
          ($y{'hour'}   * 60*60) +
          ($y{'day'}    * 60*60*24);
}

my $ta = "2 days, 6 hours, 32 minutes and 44 seconds" ;
print dhms2sec($ta), "\n";
