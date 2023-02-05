/*
 * ADC_Program.c
 *
 *  Created on: Jan 29, 2023
 *      Author: hader
 */

#include "BIT_CALC.h"
#include "STD_Types.h"
#include "GPIO_Interface.h"
#include "GPIO_Private.h"
#include "GPIO_Config.h"
#include "NVIC_Interface.h"
#include "NVIC_Private.h"
#include "NVIC_Config.h"
#include "EXTI_Interface.h"
#include "EXTI_Private.h"
#include "EXTI_Config.h"
#include "ADC_Interface.h"
#include "ADC_Private.h"
#include "ADC_Interface.h"

//--------------------------------------------------------------------
void MADC_void_SetADCResolution(u8 Copy_u8_Resolution) //0,1,2,3
{
	ADC->CR1 &= ~(3<<24); //bit mask
	ADC->CR1 |= (Copy_u8_Resolution<<24); //put the resolution bits in its place
}
//---------------------------------------------------------------------
void MADC_void_SetChannelsSamplingTime(u8 Copy_u8_ChannelNumber,u8 Copy_u8_ChannelSmaplingTime)
{
	if( (Copy_u8_ChannelNumber >=0) && (Copy_u8_ChannelNumber <= 9) ) //(ADC_SMPR2) register
	{
		u16 LOC_ShiftValue = Copy_u8_ChannelNumber + (Copy_u8_ChannelNumber*2); //0-0 , 1-3, 2-6 ---> 9-27
		ADC->SMPR2 &= ~(7<<LOC_ShiftValue);
		ADC->SMPR2 |= (Copy_u8_ChannelSmaplingTime<<LOC_ShiftValue);
	}
	else if((Copy_u8_ChannelNumber >9) && (Copy_u8_ChannelNumber <= 18)) //(ADC_SMPR1) register
	{
		switch(Copy_u8_ChannelNumber)
		{
			case 10:
				ADC->SMPR1 &= ~(7<<0);
				ADC->SMPR1 |= (Copy_u8_ChannelSmaplingTime<<0);
			break;

			case 11:
				ADC->SMPR1 &= ~(7<<3);
				ADC->SMPR1 |= (Copy_u8_ChannelSmaplingTime<<3);
			break;

			case 12:
				ADC->SMPR1 &= ~(7<<6);
				ADC->SMPR1 |= (Copy_u8_ChannelSmaplingTime<<6);
			break;

			case 13:
				ADC->SMPR1 &= ~(7<<9);
				ADC->SMPR1 |= (Copy_u8_ChannelSmaplingTime<<9);
			break;

			case 14:
				ADC->SMPR1 &= ~(7<<12);
				ADC->SMPR1 |= (Copy_u8_ChannelSmaplingTime<<12);
			break;

			case 15:
				ADC->SMPR1 &= ~(7<<15);
				ADC->SMPR1 |= (Copy_u8_ChannelSmaplingTime<<15);
			break;

			case 16:
				ADC->SMPR1 &= ~(7<<18);
				ADC->SMPR1 |= (Copy_u8_ChannelSmaplingTime<<18);
			break;

			case 17:
				ADC->SMPR1 &= ~(7<<21);
				ADC->SMPR1 |= (Copy_u8_ChannelSmaplingTime<<21);
			break;

			case 18:
				ADC->SMPR1 &= ~(7<<24);
				ADC->SMPR1 |= (Copy_u8_ChannelSmaplingTime<<24);
			break;
		}
	}
}
//---------------------------------------------------------------------
void MADC_void_SetADCRegularSeq(u8 Copy_u8_ChannelSeqLength,u8 Copy_u8_ChannelNumber, u8 Copy_u8_ConversionNumber) //up to 16 conversion on up to 19 channels(0-18) , e7na 3andena men 0-9
{
	ADC->SQR1 &= ~(15<<ADC_CSL); //4 bits
	ADC->SQR1 |= (Copy_u8_ChannelSeqLength <<ADC_CSL);
	switch(Copy_u8_ConversionNumber) //which conversion in the normal group
	{
		case  ADC_OneConversion: //i want to do single conversion on single channel (simplest ADC conversion)
			switch(Copy_u8_ChannelNumber) //which channel number will be assigned to this conversion
			{
				ADC->SQR3 &= ~(31<<0); //5 bits
				ADC->SQR3 |= (Copy_u8_ChannelNumber<<0); //hena keda ana olt en 3andy 1 conversion wel conversion de hat7sal 3alla anhy Channel
			}
		break;
	}
}
//---------------------------------------------------------------------
void MADC_void_SetADCPreScaler(u8 Copy_u8_ADCPreScaler)
{
	switch(Copy_u8_ADCPreScaler)
	{
		case ADC_PreScalerTwo: //choose 2 as prescaler
			ADC->CCR &= ~(3<<16);
			ADC->CCR |= (ADC_PreScalerTwo<<16);
		break;

		case ADC_PreScalerFour: //choose 4 as presacler
			ADC->CCR &= ~(3<<16);
			ADC->CCR |= (ADC_PreScalerFour<<16);
		break;

		case ADC_PreScalerSix: //choose 6 as prescaler
			ADC->CCR &= ~(3<<16);
			ADC->CCR |= (ADC_PreScalerSix<<16);
		break;

		case ADC_PreScalerEight: //choose 6 as prescaler
			ADC->CCR &= ~(3<<16);
			ADC->CCR |= (ADC_PreScalerEight<<16);
		break;
	}
}
//---------------------------------------------------------------------
void MADC_void_SetSequenceLength(u8 Copy_u8_ConversionsNumber)
{
	ADC->SQR1 &= ~(15<<ADC_CSL);
	ADC->SQR1 |= (Copy_u8_ConversionsNumber<<ADC_CSL); //to customize the sequence length
}
//---------------------------------------------------------------------
void MADC_void_SetChannelNumberToBeConverted(u8 Copy_u8_ChannelNumber)
{
	ADC->SQR3 &= ~(31); //bit mask
	ADC->SQR3 |= Copy_u8_ChannelNumber; //7otly el channel ely ana 3awez a3mel 3aleha el conversion fe awel 5 bits
}
//---------------------------------------------------------------------
void MADC_INIT_SingleConversion(u8 Copy_u8_Resolution) //Setup the ADC Configurations
{
	Set_Bit(ADC->CR2,ADC_ON); //enable the ADC Periphral
	MADC_void_SetADCResolution(Copy_u8_Resolution); //choose a resolution
	MADC_void_SetADCPreScaler(ADC_PreScalerTwo); //set the Prescaler of the ADC clock to be two
	Clear_Bit(ADC->CR1,ADC_DISCEN);//disable the discontinous mode on the ADC regular Channels
	Clear_Bit(ADC->CR1,ADC_SCAN);//disable the scan mode
	Set_Bit(ADC->CR2,ADC_CONT); //enable the single conversion mode
	Clear_Bit(ADC->CR2,ADC_DMA); //disable the DMA mode
	Clear_Bit(ADC->CR2,ADC_Align); //choose Right Alignment
	Clear_Bit(ADC->CR2,ADC_EOCS); // EOC = 1 and EOCS = 0 means that conversion complete
	Set_Bit(ADC->CCR,ADC_TSVREFE); //set ref voltage
	Clear_Bit(ADC->CCR,ADC_VBATE); //disable Vbat for Vref to work
	MADC_void_SetSequenceLength(ADC_1ConversionSequenceLEN);//set the length of the sequence to be 1 conversion, y3ny 3awez a3mel only one conversion
	MADC_void_SetChannelsSamplingTime(0,2); //set channel zero sampling time to be 28 cycles
}
//---------------------------------------------------------------------
void MADC_INIT_SingleConversionUsingINT(u8 Copy_u8_Resolution) //setup ADC configurations to use the interrupt
{
	Set_Bit(ADC->CR2,ADC_ON); //enable the ADC Periphral
	MADC_void_SetADCResolution(Copy_u8_Resolution); //choose a resolution
	MADC_void_SetADCPreScaler(ADC_PreScalerTwo); //set the Prescaler of the ADC clock to be two
	Clear_Bit(ADC->CR1,ADC_DISCEN);//disable the discontinous mode on the ADC regular Channels
	Clear_Bit(ADC->CR1,ADC_SCAN);//disable the scan mode
	Set_Bit(ADC->CR2,ADC_CONT); //enable the single conversion mode
	Clear_Bit(ADC->CR2,ADC_DMA); //disable the DMA mode
	//----------------------------------------------------
	Set_Bit(ADC->CR1,ADC_EOCIE);//enable the generation of an interrupt at the end of conversion , this is the only difference in the two init functions
	//----------------------------------------------------
	Clear_Bit(ADC->CR2,ADC_Align); //choose Right Alignment
	Clear_Bit(ADC->CR2,ADC_EOCS); // EOC = 1 and EOCS = 0 means that conversion complete
	Set_Bit(ADC->CCR,ADC_TSVREFE); //set ref voltage
	Clear_Bit(ADC->CCR,ADC_VBATE); //disable Vbat for Vref to work
	MADC_void_SetSequenceLength(ADC_1ConversionSequenceLEN);//set the length of the sequence to be 1 conversion, y3ny 3awez a3mel only one conversion
	MADC_void_SetChannelsSamplingTime(0,2); //set channel zero sampling time to be 28 cycles
}
//---------------------------------------------------------------------
u16 MADC_u16_StartSingleConversion(u8 Copy_u8_ChannelNumber)
{
	u16 Loc_u16_ADCResult=0;
	MADC_void_SetChannelNumberToBeConverted(Copy_u8_ChannelNumber); //set which channel to use
	Set_Bit(ADC->CR2,ADC_SWSTART); // start conversion of regular channels , ely hena hena one channel ely ana 3awez a3mel 3aleha single conversion
	while(Get_Bit(ADC->SR,ADC_EOC) != 1)
	{
		//conversion didn't end so stay here until it ends
		//polling on the flag
	}
	Clear_Bit(ADC->SR,ADC_EOC); //EOC flag is cleared by SW
	Loc_u16_ADCResult = ADC->DR; //put the 16  bit of data in the local variable
	return Loc_u16_ADCResult;
}
//---------------------------------------------------------------------
u16 Glob_u16_ADCResultUsingINT;
//---------------------------------------------------------------------
u16 MADC_u16_StartSingleConversionUsingINT(u8 Copy_u8_ChannelNumber)
{
	u16 Loc_Wait = 5000;
	MADC_void_SetChannelNumberToBeConverted(Copy_u8_ChannelNumber); //set which channel to use
	Set_Bit(ADC->CR2,ADC_SWSTART); // start conversion of regular channels , ely hena hena one channel ely ana 3awez a3mel 3aleha single conversion
	while(Loc_Wait != 0)
	{
		Loc_Wait--;
	}
	return Glob_u16_ADCResultUsingINT; //return the value written inside the data register which we put in the global variable in the ISR
}
//---------------------------------------------------------------------
void ADC_IRQHandler(void) //ISR of ADC end of conversion interrupt
{
	Clear_Bit(ADC->SR,ADC_EOC);
	Glob_u16_ADCResultUsingINT = ADC->DR;
}
//---------------------------------------------------------------------
