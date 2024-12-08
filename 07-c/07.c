#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define FILEPATH "../inputs/07.txt"
#define MAXBUF 50

typedef struct {
    long target;
    int sindex;
    long sources[MAXBUF];
} Equation;

long solve_line(long target, long sources[], int iteration, int max, long stack, int concat_bool) {
    if (stack > target) return 0;
    if (iteration == max) return stack == target ? target : 0;

    long res1 = solve_line(target,sources,iteration+1,max,stack+sources[iteration],concat_bool);
    if (res1 == target) return target;
    long res2 = solve_line(target,sources,iteration+1,max,stack*sources[iteration],concat_bool);
    if (res2 == target) return target;

    if (concat_bool) {
	char str_stack[MAXBUF];
    	char str_source[MAXBUF];
    	sprintf(str_stack, "%ld",stack);
    	sprintf(str_source, "%ld",sources[iteration]);
    	strcat(str_stack,str_source);
    	long res3 = solve_line(target,sources,iteration+1,max,strtol(str_stack,NULL,10),concat_bool);
    	if (res3 == target) { return target; }
    }
}

void solve(Equation equations[], size_t equations_count) {
    long part1 = 0;
    long part2 = 0;
    for (int i = 0; i < equations_count; i++) {
	long t = equations[i].target;
	long x = solve_line(equations[i].target, equations[i].sources, 1, equations[i].sindex, equations[i].sources[0], 0);
	if (x == t) {
	    part1+=x;
	    part2+=x;
	} else {
	    x = solve_line(equations[i].target, equations[i].sources, 1, equations[i].sindex, equations[i].sources[0], 1);
	    if (x == t) part2+=x;
	}
    }
    printf("Part 1: %ld\n", part1);
    printf("Part 2: %ld\n", part2);
}

size_t count_equations(char filepath[]) {
    FILE *f = fopen(FILEPATH,"r");
    char buf[MAXBUF] = {0};
    size_t counter = 0;
    char x;
    while ((x = fgetc(f)) != EOF) {
	if (x == '\n') { counter++; }
    }
    fclose(f);
    return counter;
}

void parse_input(char filepath[], Equation *equations) {
    FILE *f = fopen(FILEPATH,"r");
    char buf[MAXBUF] = {0};
    fopen(FILEPATH,"r");

    long equations_index = 0;
    while (fgets(buf,MAXBUF,f)) {
	Equation equation = {0};
	char line[MAXBUF];
	char target[MAXBUF];

	buf[strcspn(buf,"\n")] = 0;

	strcpy(target,buf);
	target[strcspn(target,":")] = 0;
	equation.target = strtol(target,NULL,10);

	char vals[MAXBUF];
	strncpy(vals,buf + (strlen(target)+2),strlen(buf));

	char *ch;
	ch = strtok(vals, " ");
	while (ch != NULL) {
	    equation.sources[equation.sindex++] = atoi(ch);
	    ch = strtok(NULL, " ");
	}
	equations[equations_index++] = equation;
    }
}

void main(void) {
    size_t input_size = count_equations(FILEPATH);
    Equation equations[input_size];
    parse_input(FILEPATH, equations);
    solve(equations, input_size);
}
