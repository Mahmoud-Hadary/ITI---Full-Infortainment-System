/*
 * RCC_F401_Config.h
 *
 *  Created on: Dec 28, 2022
 *      Author: moham
 */

#ifndef RCC_F401_CONFIG_H_
#define RCC_F401_CONFIG_H_

#define RDY_WAIT_TIME  5000
#define PERIPHERALENABLEMODE  1    // 0 For Low Power Mode  ,  1 For High Power Mode

// HSI - HSE - PLL
#define CLK_SOURCE 		PLL

#if CLK_SOURCE == PLL
// HSI , HSE
#define PLL_SOURCE      HSI
#endif

#define PLLP_VALUE		2
#define PLLQ_VALUE		2
#define PLLM_VALUE		2
#define PLLN_VALUE		2





#define AHB_PRESCALER	0
#define APB1_PRESCALER  0b100
#define APB2_PRESCALER  0


#endif /* RCC_F401_CONFIG_H_ */
