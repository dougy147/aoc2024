program Day4;
{$mode objfpc}
uses Sysutils;

const
    InputWidth = 140;
    InputHeight = 140;
    InputFile = '../inputs/04.txt';
    Directions: Array[1..8,1..2] of Integer = (
	(-1,0),  { N  }
	(-1,1),  { NE }
	(0,1),   { E  }
	(1,1),   { SE }
	(1,0),   { S  }
	(1,-1),  { SW }
	(0,-1),  { W  }
	(-1,-1)  { NW }
    );
    Diagonals: Array[1..4,1..2] of Integer = ((-1,-1), (-1,1), (1,1), (1,-1));

type
    WordsMap = Array[1..InputHeight, 1..InputWidth] of Char;

var
    inputTxt: TextFile;
    inputLine, s: String;
    words: WordsMap;
    i, j, k, row, d: Integer;
    nextRowIndex, nextColIndex: Integer;
    counter: Integer;
    match: Boolean;

procedure ReadFile(InputFile: String);
begin
    AssignFile(inputTxt, InputFile);
    reset(inputTxt);
    row := 1;
    while not eof(inputTxt) do
    begin
	readln(inputTxt,inputLine);
	for i := 1 to length(inputLine) do
	    words[row][i] := inputLine[i];
	Inc(row);
    end;
    CloseFile(inputTxt);
end;

procedure SolvePartOne(Words: WordsMap);
begin
    for i := 1 to InputHeight do begin
	for j := 1 to InputWidth do begin
	    if (Words[i][j] = 'X') then begin
		for d := 1 to 8 do begin
		    match := true;
		    for k := 1 to 3 do begin
			nextRowIndex := i + (k * Directions[d][1]);
			nextColIndex := j + (k * Directions[d][2]);
			if (nextRowIndex < 1) or (InputHeight < nextRowIndex) then begin
			    match := false; break;
			end;
			if (nextColIndex < 1) or (InputWidth < nextColIndex) then begin
			    match := false; break;
			end;
			if (CompareText('XMAS'[k+1], Words[nextRowIndex][nextColIndex]) <> 0) then begin
			    match := false; break;
			end;
		    end;
		    if match = true then Inc(counter);
		end;
	    end;
	end;
    end;
    writeln('Part 1: ', counter);
end;

procedure SolvePartTwo(Words: WordsMap);
begin
    counter := 0;
    for i := 2 to InputHeight - 1 do begin
	for j := 2 to InputWidth - 1 do begin
	    if (Words[i][j] = 'A') then begin
		s := '';
		for d := 1 to 4 do
		    s += Words[i+Diagonals[d][1]][j+Diagonals[d][2]];
		if (CompareText(s,'MMSS') = 0) or
		   (CompareText(s,'MSSM') = 0) or
		   (CompareText(s,'SMMS') = 0) or
		   (CompareText(s,'SSMM') = 0) then Inc(counter);
	    end;
	end;
    end;
    writeln('Part 2: ', counter);
end;

begin
    ReadFile(InputFile);
    SolvePartOne(words);
    SolvePartTwo(words);
end.
