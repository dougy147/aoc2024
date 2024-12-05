with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;
with Ada.Containers; use Ada.Containers;
with Ada.Containers.Vectors;

with Ada.Containers.Indefinite_Hashed_Maps;
with Ada.Strings.Hash;

procedure Aoc_2024_05 is
    Input_File: constant String := "../inputs/05.txt";

    package Integer_Vector is new
    Ada.Containers.Vectors
	(Index_Type => Natural,
	Element_Type => Integer);
    use Integer_Vector;

    package Integer_Hashed_Maps is new
    Ada.Containers.Indefinite_Hashed_Maps
	(Key_Type => String,
	Element_Type => Vector,
	Hash => Ada.Strings.Hash,
	Equivalent_Keys => "=");
    use Integer_Hashed_Maps;

    Orders: Map := Empty_Map;

    function Split_On_Char(Str: Unbounded_String; Delim: Character) return Vector is
	V: Vector := Empty;
	S: Unbounded_String;
	C: Character;
    begin
	for I in 1 .. Length(Str) loop
	    C := To_String(Str)(I);
	    if C = Delim then
		V.Append(Integer'Value(To_String(S)));
		S := To_Unbounded_String("");
	    else
		S := S & C;
		if I = Length(Str) then
		    V.Append(Integer'Value(To_String(S)));
		end if;
	    end if;
	end loop;
	return V;
    end;

    function Get_Middle_Value(U: Vector) return Integer is
    begin
	return U(Integer(Length(U)) / 2);
    end;

    function Is_Valid(Update: Vector) return Boolean is
	Secondings: Vector;
	X, Y: Integer;
	Match: Boolean;
    begin
	for I in 0..Length(Update)-1 loop
	    Match := False;
	    for J in I+1..Length(Update)-1 loop
		if (not Orders.Contains(Integer'Image(Update(Integer(I))))) then
		    return False;
		end if;
		Secondings := Orders(Integer'Image(Update(Integer(I))));
		X := Update(Integer(J));
		for K in 0..Length(Secondings)-1 loop
		    Y := Secondings(Integer(K));
		    if (X = Y) then
			Match := True;
		    end if;
		end loop;
		if Match = False then
		    return False;
		end if;
	    end loop;
	end loop;
	return True;
    end;

    function Is_In_Vector(X: Integer; V: Vector) return Boolean is
    begin
	for I in 0..Length(V)-1 loop
	    if X = V(Integer(I)) then
		return True;
	    end if;
	end loop;
	return False;
    end;

    function Order_Incorrect_Update(U: Vector) return Vector is
	Indexes, Reordered, Secondings: Vector := Empty;
	K: Unbounded_String;
	Y, Z: Integer;
    begin
	for I in 0..Length(U)-1 loop
	    Indexes.Append(0);
	    Reordered.Append(0);
	end loop;

	for I in 0..Length(U)-1 loop
	    for J in 0..Length(U)-1 loop
		if I = J then
		    null;
		else
		    K := To_Unbounded_String(Integer'Image(U(Integer(I))));
		    if Orders.Contains(To_String(K)) then
			Secondings := Orders(To_String(K));
			Y := U(Integer(J));
			if Is_In_Vector(Y,Secondings) then
			    Indexes(Integer(J)) := Indexes(Integer(J)) + 1;
			end if;
		    end if;
		end if;
	    end loop;
	end loop;

	for I in 0..Length(Indexes)-1 loop
	    Reordered(Indexes(Integer(I))) := U(Integer(I));
	end loop;
	return Reordered;
    end;

    procedure Read_File(File_Name: String) is
	F: File_Type;
	Parsing_Rules: Boolean := True;
	Input_Line: Unbounded_String;
	Pair, Update, V: Vector;
	K: Unbounded_String;
	Part_One_Res, Part_Two_Res: Integer := 0;

    begin
	Open(F, In_File, File_Name);
	while not End_Of_File(F) loop
	    <<Ignore_Empty_Line>>
	    Input_Line := To_Unbounded_String(Get_Line(F));
	    V := Empty;

	    if (To_String(Input_Line) = "") then
		Parsing_Rules := False;
		goto Ignore_Empty_Line;
	    end if;

	    if (Parsing_Rules) then
		Pair := Split_On_Char(Input_Line,'|');
		K := To_Unbounded_String(Integer'Image(Pair(0)));
		if (Orders.Contains(To_String(K))) then
		    V := Orders.Element(To_String(K));
		end if;
		V.Append(Pair(1));
		Orders.Include(To_String(K), V);
	    end if;

	    if (not Parsing_Rules) then
		Update := Split_On_Char(Input_Line,',');
		if Is_Valid(Update) then
		    Part_One_Res := Part_One_Res + Get_Middle_Value(Update);
		else
		    Part_Two_Res := Part_Two_Res + Get_Middle_Value(Order_Incorrect_Update(Update));
		end if;
	    end if;
	end loop;
	Close(F);
	Put_Line("Part 1: " & Integer'Image(Part_One_Res));
	Put_Line("Part 2: " & Integer'Image(Part_Two_Res));
    end Read_File;

begin
    Read_File(Input_File);
end Aoc_2024_05;
