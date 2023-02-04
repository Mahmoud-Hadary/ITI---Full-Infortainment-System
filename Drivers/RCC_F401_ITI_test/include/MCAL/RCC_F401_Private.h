/*
 * RCC_F401_Private.h
 *
 *  Created on: Dec 28, 2022
 *      Author: moham
 */

#ifndef RCC_F401_PRIVATE_H_
#define RCC_F401_PRIVATE_H_

#define RCC   ((volatile RCC_t*)0x40023800)

#define CFGR_SW_BIT0  0
#define CFGR_SW_BIT1  1



#define CR_HSI_RDY_BIT  1
#define CR_HSE_RDY_BIT  17
#define CR_PLL_RDY_BIT  25

#define PLLCFGR_PLL_Source_Bit 	22

#define GARBAGE_VALUE 10 ;

#define PLLCFGR_PLLM_LOWER_LIMIT  2
#define PLLCFGR_PLLM_UPPER_LIMIT  63

#define PLLCFGR_PLLN_LOWER_LIMIT  50
#define PLLCFGR_PLLN_UPPER_LIMIT  432

#define PLLCFGR_PLLP_LOWER_LIMIT  2
#define PLLCFGR_PLLP_UPPER_LIMIT  8

#define PLLCFGR_PLLQ_LOWER_LIMIT  2
#define PLLCFGR_PLLQ_UPPER_LIMIT  15





typedef struct
{
	volatile u32 CR ;
	volatile u32 PLLCFGR ;
	volatile u32 CFGR ;
	volatile u32 CIR ;
	volatile u32 AHB1RSTR ;
	volatile u32 AHB2RSTR ;
	volatile u32 Reserved1[2] ;
	volatile u32 APB1RSTR ;
	volatile u32 APB2RSTR ;
	volatile u32 Reserved2[2] ;
	volatile u32 AHB1ENR ;
	volatile u32 AHB2ENR ;
	volatile u32 Reserved3[2] ;
	volatile u32 APB1ENR ;
	volatile u32 APB2ENR ;
	volatile u32 Reserved4[2] ;
	volatile u32 AHB1LPENR ;
	volatile u32 AHB2LPENR ;
	volatile u32 Reserved5[2] ;
	volatile u32 APB1LPENR ;
	volatile u32 APB2LPENR ;
	volatile u32 Reserved6[2] ;
	volatile u32 BDCR ;
	volatile u32 CSR ;
	volatile u32 Reserved7[2] ;
	volatile u32 SSCGR ;
	volatile u32 PLLI2SCFGR ;
	volatile u32 DCKCFGR ;
}RCC_t;


#endif /* RCC_F401_PRIVATE_H_ */
