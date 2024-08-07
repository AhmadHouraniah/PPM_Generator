module tb();

    parameter N = 4;
	parameter M = 4;
	
    reg signed [N-1:0] A;
    reg signed [M-1:0] B;

    wire signed [N+M-1:0] OUT1, OUT2;

    PPM PPM (.A(A), .B(B), .OUT1(OUT1), .OUT2(OUT2));

    wire signed [N+M-1:0] sum = OUT1+OUT2;

    initial begin
        $dumpvars;
        A=$random;
        B=$random;
        #10;
        $display("%d x %d = %d", A, B, sum);

        A=$random;
        B=$random;
        #10;
        $display("%d x %d = %d", A, B, sum);

        A=$random;
        B=$random;
        #10;
        $display("%d x %d = %d", A, B, sum);

        A=$random;
        B=$random;
        #10;
        $display("%d x %d = %d", A, B, sum);
        $finish;
    end

endmodule
