/*
 * GPIO_Test.c
 *
 *  Created on: Jan 12, 2023
 *      Author: user
 */
#include "BIT_CALC.h"
#include "STD_Types.h"
#include "RCC_Interface.h"
#include "GPIO_Interface.h"
//-------------------------------------------------------------------
void main()
{
	MRCC_voidInit();
	MRCC_voidPeripheralEnable(AHB1,GPIOAEN);
	MGPIO_SetPinDirection(GPIO_PORTA,GPIO_Pin0,OUTPUT_PUSH_PULL,2);
	MGPIO_voidSetPinValue(GPIO_PORTA,GPIO_Pin0,1);
	while(1)
	{

	}
}
