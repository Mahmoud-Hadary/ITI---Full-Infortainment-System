/*
 * RCC_F401_Program.c
 *
 *  Created on: Dec 28, 2022
 *      Author: moham
 */
#include "STD_Types.h"
#include "BIT_CALC.h"
#include "RCC_f401_Interface.h"
#include "RCC_f401_Private.h"
#include "RCC_f401_Config.h"

// Select System Clock (HSI,HSL,PLL)
Status MRCC_StatusSetClkSource(const u8 A_u8ClkSource)
{
	Status Local_Status = NOK ;
	// Input Validation
	if(A_u8ClkSource<=PLL && A_u8ClkSource>=HSI)
	{
		// Check Clk Stable or not
		Local_Status = MRCC_StatusCheckClkStatus(A_u8ClkSource);
		if(Local_Status == RDY)
		{
			switch(A_u8ClkSource)
			{
			case HSI : Clear_Bit(RCC->CFGR,CFGR_SW_BIT0);
					   Clear_Bit(RCC->CFGR,CFGR_SW_BIT1);
					   break;
			case HSE : Set_Bit(RCC->CFGR,CFGR_SW_BIT0);
			   	   	   Clear_Bit(RCC->CFGR,CFGR_SW_BIT1);
			   	   	   break;
			case PLL : Clear_Bit(RCC->CFGR,CFGR_SW_BIT0);
			   	   	   Set_Bit(RCC->CFGR,CFGR_SW_BIT1);
			   	   	   break;
			default  : break ;
			}
			// Check if Clk Selected OK
			Local_Status = MRCC_StatusIsClkSelected(A_u8ClkSource);

		}


	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;

}
Status MRCC_StatusCheckClkStatus(const u8 A_u8ClkSource)
{
	Status Local_Status = NOK ;

	// Input Validation
	if(A_u8ClkSource<=PLL && A_u8ClkSource>=HSI)
	{
		volatile u8 Local_u8BitNo = 0 ;
		volatile u16 Local_u16Counter = 0 ;
		switch(A_u8ClkSource)
		{
		case HSI : Local_u8BitNo = CR_HSI_RDY_BIT ;break;
		case HSE : Local_u8BitNo = CR_HSE_RDY_BIT ;break;
		case PLL : Local_u8BitNo = CR_PLL_RDY_BIT ;break;
		}
		Local_Status = Get_Bit(RCC->CR,Local_u8BitNo);
		while(Local_Status == NOT_RDY && Local_u16Counter < RDY_WAIT_TIME )
		{
			Local_u16Counter++;
			Local_Status = Get_Bit(RCC->CR,Local_u8BitNo);

		}


	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;


}
Status MRCC_StatusIsClkSelected(const u8 A_u8ClkSource)
{
	Status Local_Status = NOK ;

	// Input Validation
	if(A_u8ClkSource<=PLL && A_u8ClkSource>=HSI)
	{
		volatile u8 Local_u8Read = GARBAGE_VALUE ;
		Local_u8Read = ((RCC->CFGR)>>2) && 0b11 ;
		if(A_u8ClkSource == Local_u8Read)
		{
			Local_Status = OK ;
		}
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}

Status MRCC_StautsSetPllFactors(const u8 A_u8PLLM,const u16 A_u16PLLN,const u8 A_u8PLLP,const u8 A_u8PLLQ)
{
	Status Local_Status = NOK ;
	if((A_u8PLLM>=PLLCFGR_PLLM_LOWER_LIMIT && A_u8PLLM<=PLLCFGR_PLLM_UPPER_LIMIT) &&
	   (A_u16PLLN>=PLLCFGR_PLLN_LOWER_LIMIT && A_u16PLLN <= PLLCFGR_PLLN_UPPER_LIMIT)&&
	   ((A_u8PLLP %2 == 0) && (A_u8PLLP>=PLLCFGR_PLLP_LOWER_LIMIT && A_u8PLLP<= PLLCFGR_PLLP_UPPER_LIMIT))&&
	   (A_u8PLLQ>=PLLCFGR_PLLQ_LOWER_LIMIT && A_u8PLLQ <= PLLCFGR_PLLQ_UPPER_LIMIT))
	{
		RCC->PLLCFGR &= (1<<22) ;
		RCC->PLLCFGR |= (A_u8PLLM) | (A_u16PLLN<<6) | (A_u8PLLP<<16) | (A_u8PLLQ<<24) ;
		Local_Status = OK ;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;


}
Status MRCC_StautsSetPllSourceInput(const u8 A_u8ClkSource)
{
	Status Local_Status = NOK ;
	if((A_u8ClkSource == HSI) || (A_u8ClkSource == HSE))
	{
		switch(A_u8ClkSource)
		{
		case HSI : Clear_Bit(RCC->PLLCFGR,PLLCFGR_PLL_Source_Bit);
				   Local_Status = OK ;
				   break ;
		case HSE : Set_Bit(RCC->PLLCFGR,PLLCFGR_PLL_Source_Bit);
				   Local_Status = OK ;
				   break;
		}

	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}
// High Power Mode
#if PERIPHERALENABLEMODE == 1
Status MRCC_StautsAHB1PeripheralClkEnable(AHB1 A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralName>=GPIOA && A_u8_PeripheralName<=GPIOE)||(A_u8_PeripheralName == GPIOH)||(A_u8_PeripheralName == CRC)||(A_u8_PeripheralName==DMA1)||(A_u8_PeripheralName==DMA2))
	{
		Set_Bit(RCC->AHB1ENR,A_u8_PeripheralName) ;
		Local_Status = OK;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}

Status MRCC_StautsAHB2PeripheralClkEnable(const u8 A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if(A_u8_PeripheralName == OTGFS)
	{
		Set_Bit(RCC->AHB2ENR,A_u8_PeripheralName);
		Local_Status = OK ;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}

Status MRCC_StautsAPB1PeripheralClkEnable(APB1 A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralName>=TIM2 && A_u8_PeripheralName<=TIM5)||(A_u8_PeripheralName == WWDG)||(A_u8_PeripheralName == SPI2)||(A_u8_PeripheralName==SPI3)||(A_u8_PeripheralName==USART2)||(A_u8_PeripheralName>=I2C1 && A_u8_PeripheralName<=I2C3)||(A_u8_PeripheralName == PWR))
	{
		Set_Bit(RCC->APB1ENR,A_u8_PeripheralName)   ;
		Local_Status = OK;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}

Status MRCC_StautsAPB2PeripheralClkEnable(APB2 A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralName>=SDIO && A_u8_PeripheralName<=SYSCFG)||(A_u8_PeripheralName == TIM1)||(A_u8_PeripheralName == USART1)||(A_u8_PeripheralName==USART6)||(A_u8_PeripheralName==ADC1)||(A_u8_PeripheralName>=TIM9 && A_u8_PeripheralName<=TIM11))
	{
		Set_Bit(RCC->APB2ENR,A_u8_PeripheralName) ;
		Local_Status = OK;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}


Status MRCC_StautsAHB1PeripheralClkDisable(AHB1 A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralName>=GPIOA && A_u8_PeripheralName<=GPIOE)||(A_u8_PeripheralName == GPIOH)||(A_u8_PeripheralName == CRC)||(A_u8_PeripheralName==DMA1)||(A_u8_PeripheralName==DMA2))
	{
		Clear_Bit(RCC->AHB1ENR,A_u8_PeripheralName) ;
		Local_Status = OK;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}

Status MRCC_StautsAHB2PeripheralClkDisable(const u8 A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if(A_u8_PeripheralName == OTGFS)
	{
		Clear_Bit(RCC->AHB2ENR,A_u8_PeripheralName);
		Local_Status = OK ;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}

Status MRCC_StautsAPB1PeripheralClkDisable(APB1 A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralName>=TIM2 && A_u8_PeripheralName<=TIM5)||(A_u8_PeripheralName == WWDG)||(A_u8_PeripheralName == SPI2)||(A_u8_PeripheralName==SPI3)||(A_u8_PeripheralName==USART2)||(A_u8_PeripheralName>=I2C1 && A_u8_PeripheralName<=I2C3)||(A_u8_PeripheralName == PWR))
	{
		Clear_Bit(RCC->APB1ENR,A_u8_PeripheralName)   ;
		Local_Status = OK;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}

Status MRCC_StautsAPB2PeripheralClkDisable(APB2 A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralName>=SDIO && A_u8_PeripheralName<=SYSCFG)||(A_u8_PeripheralName == TIM1)||(A_u8_PeripheralName == USART1)||(A_u8_PeripheralName==USART6)||(A_u8_PeripheralName==ADC1)||(A_u8_PeripheralName>=TIM9 && A_u8_PeripheralName<=TIM11))
	{
		Clear_Bit(RCC->APB2ENR,A_u8_PeripheralName) ;
		Local_Status = OK;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}

Status MRCC_StautsPeripheralClkEnable(Peripheral_Bus A_u8_PeripheralBus ,const u8  A_u8_Peripheral_Name)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralBus == AHB1_B) ||(A_u8_PeripheralBus == AHB2_B)||(A_u8_PeripheralBus ==APB1_B)||(A_u8_PeripheralBus ==APB2_B))
	{
		switch(A_u8_PeripheralBus)
		{
		case AHB1_B: Local_Status = MRCC_StautsAHB1PeripheralClkEnable(A_u8_Peripheral_Name);break;
		case AHB2_B: Local_Status = MRCC_StautsAHB2PeripheralClkEnable(A_u8_Peripheral_Name);break;
		case APB1_B: Local_Status = MRCC_StautsAPB1PeripheralClkEnable(A_u8_Peripheral_Name);break;
		case APB2_B: Local_Status = MRCC_StautsAPB2PeripheralClkEnable(A_u8_Peripheral_Name);break;
		default    : break;
		}

	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;

}

