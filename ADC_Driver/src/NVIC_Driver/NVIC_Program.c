/*
 * NVIC_Program.c
 *
 *  Created on: Jan 15, 2023
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
//-------------------------------------
void MNVIC_VoidEnablePeriphral(u8 Copy_u8INTID) //enable a specific int id
{
	NVIC->ISER[Copy_u8INTID/32] = 1<< (Copy_u8INTID%32); //awel goz2 rakam el register ely 3awez akteb feeh , tany goz2 bageeb anhy bit fel register da ely 3awez akteb feeha w akteb feeha 1 3ashan a enable el interrupt bta3 el periphral da
}
//-------------------------------------
void MNVIC_VoidDisablePeriphral(u8 Copy_u8INTID) //Disable a specific int id
{
	NVIC->ICER[Copy_u8INTID/32] = 1<< (Copy_u8INTID%32); //awel goz2 rakam el register ely 3awez akteb feeh , tany goz2 bageeb anhy bit fel register da ely 3awez akteb feeha w akteb feeha 1 3ashan a enable el interrupt bta3 el periphral da
}
//-------------------------------------
void MNVIC_VoidSetPending(u8 Copy_u8INTID) // we got an interrupt but it is pending not active now fa ana ba2olo be nafsy 7otholy fel taboor
{
	NVIC->ISPR[Copy_u8INTID/32] = 1<< (Copy_u8INTID%32); //awel goz2 rakam el register ely 3awez akteb feeh , tany goz2 bageeb anhy bit fel register da ely 3awez akteb feeha w akteb feeha 1 3ashan a enable el interrupt bta3 el periphral da
}
//-------------------------------------
void MNVIC_VoidClearPending(u8 Copy_u8INTID) //we can clear this bit also
{
	NVIC->ICPR[Copy_u8INTID/32] = 1<< (Copy_u8INTID%32); //awel goz2 rakam el register ely 3awez akteb feeh , tany goz2 bageeb anhy bit fel register da ely 3awez akteb feeha w akteb feeha 1 3ashan a enable el interrupt bta3 el periphral da
}
//-------------------------------------
u8 MNVIC_VoidGetActive(u8 Copy_u8INTID) //get the the active interrupt now
{
	u8 LOC_u8Active = Get_Bit(NVIC->IABR[Copy_u8INTID/32],(Copy_u8INTID%32));
	return LOC_u8Active;
}
//-------------------------------------
static u32 globalStatic_u32GroupConf;
//-------------------------------------
void MNVIC_VoidSetPriorityConfiguration(IPC_t Copy_IPC_t_Interrupt_PriorityConfiguration) //get the the active interrupt now
{
	//fel function de bnset el configuration bta3t el interrupts
	 globalStatic_u32GroupConf= 0x05FA0000 | (Copy_IPC_t_Interrupt_PriorityConfiguration << 8); //3ashan 3awzeen nwady el value ely gaya mel enum de fe b its 8,9,10 w 3amlna oring ma3 el password 3ashan n3raf nekteb fel register
	 SCB->AIRCR = globalStatic_u32GroupConf;
}
//-------------------------------------
void MNVIC_VoidSetPriority(s8 Copy_s8INTID, u8 Copy_u8GroupPriority,u8 Copy_u8SubPriority) //manage y3ny ana ely bazabat el priorities bta3t el interrupts w meen ydkhol delwa2ty w meen ystaana da ma3na manage
{
	//fel function de bn2ol el interrupt fe anhy group w anhy sub priority gowa el group de
	u8 local_u8Priority = Copy_u8SubPriority | Copy_u8GroupPriority << ((globalStatic_u32GroupConf - 0x05FA0300)/256); //0x05FA0300 is the base address we got it from the datasheet ,w el subtraction ma3 el /256 de el equation ely hatala3 el rakam ely ha shift beeh , ana hadafy hena fel satr da eny awady el 4 bits bto3 el Group wel subpriority fe makanhom el sah
	//core periphral
	if(Copy_s8INTID < 0)
	{
		if( (Copy_s8INTID == MEMORY_MANAGE) || (Copy_s8INTID == BUS_FAULT) || (Copy_s8INTID == USAGE_FAULT))
		{
			Copy_s8INTID+=3;
			SCB->SHPR1 = (local_u8Priority) << ((8 * Copy_s8INTID) +4);
		}

		else if (Copy_s8INTID == SV_CALL)
		{
			Copy_s8INTID +=7;
			SCB->SHPR2 = (local_u8Priority) << ((8 * Copy_s8INTID) +4);
		}
		else if (Copy_s8INTID == PEND_SV || Copy_s8INTID == SYSTICK)
		{
			Copy_s8INTID +=8;
			SCB->SHPR3 = (local_u8Priority) << ((8 * Copy_s8INTID) +4);
		}
	}
	//not a core periphral yeb2a nhot el value de 3alatol
	else if ( Copy_s8INTID >= 0)
	{
		NVIC->IPR[Copy_s8INTID] = local_u8Priority << 4;
	}
}
//-------------------------------------
