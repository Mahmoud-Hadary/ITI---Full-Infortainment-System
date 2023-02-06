/*
 * RCC_Interface.h
 *
 *  Created on: Dec 25, 2022
 *      Author: Mostafa Rashed
 */

#ifndef RCC_INTERFACE_H_
#define RCC_INTERFACE_H_
/****************************************** FUNCTION INIT ***************************************************/
#define ON  1
#define OFF 0
//
void MRCC_voidINIT(void);
//////////////////////////////////
//Feedback from MRCC_StatusSetClkSource Function
typedef enum
{
	NOT_RDY,
	RDY,
	OUT_OF_RANGE,
	OK,
	NOK
}Status;
//Magic Number in MRCC_StatusSetClkSource Function
#define HSI 0
#define HSE 1
#define PLL 2
//
void MRCC_voidSetClkStatus(const u8 copy_u8ClkSource , const u8 copy_u8Status);
//Fanction to set RCC Register value
Status MRCC_StatusSetClkSource(const u8 copy_u8ClkSource);
//Fanction to check from SWS IF ACTION IS RUN OR NOT
Status MRCC_StatusIsClkSelected(const u8 copy_u8ClkSource);
//Function to Check
Status MRCC_StatusCheckClkSource(const u8 copy_u8ClkSource);
/////////////////////////////////
//
void MRCC_voidSetPLLFactors (u8 copy_u8PLLM,u8 copy_u8PLLN,u8 copy_u8PLLP,u8 copy_u8PLLQ);
//
Status MRCC_voidSetPLLSourceInput(const u8 copy_u8ClkSource);
//
//***********************************************************************************************************//
typedef enum
{
	AHB1_H,AHB2_H,APB1_H,APB2_H,AHB1_L,AHB2_L,APB1_L,APB2_L
}Bus;
//
#define PeripheralEnable  1
#define PeripheralDisable 2
///////////////////////////////////High Power/////////////////////////////////////////////
/****************** AHB1 peripheral clock enable register *********************/
#define AHB1_H_GPIOAEN   0
#define AHB1_H_GPIOBEN   1
#define AHB1_H_GPIOCEN   2
#define AHB1_H_GPIODEN   3
#define AHB1_H_GPIOEEN   4
#define AHB1_H_GPIOHEN   7
#define AHB1_H_CRCEN     12
#define AHB1_H_DMA1EN    21
#define AHB1_H_DMA2EN    22
/*typedef enum
{
	GPIOAEN,GPIOBEN,GPIOCEN,GPIODEN,GPIOEEN,GPIOHEN,CRCEN,DMA1EN,DMA2EN
}AHB1_H;*/
/****************** AHB2 peripheral clock enable register*********************/
#define AHB2_H_OTGFSEN   7
/*typedef enum
{
	OTGFSEN
}AHB2_H;*/
//APB1 peripheral clock enable register
#define APB1_H_TIM2EN   0
#define APB1_H_TIM3EN   1
#define APB1_H_TIM4EN   2
#define APB1_H_TIM5EN   3
#define APB1_H_WWDGEN   11
#define APB1_H_SPI2EN   14
#define APB1_H_SPI3EN   15
#define APB1_H_USART2EN 17
#define APB1_H_I2C1EN   21
#define APB1_H_I2C2EN   22
#define APB1_H_I2C3EN   23
#define APB1_H_PWREN	28
/*typedef enum
{
	TIM2EN,TIM3EN,TIM4EN,TIM5EN,WWDGEN,SPI2EN,SPI3EN,USART2EN,I2C1EN,I2C2EN,I2C3EN,PWREN
}APB1_H;*/
/***************************** APB2 peripheral clock enable register ****************************/
#define APB2_H_TIM1EN   0
#define APB2_H_USART1EN 4
#define APB2_H_USART6EN 5
#define APB2_H_ADC1EN   8
#define APB2_H_SDIOEN   11
#define APB2_H_SPI1EN   12
#define APB2_H_SPI4EN   13
#define APB2_H_SYSCFGEN 14
#define APB2_H_TIM9EN   16
#define APB2_H_TIM10EN  17
#define APB2_H_TIM11EN  18
/*typedef enum
{
	TIM1EN,USART1EN,USART6EN,ADC1EN,SPI1EN,SPI4EN,SYSCFGEN,TIM9EN,TIM10EN,TIM11EN
}APB2_H;*/
////////////////////////////////////////////Low Power////////////////////////////////
/******************************** AHB1 peripheral clock enable in low power mode register ***************************/
#define AHB1_L_GPIOALPEN    0
#define AHB1_L_GPIOBLPEN    1
#define AHB1_L_GPIOCLPEN    2
#define AHB1_L_GPIODLPEN    3
#define AHB1_L_GPIOELPEN    4
#define AHB1_L_GPIOHLPEN    7
#define AHB1_L_CRCLPEN      12
#define AHB1_L_FLITFLPEN    15
#define AHB1_L_SRAM1LPEN    16
#define AHB1_L_DMA1LPEN     21
#define AHB1_L_DMA2LPEN     22
/*typedef enum
{
	GPIOALPEN,GPIOBLPEN,GPIOCLPEN,GPIODLPEN,GPIOELPEN,GPIOHLPEN,CRCLPEN,FLITFLPEN,SRAM1LPEN,DMA1LPEN,DMA2LPEN
}AHB1_L;*/
/********************************** AHB2 peripheral clock enable in low power mode register **************************/
#define AHB2_L_OTGFSLPEN    7
/*typedef enum
{
	OTGFSLPEN
}AHB2_L;*/
/************************************ APB1 peripheral clock enable in low power mode register **************************/
#define APB1_L_TIM2LPEN   0
#define APB1_L_TIM3LPEN   1
#define APB1_L_TIM4LPEN   2
#define APB1_L_TIM5LPEN   3
#define APB1_L_WWDGLPEN   11
#define APB1_L_SPI2LPEN   14
#define APB1_L_SPI3LPEN   15
#define APB1_L_USART2LPEN 17
#define APB1_L_I2C1LPEN   21
#define APB1_L_I2C2LPEN   22
#define APB1_L_I2C3LPEN   23
#define APB1_L_PWRLPEN	  28
/*typedef enum
{
	TIM2LPEN,TIM3LPEN,TIM4LPEN,TIM5LPEN,WWDGLPEN,SPI2LPEN,SPI3LPEN,USART2LPEN,I2C1LPEN,I2C2LPEN,I2C3LPEN,PWRLPEN
}APB1_H;*/
/************************************ APB2 peripheral clock enabled in low power mode register ****************************/
#define APB2_L_TIM1LPEN    0
#define APB2_L_USART1LPEN  4
#define APB2_L_USART6LPEN  5
#define APB2_L_ADC1LPEN    8
#define APB2_L_SDIOLPEN    11
#define APB2_L_SPI1LPEN    12
#define APB2_L_SPI4LPEN    13
#define APB2_L_SYSCFGLPEN  14
#define APB2_L_TIM9LPEN    16
#define APB2_L_TIM10LPEN   17
#define APB2_L_TIM11LPEN   18
/*typedef enum
{
	TIM1LPEN,USART1LPEN,USART6LPEN,ADC1LPEN,SPI1LPEN,SPI4LPEN,SYSCFGLPEN,TIM9LPEN,TIM10LPEN,TIM11LPEN
}APB2_H;*/
// Protype
void MRCC_voidPeripheral(Bus copy_u8Bus ,u8 copy_u8Peripheral,u8 copy_u8State);
//
void MRCC_voidPeripheral_HIGH(Bus copy_u8Bus ,u8 copy_u8Peripheral,u8 copy_u8State);
//
void MRCC_voidPeripheral_LOW(Bus copy_u8Bus ,u8 copy_u8Peripheral,u8 copy_u8State);
//
void MRCC_void_AHB1_H(u8 copy_u8Peripheral, u8 copy_u8State);
//
void MRCC_void_AHB2_H(u8 copy_u8Peripheral, u8 copy_u8State);
//
void MRCC_void_APB1_H(u8 copy_u8Peripheral, u8 copy_u8State);
//
void MRCC_void_APB2_H(u8 copy_u8Peripheral, u8 copy_u8State);
//
void MRCC_void_AHB1_L(u8 copy_u8Peripheral, u8 copy_u8State);
//
void MRCC_void_AHB2_L(u8 copy_u8Peripheral, u8 copy_u8State);
//
void MRCC_void_APB1_L(u8 copy_u8Peripheral, u8 copy_u8State);
//
void MRCC_void_APB2_L(u8 copy_u8Peripheral, u8 copy_u8State);
/******************************************** Buses Prescaler *************************************************/
//CFGR Prescaler  (AHB)(APB1)(APB2)
typedef enum
{
	PPRE1,PPRE2,HPRE
}CFGR_Prescaler;
//AHB prescaler (4 -> 7) Bit
#define RCC_CFGR_HPRE_NoPrescaler    0
#define RCC_CFGR_HPRE_PrescalerX2    8
#define RCC_CFGR_HPRE_PrescalerX4    9
#define RCC_CFGR_HPRE_PrescalerX8    10
#define RCC_CFGR_HPRE_PrescalerX16   11
#define RCC_CFGR_HPRE_PrescalerX64   12
#define RCC_CFGR_HPRE_PrescalerX128  13
#define RCC_CFGR_HPRE_PrescalerX256  14
#define RCC_CFGR_HPRE_PrescalerX512  15
//APB Low speed prescaler  (APB1)  (10->12) Bit
#define RCC_CFGR_PPRE1_NoPrescaler    0
#define RCC_CFGR_PPRE1_PrescalerX2    4
#define RCC_CFGR_PPRE1_PrescalerX4    5
#define RCC_CFGR_PPRE1_PrescalerX8    6
#define RCC_CFGR_PPRE1_PrescalerX16   7
// APB high-speed prescaler (APB2) (13->15) Bit
#define RCC_CFGR_PPRE2_NoPrescaler    0
#define RCC_CFGR_PPRE2_PrescalerX2    4
#define RCC_CFGR_PPRE2_PrescalerX4    5
#define RCC_CFGR_PPRE2_PrescalerX8    6
#define RCC_CFGR_PPRE2_PrescalerX16   7
// prototype prescaler function
//prescaler
void MRCC_voidSetBusesPrescaler(u8 copy_u8AHB,u8 Copy_u8APB1,u8 Copy_u8APB2);
void MRCC_voidSetBusPrescaler(CFGR_Prescaler copy_u8Bus,u8 Copy_u8Prescaler);
//AHB prescaler
void MRCC_voidSet_HPRE_Prescaler(u8 Copy_u8Prescaler);
//APB Low speed prescaler
void MRCC_voidSet_PPRE1_Prescaler(u8 Copy_u8Prescaler);
//APB high-speed prescaler
void MRCC_voidSet_PPRE2_Prescaler(u8 Copy_u8Prescaler);
/*************************************************                *******************************************/

#endif /* RCC_INTERFACE_H_ */