Status MRCC_StautsPeripheralClkDisable(Peripheral_Bus A_u8_PeripheralBus ,const u8  A_u8_Peripheral_Name)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralBus == AHB1_B) ||(A_u8_PeripheralBus == AHB2_B)||(A_u8_PeripheralBus ==APB1_B)||(A_u8_PeripheralBus ==APB2_B))
	{
		switch(A_u8_PeripheralBus)
		{
		case AHB1_B: Local_Status = MRCC_StautsAHB1PeripheralClkDisable(A_u8_Peripheral_Name);break;
		case AHB2_B: Local_Status = MRCC_StautsAHB2PeripheralClkDisable(A_u8_Peripheral_Name);break;
		case APB1_B: Local_Status = MRCC_StautsAPB1PeripheralClkDisable(A_u8_Peripheral_Name);break;
		case APB2_B: Local_Status = MRCC_StautsAPB2PeripheralClkDisable(A_u8_Peripheral_Name);break;
		default    : break;
		}

	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;

}
#endif

// Low Power Mode
#if PERIPHERALENABLEMODE == 0
Status MRCC_StautsAHB1PeripheralClkEnable_LowPower(AHB1LP A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralName>=GPIOA_LP && A_u8_PeripheralName<=GPIOE_LP)||(A_u8_PeripheralName == GPIOH_LP)||(A_u8_PeripheralName == CRC_LP)||(A_u8_PeripheralName == FLITF_LP)||(A_u8_PeripheralName == SRAM1_LP)||(A_u8_PeripheralName==DMA1_LP)||(A_u8_PeripheralName==DMA2_LP))
	{
		Set_Bit(RCC->AHB1LPENR,A_u8_PeripheralName) ;
		Local_Status = OK;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}
