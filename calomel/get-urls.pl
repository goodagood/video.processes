# xurl - extract unique, sorted list of links from URL
use HTML::LinkExtor;
use LWP::Simple;

$base_url = shift;
$parser = HTML::LinkExtor->new(undef, $base_url);
$parser->parse(get($base_url))->eof;
@links = $parser->links;
print "\nlinks:\n @links \n";
foreach $linkarray (@links) {

    my @element  = @$linkarray;
    print "\n @element \n";
    my $elt_type = shift @element;
    while (@element) {
        my ($attr_name , $attr_value) = splice(@element, 0, 2);
        $seen{$attr_value}++;
    }
}
for (sort keys %seen) { print $_, "\n" }
