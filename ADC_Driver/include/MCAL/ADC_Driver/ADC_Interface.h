/*
 * ADC_Interface.h
 *
 *  Created on: Jan 29, 2023
 *      Author: dubai key
 */

#ifndef ADC_INTERFACE_H_
#define ADC_INTERFACE_H_

#define ADC_OneConversion            1

#define ADC_PreScalerTwo             0
#define ADC_PreScalerFour            1
#define ADC_PreScalerSix             2
#define ADC_PreScalerEight           3

#define ADC_12BitResolution          0
#define ADC_10BitResolution          1
#define ADC_8BitResolution           2
#define ADC_6BitResolution           3

#define ADC_3CyclesSamplingTime      0
#define ADC_15CyclesSamplingTime     1
#define ADC_28CyclesSamplingTime     2

#define ADC_1ConversionSequenceLEN   0

#define ADC_Channel0                 0
#define ADC_Channel1                 1
#define ADC_Channel2                 2
#define ADC_Channel3                 3
#define ADC_Channel4                 4
#define ADC_Channel5                 5
#define ADC_Channel6                 6
#define ADC_Channel7                 7
#define ADC_Channel8                 8
#define ADC_Channel9                 9
//-----------------------------------------------------
void MADC_INIT_SingleConversion(u8 Copy_u8_Resolution);
void MADC_INIT_SingleConversionUsingINT(u8 Copy_u8_Resolution);

u16 MADC_u16_StartSingleConversion(u8 Copy_u8_ChannelNumber);
u16 MADC_u16_StartSingleConversionUsingINT(u8 Copy_u8_ChannelNumber);


#endif /* ADC_INTERFACE_H_ */
