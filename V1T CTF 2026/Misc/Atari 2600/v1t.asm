; Disassembly of v1t.bas.bin
; Disassembled Mon Jun 29 12:15:18 2026
; Using DiStella v3.02-SNAPSHOT
;
; Command Line: ./distella -pafs v1t.bas.bin 
;

      processor 6502
VSYNC   =  $00
VBLANK  =  $01
WSYNC   =  $02
NUSIZ0  =  $04
NUSIZ1  =  $05
COLUP0  =  $06
COLUP1  =  $07
COLUPF  =  $08
COLUBK  =  $09
CTRLPF  =  $0A
REFP0   =  $0B
REFP1   =  $0C
PF0     =  $0D
PF1     =  $0E
PF2     =  $0F
RESP0   =  $10
RESP1   =  $11
GRP0    =  $1B
GRP1    =  $1C
ENAM0   =  $1D
ENAM1   =  $1E
ENABL   =  $1F
HMP0    =  $20
HMP1    =  $21
VDELP0  =  $25
VDELP1  =  $26
VDELBL  =  $27
HMOVE   =  $2A
HMCLR   =  $2B
CXCLR   =  $2C
SWCHA   =  $0280
SWCHB   =  $0282
INTIM   =  $0284
TIM64T  =  $0296
LF4C3   =   $F4C3

       ORG $F000

START:
       SEI            ;2
       CLD            ;2
       LDY    #$00    ;2
       LDA    $D0     ;3
       CMP    #$2C    ;2
       BNE    LF011   ;2
       LDA    $D1     ;3
       CMP    #$A9    ;2
       BNE    LF011   ;2
       DEY            ;2
LF011: LDX    #$00    ;2
       TXA            ;2
LF014: INX            ;2
       TXS            ;2
       PHA            ;3
       BNE    LF014   ;2
       STY    $9C     ;3
       LDA    #$08    ;2
       STA    $EF     ;3
       LDX    #$05    ;2
LF021: LDA    #$9C    ;2
       STA    $96,X   ;4
       DEX            ;2
       BPL    LF021   ;2
       LDA    #$01    ;2
       STA    CTRLPF  ;3
       ORA    INTIM   ;4
       STA    $A2     ;3
       JMP    LF45D   ;3
LF034: STA    WSYNC   ;3
       LDA    #$FF    ;2
       STA    TIM64T  ;4
       LDA    #$01    ;2
       STA    VDELBL  ;3
       STA    VDELP0  ;3
       LDX    $92     ;3
       INX            ;2
       INX            ;2
       STX    $9F     ;3
       LDA    $86     ;3
       STA    $9E     ;3
       LDX    $90     ;3
       INX            ;2
       INX            ;2
       STX    $F6     ;3
       LDA    $89     ;3
       STA    $F7     ;3
       LDA    $85     ;3
       LDX    #$00    ;2
       STA    WSYNC   ;3
       STX    GRP0    ;3
       STX    GRP1    ;3
       STX    PF1     ;3
       STX    PF2     ;3
       STX    CXCLR   ;3
       .byte $04 ;.NOP;3
       BRK            ;7
       STA    $9D,X   ;4
       LDX    #$54    ;2
       DEC    $85     ;5
       LDA    $91     ;3
       STA    $A0     ;3
       LDA    $88     ;3
       STA    $A1     ;3
       LDA    $EF     ;3
       STA    $9C     ;3
       LDA    #$0A    ;2
       CLC            ;2
       SBC    $EF     ;3
       STA    $EF     ;3
       JMP    LF0A8   ;3
LF083: .byte $A9,$00,$A8,$4C,$D6,$F0,$A9,$00,$A8,$4C,$B2,$F0
LF08F: NOP            ;2
       LDA    $92     ;3
       LDY    $50,X   ;4
       STY    PF1     ;3
       LDY    $51,X   ;4
       STY    PF2     ;3
       LDY    $53,X   ;4
       STY    PF1     ;3
       LDY    $52,X   ;4
       STY    PF2     ;3
       .byte $C7 ;.DCP;5
       .byte $89 ;.NOP;2
       ROL            ;2
       ROL            ;2
