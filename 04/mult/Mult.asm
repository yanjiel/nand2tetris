// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.
    @R1
    D=M // D = M[R1]
    @i
    M=D // i start to be M[R1] = D
    @R2
    M=0 // M[R2]/sum start to be 0
(LOOP)
    @i
    D=M // D = i the counter
    @END
    D;JLE // if D = i <= 0 then end
    @R0
    D=M // D = M[R0]
    @R2
    M=M+D // M[R2] = M[R2] + M[R0] where sum in R2
    @i
    M=M-1 // decrement i which started out to be M[R1] 
    @LOOP
    0;JMP
(END)
    @END
    0;JMP

