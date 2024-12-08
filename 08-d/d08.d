import std.stdio;
import std.file;
import std.conv;

string filepath = "../inputs/08.txt";
int grid_height, grid_width;

struct Location
{
    int x,y;
}

Location[][string] parse_input(string filepath)
{
    Location[][string] antennas;
    int col, row = 0;
    foreach (c;readText(filepath)) {
	if (c == '\n') { row++; grid_width = col; col = -1; }
	else if (c != '.') {
	    Location antenna;
	    antenna.x = row;
	    antenna.y = col;
	    antennas[to!string(c)] ~= antenna;
	}
	col++;
    }
    grid_height = row;
    return antennas;
}

bool is_in_grid(Location antinode)
{
    int x = antinode.x; int y = antinode.y;
    if (x < 0 || x >= grid_height) return false;
    if (y < 0 || y >= grid_width) return false;
    return true;
}

Location[] compute_antinode(Location ant1, Location ant2)
{
    int dist_x = ant1.x - ant2.x;
    int dist_y = ant1.y - ant2.y;
    Location antinode1;
    Location antinode2;
    antinode1.x = ant1.x + dist_x; antinode1.y = ant1.y + dist_y;
    antinode2.x = ant2.x - dist_x; antinode2.y = ant2.y - dist_y;
    Location[] antinodes;
    if (is_in_grid(antinode1)) antinodes ~= antinode1;
    if (is_in_grid(antinode2)) antinodes ~= antinode2;
    return antinodes;
}

Location[] generate_antinodes(Location antinode, int direction, int x, int y, int dx, int dy)
{
    Location[] antinodes;
    int i = direction;
    while (is_in_grid(antinode)) {
        antinodes ~= antinode;
	i+=direction;
        antinode.x = x + dx * i;
        antinode.y = y + dy * i;
    }
    return antinodes;
}

Location[] compute_antinode_2(Location ant1, Location ant2)
{
    int dist_x = ant1.x - ant2.x;
    int dist_y = ant1.y - ant2.y;
    Location antinode1;
    Location antinode2;
    antinode1.x = ant1.x + dist_x; antinode1.y = ant1.y + dist_y;
    antinode2.x = ant2.x - dist_x; antinode2.y = ant2.y - dist_y;
    Location[] antinodes = [ant1,ant2];
    antinodes = antinodes ~ generate_antinodes(antinode1, 1, ant1.x, ant1.y, dist_x, dist_y);
    antinodes = antinodes ~ generate_antinodes(antinode2, 1, ant2.x, ant2.y, dist_x, dist_y);
    antinodes = antinodes ~ generate_antinodes(antinode1, -1, ant1.x, ant1.y, dist_x, dist_y);
    antinodes = antinodes ~ generate_antinodes(antinode2, -1, ant2.x, ant2.y, dist_x, dist_y);
    return antinodes;
}

void solve(Location[][string] antennas)
{
    int[Location] antinodes_part1;
    int[Location] antinodes_part2;
    foreach(freq; antennas.byKey()) {
	for(int i = 0; i < antennas[freq].length; i++) {
	    Location ant1 = antennas[freq][i];
	    for(int j = i+1; j < antennas[freq].length; j++) {
		Location ant2 = antennas[freq][j];
		if (ant1 == ant2) { continue;}
		foreach(antinode; compute_antinode(ant1,ant2)) {
		    antinodes_part1[antinode] = 1;
		}
		foreach(antinode; compute_antinode_2(ant1,ant2)) {
		    antinodes_part2[antinode] = 1;
		}
	    }
	}
    }
    writeln("Part 1: ",antinodes_part1.length);
    writeln("Part 2: ",antinodes_part2.length);
}

void main()
{
    Location[][string] antennas = parse_input(filepath);
    solve(antennas);
}