LF0A6: STA    ENABL   ;3
LF0A8: LDA    $8F     ;3
       .byte $C7 ;.DCP;5
       STX    $90     ;3
       .byte $DB ;.DCP;7
       LDY    $86     ;3
       LDA    ($8C),Y ;5
       STA    GRP1    ;3
       LDA    $87     ;3
       .byte $C7 ;.DCP;5
       DEY            ;2
       ROL            ;2
       ROL            ;2
       STA    ENAM1   ;3
       LDA    $50,X   ;4
       STA    PF1     ;3
       LDA    $51,X   ;4
       STA    PF2     ;3
       LDA    $53,X   ;4
       STA    PF1     ;3
       LDA    $52,X   ;4
       STA    PF2     ;3
       LDA    $8E     ;3
       .byte $C7 ;.DCP;5
       STA    $90     ;3
       LDA    ($A4),Y ;5
       STA    $B1     ;3
       TXA            ;2
       STA    GRP0    ;3
       LDA    $90     ;3
       .byte $C7 ;.DCP;5
       STA    ($E5),Y ;6
       INC    $85,X   ;6
       ORA    $9CC6,X ;4
       BNE    LF08F   ;2
       LDA    #$00    ;2
       STA    PF1     ;3
       STA    PF2     ;3
       TXA            ;2
       .byte $CB ;.SBX;2
       .byte $FC ;.NOP;4
       BMI    LF101   ;2
       NOP            ;2
       NOP            ;2
       NOP            ;2
       NOP            ;2
       NOP            ;2
       LDA    #$08    ;2
       STA    $9C     ;3
       LDA    $92     ;3
       .byte $C7 ;.DCP;5
       .byte $89 ;.NOP;2
       SBC    $9F     ;3
       JMP    LF0A6   ;3
LF101: NOP            ;2
       NOP            ;2
       NOP            ;2
       NOP            ;2
       NOP            ;2
       LDX    $EF     ;3
       NOP            ;2
       JMP    LF127   ;3
LF10C: .byte $A9,$00,$A8,$4C,$39,$F1,$EA,$AC,$D0,$00,$84,$0E,$AC,$D1,$00,$84
       .byte $0F,$AC,$D3,$00,$84,$0E,$AC,$D2,$00,$84,$0F
LF127: LDA    $92     ;3
       .byte $C7 ;.DCP;5
       .byte $89 ;.NOP;2
       ROL            ;2
       ROL            ;2
       STA    ENABL   ;3
       LDA    $8F     ;3
       .byte $C7 ;.DCP;5
       STX    $90     ;3
       .byte $D7 ;.DCP;6
       LDY    $86     ;3
       LDA    ($8C),Y ;5
       STA    GRP1    ;3
       LDA    $87     ;3
       .byte $C7 ;.DCP;5
       DEY            ;2
       DEX            ;2
       BEQ    LF178   ;2
       LDY.w  $00D0   ;4
       STY    PF1     ;3
       LDY.w  $00D1   ;4
       STY    PF2     ;3
       LDY.w  $00D3   ;4
       STY    PF1     ;3
       LDY.w  $00D2   ;4
       STY    PF2     ;3
       ROL            ;2
       ROL            ;2
       STA    ENAM1   ;3
       LDA.w  $008E   ;4
       .byte $C7 ;.DCP;5
       STA    $90     ;3
       ORA    ($A4),Y ;5
       STA    $B1     ;3
       TXA            ;2
LF165: STA    GRP0    ;3
       LDA    $90     ;3
       .byte $C7 ;.DCP;5
       STA    ($E5),Y ;6
       INC    $85,X   ;6
       ORA    $124C,X ;4
       SBC    ($A9),Y ;5
       BRK            ;7
       TAY            ;2
       JMP    LF165   ;3
