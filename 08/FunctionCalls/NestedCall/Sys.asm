(Sys.init)
@0
D=A
(Sys.init.declare.loop)
@Sys.init.declare.end
D;JLE
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@Sys.init.declare.loop
0;JMP
(Sys.init.declare.end)
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@THIS
M=D
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@THAT
M=D
@Sys.main.RETURN_ADDRS0
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
@Sys.main
0;JMP
(Sys.main.RETURN_ADDRS0)
@SP
AM=M-1
D=M
@6
M=D
(Sys.LOOP)
@Sys.LOOP
0;JMP
(Sys.main)
@5
D=A
(Sys.main.declare.loop)
@Sys.main.declare.end
D;JLE
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@Sys.main.declare.loop
0;JMP
(Sys.main.declare.end)
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@THIS
M=D
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@THAT
M=D
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@3
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
@Sys.add12.RETURN_ADDRS1
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
@Sys.add12
0;JMP
(Sys.add12.RETURN_ADDRS1)
@SP
AM=M-1
D=M
@5
M=D
@LCL
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
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@3
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@4
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M+D
@SP
AM=M-1
D=M
A=A-1
M=M+D
@SP
AM=M-1
D=M
A=A-1
M=M+D
@SP
AM=M-1
D=M
A=A-1
M=M+D
@LCL
D=M
@Sys.FRAME2
M=D
@Sys.FRAME2
D=M
@5
A=D-A
D=M
@Sys.RET3
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
@Sys.FRAME2
A=M-1
D=M
@THAT
M=D
@Sys.FRAME2
D=M
@2
A=D-A
D=M
@THIS
M=D
@Sys.FRAME2
D=M
@3
A=D-A
D=M
@ARG
M=D
@Sys.FRAME2
D=M
@4
A=D-A
D=M
@LCL
M=D
@Sys.RET3
A=M
0;JMP
(Sys.add12)
@0
D=A
(Sys.add12.declare.loop)
@Sys.add12.declare.end
D;JLE
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@Sys.add12.declare.loop
0;JMP
(Sys.add12.declare.end)
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@THIS
M=D
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@THAT
M=D
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
@12
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
M=M+D
@LCL
D=M
@Sys.FRAME4
M=D
@Sys.FRAME4
D=M
@5
A=D-A
D=M
@Sys.RET5
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
@Sys.FRAME4
A=M-1
D=M
@THAT
M=D
@Sys.FRAME4
D=M
@2
A=D-A
D=M
@THIS
M=D
@Sys.FRAME4
D=M
@3
A=D-A
D=M
@ARG
M=D
@Sys.FRAME4
D=M
@4
A=D-A
D=M
@LCL
M=D
@Sys.RET5
A=M
0;JMP
(EOF)
@EOF
0;JMP
