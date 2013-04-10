#!/usr/bin/perl
use WWW::Mechanize;
use Storable;

use HTML::TreeBuilder;
require HTML::FormatText;

use utf8;
binmode STDOUT, ":utf8";

=pod
get joke from :
my $baseurl = 'http://xiaohua.zol.com.cn';
=cut

my $pageurl = 'http://xiaohua.zol.com.cn/list.php';
my $baseurl = 'http://xiaohua.zol.com.cn';
my $m = WWW::Mechanize->new();
open my $webs, ">/tmp/webs" or die "Can't open /tmp/webs";
binmode  $webs, ":utf8";
while($pageurl){
    $m->get($pageurl);

    my @links = $m->links();
    my $c = $m->content;
    my $uurl='';

    for my $link (@links){
        $uurl = $link->url;
        if ($uurl =~ /\/detail/ ){
            my $content = get_content( $base . $uurl);
            #printf $webs "%s, %s\n", $link->text, $link->url;
            printf $webs $content;
            printf $webs "\n\n==========\n\n";
        }
        if ( $link->text =~ /下一页/){
            printf  "%s, %s\n", $link->text, $link->url;
            $pageurl = $base . $link->url;
        }
        else{
            $pageurl = '';
        }
        #$pageurl = ''; #stop loop


    }
}
close $webs;


sub get_content{
    my $url = shift;
    $m->get($url);

    my $tree = HTML::TreeBuilder->new_from_content($m->content);

    if (my $div = $tree->look_down(_tag => "div", class => "lastC")) {
         #my $content = $div->as_text();
         my $content = $div->as_HTML();
         my $formated = HTML::FormatText->format_string(
                        $content,
                        leftmargin => 3,
                        rightmargin => 72);
                    #print $formated, "\n";
         return $formated;
    }
    return  "";
    #$tree->delete();
}



=pod
my $formatter = HTML::FormatText->format_string(
                $file,
                leftmargin => 3,
                rightmargin => 72);
print $formatter;
=cut