LF178: STX    PF1     ;3
       STX    PF2     ;3
       STX    PF0     ;3
       CLC            ;2
       LDA    #$0A    ;2
       SBC    $EF     ;3
       STA    $EF     ;3
       TXA            ;2
       STA    WSYNC,X ;4
       STA    REFP0   ;3
       STA    REFP1   ;3
       STA    GRP0    ;3
       STA    GRP1    ;3
       STA    HMCLR   ;3
       STA    ENAM0   ;3
       STA    ENAM1   ;3
       STA    ENABL   ;3
       LDA    $9D     ;3
       STA    $85     ;3
       LDA    $9E     ;3
       STA    $86     ;3
       LDA    $A1     ;3
       STA    $88     ;3
       LDA    $A0     ;3
       STA    $91     ;3
       LDA    $F7     ;3
       STA    $89     ;3
       LDA    INTIM   ;4
       CLC            ;2
       ADC    #$8E    ;2
       STA    TIM64T  ;4
       LDA    $97     ;3
       STA    $9C     ;3
       LDA    $99     ;3
       STA    $9E     ;3
       STA    HMCLR   ;3
       TSX            ;2
       STX    $F6     ;3
       LDX    #$E0    ;2
       STX    HMP0    ;3
       LDA    $A3     ;3
       STA    COLUP0  ;3
       STA    COLUP1  ;3
       STA    WSYNC   ;3
       LDX    #$00    ;2
       STX    GRP0    ;3
       STX    GRP1    ;3
       LDA    $9B     ;3
       STA    $A0,X   ;4
       LDA    #$FF    ;2
       STA    $97     ;3
       STA    $99     ;3
       STA    $9B     ;3
       STA    $9D     ;3
       STA    $9F     ;3
       STA    $A1     ;3
       LDY    #$07    ;2
       STY    VDELP0  ;3
       STA    RESP0   ;3
       STA    RESP1   ;3
       LDA    #$03    ;2
       STA    NUSIZ0  ;3
       STA    NUSIZ1  ;3
       STA    VDELP1  ;3
       LDA    #$F0    ;2
       STA    HMP1    ;3
       LDA    ($96),Y ;5
       STA    GRP0    ;3
       STA    HMOVE   ;3
       JMP    LF20B   ;3
LF203: LDA    ($96),Y ;5
       STA    GRP0    ;3
       .byte $04 ;.NOP;3
       BRK            ;7
       NOP            ;2
       NOP            ;2
LF20B: LDA    ($9E),Y ;5
       STA    GRP1    ;3
       LDA    ($9C),Y ;5
       STA    GRP0    ;3
       .byte $B3 ;.LAX;5
       TYA            ;2
       TXS            ;2
       .byte $B3 ;.LAX;5
       TXS            ;2
       .byte $04 ;.NOP;3
       BRK            ;7
       NOP            ;2
       NOP            ;2
       NOP            ;2
       LDA    ($A0),Y ;5
       STX    GRP1    ;3
       TSX            ;2
       STX    GRP0    ;3
       STA    GRP1    ;3
       STY    GRP0    ;3
       DEY            ;2
       BPL    LF203   ;2
       LDX    $F6     ;3
       TXS            ;2
       LDY    $9C     ;3
       STY    $97     ;3
       LDA    #$00    ;2
       STA    PF1     ;3
       STA    GRP0    ;3
       STA    GRP1    ;3
       STA    VDELP0  ;3
       STA    VDELP1  ;3
       STA    NUSIZ0  ;3
       STA    NUSIZ1  ;3
       LDY    $9E     ;3
       STY    $99     ;3
       LDY    $A0     ;3
       STY    $9B     ;3
       LDA    #$02    ;2
LF24C: STA    WSYNC   ;3
       STA    VBLANK  ;3
       RTS            ;6

LF251: .byte $A2,$2F,$95,$A4,$CA,$10,$FB,$60
LF259: STX    $9D     ;3
       TAX            ;2
       LSR            ;2
       LSR            ;2
       LSR            ;2
       STA    $9C     ;3
       TYA            ;2
       ASL            ;2
       ASL            ;2
       CLC            ;2
       ADC    $9C     ;3
       TAY            ;2
       LDA    $9D     ;3
       RTS            ;6

LF26B: .byte $20,$59,$F2,$BD,$D3,$F2,$39,$A4,$00,$5D,$D3,$F2,$60
LF278: JSR    LF259   ;6
       JMP    LF2AC   ;3
LF27E: .byte $20,$59,$F2,$4C,$8B,$F2,$E8,$8A,$29,$07,$D0,$01,$C8,$20,$AC,$F2
       .byte $E4,$9E,$30,$F2,$60,$20,$59,$F2,$84,$9C,$E6,$9E,$A5,$9E,$0A,$0A
       .byte $85,$9E,$20,$AC,$F2,$C8,$C8,$C8,$C8,$C4,$9E,$30,$F5,$60
