#include "STD_Types.h"
#include "BIT_CALC.h"
#include "RCC_Interface.h"
#include "RCC_Private.h"
#include "RCC_Config.h"
//----------------------------------------------
void MRCC_voidSetClkStatus (const u8 A_u8ClockSource, const u8 A_u8Status)
{
	switch (A_u8ClockSource)
	{
	case HSI:
				switch (A_u8Status)
				{
				case ON: Set_Bit(RCC->CR,0); break;
				case OFF:Clear_Bit(RCC->CR,0); break;
				}
				break;
	case HSE:
				switch (A_u8Status)
				{
				case ON: Set_Bit(RCC->CR,16); break;
				case OFF: Clear_Bit(RCC->CR,16); break;
				}
				break;
	case PLL:
				switch (A_u8Status)
				{
				case ON: Set_Bit(RCC->CR,24); break;
				case OFF: Clear_Bit(RCC->CR,24); break;
				}
				break;
	}
}

// HSI - HSE - PLL
Status MRCC_StatusSetClkSource (const u8 A_u8ClkSource)
{
	Status local_Status = NOK;
	// Input Validation
	if ((A_u8ClkSource<=PLL) && (A_u8ClkSource>=HSI))
	{
		local_Status = MRCC_StatusCheckClkStatus(A_u8ClkSource);
		if (local_Status == RDY)
		{
			switch (A_u8ClkSource)
			{
			case HSI:	 Clear_Bit(RCC->CFGR,CFGR_SW_BIT0);
			 	 	 	 Clear_Bit(RCC->CFGR,CFGR_SW_BIT1);
						break;

			case HSE:	 Set_Bit(RCC->CFGR,CFGR_SW_BIT0);
			 	 	 	 Clear_Bit(RCC->CFGR,CFGR_SW_BIT1);
						break;

			case PLL:	 Clear_Bit(RCC->CFGR,CFGR_SW_BIT0);
						 Set_Bit(RCC->CFGR,CFGR_SW_BIT1);
						break;

			default:	break;
			}
			local_Status = MRCC_StatusIsClkSelected(A_u8ClkSource);
		}
	}
	else
	{
		local_Status = OUT_OF_RANGE;
	}
	return local_Status;
}

Status MRCC_StatusIsClkSelected (const u8 A_u8ClkSource)
{
	Status local_Status = NOK;

	// Input Validation
	if ((A_u8ClkSource<=PLL) && (A_u8ClkSource>=HSI))
	{
		u8 local_u8Read=5;
		local_u8Read = (RCC->CFGR>>2) & 0b11;
		if (local_u8Read == (A_u8ClkSource))
		{
			local_Status = OK;
		}
	}
	else
	{
		local_Status = OUT_OF_RANGE;
	}
	return local_Status;
}

Status MRCC_StatusCheckClkStatus (const u8 A_u8ClkSource)
{
	Status local_Status = NOK;
	// Input Validation
	if ((A_u8ClkSource<=PLL) && (A_u8ClkSource>=HSI))
	{
		u8 local_u8BitNo=0;
		u16 local_u16Counter=0;
		switch (A_u8ClkSource)
		{
		case HSI: local_u8BitNo = CR_HSI_RDY_BIT; break;
		case HSE: local_u8BitNo = CR_HSE_RDY_BIT; break;
		case PLL: local_u8BitNo = CR_PLL_RDY_BIT; break;
		}
		local_Status = Get_Bit(RCC->CR,local_u8BitNo);
		while ((local_Status==NOT_RDY) && (local_u16Counter<RDY_WAIT_TIME))
		{
			local_u16Counter++;
			local_Status = Get_Bit(RCC->CR,local_u8BitNo);
		}
	}
	else
	{
		local_Status = OUT_OF_RANGE;
	}
	return local_Status;
}


/* Set PLL Factors */
void MRCC_voidSetPLLFactors (u8 copy_u8PLLM, u16 copy_u16PLLN, u8 copy_u8PLLP, u8 copy_u8PLLQ)
{
	RCC->PLLCFGR &= (1<<22);
	RCC->PLLCFGR |= (copy_u8PLLM) | (copy_u16PLLN << 6) | (copy_u8PLLP<<16) | (copy_u8PLLQ<<24);
}


