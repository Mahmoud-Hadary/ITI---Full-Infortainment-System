/*
 * ADC_Test.c
 *
 *  Created on: Jan 28, 2023
 *      Author: hader
 */
#include "BIT_CALC.h"
#include "STD_Types.h"
#include "RCC_Interface.h"
#include "GPIO_Interface.h"
#include "NVIC_Interface.h"
#include "EXTI_Interface.h"
#include "ADC_Interface.h"
//------------------------------------------------------------------
int main()
{
	MRCC_voidInit();
	MRCC_voidPeripheralEnable(AHB1,GPIOAEN);
	MRCC_voidPeripheralEnable(APB2,ADC1EN);
	//MADC_INIT_SingleConversion(ADC_12BitResolution);
	MNVIC_VoidEnablePeriphral(ADC_NVIC);
	MADC_INIT_SingleConversionUsingINT(ADC_12BitResolution);

	MGPIO_SetPinDirection(GPIO_PORTA,GPIO_Pin0,INPUT_ANALOG,GPIO_MedSpeed);
	MGPIO_SetPinDirection(GPIO_PORTA,GPIO_Pin1,OUTPUT_PUSH_PULL,GPIO_MedSpeed);
	MGPIO_SetPinDirection(GPIO_PORTA,GPIO_Pin2,OUTPUT_PUSH_PULL,GPIO_MedSpeed);
	MGPIO_SetPinDirection(GPIO_PORTA,GPIO_Pin3,OUTPUT_PUSH_PULL,GPIO_MedSpeed);
	u16 ADC_Res;
	while(1)
	{
		//ADC_Res = MADC_u16_StartSingleConversion(ADC_Channel0);//from 0 to 4095
		ADC_Res = MADC_u16_StartSingleConversionUsingINT(ADC_Channel0);
		if((ADC_Res>= 0) && (ADC_Res<200))
		{
			MGPIO_voidSetPinValue(GPIO_PORTA,GPIO_Pin1,1); //LED 1 on
		}
		else
		{
			MGPIO_voidSetPinValue(GPIO_PORTA,GPIO_Pin1,0); //LED 1 off
		}
	}
	return 0;
}



