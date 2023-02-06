/*
 * ADC_Program.c
 *
 *  Created on: Jan 29, 2023
 *      Author: Mostafa Rashed
 */

#include "../include/lib/STD_Types.h"
#include "../include/lib/BIT_CALC.h"

#include "../include/MCAL/ADC/ADC_Privet.h"
#include "../include/MCAL/ADC/ADC_Interface.h"
#include "../include/MCAL/ADC/ADC_Config.h"
/////////////////////////////////////////////////////////////////////////
static void (*ADC_Callback)(void) = NULL;
///////////////////////////////////////////////////////////////////////////
/*
 * Function : Init Function
 * Input :  Prescaler in range ( 0 -> 3 )
 * 			Resolution in range ( 0 -> 3 )
 * Output :	Not return any thing
 */
void ADC_voidInit(u8 Copy_u8Prescaler,u8 Copy_u8Resolution)
{
	/* ADC ON */
	Set_Bit(ADC->CR2,ADC_CR2_ADON);
	/* Set Prescaler */
	ADC_voidSetPrescaler(Copy_u8Prescaler);
	/* Set Resolution */
	ADC_voidSetResolution(Copy_u8Resolution);
	/* Data alignment */
#if ( ADC_DataAlignment == ADC_Regular_RightAlignment )  ||  (ADC_DataAlignment == ADC_Injected_RightAlignment)
	/* Right alignment */
	Clear_Bit(ADC->CR2,ADC_CR2_ALIGN);
#elif ( ADC_DataAlignment == ADC_Regular_LeftAlignment )  ||  (ADC_DataAlignment == ADC_Injected_LeftAlignment)
	/* Left alignment */
	Set_Bit(ADC->CR2,ADC_CR2_ALIGN);
#endif

}
/////////////////////////////////////////////////////////////////////
/*
 * Function : Channels Sampling Time
 * Input :  Prescaler in range ( 0 -> 3 )
 * 			Resolution in range ( 0 -> 3 )
 * Output :	Not return any thing
 */
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
//////////////////////////////////////////////////////////////////////
/*
 * Function : DeInit Function
 * Input :  Don't take any thing
 * Output :	Not return any thing
 */
void ADC_voidDeInit(void)
{
	/* ADC  OFF */
	Clear_Bit(ADC->CR2,ADC_CR2_ADON);
	/* Reset Prescaler */
	ADC_voidSetPrescaler(0);
	/* Reset Resolution */
	ADC_voidSetResolution(0);
	/* Reset Data alignment */
	Clear_Bit(ADC->CR2,ADC_CR2_ALIGN);
}
/////////////////////////////////////////////////
/*
 * Function : to chose channels and priority to ADC run in it (In A Regular Sequence)
 * Input :  Number of channel is used
 * 			Channel priority as pointer to array
 * Output :	Not return any thing (Future return Status of Channel Selection)
 */
