module tb();

    `ifdef SET_WIDTH
        parameter N = `N;
        parameter M = `M;
    `else
        parameter N = 8;
        parameter M = 8;
    `endif 

    reg `ifdef SIGNED signed `endif [N-1:0] A;
    reg `ifdef SIGNED signed `endif [M-1:0] B;

    wire `ifdef SIGNED signed `endif [N+M-1:0] OUT1, OUT2;

    PPM PPM (.a(A), .b(B), .out1(OUT1), .out2(OUT2));

    wire `ifdef SIGNED signed `endif [N+M-1:0] sum = OUT1+OUT2;
    integer i = 0;
    initial begin
        $dumpvars;
        for (i = 0; i<50 ; i=i+1) begin
            A=$random;
            B=$random;
            #10;
            if(A*B == sum)
                $display("Correct! %d x %d = %d", A, B, sum);
            else
                $display("Error! %d x %d = %d", A, B, sum);
        end
        $finish;
    end

endmodule
