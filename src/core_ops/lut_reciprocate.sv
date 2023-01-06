
/***************************************************************
*** autogenerated by $PPU_ROOT/scripts/mant_recip_LUT_gen.py ***
***************************************************************/
module lut_reciprocate #(
  parameter LUT_WIDTH_IN = 8,
  parameter LUT_WIDTH_OUT = 9
)(
  input   [(LUT_WIDTH_IN)-1:0]    addr_i,
  output  [(LUT_WIDTH_OUT)-1:0]   out_o
);

  logic [(LUT_WIDTH_OUT)-1:0] dout;
  logic [(LUT_WIDTH_OUT)-1:0] mant_recip_rom [(2**LUT_WIDTH_IN) - 1:0];

  always_comb begin
    case (addr_i)
          8'd0 :    dout = 9'h0;
      8'd1 :    dout = 9'h1fe;
      8'd2 :    dout = 9'h1fc;
      8'd3 :    dout = 9'h1fa;
      8'd4 :    dout = 9'h1f8;
      8'd5 :    dout = 9'h1f6;
      8'd6 :    dout = 9'h1f4;
      8'd7 :    dout = 9'h1f2;
      8'd8 :    dout = 9'h1f0;
      8'd9 :    dout = 9'h1ef;
      8'd10 :    dout = 9'h1ed;
      8'd11 :    dout = 9'h1eb;
      8'd12 :    dout = 9'h1e9;
      8'd13 :    dout = 9'h1e7;
      8'd14 :    dout = 9'h1e5;
      8'd15 :    dout = 9'h1e4;
      8'd16 :    dout = 9'h1e2;
      8'd17 :    dout = 9'h1e0;
      8'd18 :    dout = 9'h1de;
      8'd19 :    dout = 9'h1dd;
      8'd20 :    dout = 9'h1db;
      8'd21 :    dout = 9'h1d9;
      8'd22 :    dout = 9'h1d7;
      8'd23 :    dout = 9'h1d6;
      8'd24 :    dout = 9'h1d4;
      8'd25 :    dout = 9'h1d2;
      8'd26 :    dout = 9'h1d1;
      8'd27 :    dout = 9'h1cf;
      8'd28 :    dout = 9'h1ce;
      8'd29 :    dout = 9'h1cc;
      8'd30 :    dout = 9'h1ca;
      8'd31 :    dout = 9'h1c9;
      8'd32 :    dout = 9'h1c7;
      8'd33 :    dout = 9'h1c6;
      8'd34 :    dout = 9'h1c4;
      8'd35 :    dout = 9'h1c2;
      8'd36 :    dout = 9'h1c1;
      8'd37 :    dout = 9'h1bf;
      8'd38 :    dout = 9'h1be;
      8'd39 :    dout = 9'h1bc;
      8'd40 :    dout = 9'h1bb;
      8'd41 :    dout = 9'h1b9;
      8'd42 :    dout = 9'h1b8;
      8'd43 :    dout = 9'h1b6;
      8'd44 :    dout = 9'h1b5;
      8'd45 :    dout = 9'h1b3;
      8'd46 :    dout = 9'h1b2;
      8'd47 :    dout = 9'h1b1;
      8'd48 :    dout = 9'h1af;
      8'd49 :    dout = 9'h1ae;
      8'd50 :    dout = 9'h1ac;
      8'd51 :    dout = 9'h1ab;
      8'd52 :    dout = 9'h1aa;
      8'd53 :    dout = 9'h1a8;
      8'd54 :    dout = 9'h1a7;
      8'd55 :    dout = 9'h1a5;
      8'd56 :    dout = 9'h1a4;
      8'd57 :    dout = 9'h1a3;
      8'd58 :    dout = 9'h1a1;
      8'd59 :    dout = 9'h1a0;
      8'd60 :    dout = 9'h19f;
      8'd61 :    dout = 9'h19d;
      8'd62 :    dout = 9'h19c;
      8'd63 :    dout = 9'h19b;
      8'd64 :    dout = 9'h19a;
      8'd65 :    dout = 9'h198;
      8'd66 :    dout = 9'h197;
      8'd67 :    dout = 9'h196;
      8'd68 :    dout = 9'h195;
      8'd69 :    dout = 9'h193;
      8'd70 :    dout = 9'h192;
      8'd71 :    dout = 9'h191;
      8'd72 :    dout = 9'h190;
      8'd73 :    dout = 9'h18e;
      8'd74 :    dout = 9'h18d;
      8'd75 :    dout = 9'h18c;
      8'd76 :    dout = 9'h18b;
      8'd77 :    dout = 9'h18a;
      8'd78 :    dout = 9'h188;
      8'd79 :    dout = 9'h187;
      8'd80 :    dout = 9'h186;
      8'd81 :    dout = 9'h185;
      8'd82 :    dout = 9'h184;
      8'd83 :    dout = 9'h183;
      8'd84 :    dout = 9'h182;
      8'd85 :    dout = 9'h180;
      8'd86 :    dout = 9'h17f;
      8'd87 :    dout = 9'h17e;
      8'd88 :    dout = 9'h17d;
      8'd89 :    dout = 9'h17c;
      8'd90 :    dout = 9'h17b;
      8'd91 :    dout = 9'h17a;
      8'd92 :    dout = 9'h179;
      8'd93 :    dout = 9'h178;
      8'd94 :    dout = 9'h176;
      8'd95 :    dout = 9'h175;
      8'd96 :    dout = 9'h174;
      8'd97 :    dout = 9'h173;
      8'd98 :    dout = 9'h172;
      8'd99 :    dout = 9'h171;
      8'd100 :    dout = 9'h170;
      8'd101 :    dout = 9'h16f;
      8'd102 :    dout = 9'h16e;
      8'd103 :    dout = 9'h16d;
      8'd104 :    dout = 9'h16c;
      8'd105 :    dout = 9'h16b;
      8'd106 :    dout = 9'h16a;
      8'd107 :    dout = 9'h169;
      8'd108 :    dout = 9'h168;
      8'd109 :    dout = 9'h167;
      8'd110 :    dout = 9'h166;
      8'd111 :    dout = 9'h165;
      8'd112 :    dout = 9'h164;
      8'd113 :    dout = 9'h163;
      8'd114 :    dout = 9'h162;
      8'd115 :    dout = 9'h161;
      8'd116 :    dout = 9'h160;
      8'd117 :    dout = 9'h15f;
      8'd118 :    dout = 9'h15e;
      8'd119 :    dout = 9'h15e;
      8'd120 :    dout = 9'h15d;
      8'd121 :    dout = 9'h15c;
      8'd122 :    dout = 9'h15b;
      8'd123 :    dout = 9'h15a;
      8'd124 :    dout = 9'h159;
      8'd125 :    dout = 9'h158;
      8'd126 :    dout = 9'h157;
      8'd127 :    dout = 9'h156;
      8'd128 :    dout = 9'h155;
      8'd129 :    dout = 9'h154;
      8'd130 :    dout = 9'h154;
      8'd131 :    dout = 9'h153;
      8'd132 :    dout = 9'h152;
      8'd133 :    dout = 9'h151;
      8'd134 :    dout = 9'h150;
      8'd135 :    dout = 9'h14f;
      8'd136 :    dout = 9'h14e;
      8'd137 :    dout = 9'h14e;
      8'd138 :    dout = 9'h14d;
      8'd139 :    dout = 9'h14c;
      8'd140 :    dout = 9'h14b;
      8'd141 :    dout = 9'h14a;
      8'd142 :    dout = 9'h149;
      8'd143 :    dout = 9'h149;
      8'd144 :    dout = 9'h148;
      8'd145 :    dout = 9'h147;
      8'd146 :    dout = 9'h146;
      8'd147 :    dout = 9'h145;
      8'd148 :    dout = 9'h144;
      8'd149 :    dout = 9'h144;
      8'd150 :    dout = 9'h143;
      8'd151 :    dout = 9'h142;
      8'd152 :    dout = 9'h141;
      8'd153 :    dout = 9'h140;
      8'd154 :    dout = 9'h140;
      8'd155 :    dout = 9'h13f;
      8'd156 :    dout = 9'h13e;
      8'd157 :    dout = 9'h13d;
      8'd158 :    dout = 9'h13d;
      8'd159 :    dout = 9'h13c;
      8'd160 :    dout = 9'h13b;
      8'd161 :    dout = 9'h13a;
      8'd162 :    dout = 9'h13a;
      8'd163 :    dout = 9'h139;
      8'd164 :    dout = 9'h138;
      8'd165 :    dout = 9'h137;
      8'd166 :    dout = 9'h137;
      8'd167 :    dout = 9'h136;
      8'd168 :    dout = 9'h135;
      8'd169 :    dout = 9'h134;
      8'd170 :    dout = 9'h134;
      8'd171 :    dout = 9'h133;
      8'd172 :    dout = 9'h132;
      8'd173 :    dout = 9'h132;
      8'd174 :    dout = 9'h131;
      8'd175 :    dout = 9'h130;
      8'd176 :    dout = 9'h12f;
      8'd177 :    dout = 9'h12f;
      8'd178 :    dout = 9'h12e;
      8'd179 :    dout = 9'h12d;
      8'd180 :    dout = 9'h12d;
      8'd181 :    dout = 9'h12c;
      8'd182 :    dout = 9'h12b;
      8'd183 :    dout = 9'h12b;
      8'd184 :    dout = 9'h12a;
      8'd185 :    dout = 9'h129;
      8'd186 :    dout = 9'h129;
      8'd187 :    dout = 9'h128;
      8'd188 :    dout = 9'h127;
      8'd189 :    dout = 9'h127;
      8'd190 :    dout = 9'h126;
      8'd191 :    dout = 9'h125;
      8'd192 :    dout = 9'h125;
      8'd193 :    dout = 9'h124;
      8'd194 :    dout = 9'h123;
      8'd195 :    dout = 9'h123;
      8'd196 :    dout = 9'h122;
      8'd197 :    dout = 9'h121;
      8'd198 :    dout = 9'h121;
      8'd199 :    dout = 9'h120;
      8'd200 :    dout = 9'h11f;
      8'd201 :    dout = 9'h11f;
      8'd202 :    dout = 9'h11e;
      8'd203 :    dout = 9'h11e;
      8'd204 :    dout = 9'h11d;
      8'd205 :    dout = 9'h11c;
      8'd206 :    dout = 9'h11c;
      8'd207 :    dout = 9'h11b;
      8'd208 :    dout = 9'h11a;
      8'd209 :    dout = 9'h11a;
      8'd210 :    dout = 9'h119;
      8'd211 :    dout = 9'h119;
      8'd212 :    dout = 9'h118;
      8'd213 :    dout = 9'h117;
      8'd214 :    dout = 9'h117;
      8'd215 :    dout = 9'h116;
      8'd216 :    dout = 9'h116;
      8'd217 :    dout = 9'h115;
      8'd218 :    dout = 9'h115;
      8'd219 :    dout = 9'h114;
      8'd220 :    dout = 9'h113;
      8'd221 :    dout = 9'h113;
      8'd222 :    dout = 9'h112;
      8'd223 :    dout = 9'h112;
      8'd224 :    dout = 9'h111;
      8'd225 :    dout = 9'h110;
      8'd226 :    dout = 9'h110;
      8'd227 :    dout = 9'h10f;
      8'd228 :    dout = 9'h10f;
      8'd229 :    dout = 9'h10e;
      8'd230 :    dout = 9'h10e;
      8'd231 :    dout = 9'h10d;
      8'd232 :    dout = 9'h10d;
      8'd233 :    dout = 9'h10c;
      8'd234 :    dout = 9'h10b;
      8'd235 :    dout = 9'h10b;
      8'd236 :    dout = 9'h10a;
      8'd237 :    dout = 9'h10a;
      8'd238 :    dout = 9'h109;
      8'd239 :    dout = 9'h109;
      8'd240 :    dout = 9'h108;
      8'd241 :    dout = 9'h108;
      8'd242 :    dout = 9'h107;
      8'd243 :    dout = 9'h107;
      8'd244 :    dout = 9'h106;
      8'd245 :    dout = 9'h106;
      8'd246 :    dout = 9'h105;
      8'd247 :    dout = 9'h105;
      8'd248 :    dout = 9'h104;
      8'd249 :    dout = 9'h104;
      8'd250 :    dout = 9'h103;
      8'd251 :    dout = 9'h103;
      8'd252 :    dout = 9'h102;
      8'd253 :    dout = 9'h102;
      8'd254 :    dout = 9'h101;
      8'd255 :    dout = 9'h101;

      default: dout = 'h0;
    endcase
  end

  assign out_o = dout; // << 1;
endmodule: lut_reciprocate