Status MRCC_StautsAHB2PeripheralClkEnable_LowPower(const u8 A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if(A_u8_PeripheralName == OTGFS_LP)
	{
		Set_Bit(RCC->AHB2LPENR,A_u8_PeripheralName);
		Local_Status = OK ;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}
Status MRCC_StautsAPB1PeripheralClkEnable_LowPower(APB1LP A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralName>=TIM2_LP && A_u8_PeripheralName<=TIM5_LP)||(A_u8_PeripheralName == WWDG_LP)||(A_u8_PeripheralName == SPI2_LP)||(A_u8_PeripheralName==SPI3_LP)||(A_u8_PeripheralName==USART2_LP)||(A_u8_PeripheralName>=I2C1_LP && A_u8_PeripheralName<=I2C3_LP)||(A_u8_PeripheralName == PWR_LP))
	{
		Set_Bit(RCC->APB1LPENR,A_u8_PeripheralName)   ;
		Local_Status = OK;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}
Status MRCC_StautsAPB2PeripheralClkEnable_LowPower(APB2LP A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralName>=SDIO_LP && A_u8_PeripheralName<=SYSCFG_LP)||(A_u8_PeripheralName == TIM1_LP)||(A_u8_PeripheralName == USART1_LP)||(A_u8_PeripheralName==USART6_LP)||(A_u8_PeripheralName==ADC1_LP)||(A_u8_PeripheralName>=TIM9_LP && A_u8_PeripheralName<=TIM11_LP))
	{
		Set_Bit(RCC->APB2LPENR,A_u8_PeripheralName) ;
		Local_Status = OK;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}
