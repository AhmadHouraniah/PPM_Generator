
module HA
(
	input A,
	input B,
	output SUM,
	output COUT
);


	assign SUM = A ^ B;
	assign COUT = A & B;

endmodule


module FA
(
	input A,
	input B,
	input CIN, 
	output SUM,
	output COUT
);

	assign SUM = A ^ B ^ CIN;
	assign COUT = A & B | A & CIN | B & CIN;

endmodule

module AND2(A, B, C);
    input A, B;
    output C;
    assign C = A&B;
endmodule

module NAND2(A, B, C);
    input A, B;
    output C;
    assign C = ~ (A&B);
endmodule