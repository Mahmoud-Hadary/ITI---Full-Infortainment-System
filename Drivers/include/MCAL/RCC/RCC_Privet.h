/*
 * RCC_Privet.h
 *
 *  Created on: Dec 25, 2022
 *      Author: Mostafa Rashed
 */

#ifndef RCC_PRIVET_H_
#define RCC_PRIVET_H_


//RCC register
#define RCC ((volatile RCC_t *)0x40023800)

typedef struct
{
	volatile u32 CR;
	volatile u32 PLLCFGR;
	volatile u32 CFGR;
	volatile u32 CIR;
	volatile u32 AHB1RSTR;
	volatile u32 AHB2RSTR;
	volatile u32 Reserved1[2];
	volatile u32 APB1RSTR;
	volatile u32 APB2RSTR;
	volatile u32 Reserved2[2];
	volatile u32 AHB1ENR;
	volatile u32 AHB2ENR;
	volatile u32 Reserved3[2];
	volatile u32 APB1ENR;
	volatile u32 APB2ENR;
	volatile u32 Reserved4[2];
	volatile u32 AHB1LPENR;
	volatile u32 AHB2LPENR;
	volatile u32 Reserved5[2];
	volatile u32 APB1LPENR;
	volatile u32 APB2LPENR;
	volatile u32 Reserved6[2];
	volatile u32 BDCR;
	volatile u32 CSR;
	volatile u32 Reserved7[2];
	volatile u32 SSCGR;
	volatile u32 PLLI2SCFGR;
	volatile u32 Reserved8;
	volatile u32 DCKCFGR;
}RCC_t;
//
#define CR_HSI_RDY_BIT 0
#define CR_HSE_RDY_BIT 17
#define CR_PLL_RDY_BIT 25
//
#define CFGR_SW_BIT0 0
#define CFGR_SW_BIT1 1
//
#define CR_HSI_ON_BIT  0
#define CR_HSI_OFF_BIT 1
//
#define CR_HSE_ON_BIT  16
#define CR_HSE_OFF_BIT 17
//
#define CR_PLL_ON_BIT  24
#define CR_PLL_OFF_BIT 25
//
#define PLLCFGR_PLL_SOURCE_BIT 22
//
#define CFGR_PPRE1 10
#define CFGR_PPRE2 13
#define CFGR_HPRE  4
//

#endif /* RCC_PRIVET_H_ */
