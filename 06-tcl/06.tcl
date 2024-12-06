set grid []
set agent []

array set directions {}
set directions("^") {-1 0}
set directions(">") {0 1}
set directions("v") {1 0}
set directions("<") {0 -1}

array set rotate {}
set rotate("^") ">"
set rotate(">") "v"
set rotate("v") "<"
set rotate("<") "^"

proc read_file { filepath } {
    set fp [open $filepath r]
    set content [read $fp]
    return $content
}

proc is_on_grid { agent grid } {
    set x [lindex $agent 1]; set y [lindex $agent 2]
    set lgrid [llength $grid]
    if { $lgrid <= $x || $x < 0 } { return "0" }
    if { $lgrid <= $y || $y < 0 } { return "0" }
    return "1"
}

proc move_or_rotate { agent grid } {
    global directions rotate
    set s [lindex $agent 0]; set x [lindex $agent 1]; set y [lindex $agent 2]
    set ns $s
    set nx [expr { $x + [lindex $directions("$s") 0]}]
    set ny [expr { $y + [lindex $directions("$s") 1]}]
    if { ! [is_on_grid [list $s $nx $ny] $grid] } { return [list $s $nx $ny ] }
    if { [lindex $grid $nx $ny] == "#" } {
	set ns $rotate("$s")
	set nx $x
	set ny $y
    }
    return [list $ns $nx $ny ]
}

proc part_one { agent grid } {
    while { [is_on_grid $agent $grid] } {
	set key "[lindex $agent 1] [lindex $agent 2]"
	set visited($key) 1
	set agent [move_or_rotate $agent $grid]
    }
    puts "Part 1: [array size visited]"
}

proc loop { agent grid } {
    while { [is_on_grid $agent $grid] } {
	if {[info exists visited("$agent")]} {return "1"}
	set visited("$agent") 1
	set agent [move_or_rotate $agent $grid]
    }
    return "0"
}

proc part_two { agent grid } {
    set start $agent
    while { [is_on_grid $agent $grid] } {
	set key "[lindex $agent 1] [lindex $agent 2]"
	set parkour($key) 1
	set agent [move_or_rotate $agent $grid]
    }
    set counter 0
    foreach key [array names parkour] {
	set agent $start
	set x [lindex $key 0]
	set y [lindex $key 1]
	if {$x == [lindex $agent 1] && $y == [lindex $agent 2]} { continue }
	lset grid $x $y "#"
	if { [loop $agent $grid] } { incr counter }
	lset grid $x $y "."
    }
    puts "Part 2: $counter"
}

set input [read_file "../inputs/06.txt"]
foreach c [split $input ""] {
    if { $c == "^" } { set agent [list "^" $row $col] }
    if { $c != "\n" } { incr col; lappend curline $c } { lappend grid $curline; set curline {}; set col 0; incr row }
}

part_one $agent $grid
part_two $agent $grid