LF2AC: LDA    $9D     ;3
       BEQ    LF2BD   ;2
       LSR            ;2
       BCS    LF2C7   ;2
       LDA.wy $00A4,Y ;4
       EOR    LF2D3,X ;4
       STA.wy $00A4,Y ;5
       RTS            ;6

LF2BD: LDA.wy $00A4,Y ;4
       ORA    LF2D3,X ;4
       STA.wy $00A4,Y ;5
       RTS            ;6

LF2C7: LDA    LF2D3,X ;4
       EOR    #$FF    ;2
       AND.wy $00A4,Y ;4
       STA.wy $00A4,Y ;5
       RTS            ;6

LF2D3: .byte $80,$40,$20,$10,$08,$04,$02,$01,$01,$02,$04,$08,$10,$20,$40,$80
       .byte $80,$40,$20,$10,$08,$04,$02,$01,$01,$02,$04,$08,$10,$20,$40,$80
       .byte $D0,$13,$A2,$30,$B5,$A3,$4A,$36,$A2,$76,$A1,$36,$A0,$76,$A3,$8A
       .byte $CB,$04,$D0,$F0,$60,$4A,$90,$13,$A2,$30,$B5,$A0,$4A,$36,$A1,$76
       .byte $A2,$36,$A3,$76,$A0,$8A,$CB,$04,$D0,$F0,$60,$4A,$90,$49,$4A,$90
       .byte $02,$C6,$EF,$C6,$EF,$F0,$02,$10,$3D,$A9,$08,$85,$EF,$A5,$A7,$85
       .byte $9F,$A5,$A6,$85,$9E,$A5,$A5,$85,$9D,$A5,$A4,$85,$9C,$A2,$00,$B5
       .byte $A8,$95,$A4,$B5,$A9,$95,$A5,$B5,$AA,$95,$A6
LF34E: .byte $B5,$AB,$95,$A7,$8A,$CB,$FC,$E0,$2C,$D0,$E9,$A5,$9F,$85,$D3,$A5
       .byte $9E,$85,$D2,$A5,$9D,$85,$D1,$A5,$9C,$85,$D0,$60,$4A,$B0,$02,$E6
       .byte $EF,$E6,$EF,$A5,$EF,$C9,$09,$90,$3B,$A9,$01,$85,$EF,$A5,$D3,$85
       .byte $9F,$A5,$D2,$85,$9E,$A5,$D1,$85,$9D,$A5,$D0,$85,$9C,$A2,$2C,$B5
       .byte $A3,$95,$A7,$B5,$A2,$95,$A6,$B5,$A1,$95,$A5,$B5,$A0,$95,$A4,$8A
       .byte $CB,$04,$D0,$EB,$A5,$9F,$85,$A7,$A5,$9E,$85,$A6,$A5,$9D,$85,$A5
       .byte $A5,$9C,$85,$A4,$60,$A5,$A2,$4A,$90,$02,$49,$B4,$85,$A2,$60
LF3BD: LDA    INTIM   ;4
       BMI    LF3BD   ;2
       LDA    #$02    ;2
       STA    WSYNC   ;3
       STA    VSYNC   ;3
       STA    WSYNC   ;3
       STA    WSYNC   ;3
       LSR            ;2
       STA    WSYNC   ;3
       STA    VSYNC   ;3
       STA    VBLANK  ;3
       LDA    #$A5    ;2
       STA    TIM64T  ;4
       STA    WSYNC   ;3
       LDX    #$04    ;2
       .byte $04 ;.NOP;3
       BRK            ;7
LF3DE: LDA    $80,X   ;4
       SEC            ;2
