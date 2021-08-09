// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
    // initialize

    @SCREEN // 16384
    D=A     // D = 16384 which is 2^14
    @i      // R[16]
    M=D     // i = R[16] start from 16384
    
(FILL_BLACK)
    @KBD // 24576
    D=M  // D=M[24576] they keyboard content
    @FILL_WHITE
    D;JEQ // if released or not pressed

    @i
    D=M // D is the screen address register (16pixels)
    @24576 // the max screen address + 1 or keyboard address
    D=D-A
    @WAIT_BLACK
    D;JGE  // if we reach the end (bottom right) of the screen

    @i
    D=M
    A=D // load address
    M=-1
    @i
    M=M+1 // screen address update to next register (16pixels)

    @FILL_BLACK
    0;JMP

(FILL_WHITE)
    @KBD
    D=M
    @FILL_BLACK
    D;JNE // if pressed again

    @i
    D=M // D is the screen address register (16pixels)
    @SCREEN
    D=D-A
    @WAIT_WHITE
    D;JLE // if we have reached the start of the screen

    @i
    D=M
    A=D // load address
    M=0 // white out
    @i
    M=M-1 // move backwards to fill up

    @FILL_WHITE
    0;JMP

(WAIT_WHITE)
    // if no key is pressed then will loop in here until a key is pressed
    @i
    D=M
    A=D // load address
    M=0 // white out current screen register

    @KBD
    D=M
    @FILL_BLACK
    D;JNE

    @WAIT_WHITE
    0;JMP

(WAIT_BLACK)
    // if keys are pressed down or we reach the end of the screen then we loop in here until keys are released
    @KBD
    D=M
    @FILL_WHITE
    D;JEQ

    @WAIT_BLACK
    0;JMP