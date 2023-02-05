/*
 * EXTI_Program.c
 *
 *  Created on: Jan 22, 2023
 *      Author: user
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
//-------------------------------------
void (*EXTI0_CallBack)(void);

/******************************************************************************************/
/*Function: MEXTI_voidConfig	                         						          */
/*I/P Parameters: Port - Line Number - Sense mode         			  			          */
/*Returns:it returns no thing	                            				  			  */
/*Desc:This Function Configures the EXTI 							          			  */
/******************************************************************************************/
/*
 * Options for copy_u8EXTILine:- EXTI0 ... EXTI15
 * Options for copy_u8PORT :- GPIOA_PORT - GPIOB_PORT - GPIOC_PORT
 * Options for copy_u8SenseMode:- FALLING_EDGE - RISING_EDGE - ON_CHANGE_EDGE
*/
void MEXTI_voidConfig(u8 copy_u8EXTILine, u8 copy_u8PORT, u8 copy_u8SenseMode)
{
    switch (copy_u8PORT)
    {
    case GPIO_PORTA:
        switch (copy_u8EXTILine)
        {
        case EXTI0_EN:
        case EXTI1_EN:
        case EXTI2_EN:
        case EXTI3_EN:
            SYSCFG->EXTICR1 &= ~(15 << (copy_u8EXTILine * 4));
            break;
        case EXTI4_EN:
        case EXTI5_EN:
        case EXTI6_EN:
        case EXTI7_EN:
        	SYSCFG->EXTICR2 &= ~(15 << (copy_u8EXTILine * 4));
            break;
        case EXTI8_EN:
        case EXTI9_EN:
        case EXTI10_EN:
        case EXTI11_EN:
        	SYSCFG->EXTICR3 &= ~(15 << (copy_u8EXTILine * 4));
            break;
        case EXTI12_EN:
        case EXTI13_EN:
        case EXTI14_EN:
        case EXTI15_EN:
        	SYSCFG->EXTICR4 &= ~(15 << (copy_u8EXTILine * 4));
            break;
        }
        break;
    case GPIO_PORTB:
        switch (copy_u8EXTILine)
        {
        case EXTI0_EN:
        case EXTI1_EN:
        case EXTI2_EN:
        case EXTI3_EN:
            SYSCFG->EXTICR1 |= (1 << (copy_u8EXTILine * 4));
            break;
        case EXTI4_EN:
        case EXTI5_EN:
        case EXTI6_EN:
        case EXTI7_EN:
            SYSCFG->EXTICR2 |= (1 << ((copy_u8EXTILine - 4) * 4));
            break;
        case EXTI8_EN:
        case EXTI9_EN:
        case EXTI10_EN:
        case EXTI11_EN:
            SYSCFG->EXTICR3 |= (1 << ((copy_u8EXTILine - 8) * 4));
            break;
        case EXTI12_EN:
        case EXTI13_EN:
        case EXTI14_EN:
        case EXTI15_EN:
            SYSCFG->EXTICR4 |= (1 << ((copy_u8EXTILine - 12) * 4));
            break;
        }
        break;
    default:
        break;
    }

    switch (copy_u8SenseMode)
    {
    case FALLING_EDGE:
        Set_Bit(EXTI->FTSR, copy_u8EXTILine);
        Clear_Bit(EXTI->RTSR, copy_u8EXTILine);
        break;
    case RISING_EDGE:
    	Clear_Bit(EXTI->FTSR, copy_u8EXTILine);
        Set_Bit(EXTI->RTSR, copy_u8EXTILine);
        break;
    case ON_CHANGE_EDGE:
    	Set_Bit(EXTI->FTSR, copy_u8EXTILine);
    	Set_Bit(EXTI->RTSR, copy_u8EXTILine);
        break;
    default:
        break;
    }
    Set_Bit(EXTI->IMR, copy_u8EXTILine); // Enable EXTI Line
}

/******************************************************************************************/
/*Function: MEXTI_voidDisable	                         						          */
/*I/P Parameters: Line Number                           			  			          */
/*Returns:it returns no thing	                            				  			  */
/*Desc:This Function Disables the EXTI 							             			  */
/******************************************************************************************/
/*
 * Options for copy_u8EXTILine:- EXTI0 ... EXTI15
*/
void MEXTI_voidDisable(u8 copy_u8EXTILine)
{
	Clear_Bit(EXTI->IMR, copy_u8EXTILine); // Disable EXTI Line
}

void EXTI0_VoidSetCallBack(void (*ptr)(void))
{
    EXTI0_CallBack = ptr;
}
void EXTI0_IRQHandler(void)
{
    EXTI0_CallBack();
    Set_Bit(EXTI->PR, 0);
}
//------------------------------------------------------------------------------------------


