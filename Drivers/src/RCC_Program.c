/*
 * RCC_Program.c
 *
 *  Created on: Dec 25, 2022
 *      Author: Mostafa Rashed
 */

#include "../include/lib/STD_Types.h"
#include "../include/lib/BIT_CALC.h"
#include "../include/MCAL/RCC/RCC_Privet.h"
#include "../include/MCAL/RCC/RCC_Interface.h"
#include "../include/MCAL/RCC/RCC_Config.h"


void MRCC_voidINIT(void)
{
#if   CLK_SOURCE == HSI
	Status local_Status = NOK;
	//1: Turn on HSI
	MRCC_voidSetClkStatus(HSI,ON);
	//2: Check HSI is ready
	//4: Switch HSI
	local_Status=MRCC_StatusSetClkSource(HSI);
	if(local_Status==OK)
	{
		//3: Set Buses Prescaler  (AHB) (APB1) (APB2)
		MRCC_voidSetBusesPrescaler(AHB_PRESCALER,APB1_PRESCALER,APB2_PRESCALER);
		//5: Turn off PLL,HSE
		MRCC_voidSetClkStatus(HSE,OFF);
		MRCC_voidSetClkStatus(PLL,OFF);
	}
#elif CLK_SOURCE == HSE
	Status local_Status = NOK;
	//1: Turn on HSI
	MRCC_voidSetClkStatus(HSE,ON);
	//2: Check HSI is ready
	//4: Switch HSI
	local_Status=MRCC_StatusSetClkSource(HSE);
	if(local_Status==OK)
	{
		//3: Set Buses Prescaler  (AHB) (APB1) (APB2)
		MRCC_voidSetBusesPrescaler(AHB_PRESCALER,APB1_PRESCALER,APB2_PRESCALER);
		//5: Turn off PLL,HSE
		MRCC_voidSetClkStatus(HSI,OFF);
		MRCC_voidSetClkStatus(PLL,OFF);
	}
#elif CLK_SOURCE == PLL
	MRCC_voidSetClkStatus(HSI,ON);
	(void)MRCC_StatusSetClkSource(HSI);
	MRCC_voidSetClkStatus(PLL,OFF);
	#if PLL_SOURCE == HSI
		MRCC_voidSetPLLSourceInput(HSI);
	#elif PLL_SOURCE == HSE
		MRCC_voidSetClkStatus(HSE,ON);
		MRCC_voidSetPLLSourceInput(HSE);
	#else
	#error "PLL Source Wrong Configrations"
	#endif
	MRCC_voidSetPLLFactors(PLLM_VALUE,PLLN_VALUE,PLLP_VALUE,PLLQ_VALUE);
	// Set Buses Prescaler
	MRCC_voidSetBusesPrescaler(AHB_PRESCALER,APB1_PRESCALER,APB2_PRESCALER);
	MRCC_voidSetClkStatus(PLL,ON);
	(void)MRCC_StatusSetClkSource(PLL);
	#if PLL_SOURCE == HSE
		MRCC_voidSetClkStatus(HSI,OFF);
	#endif
#else
#error "Clock Source Wrong Configrations"
#endif

}
//
void MRCC_voidSetClkStatus(const u8 copy_u8ClkSource , const u8 copy_u8Status)
{
	switch(copy_u8ClkSource)
	{
	case HSI:
		switch(copy_u8Status)
		{
		case ON :  Set_Bit  (RCC->CR,0); break;
		case OFF:  Clear_Bit(RCC->CR,0); break;
		default: break;
		}
		break;
	case HSE:
		switch(copy_u8Status)
		{
		case ON :  Set_Bit  (RCC->CR,16); break;
		case OFF:  Clear_Bit(RCC->CR,16); break;
		default: break;
		}
		break;
	case PLL:
		switch(copy_u8Status)
		{
		case ON :  Set_Bit  (RCC->CR,24); break;
		case OFF:  Clear_Bit(RCC->CR,24); break;
		default: break;
		}
		break;
	default:
		break;
	}
}
//Fanction to set RCC Register value (HSI-HSE-PLL)
Status MRCC_StatusSetClkSource(const u8 copy_u8ClkSource)
{
	Status local_Status =NOK;
	//Input Valldation
	if((copy_u8ClkSource <= PLL)&&(copy_u8ClkSource>0))
	{
		local_Status = MRCC_StatusCheckClkSource(copy_u8ClkSource);
		switch (local_Status)
		{
		case RDY:
			switch(copy_u8ClkSource)
			{
			case HSI:Clear_Bit(RCC->CFGR,CFGR_SW_BIT0);
					 Clear_Bit(RCC->CFGR,CFGR_SW_BIT1);
					 break;
			case HSE:Clear_Bit(RCC->CFGR,CFGR_SW_BIT1);
					 Set_Bit(RCC->CFGR,CFGR_SW_BIT0);
					 break;
			case PLL:Clear_Bit(RCC->CFGR,CFGR_SW_BIT0);
			 	 	 Set_Bit(RCC->CFGR,CFGR_SW_BIT1);
			 	 	 break;
			default: break;
			}
			local_Status = MRCC_StatusIsClkSelected(copy_u8ClkSource);
			break;
		default: break;
		}
	}
	else
	{
		local_Status = OUT_OF_RANGE;
	}
	return local_Status;
}
//Fanction to check from SWS IF ACTION IS RUN OR NOT
Status MRCC_StatusIsClkSelected(const u8 copy_u8ClkSource)
{
	Status local_Status =NOK;
	//Input Valldation
	if((copy_u8ClkSource <= PLL)&&(copy_u8ClkSource>0))
	{
		u8 local_u8Read = (((RCC->CFGR)>>2)&3);
		if(local_u8Read == copy_u8ClkSource)
		{
			local_u8Read = OK;
		}
	}
	else
	{
		local_Status = OUT_OF_RANGE;
	}
	return local_Status;
}
//
Status MRCC_StatusCheckClkSource(const u8 copy_u8ClkSource)
{
	Status local_Status =NOK;
	//Input Valldation
	if((copy_u8ClkSource <= PLL)&&(copy_u8ClkSource>0))
	{
		u8 local_u8BitNo =0;
		u16 local_u8Counter =0;
		switch(copy_u8ClkSource)
		{
		case HSI: local_u8BitNo = CR_HSI_RDY_BIT;  break;
		case HSE: local_u8BitNo = CR_HSE_RDY_BIT;  break;
		case PLL: local_u8BitNo = CR_PLL_RDY_BIT;  break;
		default: break;
		}
		local_Status =Get_Bit(RCC->CR,local_u8BitNo);
		while((local_Status==NOT_RDY)&&(local_u8Counter<RDY_WAIT_TIME))
		{
			local_u8Counter++;
			local_Status = Get_Bit(RCC->CR,local_u8BitNo);
		}
	}
	else
	{
		local_Status = OUT_OF_RANGE;
	}
	return local_Status;
}
//
void MRCC_voidSetPLLFactors (u8 copy_u8PLLM,u8 copy_u8PLLN,u8 copy_u8PLLP,u8 copy_u8PLLQ)
{
	RCC->PLLCFGR &=(1 << PLLCFGR_PLL_SOURCE_BIT);
	RCC->PLLCFGR |= (copy_u8PLLM) | (copy_u8PLLN << 6) | (copy_u8PLLP << 16) | (copy_u8PLLQ << 24);
}
//
Status MRCC_voidSetPLLSourceInput(const u8 copy_u8ClkSource)
{
	Status local_Status =NOK;
	//Input Valldation
	if((copy_u8ClkSource == HSI)||(copy_u8ClkSource == HSE))
	{
		switch(copy_u8ClkSource)
		{
		case HSI: Clear_Bit(RCC->PLLCFGR,PLLCFGR_PLL_SOURCE_BIT); local_Status =OK; break;
		case HSE: SET_BYTE (RCC->PLLCFGR,PLLCFGR_PLL_SOURCE_BIT); local_Status =OK; break;
		default: break;
		}
	}
	else
	{
		local_Status = OUT_OF_RANGE;
	}
	return local_Status;
}
//
void MRCC_voidPeripheral(Bus copy_u8Bus ,u8 copy_u8Peripheral,u8 copy_u8State )
{
	switch(copy_u8Bus)
	{
	case AHB1_H...APB2_H: MRCC_voidPeripheral_HIGH(copy_u8Bus,copy_u8Peripheral,copy_u8State); break;
	case AHB1_L...APB2_L: MRCC_voidPeripheral_LOW(copy_u8Bus,copy_u8Peripheral,copy_u8State); break;
	default: break;
	}
}
//
void MRCC_voidPeripheral_HIGH(Bus copy_u8Bus ,u8 copy_u8Peripheral,u8 copy_u8State )
{
	switch(copy_u8Bus)
	{
	case AHB1_H: MRCC_void_AHB1_H(copy_u8Peripheral,copy_u8State); break;
	case AHB2_H: MRCC_void_AHB2_H(copy_u8Peripheral,copy_u8State); break;
	case APB1_H: MRCC_void_APB1_H(copy_u8Peripheral,copy_u8State); break;
	case APB2_H: MRCC_void_APB2_H(copy_u8Peripheral,copy_u8State); break;
	default:
		break;
	}
}
//
void MRCC_voidPeripheral_LOW(Bus copy_u8Bus ,u8 copy_u8Peripheral,u8 copy_u8State )
{
	switch(copy_u8Bus)
	{
	case AHB1_L: MRCC_void_AHB1_L(copy_u8Peripheral, copy_u8State); break;
	case AHB2_L: MRCC_void_AHB2_L(copy_u8Peripheral,copy_u8State); break;
	case APB1_L: MRCC_void_APB1_L(copy_u8Peripheral,copy_u8State); break;
	case APB2_L: MRCC_void_APB2_L(copy_u8Peripheral,copy_u8State); break;
	default: break;
	}
}
//
void MRCC_void_AHB1_H(u8 copy_u8Peripheral, u8 copy_u8State)
{
	Assign_Bit(RCC->AHB1ENR,copy_u8Peripheral,copy_u8State);
}
//
void MRCC_void_AHB2_H(u8 copy_u8Peripheral, u8 copy_u8State)
{
	Assign_Bit(RCC->AHB2ENR,copy_u8Peripheral,copy_u8State);
}
//
void MRCC_void_APB1_H(u8 copy_u8Peripheral, u8 copy_u8State)
{
	Assign_Bit(RCC->APB1ENR,copy_u8Peripheral,copy_u8State);
}
//
void MRCC_void_APB2_H(u8 copy_u8Peripheral, u8 copy_u8State)
{
	Assign_Bit(RCC->APB2ENR,copy_u8Peripheral,copy_u8State);
}
//
void MRCC_void_AHB1_L(u8 copy_u8Peripheral, u8 copy_u8State)
{
	Assign_Bit(RCC->AHB1LPENR,copy_u8Peripheral,copy_u8State);
}
//
void MRCC_void_AHB2_L(u8 copy_u8Peripheral, u8 copy_u8State)
{
	Assign_Bit(RCC->AHB2LPENR,copy_u8Peripheral,copy_u8State);
}
//
void MRCC_void_APB1_L(u8 copy_u8Peripheral, u8 copy_u8State)
{
	Assign_Bit(RCC->APB1LPENR,copy_u8Peripheral,copy_u8State);
}
//
void MRCC_void_APB2_L(u8 copy_u8Peripheral, u8 copy_u8State)
{
	Assign_Bit(RCC->APB2LPENR,copy_u8Peripheral,copy_u8State);
}
//
void MRCC_voidSetBusesPrescaler(u8 copy_u8AHB,u8 Copy_u8APB1,u8 Copy_u8APB2)   //  Input ->  8 , 0 , 0
{
	RCC->CFGR &=~((15<<CFGR_HPRE)|(7<<CFGR_PPRE1)|(7<<CFGR_PPRE2));
	RCC->CFGR |=((copy_u8AHB<<CFGR_HPRE)|(Copy_u8APB1<<CFGR_PPRE1)|(Copy_u8APB2<<CFGR_PPRE2));
}
//
void MRCC_voidSetBusPrescaler(CFGR_Prescaler copy_u8Bus,u8 Copy_u8Prescaler)
{
	switch(copy_u8Bus)
	{
	case PPRE1: MRCC_voidSet_PPRE1_Prescaler(Copy_u8Prescaler); break;
	case PPRE2: MRCC_voidSet_PPRE2_Prescaler(Copy_u8Prescaler); break;
	case HPRE:  MRCC_voidSet_HPRE_Prescaler(Copy_u8Prescaler); break;
	}
}
//AHB prescaler
void MRCC_voidSet_HPRE_Prescaler(u8 Copy_u8Prescaler)
{
	RCC->CFGR &=0xFFFFFF0F;
	RCC->CFGR |= (Copy_u8Prescaler <<CFGR_HPRE);
}
//APB Low speed prescaler
void MRCC_voidSet_PPRE1_Prescaler(u8 Copy_u8Prescaler)
{
	RCC->CFGR &=0xFFFFE3FF;
	RCC->CFGR |= (Copy_u8Prescaler <<CFGR_PPRE1);
}
//
void MRCC_voidSet_PPRE2_Prescaler(u8 Copy_u8Prescaler)
{
	RCC->CFGR &=0xFFFF1FFF;
	RCC->CFGR |= (Copy_u8Prescaler << CFGR_PPRE2);
}












