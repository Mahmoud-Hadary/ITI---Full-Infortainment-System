/*
 * RCC_F401_Interface.h
 *
 *  Created on: Dec 28, 2022
 *      Author: moham
 */

#ifndef RCC_F401_INTERFACE_H_
#define RCC_F401_INTERFACE_H_

#define HSI 	   0
#define HSE	       1
#define PLL 	   2

#define ON    1
#define OFF   0

#define OTGFS      7
#define OTGFS_LP   7

typedef enum
{
	NOT_RDY,
	RDY    ,
	OUT_OF_RANGE,
	NOK    ,
	OK

}Status;

typedef enum
{
	GPIOA,GPIOB,GPIOC,GPIOD,GPIOE,GPIOH=7,CRC=12,DMA1=21,DMA2

}AHB1;


typedef enum
{
	TIM2,TIM3,TIM4,TIM5,WWDG=11,SPI2=14,SPI3,USART2=17,I2C1=21,I2C2,I2C3,PWR=28

}APB1;

typedef enum
{
	TIM1,USART1=4,USART6,ADC1=8,SDIO=11,SPI1,SPI4,SYSCFG,TIM9=16,TIM10,TIM11

}APB2;

typedef enum
{
	AHB1_B,AHB2_B,APB1_B,APB2_B

}Peripheral_Bus;

typedef enum
{
	GPIOA_LP,GPIOB_LP,GPIOC_LP,GPIOD_LP,GPIOE_LP,GPIOH_LP=7,CRC_LP=12,FLITF_LP=15,SRAM1_LP,DMA1_LP=21,DMA2_LP

}AHB1LP;

typedef enum
{
	TIM2_LP,TIM3_LP,TIM4_LP,TIM5_LP,WWDG_LP=11,SPI2_LP=14,SPI3_LP,USART2_LP=17,I2C1_LP=21,I2C2_LP,I2C3_LP,PWR_LP=28

}APB1LP;

typedef enum
{
	TIM1_LP,USART1_LP=4,USART6_LP,ADC1_LP=8,SDIO_LP=11,SPI1_LP,SPI4_LP,SYSCFG_LP,TIM9_LP=16,TIM10_LP,TIM11_LP

}APB2LP;

typedef enum
{
	AHB1LP_B,AHB2LP_B,APB1LP_B,APB2LP_B

}Peripheral_Bus_LP;

typedef enum {
    NoPrescaler,Prescalerx2=8,Prescalerx4,Prescalerx8,Prescalerx16,Prescalerx64,Prescalerx128,Prescalerx256,Prescalerx512
}AHB_Prescaler;

typedef enum {
    NoPrescaler,Prescalerx2=4,Prescalerx4,Prescalerx8,Prescalerx16
}APB1_Prescaler;

typedef enum {
    NoPrescaler,Prescalerx2=4,Prescalerx4,Prescalerx8,Prescalerx16
}APB2_Prescaler;

Status MRCC_StatusSetClkSource(const u8 A_u8ClkSource);
Status MRCC_StatusCheckClkStatus(const u8 A_u8ClkSource);
Status MRCC_StatusIsClkSelected(const u8 A_u8ClkSource);
Status MRCC_StautsSetPllFactors(const u8 A_u8PLLM,const u16 A_u16PLLN,const u8 A_u8PLLP,const u8 A_u8PLLQ);
Status MRCC_StautsSetPllSourceInput(const u8 A_u8ClkSource);

Status MRCC_StautsPeripheralClkEnable(Peripheral_Bus A_u8_PeripheralBus ,const u8  A_u8_Peripheral_Name);
Status MRCC_StautsPeripheralClkDisable(Peripheral_Bus A_u8_PeripheralBus ,const u8  A_u8_Peripheral_Name);

Status MRCC_StautsPeripheralClkEnableLowPower(Peripheral_Bus_LP A_u8_PeripheralBus ,const u8  A_u8_Peripheral_Name);
Status MRCC_StautsPeripheralClkDisableLowPower(Peripheral_Bus_LP A_u8_PeripheralBus ,const u8  A_u8_Peripheral_Name);

//Status MRCC_StatusSetAHBPrescaler(AHB_Prescaler Copy_Bus_Prescaler);
//Status MRCC_StatusSetAPB1Prescaler(APB1_Prescaler Copy_Bus_Prescaler);
//Status MRCC_StatusSetAPB2Prescaler(APB2_Prescaler Copy_Bus_Prescaler);


void MRCC_voidSetClkStauts(const u8 A_u8ClockSource,const u8 A_u8Stauts);
void MRCC_voidSetBusesPrescaler(u8 A_u8AHB,u8 A_u8APB1,u8 A_u8APB2);
void MRCC_voidInit();




#endif /* RCC_F401_INTERFACE_H_ */
