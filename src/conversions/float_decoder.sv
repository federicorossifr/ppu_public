/*

iverilog -g2012 -DN=16 -DES=1 -DF=64 -DTB_FLOAT_DECODE ../src/conversions/defines.vh ../src/conversions/float_decoder.sv && ./a.out


so far with the simplified assumption that the float fields are larger than the posit fields. also no dealing with subnormals
*/

module float_decoder #(
        parameter FSIZE = 64
    )(
        input [FSIZE-1:0] bits,
        output sign,
        output signed [FLOAT_EXP_SIZE-1:0] exp,
        output [FLOAT_MANT_SIZE-1:0] frac
    );

    localparam FLOAT_EXP_SIZE = FLOAT_EXP_SIZE_F`F;
    localparam FLOAT_MANT_SIZE = FLOAT_MANT_SIZE_F`F;

    localparam exp_bias = (1 << (FLOAT_EXP_SIZE - 1)) - 1;

    assign sign = bits >> (FSIZE - 1) != 0;
    
    wire [FLOAT_EXP_SIZE-1:0] biased_exp;
    assign biased_exp = bits[(FSIZE-1)-:FLOAT_EXP_SIZE+1];    
        // ((bits & ((1 << (FSIZE - 1)) - 1)) >> FLOAT_MANT_SIZE) & ((1 << FLOAT_MANT_SIZE) - 1);

    assign exp = biased_exp - exp_bias; // unbiased exponent
    assign frac = bits[FLOAT_MANT_SIZE-1:0];  // bits & ((1 << FLOAT_MANT_SIZE) - 1);

endmodule


`ifdef TB_FLOAT_DECODE
`define STRINGIFY(DEFINE) $sformatf("%0s", `"DEFINE`")

module tb_float_decoder;

    parameter FSIZE = 64;

    reg [FSIZE-1:0] bits;
    wire sign;
    wire [FLOAT_EXP_SIZE_F`F-1:0] exp;
    wire [FLOAT_MANT_SIZE_F`F-1:0] frac;

    
    float_decoder #(
        .FSIZE(FSIZE)
    ) float_decoder_inst (
        .bits(bits),
        .sign(sign),
        .exp(exp),
        .frac(frac)
    );


    initial begin
        $dumpfile({"tb_float_decoder_F",`STRINGIFY(`F),".vcd"});
        $dumpvars(0, tb_float_decoder);                        

        bits = 64'h405ee00000000000; #10;

    end


endmodule
`endif
