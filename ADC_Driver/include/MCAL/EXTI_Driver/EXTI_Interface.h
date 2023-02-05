/*
 * EXTI_Interface.h
 *
 *  Created on: Jan 22, 2023
 *      Author: user
 */

#ifndef INCLUDE_MCAL_LAYER_EXTI_DRIVER_EXTI_INTERFACE_H_
#define INCLUDE_MCAL_LAYER_EXTI_DRIVER_EXTI_INTERFACE_H_
//------------------------------------------------------
#define EXTI0_EN  0
#define EXTI1_EN  1
#define EXTI2_EN  2
#define EXTI3_EN  3
#define EXTI4_EN  4
#define EXTI5_EN  5
#define EXTI6_EN  6
#define EXTI7_EN  7
#define EXTI8_EN  8
#define EXTI9_EN  9
#define EXTI10_EN 10
#define EXTI11_EN 11
#define EXTI12_EN 12
#define EXTI13_EN 13
#define EXTI14_EN 14
#define EXTI15_EN 15

#define FALLING_EDGE 0
#define RISING_EDGE 1
#define ON_CHANGE_EDGE 2

void MEXTI_voidConfig(u8 copy_u8EXTILine, u8 copy_u8PORT, u8 copy_u8SenseMode);
void EXTI0_VoidSetCallBack(void (*ptr)(void));
void MEXTI_voidDisable(u8 copy_u8EXTILine);
//-------------------------------------------------------
#endif /* INCLUDE_MCAL_LAYER_EXTI_DRIVER_EXTI_INTERFACE_H_ */
