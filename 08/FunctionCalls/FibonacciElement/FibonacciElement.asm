@256
D=A
@SP
M=D
@FibonacciElement.Sys.init.RETURN_ADDRS0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@FibonacciElement.Sys.init
0;JMP
(FibonacciElement.Sys.init.RETURN_ADDRS0)
(FibonacciElement.Main.fibonacci)
@0
D=A
(FibonacciElement.Main.fibonacci.declare.loop)
@FibonacciElement.Main.fibonacci.declare.end
D;JLE
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@FibonacciElement.Main.fibonacci.declare.loop
0;JMP
(FibonacciElement.Main.fibonacci.declare.end)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
M=-1
@CONT_1
D;JLT
@SP
A=M-1
M=0
(CONT_1)
@SP
AM=M-1
D=M
@FibonacciElement.Main.IF_TRUE
D;JNE
@FibonacciElement.Main.IF_FALSE
0;JMP
(FibonacciElement.Main.IF_TRUE)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@FibonacciElement.Main.FRAME2
M=D
@FibonacciElement.Main.FRAME2
D=M
@5
A=D-A
D=M
@FibonacciElement.Main.RET3
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@FibonacciElement.Main.FRAME2
A=M-1
D=M
@THAT
M=D
@FibonacciElement.Main.FRAME2
D=M
@2
A=D-A
D=M
@THIS
M=D
@FibonacciElement.Main.FRAME2
D=M
@3
A=D-A
D=M
@ARG
M=D
@FibonacciElement.Main.FRAME2
D=M
@4
A=D-A
D=M
@LCL
M=D
@FibonacciElement.Main.RET3
A=M
0;JMP
(FibonacciElement.Main.IF_FALSE)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M-D
@FibonacciElement.Main.fibonacci.RETURN_ADDRS4
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@FibonacciElement.Main.fibonacci
0;JMP
(FibonacciElement.Main.fibonacci.RETURN_ADDRS4)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M-D
@FibonacciElement.Main.fibonacci.RETURN_ADDRS5
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@FibonacciElement.Main.fibonacci
0;JMP
(FibonacciElement.Main.fibonacci.RETURN_ADDRS5)
@SP
AM=M-1
D=M
A=A-1
M=M+D
@LCL
D=M
@FibonacciElement.Main.FRAME6
M=D
@FibonacciElement.Main.FRAME6
D=M
@5
A=D-A
D=M
@FibonacciElement.Main.RET7
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@FibonacciElement.Main.FRAME6
A=M-1
D=M
@THAT
M=D
@FibonacciElement.Main.FRAME6
D=M
@2
A=D-A
D=M
@THIS
M=D
@FibonacciElement.Main.FRAME6
D=M
@3
A=D-A
D=M
@ARG
M=D
@FibonacciElement.Main.FRAME6
D=M
@4
A=D-A
D=M
@LCL
M=D
@FibonacciElement.Main.RET7
A=M
0;JMP
(FibonacciElement.Sys.init)
@0
D=A
(FibonacciElement.Sys.init.declare.loop)
@FibonacciElement.Sys.init.declare.end
D;JLE
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@FibonacciElement.Sys.init.declare.loop
0;JMP
(FibonacciElement.Sys.init.declare.end)
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
@FibonacciElement.Main.fibonacci.RETURN_ADDRS8
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@FibonacciElement.Main.fibonacci
0;JMP
(FibonacciElement.Main.fibonacci.RETURN_ADDRS8)
(FibonacciElement.Sys.WHILE)
@FibonacciElement.Sys.WHILE
0;JMP
(EOF)
@EOF
0;JMP