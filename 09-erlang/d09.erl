-module(d09).
-export([main/0,
	 read_input/1,
	 parse_input/2, parse_input/5,
	 flatten/1, flatten/2,
	 defrag1/1, defrag1/5,
	 defrag2/1, defrag2_from_last/1,
	 find_a_place/3,
	 checksum/1, checksum/3,
	 checksum2/1, checksum2/3,
	 solve_part_one/1,
	 solve_part_two/1]).

read_input(FileName) ->
    { ok, Binary } = file:read_file(FileName),
    Line = binary_to_list(Binary),
    ToList = lists:map(fun(X) -> X-48 end, Line),
    lists:reverse(tl(lists:reverse(ToList))).

parse_input(Input,Part) -> parse_input(Input,0,true,[],Part).
parse_input([],_,_,Acc,_) -> Acc;
parse_input([H|T],Label,File,Acc,Part) ->
    case File of
	true -> Value = Label, NextLabel = Label+1;
	false -> Value = -1, NextLabel = Label
    end,
    if
	H /= 0, Part == 1 -> NAcc = lists:append(Acc,[lists:duplicate(H,[Value])]);
	H /= 0, Part == 2 -> NAcc = Acc ++ [{H, Value}];
	true -> NAcc = Acc
    end,
    parse_input(T,NextLabel,not File,NAcc,Part).

flatten(List) -> lists:reverse(flatten(List,[])).
flatten([],Acc) -> Acc;
flatten([H|T], Acc) when is_list(H) -> flatten(T,flatten(H,Acc));
flatten([H|T], Acc) -> flatten(T,[H|Acc]).

checksum(Disk) -> checksum(Disk,0,0).
checksum([],_,Acc) -> Acc;
checksum([H|T],Index,Acc) ->
    if
	H >= 0 -> checksum(T,Index+1,Acc + (Index * H));
	true -> checksum(T,Index+1,Acc)
    end.

checksum2(Disk) -> checksum2(Disk,0,0).
checksum2([],_,Acc) -> Acc;
checksum2([{Size,Label}|Rest],Index,Acc) ->
    if
	Label >= 0 ->
	    NewValue = lists:sum(lists:map(fun(X) -> (X + Index) * Label end,lists:seq(0,Size-1))),
	    checksum2(Rest,Index+Size,Acc + NewValue);
	true -> checksum2(Rest,Index+Size,Acc)
    end.

defrag1(Disk) ->
    NbNums = length(lists:filter(fun(X) -> X >= 0 end,Disk)),
    ReversedDisk = lists:reverse(Disk),
    defrag1(Disk,ReversedDisk,0,NbNums,[]).

defrag1(_,_,Index,ToReach,Acc) when Index == ToReach -> lists:reverse(Acc);
defrag1([HB|TB],[HR|TR],Index,ToReach,Acc) ->
    if
	HB >= 0 -> defrag1(TB,[HR|TR],Index+1,ToReach,[HB|Acc]);
	HR < 0 -> defrag1([HB|TB],TR,Index,ToReach,Acc);
	true -> defrag1(TB,TR,Index+1,ToReach,[HR|Acc])
    end.

find_a_place(Block,[],_) -> {Block,[]};
find_a_place(Block,[PossiblePlace|Rest],Acc) ->
    {SizeBlock,_} = Block,
    {SizeRest,LabelRest} = PossiblePlace,
    if
	LabelRest > -1 -> find_a_place(Block,Rest,Acc ++ [PossiblePlace]);
	SizeRest < SizeBlock -> find_a_place(Block,Rest,Acc ++ [PossiblePlace]);
	SizeRest - SizeBlock == 0 ->
	    {{SizeBlock,-1}, lists:reverse(Acc ++ [Block] ++ Rest)};
	true ->
	    {{SizeBlock,-1}, lists:reverse(Acc ++ [Block] ++ [{SizeRest-SizeBlock,-1}] ++ Rest)}
    end.

defrag2_from_last([]) -> [];
defrag2_from_last([{Size,-1} | Rest]) -> [{Size,-1} | defrag2_from_last(Rest)];
defrag2_from_last([CurrentBlock | Rest]) ->
    {NewBlock, NewRest} = find_a_place(CurrentBlock, lists:reverse(Rest),[]),
    if
	NewRest == [] ->
	    [NewBlock | defrag2_from_last(Rest)];
	true ->
	    [NewBlock | defrag2_from_last(NewRest)]
    end.
defrag2(Disk) -> lists:reverse(defrag2_from_last(lists:reverse(Disk))).

solve_part_one(Disk) ->
    Checksum = checksum(defrag1(Disk)),
    io:format("Part 1: ~p~n", [Checksum]).

solve_part_two(Disk) ->
    Checksum = checksum2(defrag2(Disk)),
    io:format("Part 2: ~p~n", [Checksum]).

main() ->
    Input = read_input("../inputs/09.txt"),
    InputPart1 = flatten(parse_input(Input,1)),
    InputPart2 = parse_input(Input,2),
    solve_part_one(InputPart1),
    solve_part_two(InputPart2).
