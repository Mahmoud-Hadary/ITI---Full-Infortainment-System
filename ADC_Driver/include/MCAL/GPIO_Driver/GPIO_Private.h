/*
 * GPIO_Private.h
 *
 *  Created on: Jan 12, 2023
 *      Author: user
 */
#ifndef INCLUDE_MCAL_LAYER_GPIO_DRIVER_GPIO_PRIVATE_H_
#define INCLUDE_MCAL_LAYER_GPIO_DRIVER_GPIO_PRIVATE_H_
//----------------------------------------------------
#define GPIOC  ((volatile GPIO_t *)0x40020800)
#define GPIOB  ((volatile GPIO_t *)0x40020400)
#define GPIOA  ((volatile GPIO_t *)0x40020000)

typedef struct {

	volatile u32 MODER;
	volatile u32 OTYPER;
	volatile u32 OSPEEDR;
	volatile u32 PUPDR;
	volatile u32 IDR;
	volatile u32 ODR;
	volatile u32 BSRR;
	volatile u32 LCKR;
	volatile u32 AFRL;
	volatile u32 AFRH;

}GPIO_t;
//----------------------------------------------------
#endif /* INCLUDE_MCAL_LAYER_GPIO_DRIVER_GPIO_PRIVATE_H_ */
