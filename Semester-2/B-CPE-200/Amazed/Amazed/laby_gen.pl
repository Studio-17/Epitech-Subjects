#!/usr/bin/perl -w


use strict;

# gmin.pl taille densite nb home name end name
if (scalar @ARGV < 3)
{
    print "usage : laby_gen.pl size density nb_of_robots\nWhen size is the number of rooms and density the percentage of probability of connexions between rooms\n";
    exit -1;
}

my $i = 0;
my $j = 0;

my $size = shift @ARGV;
my $density = int(shift @ARGV);
my $nb = int(shift @ARGV);

my $home = int(rand($size));
my $end  = int(rand($size));
while ($end == $home)
{
    my $end  = int(rand($size));
}

print $nb . "\n";
while ($i < $size)
{
    print "##start\n" if ($i == $home);
    print "##end\n" if ($i == $end);
    print $i;
    print " " . int(rand(10 * $size));
    print " " . int(rand(10 * $size));
    print "\n";
    $i++;
}

$i = 0;

while ($i < $size)
{
    $j = 0;
    while ($j < $size)
    {
	if ($density > int(rand(100)))
	{
	    print $i . "-" . $j . "\n";
	}
	$j++;
    }
    $i++;
}