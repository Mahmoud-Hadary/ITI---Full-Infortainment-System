/*
 * RCC_Config.h
 *
 *  Created on: Dec 25, 2022
 *      Author: Mostafa Rashed
 */

#ifndef RCC_CONFIG_H_
#define RCC_CONFIG_H_

#define RDY_WAIT_TIME 5000
/* 2 - 3 - 4 -....64*/
#define PLLM_VALUE 25
/*  PLLN =2
 * 	PLLN =4
 * 	PLLN =6
 * 	PLLN =8
 */
#define PLLN_VALUE  2
/*       */
#define PLLP_VALUE  4
/*       */
#define PLLQ_VALUE  8
/*HSI - HSE - PLL*/
#define CLK_SOURCE HSI
/* HSI - HSE */
#define PLL_SOURCE HSI

// AHB PRECALER  prescaler
/*
 * RCC_CFGR_HPRE_NoPrescaler    0
 * RCC_CFGR_HPRE_PrescalerX2    8
 * RCC_CFGR_HPRE_PrescalerX4    9
 * RCC_CFGR_HPRE_PrescalerX8    10
 * RCC_CFGR_HPRE_PrescalerX16   11
 * RCC_CFGR_HPRE_PrescalerX64   12
 * RCC_CFGR_HPRE_PrescalerX128  13
 * RCC_CFGR_HPRE_PrescalerX256  14
 * RCC_CFGR_HPRE_PrescalerX512  15
 */
#define AHB_PRESCALER  RCC_CFGR_HPRE_PrescalerX2
/*
 * RCC_CFGR_PPRE1_NoPrescaler    0
 * RCC_CFGR_PPRE1_PrescalerX2    4
 * RCC_CFGR_PPRE1_PrescalerX4    5
 * RCC_CFGR_PPRE1_PrescalerX8    6
 * RCC_CFGR_PPRE1_PrescalerX16   7
 */
#define APB1_PRESCALER RCC_CFGR_PPRE1_NoPrescaler
/*
 * RCC_CFGR_PPRE2_NoPrescaler    0
 * RCC_CFGR_PPRE2_PrescalerX2    4
 * RCC_CFGR_PPRE2_PrescalerX4    5
 * RCC_CFGR_PPRE2_PrescalerX8    6
 * RCC_CFGR_PPRE2_PrescalerX16   7
 */
#define APB2_PRESCALER RCC_CFGR_PPRE2_NoPrescaler
#endif /* RCC_CONFIG_H_ */
