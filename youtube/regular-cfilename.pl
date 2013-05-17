#!/usr/bin/perl
#
my $folder = '/mnt/tos3/cswim2/';
print $ARGV[0] . "\n";
if ($ARGV[0] !~ /\/$/){
    $folder = $ARGV[0] . '/';
}else{
    $folder = $ARGV[0];
}

if (! -d $folder){
    print "not a folder: $folder \n";
    exit 1;
}

my $cname_fn = $folder . 'cname';

my $new_filename = 'a0001';

my @files = `ls $folder`;
# get rid of new-line-endding
chomp(@files);

local $/ = undef;
open( my $cname,  $cname_fn) or die "Can not open $cname_fn\n";
binmode $cname;
my $str_cname = <$cname>;
close($cname);
#print $str_cname;

foreach my $f (@files){
    my $fn = file_filter($f);
    my $nfn = '';
    if($fn){
        #print $fn;
        $nfn = make_new_filename($fn);
        rename_file($folder, $fn, $nfn);
        replace($fn, $nfn);
    }
}


open( CNAME,  ">", $cname_fn) or die "Can not open $cname_fn\n";
#open( CNAME,  ">", '/tmp/cname') or die "Can not open /tmp/cname \n";
binmode CNAME;
print CNAME  $str_cname; 
close(CNAME);


sub rename_file{
    my $folder = shift;
    my $filename = shift;
    my $new_filename = shift;

    #$folder = chomp $folder;
    #$filename = chomp $filename;
    #$new_filename = chomp $new_filename;

    my $old = $folder . $filename;
    my $new = $folder . $new_filename;
    my $cmd = "mv $old $new";
    `$cmd`;
    #print "$cmd \n";
}

sub replace{
    my $old = shift;
    my $new = shift;

    $str_cname =~ s/$old/$new/;

}

sub make_new_filename{
    my $fn = shift;

    $fn =~ s/(\.[\w\d]+$)//;
    #print "\n$fn\n";
    #print " \$1 is $1\n";
    $nfn = $new_filename . $1;
    $new_filename ++;
    #print " \$nfn is $nfn\n";

    return $nfn;

}

sub file_filter{
    my $filename = shift;
    if($filename =~ /description$/){
        `mv $filename /tmp/`;
        return '';
    }
    if($filename =~ /part$/){
        `mv $filename /tmp/`;
        return '';
    }
    if($filename =~ /\.pl$/){
        `mv $filename /tmp/`;
        return '';
    }
    return $filename;
}

=pod
=cut