Status MRCC_StautsAHB1PeripheralClkDisable_LowPower(AHB1LP A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralName>=GPIOA_LP && A_u8_PeripheralName<=GPIOE_LP)||(A_u8_PeripheralName == GPIOH_LP)||(A_u8_PeripheralName == CRC_LP)||(A_u8_PeripheralName == FLITF_LP)||(A_u8_PeripheralName == SRAM1_LP)||(A_u8_PeripheralName==DMA1_LP)||(A_u8_PeripheralName==DMA2_LP))
	{
		Clear_Bit(RCC->AHB1LPENR,A_u8_PeripheralName) ;
		Local_Status = OK;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}
Status MRCC_StautsAHB2PeripheralClkDisable_LowPower(const u8 A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if(A_u8_PeripheralName == OTGFS_LP)
	{
		Clear_Bit(RCC->AHB2LPENR,A_u8_PeripheralName);
		Local_Status = OK ;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}
Status MRCC_StautsAPB1PeripheralClkDisable_LowPower(APB1LP A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralName>=TIM2_LP && A_u8_PeripheralName<=TIM5_LP)||(A_u8_PeripheralName == WWDG_LP)||(A_u8_PeripheralName == SPI2_LP)||(A_u8_PeripheralName==SPI3_LP)||(A_u8_PeripheralName==USART2_LP)||(A_u8_PeripheralName>=I2C1_LP && A_u8_PeripheralName<=I2C3_LP)||(A_u8_PeripheralName == PWR_LP))
	{
		Clear_Bit(RCC->APB1LPENR,PWR_LP)   ;
		Local_Status = OK;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}
Status MRCC_StautsAPB2PeripheralClkDisable_LowPower(APB2LP A_u8_PeripheralName)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralName>=SDIO_LP && A_u8_PeripheralName<=SYSCFG_LP)||(A_u8_PeripheralName == TIM1_LP)||(A_u8_PeripheralName == USART1_LP)||(A_u8_PeripheralName==USART6_LP)||(A_u8_PeripheralName==ADC1_LP)||(A_u8_PeripheralName>=TIM9_LP && A_u8_PeripheralName<=TIM11_LP))
	{
		Clear_Bit(RCC->APB2LPENR,A_u8_PeripheralName) ;
		Local_Status = OK;
	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;
}

