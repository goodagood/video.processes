use File::Copy;

while(<>){
    print($_) ;

    # this not work:
    `cd $_ && rm *pl yhb fyoutube`;

    chomp($_);
    `rm $_/*pl`;
    `rm $_/yhb`;
    `rm $_/fyoutube`;
    my $cmd = qx{mv $_ /mnt/src/};
    print "cmd is :  $cmd \n";
}