LF3E1: SBC    #$0F    ;2
       BCS    LF3E1   ;2
       STA    $9C,X   ;4
       STA    RESP0,X ;4
       STA    WSYNC   ;3
       DEX            ;2
       BPL    LF3DE   ;2
       LDX    #$04    ;2
       LDY    $9C,X   ;4
       LDA    LF34E,Y ;4
       STA    HMP0,X  ;4
       DEX            ;2
       LDY    $9C,X   ;4
       LDA    LF34E,Y ;4
       STA    HMP0,X  ;4
       DEX            ;2
       LDY    $9C,X   ;4
       LDA    LF34E,Y ;4
       STA    HMP0,X  ;4
       DEX            ;2
       LDY    $9C,X   ;4
       LDA    LF34E,Y ;4
       STA    HMP0,X  ;4
       DEX            ;2
       LDY    $9C,X   ;4
       LDA    LF34E,Y ;4
       STA    HMP0,X  ;4
       STA    WSYNC   ;3
       STA    HMOVE   ;3
       .byte $A7 ;.LAX;3
       STA    HMP0,X  ;4
       LSR    $84F4   ;6
       .byte $9B ;.SHS;5
       STX    $98     ;3
       .byte $A7 ;.LAX;3
       STY    HMP0,X  ;4
       LSR    $84F4   ;6
       TXS            ;2
       STX    $97     ;3
       .byte $A7 ;.LAX;3
       .byte $93 ;.SHA;6
       JSR    LF44E   ;6
       STY    $99     ;3
       STX    $96     ;3
LF436: LDA    INTIM   ;4
       BMI    LF436   ;2
       JMP    LF034   ;3
LF43E: .byte $80,$70,$60,$50,$40,$30,$20,$10,$00,$F0,$E0,$D0,$C0,$B0,$A0,$90
LF44E: AND    #$0F    ;2
       ASL            ;2
       ASL            ;2
       ASL            ;2
       ADC    #$9C    ;2
       TAY            ;2
       TXA            ;2
       .byte $4B ;.ASR;2
       BEQ    LF4C3   ;2
       .byte $9C ;.SHY;5
       TAX            ;2
       RTS            ;6

LF45D: LDA    #$0E    ;2
       STA    $A3     ;3
       LDA    #$3A    ;2
       STA    COLUPF  ;3
       LDA    #$C6    ;2
       STA    COLUP0  ;3
       LDA    #$1E    ;2
       STA    COLUP1  ;3
       LDA    #$00    ;2
       STA    COLUBK  ;3
       LDX    #$2F    ;2
       STX    $8A     ;3
       LDA    #$F9    ;2
       STA    $8B     ;3
       LDA    #$07    ;2
       STA    $8E     ;3
       LDX    #$37    ;2
       STX    $8C     ;3
       LDA    #$F9    ;2
       STA    $8D     ;3
       LDA    #$07    ;2
       STA    $8F     ;3
       LDX    #$1F    ;2
       JMP    LF4AE   ;3
LF48E: .byte $FF,$FF,$FF,$FF,$80,$00,$00,$80,$80,$00,$00,$80,$80,$00,$00,$80
       .byte $80,$00,$FF,$83,$80,$00,$80,$82,$80,$00,$80,$82,$FF,$FF,$FF,$FF
LF4AE: LDA    LF48E,X ;4
       STA    $A4,X   ;4
       DEX            ;2
       BPL    LF4AE   ;2
       LDA    #$20    ;2
       STA    $80     ;3
       LDA    #$20    ;2
       STA    $85     ;3
       LDA    #$64    ;2
       STA    $81     ;3
       LDA    #$32    ;2
       STA    $86     ;3
       LDA    #$00    ;2
       STA    $95     ;3
       LDA    #$00    ;2
       STA    $94     ;3
       LDA    #$00    ;2
       STA    $93     ;3
       LDA    #$00    ;2
       STA    $D6     ;3
LF4D6: LDA    $D6     ;3
       BEQ    LF4DD   ;2
       JMP    LF50A   ;3
LF4DD: JSR    LF525   ;6
       BIT    WSYNC   ;3
       BPL    LF4EC   ;2
       LDA    $D4     ;3
       STA    $80     ;3
       LDA    $D5     ;3
       STA    $85     ;3
LF4EC: BIT    COLUP1  ;3
       BPL    LF504   ;2
       LDA    #$01    ;2
       STA    $D6     ;3
LF4F4: LDA    #$00    ;2
       STA    $D7     ;3
       LDA    #$74    ;2
       STA    $95     ;3
       LDA    #$31    ;2
       STA    $94     ;3
       LDA    #$76    ;2
       STA    $93     ;3
LF504: JSR    LF3BD   ;6
       JMP    LF4D6   ;3
LF50A: LDA    $D7     ;3
       BNE    LF515   ;2
       JSR    LF562   ;6
       LDA    #$01    ;2
       STA    $D7     ;3