Status MRCC_StautsPeripheralClkEnableLowPower(Peripheral_Bus_LP A_u8_PeripheralBus ,const u8  A_u8_Peripheral_Name)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralBus == AHB1LP_B) ||(A_u8_PeripheralBus == AHB2LP_B)||(A_u8_PeripheralBus ==APB1LP_B)||(A_u8_PeripheralBus ==APB2LP_B))
	{
		switch(A_u8_PeripheralBus)
		{
		case AHB1LP_B: Local_Status = MRCC_StautsAHB1PeripheralClkEnable_LowPower(A_u8_Peripheral_Name);break;
		case AHB2LP_B: Local_Status = MRCC_StautsAHB2PeripheralClkEnable_LowPower(A_u8_Peripheral_Name);break;
		case APB1LP_B: Local_Status = MRCC_StautsAPB1PeripheralClkEnable_LowPower(A_u8_Peripheral_Name);break;
		case APB2LP_B: Local_Status = MRCC_StautsAPB2PeripheralClkEnable_LowPower(A_u8_Peripheral_Name);break;
		default    : break;
		}

	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;

}

Status MRCC_StautsPeripheralClkDisableLowPower(Peripheral_Bus_LP A_u8_PeripheralBus ,const u8  A_u8_Peripheral_Name)
{
	Status Local_Status = NOK ;
	if((A_u8_PeripheralBus == AHB1LP_B) ||(A_u8_PeripheralBus == AHB2LP_B)||(A_u8_PeripheralBus ==APB1LP_B)||(A_u8_PeripheralBus ==APB2LP_B))
	{
		switch(A_u8_PeripheralBus)
		{
		case AHB1LP_B: Local_Status = MRCC_StautsAHB1PeripheralClkDisable_LowPower(A_u8_Peripheral_Name);break;
		case AHB2LP_B: Local_Status = MRCC_StautsAHB2PeripheralClkDisable_LowPower(A_u8_Peripheral_Name);break;
		case APB1LP_B: Local_Status = MRCC_StautsAPB1PeripheralClkDisable_LowPower(A_u8_Peripheral_Name);break;
		case APB2LP_B: Local_Status = MRCC_StautsAPB2PeripheralClkDisable_LowPower(A_u8_Peripheral_Name);break;
		default    : break;
		}

	}
	else
	{
		Local_Status = OUT_OF_RANGE;
	}
	return Local_Status ;

}
#endif
//-------------------------------------------------------------------------------
// Prescaler bus
/*Status MRCC_StatusSetAHBPrescaler(AHB_Prescaler Copy_Bus_Prescaler){
    Status Local_Status =NOK;
    if(Copy_Bus_Prescaler<=15 && Copy_Bus_Prescaler>=0)
    {
            RCC->CFGR &= 0xFFFFFF0F;
            //RCC->CFGR &= ~ ((15<<4)|(7<<10)|(7<<13));
            RCC->CFGR |= (Copy_Bus_Prescaler<<4);
            Local_Status = OK;
    }
    else{
        Local_Status=OUT_OF_RANGE;
    }
    return Local_Status;
}

Status MRCC_StatusSetAPB1Prescaler(APB1_Prescaler Copy_Bus_Prescaler){
    Status Local_Status =NOK;
    if(Copy_Bus_Prescaler<=7 && Copy_Bus_Prescaler>=0)
    {
            RCC->CFGR &= 0xFFFFE3FF;
            RCC->CFGR |= (Copy_Bus_Prescaler<<10);
            Local_Status = OK;
    }
    else{
        Local_Status=OUT_OF_RANGE;
    }
    return Local_Status;
}
Status MRCC_StatusSetAPB2Prescaler(APB2_Prescaler Copy_Bus_Prescaler){
    Status Local_Status =NOK;
    if(Copy_Bus_Prescaler<=7 && Copy_Bus_Prescaler>=0)
    {
            RCC->CFGR &= 0xFFFF1FFF;
            RCC->CFGR |= (Copy_Bus_Prescaler<<13);
            Local_Status = OK;
    }
    else{
        Local_Status=OUT_OF_RANGE;
    }
    return Local_Status;
}*/
//----------------------------------------------------------------------------------
void MRCC_voidSetBusesPrescaler(u8 A_u8AHB,u8 A_u8APB1,u8 A_u8APB2){
    RCC->CFGR &= ~ ((15<<4)|(7<<10)|(7<<13));
    RCC->CFGR |= (A_u8AHB<<4) | (A_u8APB1<<10) | (A_u8APB2<<13);
}
//-----------------------------------------------------------------------------
void MRCC_voidInit()
{

#if CLK_SOURCE == HSI
	Status Local_Sts = NOK ;
	// Turn on HSI
	MRCC_voidSetClkStauts(HSI,ON);
	// Check HSI is ready
	// Switch HSI
	Local_Sts = MRCC_StatusCheckClkStatus(HSI);
	if(Local_Sts == OK)
	{
		// Set Buses Prescaler
		MRCC_voidSetBusesPrescaler(AHB_PRESCALER,APB1_PRESCALER,APB2_PRESCALER);
		// Turn off HSE , PLL
		MRCC_voidSetClkStauts(HSE,OFF);
		MRCC_voidSetClkStauts(PLL,OFF);
	}

#elif CLK_SOURCE == HSE
	Status Local_Sts = NOK ;
	// Turn on HSE
	MRCC_voidSetClkStauts(HSE,ON);
	// Check HSE is ready
	// Switch HSE
	Local_Sts = MRCC_StatusCheckClkStatus(HSE);
	if(Local_Sts == OK)
	{
		// Set Buses Prescaler
		MRCC_voidSetBusesPrescaler(AHB_PRESCALER,APB1_PRESCALER,APB2_PRESCALER);
		// Turn off HSI , PLL
		MRCC_voidSetClkStauts(HSI,OFF);
		MRCC_voidSetClkStauts(PLL,OFF);
	}

#elif CLK_SOURCE == PLL
	MRCC_voidSetClkStatus(HSI,ON);
	(void)MRCC_StatusCheckClkSource(HSI);
	MRCC_voidSetClkStauts(PLL,OFF);
	#if PLL_SOURCE == HSI
	MRCC_voidSetPLLSourceInput(HSI);
	#elif PLL_SOURCE == HSE
	MRCC_voidSetClkStauts(HSE,ON);
	MRCC_voidSetPLLSourceInput(HSE);
	#endif
	MRCC_StautsSetPllFactors(PLLM_VALUE,PLLN_VALUE,PLLP_VALUE,PLLQ_VALUE);
	// Set Buses Prescaler
	MRCC_voidSetBusesPrescaler(AHB_PRESCALER,APB1_PRESCALER,APB2_PRESCALER);
	MRCC_voidSetClkStauts(PLL,ON);
	(void)MRCC_StautsSetClkSource(PLL);
    #if PLL_SOURCE == HSE
		MRCC_voidSetClkStauts(HSI,OFF);
	#endif

#else
#error "Clock Source Wrong Configurations"
#endif

void MRCC_voidSetClkStauts(const u8 A_u8ClockSource,const u8 A_u8Stauts)
{
	switch(A_u8ClockSource)
	{
	case HSI :
		switch(A_u8Stauts)
		{
		case ON : Set_Bit(RCC->CR,0);break;
		case OFF: Clear_Bit(RCC->CR,0);break;
		}
		break;

		case HSE :
			switch(A_u8Stauts)
			{
			case ON : Set_Bit(RCC->CR,16);break;
			case OFF: Clear_Bit(RCC->CR,16);break;
			}
			break;
		case HSI :
			switch(A_u8Stauts)
			{
			case ON : Set_Bit(RCC->CR,24);break;
			case OFF: Clear_Bit(RCC->CR,24);break;
			}
			break;
		default :




	}

}
}
