/*
 * Interrupt_Test.c
 *
 *  Created on: Jan 23, 2023
 *      Author: user
 */
#include "BIT_CALC.h"
#include "STD_Types.h"
#include "RCC_Interface.h"
#include "GPIO_Interface.h"
#include "NVIC_Interface.h"
#include "EXTI_Interface.h"
//--------------------------------------------------------------
void BlinkLED(void)
{
	static u8 flag =0;
	if (flag==0)
	{
		MGPIO_voidSetPinValue(GPIO_PORTA,1,1); //dosa el lamba tnawar
		flag =1;
	}
	else
	{
		MGPIO_voidSetPinValue(GPIO_PORTA,1,0); //dosa el lamba ttfy
		flag =0;
	}
}
//--------------------------------------------------------------
int main()
{
	MRCC_voidInit();
	MRCC_voidPeripheralEnable(AHB1,GPIOAEN);
	MGPIO_SetPinDirection(GPIO_PORTA,GPIO_Pin1,OUTPUT_PUSH_PULL,GPIO_MedSpeed);
	MGPIO_SetPinDirection(GPIO_PORTA,GPIO_Pin0,INPUT_PULL_UP,GPIO_MedSpeed);
	EXTI0_VoidSetCallBack(BlinkLED);
	MEXTI_voidConfig(EXTI0_EN,GPIO_PORTA,FALLING_EDGE);
	MNVIC_VoidEnablePeriphral(EXTI0);
	while(1)
	{

	}
}