LF515: LDA    #$01    ;2
       BIT    SWCHB   ;4
       BNE    LF51F   ;2
       JMP    (LFFFC) ;5
LF51F: JSR    LF3BD   ;6
       JMP    LF50A   ;3
LF525: LDA    $80     ;3
       STA    $D4     ;3
       LDA    $85     ;3
       STA    $D5     ;3
       BIT    SWCHA   ;4
       BVS    LF539   ;2
       LDA    $80     ;3
       SEC            ;2
       SBC    #$01    ;2
       STA    $80     ;3
LF539: BIT    SWCHA   ;4
       BMI    LF545   ;2
       LDA    $80     ;3
       CLC            ;2
       ADC    #$01    ;2
       STA    $80     ;3
LF545: LDA    #$10    ;2
       BIT    SWCHA   ;4
       BNE    LF553   ;2
       LDA    $85     ;3
       SEC            ;2
       SBC    #$01    ;2
       STA    $85     ;3
LF553: LDA    #$20    ;2
       BIT    SWCHA   ;4
       BNE    LF561   ;2
       LDA    $85     ;3
       CLC            ;2
       ADC    #$01    ;2
       STA    $85     ;3
LF561: RTS            ;6

LF562: LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$00    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$02    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$02    ;2
       LDA    #$00    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$02    ;2
       LDA    #$02    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$01    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$05    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$02    ;2
       LDA    #$04    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$02    ;2
       LDA    #$05    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$05    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$08    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$09    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$0A    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$02    ;2
       LDA    #$09    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$09    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$0D    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$0E    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$02    ;2
       LDA    #$0C    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$02    ;2
       LDA    #$0D    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$0D    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$0E    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$10    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$11    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$12    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$02    ;2
       LDA    #$10    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$02    ;2
       LDA    #$12    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$10    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$11    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$12    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$14    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$15    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$16    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$18    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$19    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$1A    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$02    ;2
       LDA    #$18    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$02    ;2
       LDA    #$1A    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$18    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$19    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$1A    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$1C    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$01    ;2
       LDA    #$1D    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$02    ;2
       LDA    #$1D    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$02    ;2
       LDA    #$1E    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$1C    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$03    ;2
       LDA    #$1D    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$19    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$02    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$18    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$1D    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$04    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$16    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$1E    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$01    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$0A    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$15    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$08    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$0E    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$0D    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$0C    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$14    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$00    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$12    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$11    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$09    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$1C    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$05    ;2
       LDA    #$1A    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$15    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$0C    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$1E    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$08    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$19    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$09    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$00    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$0A    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$12    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$18    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$02    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$16    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$11    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$14    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$0D    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$10    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$0E    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$1D    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$01    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$1C    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$06    ;2
       LDA    #$04    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$0D    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$1C    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$18    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$09    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$0E    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$16    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$02    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$12    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$00    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$11    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$19    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$1D    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$04    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$10    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$15    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$0A    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$14    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$1A    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$0C    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$01    ;2
       JSR    LF278   ;6
       LDX    #$00    ;2
       LDY    #$07    ;2
       LDA    #$08    ;2
       JSR    LF278   ;6
       RTS            ;6

LF92F: .byte $3C,$7E,$FF,$DB,$FF,$7E,$3C,$18,$18,$3C,$7E,$18,$18,$7E,$FF,$7E
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF
LFCC6: .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF,$3C,$66,$66,$66,$66,$66,$66,$3C,$7E,$18
       .byte $18,$18,$18,$38,$18,$08,$7E,$60,$60,$3C,$06,$06,$46,$3C,$3C,$46
       .byte $06,$06,$1C,$06,$46,$3C,$0C,$0C,$7E,$4C,$4C,$2C,$1C,$0C,$3C,$46
       .byte $06,$06,$3C,$60,$60,$7E,$3C,$66,$66,$66,$7C,$60,$62,$3C,$30,$30
       .byte $30,$18,$0C,$06,$42,$3E,$3C,$66,$66,$66,$3C,$66,$66,$3C,$3C,$46
       .byte $06,$3E,$66,$66,$66,$3C,$00,$00,$00,$00,$00,$00,$00,$00,$FF,$FF
       .byte $FF,$FF,$FF,$FF,$FF,$FF
LFFFC: .byte $00,$F0,$00,$F0
