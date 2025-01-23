`timescale 1ns / 1ps
module Led_Display_Controller_Test(
    output hsync,vsync,
    output [3:0] vga_r,vga_g,vga_b,
    
    output [7:0]AN,         // Anodes (active low)
    output [6:0]seg,        // segment pins (active low)
    
    output AUD_PWM,       // for the audio
    output AUD_SD,


    input [3:0]buttons,input clock_100Mhz,reset
    );

wire [999:0]pos_x,pos_y;
wire clock_1hz,clock_50Mhz,clock_25Mhz;
reg [3:0] color_r,color_g,color_b;
wire [9:0]pos_x_rand,pos_y_rand;
reg [9:0]curr_apple_x , curr_apple_y;
parameter [19:0]rand_seed = 212701;
reg apple_eaten;
reg [9:0]length = 0;
wire [9:0]head_x,head_y;
wire locked;

assign head_x = pos_x[9:0];
assign head_y = pos_y[9:0];



reg [3:0] unit,tens,hundreds,thousands,h_unit,h_tens,h_hundreds,h_thousands;
reg [19:0] score,high_score=0;
reg [4:0] digit_holder;
wire [2:0] rr;

 
Snake_Position_Controller control1(.pos_x(pos_x), .pos_y(pos_y),.buttons(buttons),.clock(clock_1hz), .reset(reset),.length(length));
Clock_Divider_1s clock1s(clock_1hz,clock_100Mhz,reset);
Clock_Divider_2 clock_by_two(clock_50Mhz,clock_100Mhz,reset);
Clock_Divider_25Mhz clock_3(clock_25Mhz,clock_100Mhz,reset);
Random_Generator random1(pos_x_rand,pos_y_rand,rand_seed,clock_1hz,reset);
vga_controller snake_display(
    .clk_25Mhz(clock_25Mhz),           // Main clock input
    .rst(reset),                // Reset signal
    .x_input(pos_x),      // X-coordinate (0-639 for 640x480 resolution)
    .y_input(pos_y),      // Y-coordinate (0-479 for 640x480 resolution)
    .length(length),
    .x_apple(curr_apple_x),
    .y_apple(curr_apple_y),
    .color_r(color_r),      // Red color (8 bits)
    .color_g(color_g),      // Green color (8 bits)
    .color_b(color_b),      // Blue color (8 bits)
    .hsync(hsync),         // Horizontal sync output
    .vsync(vsync),         // Vertical sync output
    .vga_r(vga_r),   // VGA red signal
    .vga_g(vga_g),   // VGA green signal
    .vga_b(vga_b)    // VGA blue signal
);

always @(posedge clock_100Mhz)begin
    color_r <= 4'b0;
    color_g <= 4'b1111;
    color_b <= 4'b0;
end

always @(posedge clock_1hz or posedge reset) begin
    if (reset) begin
        apple_eaten <= 0;
        curr_apple_x <= 400;
        curr_apple_y <= 200;
        length <= 1;
        score <= 0;
        
    end
    else begin
        if (head_x <= curr_apple_x + 4 && head_x >= curr_apple_x - 4 &&
            head_y <= curr_apple_y + 4 && head_y >= curr_apple_y - 4) begin
            apple_eaten <= 1;
            length <= length + 2;
            score <= score + 4;
           if(score>high_score) begin high_score <= score + 4; end
        end
        else begin
            apple_eaten <= 0;
        end

        if (apple_eaten) begin
            curr_apple_x <= pos_x_rand;
            curr_apple_y <= pos_y_rand;
        end
    end
end

always @(*) begin
    unit = score % 10; 
    tens = ((score % 100) - unit) / 10 ; 
    hundreds = ((score % 1000)- unit - tens*10 ) / 100;  
    thousands = ((score % 10000)- unit - tens*10 - hundreds*100) / 1000;
    
    h_unit = high_score % 10; 
    h_tens = ((high_score % 100) - h_unit) / 10 ; 
    h_hundreds = ((high_score % 1000)- h_unit - h_tens*10 ) / 100;  
    h_thousands = ((high_score % 10000)- h_unit - h_tens*10 - h_hundreds*100) / 1000;
    
end

  always @(posedge clock_100Mhz)begin
        case(rr)
            3'b111: digit_holder <= unit;
            3'b110: digit_holder <= tens;
            3'b101: digit_holder <= hundreds;
            3'b100: digit_holder <= thousands;
            3'b011: digit_holder <= h_unit;
            3'b010: digit_holder <= h_tens;
            3'b001: digit_holder <= h_hundreds;
            3'b000: digit_holder <= h_thousands;
            default: digit_holder <= 5'b10000;
        endcase
    end

        // scoreboard
        
  disp_7_seg scoreboard(.clk(clock_100Mhz), .digit_holder(digit_holder), .refresh_rate(rr), .AN(AN), .seg(seg));

       // play a sound when snake eats the apple
       
   play_sound music(.clk(clock_100Mhz), .Alarm(apple_eaten), .AUD_PWM(AUD_PWM), .AUD_SD(AUD_SD));
   
   
endmodule
