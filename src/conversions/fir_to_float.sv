`ifdef FLOAT_TO_POSIT
module fir_to_float #(
        parameter N = 10,
        parameter ES = 1,
        parameter FSIZE = 54
    )(
        input                   clk,
        input                   rst,
        input  [FIR_SIZE-1:0]   fir,
        output [FSIZE-1:0]      float
    );

    parameter FLOAT_EXP_SIZE = FLOAT_EXP_SIZE_F`F;
    parameter FLOAT_MANT_SIZE = FLOAT_MANT_SIZE_F`F;

    logic [FIR_SIZE-1:0] fir_st0, fir_st1;
    assign fir_st0 = fir;
    
    always_ff @(posedge clk) begin
        if (rst) begin
            fir_st1 <= 0;
        end else begin
            fir_st1 <= fir_st0;
        end
    end



    wire posit_sign;
    wire signed [TE_SIZE-1:0] posit_te;
    wire [MANT_SIZE-1:0] posit_frac;

    assign {posit_sign, posit_te, posit_frac} = fir_st1;

    

    wire float_sign;
    wire signed [FLOAT_EXP_SIZE-1:0] float_exp;
    wire [FLOAT_MANT_SIZE-1:0] float_frac;

    assign float_sign = posit_sign;
    
    sign_extend #(
        .POSIT_TOTAL_EXPONENT_SIZE(TE_SIZE),
        .FLOAT_EXPONENT_SIZE(FLOAT_EXP_SIZE)
    ) sign_extend_inst (
        .posit_total_exponent(posit_te),
        .float_exponent(float_exp)
    );      


    assign float_frac = posit_frac << (FLOAT_MANT_SIZE - MANT_SIZE + 1);

    float_encoder #(
        .FSIZE(FSIZE)
    ) float_encoder_inst (
        .sign(float_sign),
        .exp(float_exp),
        .frac(float_frac),
        .bits(float)
    );


endmodule
`endif