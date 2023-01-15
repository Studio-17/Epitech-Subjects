#!/usr/bin/perl -w

if
    ((scalar @ARGV) != 3)
{
    print "program x y density\n";
    exit;
}

my $x = $ARGV[0];
my $y = $ARGV[1];
my $density = $ARGV[2];
my $i = 0;
my $j = 0;

print $y . "\n";


while ($i < $y)
{
    $j = 0;

    while ($j < $x)
    {
	if (int(rand(100)) <= $density)
	{
	    print "o";
	}
	else
	{
	    print ".";
	}
	$j++;
    }
    print "\n";
    $i++;
}