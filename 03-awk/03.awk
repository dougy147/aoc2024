BEGIN {
    input[any]
    read_file("../inputs/03.txt")
    solve_part_one(input)
    solve_part_two(input)
}

function read_file(filepath) {
    while ((getline data < filepath) > 0) input[length(input)] = data
}

function get_matches(str) {
    if ( match(str, /mul\([0-9]{1,3},[0-9]{1,3}\)/) ) {
	matches[length(matches)] = substr(str, RSTART, RLENGTH)
	get_matches(substr(str, RSTART+RLENGTH, length(str)))
    }
}

function get_matches2(input_string) {
    if (input_string == "") return
    if (match(input_string, /^(do\(\)|don't\(\))/, dos)) {
	if (dos[1] == "do()") inst = 1
	else inst = 0
	get_matches2(substr(input_string,RLENGTH,length(input_string)))
    }
    else if ( match(input_string, /^mul\([0-9]{1,3},[0-9]{1,3}\)/) ) {
	if (inst) matches2[length(matches2)] = substr(input_string, RSTART, RLENGTH)
	get_matches2(substr(input_string,RLENGTH,length(input_string)))
    }
    else get_matches2(substr(input_string, 2, length(input_string)))
}

function multiply_pair(pair) {
    match(pair, /mul\(([0-9]{1,3}),([0-9]{1,3})\)/, nums)
    return nums[1] * nums[2]
}

function solve_part_one(data) {
    matches[any]
    for (d = 1; d < length(data); d++) get_matches(data[d])
    for (i = 1; i < length(matches); i++) sum += multiply_pair(matches[i])
    print "Part 1: " sum
}

function solve_part_two(data) {
    matches2[any]
    inst = 1
    for (d = 1; d < length(data); d++) get_matches2(data[d])
    sum = 0
    for (i = 1; i < length(matches2); i++) sum += multiply_pair(matches2[i])
    print "Part 2: " sum
}
