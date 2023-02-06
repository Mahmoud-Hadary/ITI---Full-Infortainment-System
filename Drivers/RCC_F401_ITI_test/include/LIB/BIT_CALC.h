#ifndef BIT_CALC_H
#define BIT_CALC_H

#define Set_Bit(Var,Bit_No)    (Var) |=  (1 << (Bit_No))

#define Clear_Bit(Var,Bit_No)  (Var) &= ~(1 << (Bit_No))

#define Toggle_Bit(Var,Bit_No) (Var) ^=  (1 << (Bit_No))

#define Get_Bit(Var,Bit_No)    ( ((Var) >> (Bit_No)) & (1) )

#define Assign_Bit(Var,Bit_No,Value) do{if(Value == 1) Set_Bit(Var,Bit_No); \
										else Clear_Bit(Var,Bit_No);}while(0)

#define CONC_BIt(b7,b6,b5,b4,b3,b2,b1,b0)       Conc_help(b7,b6,b5,b4,b3,b2,b1,b0)
#define Conc_help(b7,b6,b5,b4,b3,b2,b1,b0)      0b##b7##b6##b5##b4##b3##b2##b1##bo

#endif