void ADC_voidChannelSelection(u8 Copy_u8Length, u8 *Copy_u8ChannelPriority)
{
	/* Check for Limited Number of Channels */
	if ( ( Copy_u8Length > 0 ) && (Copy_u8Length <= ADC_NumOfChannels) && (sizeof(Copy_u8ChannelPriority) <= ADC_NumOfChannels))
	{
		/* Set Length of Channels in SQR1 Register */
		ADC->SQR1 |= (Copy_u8Length<<ADC_SQR1_Length);
		/* Set priority of Channel Selected */
		while(Copy_u8Length != 0)
		{
			/* Selected from register SQR1 OR SQR2 OR SQR3 */
			switch (Copy_u8Length)
			{
			case ADC_SQ1:  ADC->SQR3 |= (Copy_u8ChannelPriority[Copy_u8Length]); 		 				break;
			case ADC_SQ2:  ADC->SQR3 |= (Copy_u8ChannelPriority[Copy_u8Length] << ADC_SQRX_Shifted5);  	break;
			case ADC_SQ3:  ADC->SQR3 |= (Copy_u8ChannelPriority[Copy_u8Length] << ADC_SQRX_Shifted10); 	break;
			case ADC_SQ4:  ADC->SQR3 |= (Copy_u8ChannelPriority[Copy_u8Length] << ADC_SQRX_Shifted15); 	break;
			case ADC_SQ5:  ADC->SQR3 |= (Copy_u8ChannelPriority[Copy_u8Length] << ADC_SQRX_Shifted20); 	break;
			case ADC_SQ6:  ADC->SQR3 |= (Copy_u8ChannelPriority[Copy_u8Length] << ADC_SQRX_Shifted25); 	break;
			case ADC_SQ7:  ADC->SQR2 |= (Copy_u8ChannelPriority[Copy_u8Length]); 		 				break;
			case ADC_SQ8:  ADC->SQR2 |= (Copy_u8ChannelPriority[Copy_u8Length] << ADC_SQRX_Shifted5);  	break;
			case ADC_SQ9:  ADC->SQR2 |= (Copy_u8ChannelPriority[Copy_u8Length] << ADC_SQRX_Shifted10); 	break;
			case ADC_SQ10: ADC->SQR2 |= (Copy_u8ChannelPriority[Copy_u8Length] << ADC_SQRX_Shifted15); 	break;
			case ADC_SQ11: ADC->SQR2 |= (Copy_u8ChannelPriority[Copy_u8Length] << ADC_SQRX_Shifted20); 	break;
			case ADC_SQ12: ADC->SQR2 |= (Copy_u8ChannelPriority[Copy_u8Length] << ADC_SQRX_Shifted25); 	break;
			case ADC_SQ13: ADC->SQR1 |= (Copy_u8ChannelPriority[Copy_u8Length]); 		 				break;
			case ADC_SQ14: ADC->SQR1 |= (Copy_u8ChannelPriority[Copy_u8Length] << ADC_SQRX_Shifted5);  	break;
			case ADC_SQ15: ADC->SQR1 |= (Copy_u8ChannelPriority[Copy_u8Length] << ADC_SQRX_Shifted10); 	break;
			case ADC_SQ16: ADC->SQR1 |= (Copy_u8ChannelPriority[Copy_u8Length] << ADC_SQRX_Shifted15); 	break;
			default: /* Error Input */										   	 				 	   	break;
			}
			Copy_u8Length--;
		}
	}
	else
	{
		// Error in input
	}
}
////////////////////////////////////////////////////
/*
 * Function : To Get Data is Converted
 * Input :  No Input
 * Output :	Return Data Converted in (u16)
 */
u16 ADC_u16GetData(void)
{
	/* Clear end of conversion bit */
	Clear_Bit(ADC->SR,ADC_EOC);
	/* Get Data from Data Register and cast it */
#if ADC_DataAlignment == ADC_Regular_RightAlignment
	// IN case  Right alignment (regular group)
	return (u16)(ADC->DR);
#elif ADC_DataAlignment == ADC_Regular_LeftAlignment
	// Read Resolution Bits for now if 6-bit or larger
	if((Get_Bit(ADC->CR1,24)==1)&&(Get_Bit(ADC->CR1,25)==1))
	{
		// IN case  Left  alignment (regular group)  6-bit
		return (u16)((ADC->DR)>>2);
	}
	else if ((Get_Bit(ADC->CR1,24)==0)&&(Get_Bit(ADC->CR1,25)==0))
	{
		// IN case  Left  alignment (regular group)  12-bit
		return (u16)((ADC->DR)>>4);
	}
	else if ((Get_Bit(ADC->CR1,24)==1)&&(Get_Bit(ADC->CR1,25)==0))
	{
		// IN case  Left  alignment (regular group)  12-bit
		return (u16)((ADC->DR)>>6);
	}
	else if ((Get_Bit(ADC->CR1,24)==0)&&(Get_Bit(ADC->CR1,25)==1))
	{
		// IN case  Left  alignment (regular group)  12-bit
		return (u16)((ADC->DR)>>8);
	}
	else
	{
		// Error Reading
	}
#endif
}
///////////////////////////////////////////////////////////////////////
/*
 * Function : Set Prescaler
 * Input :  Prescaler in range ( 0 -> 3 )
 * Output : Return No Thing
 */
void ADC_voidSetPrescaler(u8 Copy_u8Prescaler)
{
	/* Check Prescaler in range */
	if(Copy_u8Prescaler <= 3)
	{
		// Set 16,17 -> 0
		Clear_Bit(ADC->CCR,16);
		Clear_Bit(ADC->CCR,17);
		// Set Prescaler in CCR Register
		switch(Copy_u8Prescaler)
		{
		case ADC_Prescaler_2: ADC->CCR |= (ADC_Prescaler_2 << ADC_CCR_prescaler); break;
		case ADC_Prescaler_4: ADC->CCR |= (ADC_Prescaler_4 << ADC_CCR_prescaler); break;
		case ADC_Prescaler_6: ADC->CCR |= (ADC_Prescaler_6 << ADC_CCR_prescaler); break;
		case ADC_Prescaler_8: ADC->CCR |= (ADC_Prescaler_8 << ADC_CCR_prescaler); break;
		default: /* Error Input */ break;
		}
	}
	else
	{
		// Error Input
	}
}
/*
 * Function : Set Resolution
 * Input :  Resolution in range ( 0 -> 3 )
 * Output : Return No Thing
 */
