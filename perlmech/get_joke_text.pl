#!/usr/bin/perl
use WWW::Mechanize;
use Storable;
use HTML::TreeBuilder;
require HTML::FormatText;

use utf8;

binmode STDOUT, ":utf8";

my $url = 'http://xiaohua.zol.com.cn/detail16/15129.html';


my $mech = WWW::Mechanize->new;

sub get_content{
    my $url = shift;
    $mech->get($url);

    my $tree = HTML::TreeBuilder->new_from_content($mech->content);

    if (my $div = $tree->look_down(_tag => "div", class => "lastC")) {
         my $content = $div->as_text();
         #print $div->as_text(), "\n";
         return $content;
    }
    return  "";
    #$tree->delete();
}




sub get_content2{
    my $url = 'http://xiaohua.zol.com.cn/detail16/15129.html';


    my $m = WWW::Mechanize->new;
    $m->get($url);

    my $tree = HTML::TreeBuilder->new_from_content($m->content);

    if (my $div = $tree->look_down(_tag => "div", class => "lastC")) {
         my $content = $div->as_text();
         $content = $div->as_HTML();
         my $formated = HTML::FormatText->format_string(
                        $content,
                        leftmargin => 3,
                        rightmargin => 72);
         print $formated, "\n";
         return $formated;
    }
    return  "";
    #$tree->delete();
}

get_content2();
