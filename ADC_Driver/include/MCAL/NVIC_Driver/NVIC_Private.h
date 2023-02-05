/*
 * NVIC_Private.h
 *
 *  Created on: Jan 15, 2023
 *      Author: user
 */

#ifndef INCLUDE_MCAL_LAYER_NVIC_DRIVER_NVIC_PRIVATE_H_
#define INCLUDE_MCAL_LAYER_NVIC_DRIVER_NVIC_PRIVATE_H_
//-----------------------------------------------------
#define NVIC      ((volatile NVIC_t *)0xE000E100)
#define NVIC_STIR ((volatile u32 *)0xE000EF00)
#define SCB 	  ((volatile SCB_t *)0xE000ED00)

typedef struct {

    volatile u32 ISER[32];
    volatile u32 ICER[32];
    volatile u32 ISPR[32];
    volatile u32 ICPR[32];
    volatile u32 IABR[32];
    volatile u32 RESERVED[32];
    volatile u8  IPR[128];//IPR da byte accessible fa khalenah u8 w zawnda el 3adad le 128 3ashan n3raf n accesso byte by byte, kol register byhold priority bta3t 4 interrupts 3ashan ehna maftoo7 leena 4 bits bs men el 8 3ashan ehna msh 3andena kol el interrupts ely homa 240 wahed

}NVIC_t;


typedef struct { //we need SCB because the AIRCR will control the configurations of the interrupt priorities in the system (core periphrals --> inside the processor)

    volatile u32 CPUID;
    volatile u32 ICSR;
    volatile u32 VTOR;
    volatile u32 AIRCR; // law nafs el group w nafs el sub priority yeb2a nshoof HW ba2a meen mtwasal el awal 3al nvic
    volatile u32 SCR;
    volatile u32 CCR;
    volatile u32 SHPR1;
    volatile u32 SHPR2;
    volatile u32 SHPR3;
    volatile u32 SHCSR;
    volatile u32 CFSR;
    volatile u32 HFSR;
    volatile u32 RESERVED;
    volatile u32 MMFAR;
    volatile u32 BFAR;

}SCB_t;

//-----------------------------------------------------
#endif /* INCLUDE_MCAL_LAYER_NVIC_DRIVER_NVIC_PRIVATE_H_ */
