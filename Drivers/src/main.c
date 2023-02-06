/*
 * This file is part of the µOS++ distribution.
 *   (https://github.com/micro-os-plus)
 * Copyright (c) 2014 Liviu Ionescu.
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom
 * the Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

#include "../include/lib/BIT_CALC.h"
#include "../include/lib/STD_Types.h"
#include "../include/MCAL/RCC/RCC_Interface.h"
#include "../include/MCAL/GPIO/GPIO_Interface.h"
#include "../include/MCAL/NVIC/NVIC_Interface.h"
#include "../include/MCAL/EXTI/EXTI_Interface.h"
#include "../include/MCAL/ADC/ADC_Interface.h"
#include "../include/MCAL/SYSTICK/SYSTICK_Interface.h"
////////////////////////////////////////////////////////////////
u16 Global_u16Data=0;
///////////////////////////////////////////////////////////
void LED(void)
{
	//GPIO_voidSetPinValue(GPIOA_PORT,PIN0,1);
	MSYSTICK_voidSetBusyWait(10,SEC);
	//GPIO_voidSetPinValue(GPIOA_PORT,PIN0,0);
	MSYSTICK_voidSetBusyWait(10,SEC);
}
/////////////////////////////////////////////////////
void ADC_Test(void)
{
	/* Read Data */
	Global_u16Data = ADC_u16GetData();
}
////////////////////////////////////////////////////////
int main()
{
	u8 arr[1]={7};
	f32 data=0;
	u16 fg=0;
	MRCC_voidINIT();
	MRCC_voidPeripheral(AHB1_H,AHB1_H_GPIOAEN,ON);
	MRCC_voidPeripheral(APB2_H,APB2_H_ADC1EN,ON);
	ADC_voidInit(0,0);
	//ADC_voidChannelSelection(1, arr);
	MGPIO_voidSetPinDirection(GPIOA_PORT,PIN7,ANALOG,2);
	MGPIO_voidSetPinDirection(GPIOA_PORT,PIN0,OUTPUT_PUSH_PULL_DOWN,2);
	MGPIO_voidSetPinDirection(GPIOA_PORT,PIN1,OUTPUT_PUSH_PULL_DOWN,2);
	MGPIO_voidSetPinDirection(GPIOA_PORT,PIN3,OUTPUT_PUSH_PULL_DOWN,2);
	while(1)
	{
		fg = ADC_u16SingleConversion_Regular();
		data = (3.3*1000*fg)/4096.0;
		if(data <= 2 )
		{
			GPIO_voidSetPinValue(GPIOA_PORT,PIN0,1);
			GPIO_voidSetPinValue(GPIOA_PORT,PIN1,0);
		}
		else if (data > 2)
		{
			GPIO_voidSetPinValue(GPIOA_PORT,PIN0,0);
			GPIO_voidSetPinValue(GPIOA_PORT,PIN1,1);
		}



	}
return 0;
}
