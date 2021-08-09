// Adds 1+2+...+100
    @i
    M=1
    @sum
    M=0
(LOOP)
    @i
    D=M // D=i
    @100
    D=D-A // D = i - 100
    @END // referencing line 20
    D;JGT // if D = i-100 is greater than 0 then jump to END
    @i
    D=M // D = i start with 0
    @sum
    M=D+M //sum = i + sum
    @i
    M=M+1 // increment i
    @LOOP
    0;JMP // unconditional jump to start of LOOP
(END)
    @END
    0;JMP