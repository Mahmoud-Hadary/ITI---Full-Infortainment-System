/*
 * GPIO_Interface.h
 *
 *  Created on: Jan 12, 2023
 *      Author: user
 */

#ifndef INCLUDE_MCAL_LAYER_GPIO_DRIVER_GPIO_INTERFACE_H_
#define INCLUDE_MCAL_LAYER_GPIO_DRIVER_GPIO_INTERFACE_H_
//------------------------------------------------------
#define GPIO_Pin0		0
#define GPIO_Pin1      1
#define GPIO_Pin2      2
#define GPIO_Pin3      3
#define GPIO_Pin4      4
#define GPIO_Pin5      5
#define GPIO_Pin6      6
#define GPIO_Pin7      7
#define GPIO_Pin8      8
#define GPIO_Pin9      9
#define GPIO_Pin10     10
#define GPIO_Pin11     11
#define GPIO_Pin12     12
#define GPIO_Pin13     13
#define GPIO_Pin14     14
#define GPIO_Pin15     15

#define GPIO_PORTA		0
#define GPIO_PORTB		1
#define GPIO_PORTC		2

#define GPIO_LowSpeed 		0
#define GPIO_MedSpeed 		1
#define GPIO_HighSpeed 		2
#define GPIO_VHighSpeed 	3

#define GPIO_OUTPUT		1
#define GPIO_INPUT		0
//-------------------------------------------------
typedef enum
{
	INPUT_FLOATING = 1,
	INPUT_PULL_UP ,
	INPUT_PULL_DOWN ,
	INPUT_ANALOG ,

	OUTPUT_PUSH_PULL ,
	OUTPUT_PUSH_PULL_PULL_UP ,
	OUTPUT_PUSH_PULL_PULL_DOWN ,

	OUTPUT_OPEN_DRAIN ,
	OUTPUT_PUSH_OPEN_DRAIN_UP ,
	OUTPUT_PUSH_OPEN_DRAIN_DOWN ,

	AF_PUSH_PULL ,
	AF_PUSH_PULL_PULL_UP ,
	AF_PUSH_PULL_PULL_DOWN ,

	AF_OPEN_DRAIN ,
	AF_OPEN_DRAIN_PULL_UP ,
	AF_OPEN_DRAIN_PULL_DOWN ,

}mode;
//---------------------------------------------------
void MGPIO_SetPinDirection(u8 A_u8PortID,u8 A_u8PinID,u8 A_u8Direction,u8 copy_u8Speed);
void MGPIO_voidSetPinValue(u8 A_u8PortID,u8 A_u8PinID,u8 copy_u8Value);
void MGPIO_voidGetPinValue(u8 A_u8PortID,u8 A_u8PinID,u8* copy_u8Value);
void AtomicMGPIO_voidSetPinValue(u8 A_u8PortID,u8 A_u8PinID,u8 copy_u8Value);
//------------------------------------------------------
#endif /* INCLUDE_MCAL_LAYER_GPIO_DRIVER_GPIO_INTERFACE_H_ */
