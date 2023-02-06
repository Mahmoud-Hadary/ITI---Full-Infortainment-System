/*
 * RCCC_Config.h
 *
 *  Created on: Jan 12, 2023
 *      Author: user
 */
#ifndef INCLUDE_MCAL_LAYER_RCC_DRIVER_RCCC_CONFIG_H_
#define INCLUDE_MCAL_LAYER_RCC_DRIVER_RCCC_CONFIG_H_
//--------------------------------------------------
#define RDY_WAIT_TIME 5000


/* HSI  -  HSE  -  PLL */
#define CLK_SOURCE  HSI

/* HSI  -  HSE */
#define PLL_SOURCE  HSE

/* 2 - 3 - 4 - .... 63 */
#define PLLM_VALUE  25

/* 50 - 51 - 52 - .... 432 */
#define PLLN_VALUE  160

/*
 * 0: PLLP = 2
 * 1: PLLP = 4
 * 2: PLLP = 6
 * 3: PLLP = 8
 */
#define PLLP_VALUE  2

#define PLLQ_VALUE  2
/*
 * 0xxx: system clock not divided
 * 1000: system clock divided by 2
 * 1001: system clock divided by 4
 * 1010: system clock divided by 8
 * 1011: system clock divided by 16
 * 1100: system clock divided by 64
 * 1101: system clock divided by 128
 * 1110: system clock divided by 256
 * 1111: system clock divided by 512
 */
#define AHB_PRESCALER	0


/*
 * 0xx: AHB clock not divided
 * 100: AHB clock divided by 2
 * 101: AHB clock divided by 4
 * 110: AHB clock divided by 8
 * 111: AHB clock divided by 16
 */
#define APB1_PRESCALER	0b100
#define APB2_PRESCALER	0
//--------------------------------------------------
#endif /* INCLUDE_MCAL_LAYER_RCC_DRIVER_RCCC_CONFIG_H_ */
