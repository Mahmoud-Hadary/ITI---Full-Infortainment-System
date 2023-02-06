/*
 * ADC_Private.h
 *
 *  Created on: Jan 29, 2023
 *      Author: dubai key
 */

#ifndef ADC_PRIVATE_H_
#define ADC_PRIVATE_H_
//**********************************************************


//--------locations of bits in the ADC Registers--------
#define ADC_SWSTART   30 //start conversion bit in ADC_CR2
#define ADC_Align     11 //bit to choose allignment left or right
#define ADC_EOCS      10 //bit to choose type of end of conversion
#define ADC_ON        0  //bit to enable ADC
#define ADC_CSL       20 //4bits to chose the sequence length of regular channel
#define ADC_PreScaler 16 //2bits to choose pre-Scaler of the ADC clock
#define ADC_TSVREFE   23 //1 bit to enable or disable the Vref
#define ADC_VBATE     22 //1 bit to enable or disable the Vbat
#define ADC_DISCEN    11 //1 bit to enable or disable the discontinous mode on the regular channels
#define ADC_SCAN      8  //1 bit to enable or disable the scan mode
#define ADC_CONT      1  //1 bit to enable or disable the continous mode or the single conversion mode
#define ADC_DMA       8  //1 bit to enable or disbale the DMA mode
#define ADC_EOC       1  //1 bit to indicate the end of conversion of a regular channel
#define ADC_EOCIE     5  //1 bit to enable or disable the generation of interrupt at the end of conversion

//------------------------------------------------------
#define ADC ((volatile ADC_t *)0x40012000)

typedef struct
{
	volatile u32 SR;
	volatile u32 CR1;
	volatile u32 CR2;
	volatile u32 SMPR1;
	volatile u32 SMPR2;
	volatile u32 JOFR1;
	volatile u32 JOFR2;
	volatile u32 JOFR3;
	volatile u32 JOFR4;
	volatile u32 HTR;
	volatile u32 LTR;
	volatile u32 SQR1;
	volatile u32 SQR2;
	volatile u32 SQR3;
	volatile u32 JSQR;
	volatile u16 JDR1;
	volatile u16 JDR1_MSB;//reserved
	volatile u16 JDR2;
	volatile u16 JDR2_MSB;//reserved
	volatile u16 JDR3;
	volatile u16 JDR3_MSB;//reserved
	volatile u16 JDR4;
	volatile u16 JDR4_MSB;//reserved
	volatile u16 DR;
	volatile u16 DR_MSB;//reserved
	volatile u32 CCR;
}ADC_t;


#endif /* ADC_PRIVATE_H_ */
