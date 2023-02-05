/*
 * ADC_Privet.h
 *
 *  Created on: Jan 29, 2023
 *      Author: Mostafa Rashed
 */

#ifndef ADC_PRIVET_H_
#define ADC_PRIVET_H_

////////////////////////////////////////////////////////////////////////////
//ADC register
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
	volatile u32 JDR1;
	volatile u32 JDR2;
	volatile u32 JDR3;
	volatile u32 JDR4;
	volatile u32 DR;
	volatile u32 Reserved[173];
	volatile u32 CCR;
}ADC_t;
/////////////////////////////////////////////////////////////////////////////
// ADC Status Register
typedef enum
{
	ADC_AWD,ADC_EOC,ADC_JEOC,ADC_JSTRT,ADC_STRT,ADC_OVR
}ADC_SR_t;
/////////////////////////////////////////////////////////////////////////////
// ADC Control register (1)
typedef enum
{
	ADC_CR1_AWDCH,ADC_CR1_EOCIE=5,ADC_CR1_AWDIE,ADC_CR1_JEOCIE,ADC_CR1_SCAN,
	ADC_CR1_AWDSGL,ADC_CR1_JAUTO,ADC_CR1_DISCEN,ADC_CR1_JDISCEN,ADC_CR1_DISCNUM,
	ADC_CR1_JAWDEN=22,ADC_CR1_AWDEN,ADC_CR1_Resolution,ADC_CR1_OVRIE=26
}ADC_CR1_t;

// ADC CR1 Resolution
/*
 * 00: 12-bit (15 ADCCLK cycles)
 * 01: 10-bit (13 ADCCLK cycles)
 * 10: 8-bit (11 ADCCLK cycles)
 * 11: 6-bit (9 ADCCLK cycles)
 */
#define ADC_Resolution_12 0
#define ADC_Resolution_10 1
#define ADC_Resolution_8  2
#define ADC_Resolution_6  3

// ADC Control register (2)
typedef enum
{
	ADC_CR2_ADON,ADC_CR2_CONT,ADC_CR2_DMA=8,ADC_CR2_DDS,ADC_CR2_EOCS,
	ADC_CR2_ALIGN,ADC_CR2_JEXTSEL=16,ADC_CR2_JEXTEN=20,ADC_CR2_JSWSTART=22,
	ADC_CR2_EXTSEL=24,ADC_CR2_EXTEN=28,ADC_CR2_SWSTART=30
}ADC_CR2_t;
// Data alignment
/* Regular Group */
#define ADC_Regular_RightAlignment   0
#define ADC_Regular_LeftAlignment    1
/* Injected Group */
#define ADC_Injected_RightAlignment  2
#define ADC_Injected_LeftAlignment   3
//////////////////////////////////////////////////////////////////////
// ADC common control register (CCR)
#define ADC_CCR_prescaler 16
#define ADC_CCR_VBATE     22
#define ADC_CCR_TSVREFE   23
/* ADC CCR Prescaler */
/*
 *	00: PCLK2 divided by 2
 *	01: PCLK2 divided by 4
 *	10: PCLK2 divided by 6
 *	11: PCLK2 divided by 8
 */
#define ADC_Prescaler_2  0
#define ADC_Prescaler_4  1
#define ADC_Prescaler_6  2
#define ADC_Prescaler_8  3
///////////////////////////////////////////////////////////////////////
// ADC  regular sequence register 1 (SQR1)
#define ADC_NumOfChannels 16
/* To detect Length of Channels */
#define ADC_SQR1_Length  20
/* Number of Shifted Bit in SQR1,SQR2,SQR3 */
#define ADC_SQRX_Shifted5  5
#define ADC_SQRX_Shifted10 10
#define ADC_SQRX_Shifted15 15
#define ADC_SQRX_Shifted20 20
#define ADC_SQRX_Shifted25 25
/* Number of Priority */
#define ADC_SQ1  1
#define ADC_SQ2  2
#define ADC_SQ3  3
#define ADC_SQ4  4
#define ADC_SQ5  5
#define ADC_SQ6  6
#define ADC_SQ7  7
#define ADC_SQ8  8
#define ADC_SQ9  9
#define ADC_SQ10 10
#define ADC_SQ11 11
#define ADC_SQ12 12
#define ADC_SQ13 13
#define ADC_SQ14 14
#define ADC_SQ15 15
#define ADC_SQ16 16
//////////////////////////////////////////////////////////////////////////
//
#endif /* ADC_PRIVET_H_ */


