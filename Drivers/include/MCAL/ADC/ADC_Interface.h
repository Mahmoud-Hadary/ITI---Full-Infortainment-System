/*
 * ADC_Interface.h
 *
 *  Created on: Jan 29, 2023
 *      Author: Mostafa Rashed
 */

#ifndef ADC_INTERFACE_H_
#define ADC_INTERFACE_H_
/*
 * Function : Init Function
 * Input :  Prescaler in range ( 0 -> 3 )
 * 			Resolution in range ( 0 -> 3 )
 * Output :	Not return any thing
 */
void ADC_voidInit(u8 Copy_u8Prescaler,u8 Copy_u8Resolution);
/*
 * Function : DeInit Function
 * Input :  Don't take any thing
 * Output :	Not return any thing
 */
void ADC_voidDeInit(void);
/*
 * Function : to chose channels and priority to ADC run in it (In A Regular Sequence)
 * Input :  Number of channel is used
 * 			Channel priority as pointer to array
 * Output :	Not return any thing (Future return Status of Channel Selection)
 */
void ADC_voidChannelSelection(u8 Copy_u8Length, u8 *Copy_u8ChannelPriority);
/*
 * Function : Set Resolution
 * Input :  Resolution in range ( 0 -> 3 )
 * Output : Return No Thing
 */
void ADC_voidSetResolution(u8 Copy_u8Resolution);
/*
 * Function : Set Prescaler
 * Input :  Prescaler in range ( 0 -> 3 )
 * Output : Return No Thing
 */
void ADC_voidSetPrescaler(u8 Copy_u8Prescaler);
/*
 * Function : To Get Data is Converted
 * Input :  No Input
 * Output :	Return Data Converted in (u16)
 */
u16 ADC_u16GetData(void);
/*
 * Function : Single Conversion mode "One Conversion"  (regular group)
 * Input :  No Input
 * Output : Return Data Converted in (u16)
 */
u16 ADC_u16SingleConversion_Regular(void);
/*
 * Function : Continuous Conversion mode  (regular group)
 * Input :  No Input
 * Output : Return Data Converted in (u16)
 */
u16 ADC_u16ContinuousConversion_Regular(void);
/*
 * Function : Continuous Conversion mode with Interrupt (regular group)
 * Input :  No Input
 * Output : Return No Thing
 */
void ADC_u16ContinuousConversionIN_Regular(void (*A_ptrToFunc)(void));
#endif /* ADC_INTERFACE_H_ */