Status MRCC_voidSetPLLSourceInput (const u8 A_u8ClkSource)
{
	Status local_Status= NOK;
	if ((A_u8ClkSource==HSI)||(A_u8ClkSource==HSE))
	{
		switch (A_u8ClkSource)
		{
		case HSI: Clear_Bit(RCC->PLLCFGR,PLLCFGR_PLL_SOURCE_BIT);
				  local_Status = OK; break;
		case HSE: Set_Bit(RCC->PLLCFGR,PLLCFGR_PLL_SOURCE_BIT);
				  local_Status = OK; break;
		}
	}
	else
	{
		local_Status = OUT_OF_RANGE;
	}
	return local_Status;
}

void MRCC_voidPeripheralEnable(u8 A_u8Bus, u8 A_u8Peripheral)
{
	switch (A_u8Bus)
	{
	case AHB1: Set_Bit (RCC->AHB1ENR,A_u8Peripheral); break;
	case AHB2: Set_Bit (RCC->AHB2ENR,A_u8Peripheral); break;
	case APB1: Set_Bit (RCC->APB1ENR,A_u8Peripheral); break;
	case APB2: Set_Bit (RCC->APB2ENR,A_u8Peripheral); break;
	}
}
void MRCC_voidPeripheralDisable(u8 A_u8Bus, u8 A_u8Peripheral)

{
	switch (A_u8Bus)
		{
		case AHB1: Clear_Bit(RCC->AHB1ENR,A_u8Peripheral); break;
		case AHB2: Clear_Bit(RCC->AHB2ENR,A_u8Peripheral); break;
		case APB1: Clear_Bit(RCC->APB1ENR,A_u8Peripheral); break;
		case APB2: Clear_Bit(RCC->APB2ENR,A_u8Peripheral); break;
		}
}

/* Set AHB1 and APB1 and APB2 Prescalers */
void MRCC_voidSetBusesPrescaler (u8 A_u8AHB,u8 A_u8APB1,u8 A_u8APB2)
{
	RCC->CFGR &= ~((15<<4)|(7<<10)|(7<<13));
	RCC->CFGR |=  (A_u8AHB<<4) | (A_u8APB1<<10) | (A_u8APB2<<13);
}

void MRCC_voidInit()
{
#if     CLK_SOURCE == HSI
		Status local_Stste = NOK;
		// Turn On HSI
		MRCC_voidSetClkStatus (HSI, ON);
		// Check HSI is ready
		// Switch HSI
		local_Stste=MRCC_StatusSetClkSource(HSI);
		if (local_Stste==OK)
		{
			// Set Buses Prescaler
			MRCC_voidSetBusesPrescaler(AHB_PRESCALER,APB1_PRESCALER,APB2_PRESCALER);
			// Turn off PLL, HSE
			MRCC_voidSetClkStatus (HSE, OFF);
			MRCC_voidSetClkStatus (PLL, OFF);
		}
#elif  CLK_SOURCE == HSE
		Status local_Stste = NOK;
		// Turn On HSE
		MRCC_voidSetClkStatus (HSE, ON);
		// Check HSE is ready
		// Switch HSE
		local_Stste = MRCC_StatusSetClkSource(HSE);
		if (local_Stste==OK)
		{
			// Set Buses Prescaler
			MRCC_voidSetBusesPrescaler(AHB_PRESCALER,APB1_PRESCALER,APB2_PRESCALER);
			// Turn off PLL, HSE
			MRCC_voidSetClkStatus (HSI, OFF);
			MRCC_voidSetClkStatus (PLL, OFF);
		}
#elif  CLK_SOURCE == PLL
		MRCC_voidSetClkStatus (HSI, ON);
		(void)MRCC_StatusSetClkSource(HSI);
		MRCC_voidSetClkStatus (PLL, OFF);

		#if PLL_SOURCE == HSI
		MRCC_voidSetPLLSourceInput (HSI);
		#elif PLL_SOURCE == HSE
		MRCC_voidSetClkStatus (HSE, ON);
		MRCC_voidSetPLLSourceInput (HSE);
		#endif
		MRCC_voidSetPLLFactors(PLLM_VALUE,PLLN_VALUE,PLLP_VALUE,PLLQ_VALUE);
		// Set Buses Prescaler
		MRCC_voidSetBusesPrescaler(AHB_PRESCALER,APB1_PRESCALER,APB2_PRESCALER);
		MRCC_voidSetClkStatus (PLL, ON);
		(void)MRCC_StatusSetClkSource(PLL);
		#if PLL_SOURCE == HSE
				MRCC_voidSetClkStatus (HSI, OFF);
		#endif
#else
#error "Clock Source Wrong Configurations"

#endif
}
