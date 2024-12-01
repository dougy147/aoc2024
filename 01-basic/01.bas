function ReadFile( filepath as string ) as string
    dim content as string
    open filepath for binary as 1
    content = space$(lof(1))
    get #1, 1, content
    close 1
    return content
end function

function CountLines( s as string ) as integer
    dim counter as integer = 0
    for i as integer = 0 to len(s) - 1
	if ( chr(s[i]) = !"\n" ) then
	    counter = counter + 1
	end if
    next i
    return counter
end function

sub SplitStringOnChar ( s as string, c as string, destination_array(any) as string )
    dim current_word as string = ""
    dim index as integer = 0
    for i as integer = 0 to len(s) - 1
	dim current_char as string = chr(s[i])
	if ( current_char = c ) then
	    if ( not current_word = "" ) then
		destination_array(index) = current_word
		index += 1
		current_word = ""
	    end if
	    continue for
	else
	    current_word += current_char
	end if
    next i
    if ( not current_word = "" ) then
	destination_array(index) = current_word
    end if
end sub

sub PopulateLists (content_lines(any) as string, content_length as integer, left_lst(any) as integer, right_lst(any) as integer)
    for i as integer = 0 to content_length - 1
	dim splitted(2) as string
	dim current_line as string = content_lines(i)
	SplitStringOnChar(current_line, " ", splitted())
	left_lst(i) = cast(integer, splitted(0))
	right_lst(i) = cast(integer, splitted(1))
    next i
end sub

function FindSmallestValueIndex ( array(any) as integer, array_length as integer ) as integer
    dim index as integer
    dim min_value as integer = 999999 'duh
    for i as integer = 0 to array_length - 1
	if ( array(i) < min_value ) then
	    min_value = array(i)
	    index = i
	end if
    next i
    return index
end function

sub CopyArray( dest(any) as integer, source(any) as integer, array_length as integer )
    for i as integer = 0 to array_length - 1
	dest(i) = source(i)
    next i
end sub

function SolvePartOne ( left_lst(any) as integer, right_lst(any) as integer, lst_length as integer ) as integer
    dim left_copy(lst_length) as integer
    dim right_copy(lst_length) as integer
    CopyArray(left_copy(), left_lst(), lst_length)
    CopyArray(right_copy(), right_lst(), lst_length)
    dim sum as integer = 0
    for i as integer = 0 to lst_length - 1
	dim min_left_index as integer = FindSmallestValueIndex(left_copy(), lst_length)
	dim min_right_index as integer = FindSmallestValueIndex(right_copy(), lst_length)
	dim distance as integer = left_copy(min_left_index) - right_copy(min_right_index)
	if (distance < 0) then
	    distance = distance * (-1)
	end if
	sum += distance
	left_copy(min_left_index) = 999999
	right_copy(min_right_index) = 999999
    next i
    return sum
end function

function CountInList(value as integer, lst(any) as integer, lst_length as integer) as integer
    dim counter as integer = 0
    for i as integer = 0 to lst_length - 1
	if ( lst(i) = value ) then
	    counter += 1
	end if
    next i
    return counter
end function

function SolvePartTwo ( left_lst(any) as integer, right_lst(any) as integer, lst_length as integer ) as integer
    dim sum as integer = 0
    for i as integer = 0 to lst_length - 1
	dim similarity_score as integer = left_lst(i) * CountInList(left_lst(i), right_lst(), lst_length)
	sum += similarity_score
    next i
    return sum
end function

dim content as string = ReadFile("../inputs/01.txt")
dim content_length as integer = CountLines(content)
dim content_lines_array(content_length) as string
SplitStringOnChar(content, !"\n", content_lines_array())

dim left_values_lst(content_length) as integer
dim right_values_lst(content_length) as integer
PopulateLists(content_lines_array(), content_length, left_values_lst(), right_values_lst())

print "Part 1: "; SolvePartOne(left_values_lst(), right_values_lst(), content_length)
print "Part 2: "; SolvePartTwo(left_values_lst(), right_values_lst(), content_length)