void ADC_voidSetResolution(u8 Copy_u8Resolution)
{
	/* Check Resolution in range */
	if(Copy_u8Resolution <= 3)
	{
		// Set 16,17 -> 0
		Clear_Bit(ADC->CR1,24);
		Clear_Bit(ADC->CR1,25);
		// Set Resolution in CR1 Register
		switch(Copy_u8Resolution)
		{
		case ADC_Resolution_12: ADC->CR1 |= (ADC_Resolution_12 << ADC_CR1_Resolution); break;
		case ADC_Resolution_10: ADC->CR1 |= (ADC_Resolution_10 << ADC_CR1_Resolution); break;
		case ADC_Resolution_8 : ADC->CR1 |= (ADC_Resolution_8  << ADC_CR1_Resolution); break;
		case ADC_Resolution_6 : ADC->CR1 |= (ADC_Resolution_6  << ADC_CR1_Resolution); break;
		default: /* Error Input */ break;
		}
	}
	else
	{
		// Error Input
	}
}
/*
 * Function : Single Conversion mode "One Conversion"  (regular group)
 * Input : 	No Input
 * Output : Return Data Converted in (u16)
 */
u16 ADC_u16SingleConversion_Regular(void)
{
	ADC->SQR1 = 1<<ADC_SQR1_Length;
	ADC->SQR3 = 7;
	u16 Local_u16Data = 0;
	/* Clear Continuous conversion */
	Clear_Bit(ADC->CR2,ADC_CR2_CONT);
	/*  Start conversion of regular channels */
	Set_Bit(ADC->CR2,ADC_CR2_SWSTART);
	/* Check Status of Regular channel start flag */
	if(Get_Bit(ADC->SR,ADC_STRT) == 1)
	{
		/* Pooling on flag for Regular channel end of conversion */
		while(Get_Bit(ADC->SR,ADC_EOC) != 1);
	}
	/* Read Data */
	Local_u16Data = ADC_u16GetData();
	/* Return Data conversion */
	return Local_u16Data;
}
/*
 * Function : Continuous Conversion mode  (regular group)
 * Input :  No Input
 * Output : Return Data Converted in (u16)
 */
u16 ADC_u16ContinuousConversion_Regular(void)
{
	u16 Local_u16Data = 0;
	/* Set Continuous conversion */
	Set_Bit(ADC->CR2,ADC_CR2_CONT);
	/*  Start conversion of regular channels */    // for make sure Start conversion
	Set_Bit(ADC->CR2,ADC_CR2_SWSTART);
	/* Check Status of Regular channel start flag */
	if(Get_Bit(ADC->SR,ADC_STRT) == 1)
	{
		/* Pooling on flag for Regular channel end of conversion */
		while(Get_Bit(ADC->SR,ADC_EOC) != 1);
	}
	/* Read Data */
	Local_u16Data = ADC_u16GetData();
	/* Return Data conversion */
	return Local_u16Data;
}
/*
 * Function : Continuous Conversion mode with Interrupt (regular group)
 * Input :  No Input
 * Output : Return No Thing
 */
void ADC_u16ContinuousConversionIN_Regular(void (*A_ptrToFunc)(void))
{
	/* Set Continuous conversion */
	Set_Bit(ADC->CR2,ADC_CR2_CONT);
	/*  Start conversion of regular channels */    // for make sure Start conversion
	Set_Bit(ADC->CR2,ADC_CR2_SWSTART);

	if (A_ptrToFunc != NULL)
	{
		ADC_Callback = A_ptrToFunc;
		/* ADC Enable interrupts */
		Set_Bit(ADC->CR1,ADC_CR1_EOCIE);
	}
}
/*
 * Function : Continuous Conversion mode with Interrupt (regular group) "ISR"
 * Input :  No Input
 * Output : Return No Thing
 */
void ADC_IRQHandler (void)
{
	/* Clear end of conversion bit */
	Clear_Bit(ADC->SR,ADC_EOC);
	/* Call Back */
	ADC_Callback();
}
