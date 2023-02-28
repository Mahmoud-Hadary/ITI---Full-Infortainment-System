
########################################################################
# IMPORTS
########################################################################

import os
import sys
import math
import random
import time
import serial


try:
    from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication

    from PyQt5.QtGui import QPolygon, QPolygonF, QColor, QPen, QFont, QPainter, QFontMetrics, QConicalGradient, QRadialGradient, QFontDatabase

    from PyQt5.QtCore import Qt, QTime, QTimer, QPoint, QPointF, QRect, QSize, QObject, pyqtSignal

except:
    print("Error while importing PyQt5")
    exit()

################################################################################################
# AnalogGaugeWidget CLASS
################################################################################################


class AnalogGaugeWidget(QWidget):
    """Fetches rows from a Bigtable.
    Args: 
        none

    """
    valueChanged = pyqtSignal(int)
    def __init__(self, parent=None):
        super(AnalogGaugeWidget, self).__init__(parent)
        self.counter = 0
        # DEFAULT TIMER VALUE
        self.use_timer_event = True
        # DEFAULT NEEDLE COLOR
        self.setNeedleColor(0, 0, 0, 255)
        # DEFAULT NEEDLE WHEN RELEASED
        self.NeedleColorReleased = self.NeedleColor
        # DEFAULT NEEDLE COLOR ON DRAG
        # self.NeedleColorDrag = QColor(255, 0, 00, 255)
        self.setNeedleColorOnDrag(255, 0, 00, 255)
        # DEFAULT SCALE TEXT COLOR
        self.setScaleValueColor(0, 0, 0, 255)
        # DEFAULT VALUE COLOR
        self.setDisplayValueColor(0, 0, 0, 255)
        # DEFAULT CENTER POINTER COLOR
        # self.CenterPointColor = QColor(50, 50, 50, 255)
        self.set_CenterPointColor(0, 0, 0, 255)

        # DEFAULT NEEDLE COUNT
        self.value_needle_count = 1

        self.value_needle = QObject

        # DEFAULT MINIMUM AND MAXIMUM VALUE
        self.minValue = 40
        self.maxValue = 200
        # DEFAULT START VALUE
        self.value = self.minValue

        # DEFAULT OFFSET
        self.value_offset = 0

        self.valueNeedleSnapzone = 0.05
        self.last_value = 0

        # self.value2 = 0
        # self.value2Color = QColor(0, 0, 0, 255)

        # DEFAULT RADIUS
        self.gauge_color_outer_radius_factor = 1
        self.gauge_color_inner_radius_factor = 0.9

        self.center_horizontal_value = 0
        self.center_vertical_value = 0

        # DEFAULT SCALE VALUE
        self.scale_angle_start_value = 135
        self.scale_angle_size = 270

        self.angle_offset = 0

        self.setScalaCount(10)
        self.scala_subdiv_count = 5

        self.pen = QPen(QColor(0, 0, 0))

        # LOAD CUSTOM FONT
        QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(
            __file__), 'fonts/Orbitron/Orbitron-VariableFont_wght.ttf'))

        # DEFAULT POLYGON COLOR
        self.scale_polygon_colors = []

        # BIG SCALE COLOR
        self.bigScaleMarker = Qt.black

        # FINE SCALE COLOR
        self.fineScaleColor = Qt.black

        # DEFAULT SCALE TEXT STATUS
        self.setEnableScaleText(True)
        self.scale_fontname = "Orbitron"
        self.initial_scale_fontsize = 14
        self.scale_fontsize = self.initial_scale_fontsize

        # DEFAULT VALUE TEXT STATUS
        self.enable_value_text = True
        self.value_fontname = "Orbitron"
        self.initial_value_fontsize = 40
        self.value_fontsize = self.initial_value_fontsize
        self.text_radius_factor = 0.5

        # ENABLE BAR GRAPH BY DEFAULT
        self.setEnableBarGraph(False)
        # FILL POLYGON COLOR BY DEFAULT
        self.setEnableScalePolygon(True)
        # ENABLE CENTER POINTER BY DEFAULT
        self.enable_CenterPoint = True
        # ENABLE FINE SCALE BY DEFAULT
        self.enable_fine_scaled_marker = True
        # ENABLE BIG SCALE BY DEFAULT
        self.enable_big_scaled_marker = True

        # NEEDLE SCALE FACTOR/LENGTH
        self.needle_scale_factor = 0.8
        # ENABLE NEEDLE POLYGON BY DEFAULT
        self.enable_Needle_Polygon = True

        # ENABLE NEEDLE MOUSE TRACKING BY DEFAULT
        self.setMouseTracking(False)

        # SET GAUGE UNITS
        self.units = "BPM"

        if self.use_timer_event:
            timer = QTimer(self)
            timer.timeout.connect(self.updateValueByVariable)
            timer.start(1000)
        else:
            self.update()

        # SET DEFAULT THEME
        self.setGaugeTheme(50)

        # RESIZE GAUGE
        self.rescale_method()
        
        

    ################################################################################################
    # SET SCALE FONT FAMILY
    ################################################################################################


    def setScaleFontFamily(self, font):
        '''
        Sets the font family for the scale in the plot.
        @param font A string specifying the font family to use for the scale.
        @type font: str
        @return: None

        '''
        self.scale_fontname = str(font)

    ################################################################################################
    # SET VALUE FONT FAMILY
    ################################################################################################
    def setValueFontFamily(self, font):
        """
        Set the font family for the value text displayed on the gauge.

        @param font: A string indicating the font family to use for the value text.
        @type font: str
        @return: None

        """
        self.value_fontname = str(font)

    ################################################################################################
    # SET BIG SCALE COLOR
    ################################################################################################
    def setBigScaleColor(self, color):
        """
        Set the color of the big scale marker.

        @param color: The color of the big scale marker. This can be a string representation of a color name or an RGB value.
        @type color: str

        @return: None
        """
        self.bigScaleMarker = QColor(color)
    ################################################################################################
    # SET FINE SCALE COLOR
    ################################################################################################
    def setFineScaleColor(self, color):
        """
        Set the color of the fine scale markers.
    
        Args:
            color (str): The color to set in string format (e.g. 'red', '#FF0000').
        """
        self.fineScaleColor = QColor(color)

    ################################################################################################
    # GAUGE THEMES
    ################################################################################################
    def setGaugeTheme(self, Theme=1):
        """
        Sets the theme of the gauge.

        Args:
            Theme (int): The theme of the gauge. Possible values are 0, 1, 2, 3, 4, 5 and 6. Default is 1.
    
        Returns:
            None
        """
        if Theme == 0 or Theme == None:
            self.set_scale_polygon_colors([[.00, Qt.red],
                                           [.1, Qt.yellow],
                                           [.15, Qt.green],
                                           [1, Qt.transparent]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 1:
            self.set_scale_polygon_colors([[.75, Qt.red],
                                           [.5, Qt.yellow],
                                           [.25, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 2:
            self.set_scale_polygon_colors([[.25, Qt.red],
                                           [.5, Qt.yellow],
                                           [.75, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        elif Theme == 3:
            self.set_scale_polygon_colors([[.00, Qt.white]])

            self.needle_center_bg = [
                                    [0, Qt.white],
            ]

            self.outer_circle_bg = [
                [0, Qt.white],
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 4:
            self.set_scale_polygon_colors([[1, Qt.black]])

            self.needle_center_bg = [
                                    [0, Qt.black],
            ]

            self.outer_circle_bg = [
                [0, Qt.black],
            ]

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 5:
            self.set_scale_polygon_colors([[1, QColor("#029CDE")]])

            self.needle_center_bg = [
                                    [0, QColor("#029CDE")],
            ]

            self.outer_circle_bg = [
                [0, QColor("#029CDE")],
            ]

        elif Theme == 6:
            self.set_scale_polygon_colors([[.75, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.25, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 7:
            self.set_scale_polygon_colors([[.25, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.75, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 8:
            self.setCustomGaugeTheme(
                color1="#ffaa00",
                color2="#7d5300",
                color3="#3e2900"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 9:
            self.setCustomGaugeTheme(
                color1="#3e2900",
                color2="#7d5300",
                color3="#ffaa00"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white
        elif Theme == 50:
            self.setCustomGaugeTheme(
                color1="#3a86ff",
                color2="#8338ec",
                color3="#ff006e"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 10:
            self.setCustomGaugeTheme(
                color1="#ff007f",
                color2="#aa0055",
                color3="#830042"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 11:
            self.setCustomGaugeTheme(
                color1="#830042",
                color2="#aa0055",
                color3="#ff007f"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 12:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 13:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 14:
            self.setCustomGaugeTheme(
                color1="#232803",
                color2="#821600",
                color3="#ffe75d"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 15:
            self.setCustomGaugeTheme(
                color1="#00FF11",
                color2="#00990A",
                color3="#002603"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 16:
            self.setCustomGaugeTheme(
                color1="#002603",
                color2="#00990A",
                color3="#00FF11"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 17:
            self.setCustomGaugeTheme(
                color1="#00FFCC",
                color2="#00876C",
                color3="#00211B"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 18:
            self.setCustomGaugeTheme(
                color1="#00211B",
                color2="#00876C",
                color3="#00FFCC"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 19:
            self.setCustomGaugeTheme(
                color1="#001EFF",
                color2="#001299",
                color3="#000426"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 20:
            self.setCustomGaugeTheme(
                color1="#000426",
                color2="#001299",
                color3="#001EFF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 21:
            self.setCustomGaugeTheme(
                color1="#F200FF",
                color2="#85008C",
                color3="#240026"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 22:
            self.setCustomGaugeTheme(
                color1="#240026",
                color2="#85008C",
                color3="#F200FF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 23:
            self.setCustomGaugeTheme(
                color1="#FF0022",
                color2="#080001",
                color3="#009991"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 24:
            self.setCustomGaugeTheme(
                color1="#009991",
                color2="#080001",
                color3="#FF0022"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

    ################################################################################################
    # SET CUSTOM GAUGE THEME
    ################################################################################################
    def setCustomGaugeTheme(self, **colors):
        '''
        Sets the custom gauge theme colors.

        @param colors A dictionary containing color values.

        @param colors['color1'] The first color value.

        @param colors['color2'] The second color value.

        @param colors['color3'] The third color value.

        If 'color3' is defined, sets the polygon colors of the gauge scale and the background colors of the needle center and outer circle.

        If 'color3' is not defined, sets the polygon colors of the gauge scale and the background colors of the needle center and outer circle using only 'color1' and 'color2'.

        If 'color1' is not defined, sets the gauge theme to the default value.
        '''
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.36, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:

            self.setGaugeTheme(0)
            print("color1 is not defined")

    ################################################################################################
    # SET SCALE POLYGON COLOR
    ################################################################################################
    def setScalePolygonColor(self, **colors):
        '''
        @brief Set the colors of the scale polygon.

        The method sets the colors of the scale polygon in a gauge. The colors are defined as

        dictionary with keys 'color1', 'color2', and 'color3' respectively for the colors in the

        positions 0.25, 0.5 and 0.75 of the polygon. If a color is not defined or it has length 0,

        it is not set and the default color is used.

        @param colors A dictionary containing the color information as strings, with keys 'color1',

        'color2', and 'color3'.

        @return void
        '''
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

        else:
            print("color1 is not defined")

    ################################################################################################
    # SET NEEDLE CENTER COLOR
    ################################################################################################
    def setNeedleCenterColor(self, **colors):
        '''
        @brief Sets the color for the center of the needle.
        @param colors A dictionary containing up to three color values with keys "color1", "color2", and "color3".
        If a color is not provided or its value is empty, the default color will be used.
        If only "color1" is provided, that color will be used as the solid center color.
        If "color1", "color2", and "color3" are provided, a gradient of the three colors will be used.
            '''
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                else:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

            else:

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]
        else:
            print("color1 is not defined")

    ################################################################################################
    # SET OUTER CIRCLE COLOR
    ################################################################################################
    def setOuterCircleColor(self, **colors):
        """
        Set the colors of the outer circle of the widget.

        :param colors: A dictionary containing up to three keys: 'color1', 'color2', and 'color3'.
                   The value of each key should be a string representing the color in the format "#RRGGBB".
                   'color1' corresponds to the innermost part of the circle, 'color2' corresponds to the
                   middle part of the circle, and 'color3' corresponds to the outermost part of the circle.
        """
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.37788, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:
            print("color1 is not defined")

    ################################################################################################
    # RESCALE
    ################################################################################################

    def rescale_method(self):
        '''
        Rescales various elements of the widget based on its current size.

        This method adjusts the widget diameter, needle size, and font sizes according to the current width and height
        of the widget.

        Returns:
            None
        '''
        ################################################################################################
        # SET WIDTH AND HEIGHT
        ################################################################################################
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()

        ################################################################################################
        # SET NEEDLE SIZE
        ################################################################################################
        self.change_value_needle_style([QPolygon([
            QPoint(4, 30),
            QPoint(-4, 30),
            QPoint(-2, int(- self.widget_diameter / 2 * self.needle_scale_factor)),
            QPoint(0, int(- self.widget_diameter /
                   2 * self.needle_scale_factor - 6)),
            QPoint(2, int(- self.widget_diameter / 2 * self.needle_scale_factor))
        ])])

        ################################################################################################
        # SET FONT SIZE
        ################################################################################################
        self.scale_fontsize = int(
            self.initial_scale_fontsize * self.widget_diameter / 400)
        self.value_fontsize = int(
            self.initial_value_fontsize * self.widget_diameter / 400)

    def change_value_needle_style(self, design):
        '''
        Change the design of the needle of the gauge widget.

        Args:
            design (List[QPolygon]): A list of QPolygon objects that describe the design of the needle.
        '''
        # prepared for multiple needle instrument
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)
        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # UPDATE VALUE
    ################################################################################################
    def updateValue(self, value, mouse_controlled=False):
        """
        Updates the value displayed by the gauge widget.

        Args:
            value (float): The value to be displayed.
            mouse_controlled (bool, optional): Flag indicating whether the update was triggered by a mouse event. Defaults to False.
        """
        if value <= self.minValue:
            self.value = self.minValue
        elif value >= self.maxValue:
            self.value = self.maxValue
        else:
            self.value = value

        self.value = value
        self.update()
    def updateAngleOffset(self, offset):
        """
        Updates the angle offset of the gauge widget.

        Args:
            offset (float): The angle offset to be applied.
        """
        self.angle_offset = offset
        if not self.use_timer_event:
            self.update()

    def center_horizontal(self, value):
        """
        Sets the horizontal center of the gauge widget.

        Args:
            value (float): The value representing the horizontal center.
        """
        self.center_horizontal_value = value
        # print("horizontal: " + str(self.center_horizontal_value))

    def center_vertical(self, value):
        """
        Sets the vertical center of the gauge widget.

        Args:
            value (float): The value representing the vertical center.
        """
        self.center_vertical_value = value
        # print("vertical: " + str(self.center_vertical_value))

    ################################################################################################
    # SET NEEDLE COLOR
    ################################################################################################
    def setNeedleColor(self, R=50, G=50, B=50, Transparency=255):
        '''
        @brief Sets the color of the needle.

        @param R The red value of the needle color (0-255).

        @param G The green value of the needle color (0-255).

        @param B The blue value of the needle color (0-255).

        @param Transparency The transparency value of the needle color (0-255).
        '''
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColor = QColor(R, G, B, Transparency)
        self.NeedleColorReleased = self.NeedleColor

        if not self.use_timer_event:
            self.update()
    ################################################################################################
    # SET NEEDLE COLOR ON DRAG
    ################################################################################################

    def setNeedleColorOnDrag(self, R=50, G=50, B=50, Transparency=255):
        '''
        @brief Sets the color of the needle when it is being dragged.

        @param R The red value of the needle color (0-255).

        @param G The green value of the needle color (0-255).

        @param B The blue value of the needle color (0-255).

        @param Transparency The transparency value of the needle color (0-255).
        '''
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColorDrag = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET SCALE VALUE COLOR
    ################################################################################################
    def setScaleValueColor(self, R=50, G=50, B=50, Transparency=255):
        '''
        @brief Sets the color of the scale value.

        @param R The red value of the scale value color (0-255).

        @param G The green value of the scale value color (0-255).

        @param B The blue value of the scale value color (0-255).

        @param Transparency The transparency value of the scale value color (0-255).
        '''
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.ScaleValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET DISPLAY VALUE COLOR
    ################################################################################################
    def setDisplayValueColor(self, R=50, G=50, B=50, Transparency=255):
        '''
        @brief Sets the color of the display value.

        @param R The red value of the display value color (0-255).

        @param G The green value of the display value color (0-255).

        @param B The blue value of the display value color (0-255).

        @param Transparency The transparency value of the display value color (0-255).
        '''
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.DisplayValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET CENTER POINTER COLOR
    ################################################################################################
    def set_CenterPointColor(self, R=50, G=50, B=50, Transparency=255):
        '''
        @brief Set the center point color
        @param R The Red color value (0-255)
        @param G The Green color value (0-255)
        @param B The Blue color value (0-255)
        @param Transparency The transparency value (0-255)
        '''
        self.CenterPointColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE NEEDLE POLYGON
    ################################################################################################
    def setEnableNeedlePolygon(self, enable=True):
        '''
        @brief Enable or disable the display of the needle polygon
        @param enable Set to true to enable and false to disable
        '''
        self.enable_Needle_Polygon = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE SCALE TEXT
    ################################################################################################
    def setEnableScaleText(self, enable=True):
        '''
        @brief Enable or disable the display of the scale text
        @param enable Set to true to enable and false to disable
        '''
        self.enable_scale_text = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE BAR GRAPH
    ################################################################################################
    def setEnableBarGraph(self, enable=True):
        '''
        @brief Enable or disable the display of the bar graph
        @param enable Set to true to enable and false to disable
        '''
        self.enableBarGraph = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE VALUE TEXT
    ################################################################################################
    def setEnableValueText(self, enable=True):
        '''
        @brief Enable or disable the display of the value text
        @param enable Set to true to enable and false to disable
        '''
        self.enable_value_text = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE CENTER POINTER
    ################################################################################################
    def setEnableCenterPoint(self, enable=True):
        """
        Set whether to show the center point.

        @param enable: True to show the center point, False otherwise.
        """
        self.enable_CenterPoint = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE FILLED POLYGON
    ################################################################################################
    def setEnableScalePolygon(self, enable=True):
        """
        Set whether to show the filled polygon.

        @param enable: True to show the filled polygon, False otherwise.
        """
        self.enable_filled_Polygon = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE BIG SCALE
    ################################################################################################
    def setEnableBigScaleGrid(self, enable=True):
        """
        Set whether to show the big scale.

        @param enable: True to show the big scale, False otherwise.
        """
        self.enable_big_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE FINE SCALE
    ################################################################################################

    def setEnableFineScaleGrid(self, enable=True):
        """
        Set whether to show the fine scale.

        @param enable: True to show the fine scale, False otherwise.
        """
        self.enable_fine_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE SCALA MAIN CONT
    ################################################################################################
    def setScalaCount(self, count):
        """
        Set the number of scale marks.

        @param count: The number of scale marks to show.
        """
        if count < 1:
            count = 1
        self.scalaCount = count

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET MINIMUM VALUE
    ################################################################################################
    def setMinValue(self, min):
        """
        Set the minimum value of the widget.

        @param min: The minimum value to set.
        """
        if self.value < min:
            self.value = min
        if min >= self.maxValue:
            self.minValue = self.maxValue - 1
        else:
            self.minValue = min

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET MAXIMUM VALUE
    ################################################################################################
    def setMaxValue(self, max):
        """
        Set the maximum value of the gauge.

        If the current value of the gauge is greater than the new maximum value,
        the value of the gauge is set to the new maximum value. If the new maximum
        value is less than or equal to the minimum value, the maximum value is set
        to the minimum value plus one.

        :param max: The new maximum value of the gauge.
        """
        if self.value > max:
            self.value = max
        if max <= self.minValue:
            self.maxValue = self.minValue + 1
        else:
            self.maxValue = max

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET SCALE ANGLE
    ################################################################################################
    def setScaleStartAngle(self, value):
        """
        Set the starting angle of the gauge scale.

        The value should be in degrees and in the range of 0 to 360.

        :param value: The new starting angle of the gauge scale in degrees.
        """
        # Value range in DEG: 0 - 360
        self.scale_angle_start_value = value
        # print("startFill: " + str(self.scale_angle_start_value))

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET SCALE SIZE
    ################################################################################################
    def setTotalScaleAngleSize(self, value):
        """
        Set the total angle size of the gauge scale.

        The value should be in degrees.

        :param value: The new total angle size of the gauge scale in degrees.
        """
        self.scale_angle_size = value
        # print("stopFill: " + str(self.scale_angle_size))

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET GAUGE COLOR OUTER RADIUS
    ################################################################################################
    def setGaugeColorOuterRadiusFactor(self, value):
        """
        Set the factor that determines the outer radius of the gauge color.

        The value should be a float between 0 and 1.

        :param value: The new factor that determines the outer radius of the gauge color.
        """
        self.gauge_color_outer_radius_factor = float(value) / 1000
        # print(self.gauge_color_outer_radius_factor)

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET GAUGE COLOR INNER RADIUS
    ################################################################################################
    def setGaugeColorInnerRadiusFactor(self, value):
        """
        Set the factor that determines the inner radius of the gauge color.

        The value should be a float between 0 and 1.

        :param value: The new factor that determines the inner radius of the gauge color.
        """
        self.gauge_color_inner_radius_factor = float(value) / 1000
        # print(self.gauge_color_inner_radius_factor)

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET SCALE POLYGON COLOR
    ################################################################################################
    def set_scale_polygon_colors(self, color_array):
        """
        Set the colors of the gauge scale polygons.

        The colors should be specified as a list of pairs, where the first element
        of each pair is the position of the color on the scale (a float between 0 and 1),
        and the second element is the color itself (a QColor object).

        :param color_array: The new colors of the gauge scale polygons.
        """
        # print(type(color_array))
        if 'list' in str(type(color_array)):
            self.scale_polygon_colors = color_array
        elif color_array == None:
            self.scale_polygon_colors = [[.0, Qt.transparent]]
        else:
            self.scale_polygon_colors = [[.0, Qt.transparent]]

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # GET MAXIMUM VALUE
    ################################################################################################
    def get_value_max(self):
        """
        Get the maximum value of the gauge.

        :return: The maximum value of the gauge.
        """
        return self.maxValue

    ###############################################################################################
    # SCALE PAINTER
    ###############################################################################################

    ################################################################################################
    # CREATE PIE
    ################################################################################################
    def create_polygon_pie(self, outer_radius, inner_raduis, start, lenght, bar_graph=True):
        '''
        @brief Creates a polygon shape in the form of a pie chart.

        @param outer_radius The radius of the outer circle of the pie chart.

        @param inner_raduis The radius of the inner circle of the pie chart.

        @param start The starting angle of the pie chart.

        @param lenght The length of the pie chart.

        @param bar_graph Determines whether to enable/disable bar graph.

        @return A QPolygonF object representing the polygon shape of the pie chart.
        '''
        polygon_pie = QPolygonF()
        # start = self.scale_angle_start_value
        # start = 0
        # lenght = self.scale_angle_size
        # lenght = 180
        # inner_raduis = self.width()/4
        # print(start)
        n = 360     # angle steps size for full circle
        # changing n value will causes drawing issues
        w = 360 / n   # angle per step
        # create outer circle line from "start"-angle to "start + lenght"-angle
        x = 0
        y = 0

        # todo enable/disable bar graf here
        if not self.enableBarGraph and bar_graph:
            # float_value = ((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue))
            lenght = int(
                round((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue)))
            # print("f: %s, l: %s" %(float_value, lenght))
            pass

        # mymax = 0

        # add the points of polygon
        for i in range(lenght + 1):
            t = w * i + start - self.angle_offset
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        # add the points of polygon
        for i in range(lenght + 1):
            # print("2 " + str(i))
            t = w * (lenght - i) + start - self.angle_offset
            x = inner_raduis * math.cos(math.radians(t))
            y = inner_raduis * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        # close outer line
        polygon_pie.append(QPointF(x, y))
        return polygon_pie

    def draw_filled_polygon(self, outline_pen_with=0):
        '''
        @brief Draws a filled polygon on the widget, using the scale colors defined in self.scale_polygon_colors.

        @param outline_pen_with The width of the outline pen. Defaults to 0.

        @return void
        '''
        if not self.scale_polygon_colors == None:
            painter_filled_polygon = QPainter(self)
            painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
            # Koordinatenursprung in die Mitte der Flaeche legen
            painter_filled_polygon.translate(
                self.width() / 2, self.height() / 2)

            painter_filled_polygon.setPen(Qt.NoPen)

            self.pen.setWidth(outline_pen_with)
            if outline_pen_with > 0:
                painter_filled_polygon.setPen(self.pen)

            colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self.pen.width() / 2)) *
                self.gauge_color_outer_radius_factor,
                (((self.widget_diameter / 2) - (self.pen.width() / 2))
                 * self.gauge_color_inner_radius_factor),
                self.scale_angle_start_value, self.scale_angle_size)

            gauge_rect = QRect(QPoint(0, 0), QSize(
                int(self.widget_diameter / 2 - 1), int(self.widget_diameter - 1)))
            grad = QConicalGradient(QPointF(0, 0), - self.scale_angle_size - self.scale_angle_start_value +
                                    self.angle_offset - 1)

            # todo definition scale color as array here
            for eachcolor in self.scale_polygon_colors:
                grad.setColorAt(eachcolor[0], eachcolor[1])
            # grad.setColorAt(.00, Qt.red)
            # grad.setColorAt(.1, Qt.yellow)
            # grad.setColorAt(.15, Qt.green)
            # grad.setColorAt(1, Qt.transparent)
            # self.brush = QBrush(QColor(255, 0, 255, 255))
            # grad.setStyle(Qt.Dense6Pattern)
            # painter_filled_polygon.setBrush(self.brush)
            painter_filled_polygon.setBrush(grad)

            painter_filled_polygon.drawPolygon(colored_scale_polygon)
            # return painter_filled_polygon

    def draw_icon_image(self):
        """
        Draws an icon image on the gauge widget.

        :return: None
        """
        pass

    ###############################################################################################
    # BIG SCALE MARKERS
    ###############################################################################################
    def draw_big_scaled_marker(self):
        '''
        @brief Draws the big scaled marker on the gauge widget.

        @details This function draws a big scaled marker on the gauge widget, indicating the position of the current value.

        The marker is drawn using a QPainter object, which is translated to the center of the gauge widget, and rotated to

        the start angle of the scale. The marker is then drawn by repeatedly drawing lines at equally spaced angles along

        the scale. The number of lines is determined by the scalaCount property of the widget.

        @note The bigScaleMarker property must be set before calling this function, to determine the color of the marker.

        The scalaCount property determines the number of lines to be drawn, and is set by default to 10.

        @param None

        @return None
        '''
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        my_painter.translate(self.width() / 2, self.height() / 2)

        # my_painter.setPen(Qt.NoPen)
        self.pen = QPen(self.bigScaleMarker)
        self.pen.setWidth(2)
        # # if outline_pen_with > 0:
        my_painter.setPen(self.pen)

        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scalaCount))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int((self.widget_diameter / 2) -
                                (self.widget_diameter / 20))
        # print(stepszize)
        for i in range(self.scalaCount + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        '''
        @brief Creates and draws the scale marker values on the widget.

        This function creates and draws the scale marker values on the widget. It uses QPainter to draw the text.

        The text is centered on each marker and placed at a specified radius from the center of the widget.

        The font size, font name, and color of the text are determined by the user-specified parameters in the constructor.

        The number of markers and the range of values they represent are also determined by the user-specified parameters in the constructor.

        @param None

        @return None
        '''
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        # painter.save()
        font = QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.ScaleValueColor)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter / 2 * text_radius_factor

        scale_per_div = int((self.maxValue - self.minValue) / self.scalaCount)

        angle_distance = (float(self.scale_angle_size) /
                          float(self.scalaCount))
        for i in range(self.scalaCount + 1):
            # text = str(int((self.maxValue - self.minValue) / self.scalaCount * i))
            text = str(int(self.minValue + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scale_fontname,
                            self.scale_fontsize, QFont.Bold))
            angle = angle_distance * i + \
                float(self.scale_angle_start_value - self.angle_offset)
            x = text_radius * math.cos(math.radians(angle))
            y = text_radius * math.sin(math.radians(angle))
            # print(w, h, x, y, text)

            painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                             int(h), Qt.AlignCenter, text)
        # painter.restore()

    ################################################################################################
    # FINE SCALE MARKERS
    ################################################################################################
    def create_fine_scaled_marker(self):
        '''
        Draws the fine scale marker on the widget.

        This function uses QPainter to draw a series of lines representing the fine scale marker on the widget. The lines are drawn in the color specified by `self.fineScaleColor`, and are rotated according to the `self.scale_angle_start_value` and `self.angle_offset` attributes.

        :return: None
        
        '''
        #  Description_dict = 0
        my_painter = QPainter(self)

        my_painter.setRenderHint(QPainter.Antialiasing)
        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(self.fineScaleColor)
        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) /
                      float(self.scalaCount * self.scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int(
            (self.widget_diameter / 2) - (self.widget_diameter / 40))
        for i in range((self.scalaCount * self.scala_subdiv_count) + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    ################################################################################################
    # VALUE TEXT
    ################################################################################################
    def create_values_text(self):
        """
        Draws the value text on the widget.

        This function uses QPainter to draw the value text on the widget. The text is drawn in the color specified by `self.DisplayValueColor`, and is positioned at a certain radius from the center of the widget based on the `self.text_radius_factor` attribute. The font size and font family are specified by the `self.value_fontsize` and `self.value_fontname` attributes, respectively.

        :return: None
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        # painter.save()
        # xShadow = 3.0
        # yShadow = 3.0
        font = QFont(self.value_fontname, self.value_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        # angle_distance = (float(self.scale_angle_size) / float(self.scalaCount))
        # for i in range(self.scalaCount + 1):
        text = str(int(self.value))
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname,
                        self.value_fontsize, QFont.Bold))

        # Mitte zwischen Skalenstart und Skalenende:
        # Skalenende = Skalenanfang - 360 + Skalenlaenge
        # Skalenmitte = (Skalenende - Skalenanfang) / 2 + Skalenanfang
        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size - 360)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)

    ################################################################################################
    # UNITS TEXT
    ################################################################################################

    def create_units_text(self):
        '''
        @brief Create the units text for the custom widget
        This function creates the units text for the custom widget using QPainter to draw
        the text on the widget. The units text is displayed at the center of the widget,
        on the outer edge of the scale.
        '''
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(self.units)
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold))

        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size + 180)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)

    ################################################################################################
    # CENTER POINTER
    ################################################################################################

    def draw_big_needle_center_point(self, diameter=30):
        '''
        @brief Draw a big needle center point using a QConicalGradient brush
        @param diameter The diameter of the center point (default = 30)
        This function draws a big needle center point using a QConicalGradient brush.
        It sets the render hint to antialiasing to ensure smooth edges of the center point.
        The coordinate system origin is set to the center of the widget.
        It then creates a colored scale polygon using the create_polygon_pie() function, which creates a pie-shaped polygon.
        The outer radius is calculated as the widget diameter divided by 8 minus half the pen width.
        The inner radius is set to 0, the start angle is set to self.scale_angle_start_value, and the length of the arc is set to 360.
        The function then sets up the QConicalGradient brush using the needle_center_bg color array.
        Finally, the function uses the QConicalGradient brush to fill the polygon, and returns nothing.
        '''
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        # painter.setPen(Qt.NoPen)

        # painter.setBrush(self.CenterPointColor)
        # diameter = diameter # self.widget_diameter/6
        # painter.drawEllipse(int(-diameter / 2), int(-diameter / 2), int(diameter), int(diameter))

        # create_polygon_pie(self, outer_radius, inner_raduis, start, lenght)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 8) - (self.pen.width() / 2)),
            0,
            self.scale_angle_start_value, 360, False)

        # 150.0 0.0 131 360

        grad = QConicalGradient(QPointF(0, 0), 0)

        # todo definition scale color as array here
        for eachcolor in self.needle_center_bg:
            grad.setColorAt(eachcolor[0], eachcolor[1])
        # grad.setColorAt(.00, Qt.red)
        # grad.setColorAt(.1, Qt.yellow)
        # grad.setColorAt(.15, Qt.green)
        # grad.setColorAt(1, Qt.transparent)
        painter.setBrush(grad)
        # self.brush = QBrush(QColor(255, 0, 255, 255))
        # painter_filled_polygon.setBrush(self.brush)

        painter.drawPolygon(colored_scale_polygon)
        # return painter_filled_polygon

    ################################################################################################
    # CREATE OUTER COVER
    ################################################################################################
    def draw_outer_circle(self, diameter=30):
        '''
        @brief Draw the outer circle of the gauge widget with a radial gradient brush.

        This function draws the outer circle of the gauge widget using a radial gradient brush.

        It sets the appropriate rendering hints, translates the painter to the center of the widget,

        sets the pen to no pen, creates a polygon pie shape using the create_polygon_pie function,

        creates a radial gradient using the QRadialGradient function, and sets the brush to the gradient.

        Finally, it draws the polygon using the painter's drawPolygon function.

        @param diameter The diameter of the outer circle. Defaults to 30.
        '''
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 2) - (self.pen.width())),
            (self.widget_diameter / 6),
            self.scale_angle_start_value / 10, 360, False)

        radialGradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outer_circle_bg:
            radialGradient.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(radialGradient)

        painter.drawPolygon(colored_scale_polygon)

    ################################################################################################
    # NEEDLE POINTER
    ################################################################################################

    def draw_needle(self):
        """
        Draws the needle of the gauge widget at the current value.

        The needle is drawn using a convex polygon with a color defined by the `NeedleColor` property of the widget.

        Args:
            None

        Returns:
            None
        """
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.NeedleColor)
        painter.rotate(((self.value - self.value_offset - self.minValue) * self.scale_angle_size /
                        (self.maxValue - self.minValue)) + 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    ###############################################################################################
    # EVENTS
    ###############################################################################################

    ################################################################################################
    # ON WINDOW RESIZE
    ################################################################################################
    def resizeEvent(self, event):
        """
        Event handler for the resize event.

        Resizes the widget and calls the rescale method to update the size of the elements.

        :param event: the resize event object
        """
        # self.resized.emit()
        # return super(self.parent, self).resizeEvent(event)
        # print("resized")
        # print(self.width())
        self.rescale_method()
        # self.emit(QtCore.SIGNAL("resize()"))
        # print("resizeEvent")

    ################################################################################################
    # ON PAINT EVENT
    ################################################################################################
    def paintEvent(self, event):
        """
        This function is called every time the widget needs to be repainted. It is responsible for drawing all the
        components of the widget.

        Args:
            event (QPaintEvent): the event that triggered the paint event.

        Returns:
            None
        """
        # Main Drawing Event:
        # Will be executed on every change
        # vgl http://doc.qt.io/qt-4.8/qt-demos-affine-xform-cpp.html
        # print("event", event)

        self.draw_outer_circle()
        self.draw_icon_image()
        # colored pie area
        if self.enable_filled_Polygon:
            self.draw_filled_polygon()

        # draw scale marker lines
        if self.enable_fine_scaled_marker:
            self.create_fine_scaled_marker()
        if self.enable_big_scaled_marker:
            self.draw_big_scaled_marker()

        # draw scale marker value text
        if self.enable_scale_text:
            self.create_scale_marker_values_text()

        # Display Value
        if self.enable_value_text:
            self.create_values_text()
            self.create_units_text()

        # draw needle 1
        if self.enable_Needle_Polygon:
            self.draw_needle()

        # Draw Center Point
        if self.enable_CenterPoint:
            self.draw_big_needle_center_point(
                diameter=(self.widget_diameter / 6))

    ###############################################################################################
    # MOUSE EVENTS
    ###############################################################################################

    def setMouseTracking(self, flag):
        '''
        @brief Enable/disable mouse tracking recursively for all child widgets.

        @param flag Flag to set mouse tracking (True to enable, False to disable).
        '''
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseReleaseEvent(self, QMouseEvent):
        """
        This method is called when the mouse button is released over the widget. It sets the needle color to NeedleColorReleased and updates the widget if `use_timer_event` is False.

        Args:
            QMouseEvent: The mouse event object.

        Returns:
            None
        """
        self.NeedleColor = self.NeedleColorReleased

        if not self.use_timer_event:
            self.update()
        pass

    ########################################################################
    # MOUSE LEAVE EVENT
    ########################################################################
    def leaveEvent(self, event):
        """
        This method is called when the mouse cursor leaves the widget. It sets the needle color to NeedleColorReleased and updates the widget.

        Args:
            event: The leave event object.

        Returns:
            None
        """
        self.NeedleColor = self.NeedleColorReleased
        self.update()
    
    
                
    def updateValueByVariable(self):
        """
        This method reads heart rate data from a serial port and updates the widget's value by calling `updateValue` method. If `use_timer_event` is True, this method is called by the timer event. Otherwise, it needs to be called manually.

        Args:
            None

        Returns:
            None
        """
        self.counter = self.counter + 1
        ser = serial.Serial('/dev/ttyUSB0', 9600,timeout=1)
    
        # if you want to store heart rate data in excel file in example use this
        heart_rate_readings = []
        reading = ser.read(2).decode().strip()
        if self.counter == 1 or reading.isdigit()==False : 
            self.heart_rate = 40 
        else:   
            self.heart_rate = int(reading)
                
                
            #heart_rate_readings.append(heart_rate)
            print("Heart rate: {} bpm".format(self.heart_rate))
            #time you need between readings            
            #self.heart_rate = random.randint(50, 150)
    
        self.updateValue(self.heart_rate, mouse_controlled=False) 
        
        
                
                

################################################################################################
# END ==>
################################################################################################
