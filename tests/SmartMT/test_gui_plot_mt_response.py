from mtpy.gui.SmartMT.visualization import MTResponse
from tests.SmartMT import SmartMTGUITestCase, _click_area


class TestGUIPlotMTResponse(SmartMTGUITestCase):
    def test_plot_mt_response_enable_type_1(self):
        plot_config = self._switch_to_plot(MTResponse)  # type:MTResponse
        _click_area(plot_config._arrow_ui.ui.checkBox_real, pos=self._pos_check_box)
        _click_area(plot_config._arrow_ui.ui.checkBox_imaginary, pos=self._pos_check_box)
        _click_area(plot_config._plot_control_ui.ui.checkBox_pt, pos=self._pos_check_box)
        _click_area(plot_config._rotation_ui.ui.dial_rotation, pos=self._pos_check_box)
        _click_area(plot_config._plot_control_ui.ui.radioButton_1, pos=self._pos_check_box)

        self._plot()

    def test_plot_mt_response_enable_type_2(self):
        plot_config = self._switch_to_plot(MTResponse)  # type:MTResponse

        # config plot
        _click_area(plot_config._arrow_ui.ui.checkBox_real, pos=self._pos_check_box)
        _click_area(plot_config._arrow_ui.ui.checkBox_imaginary, pos=self._pos_check_box)
        _click_area(plot_config._plot_control_ui.ui.checkBox_pt, pos=self._pos_check_box)
        _click_area(plot_config._plot_control_ui.ui.radioButton_2, pos=self._pos_check_box)
        _click_area(plot_config._rotation_ui.ui.dial_rotation)

        self._plot()

    def test_plot_mt_response_enable_type_3(self):
        plot_config = self._switch_to_plot(MTResponse)  # type:MTResponse

        # config plot
        _click_area(plot_config._arrow_ui.ui.checkBox_real, pos=self._pos_check_box)
        _click_area(plot_config._arrow_ui.ui.checkBox_imaginary, pos=self._pos_check_box)
        _click_area(plot_config._plot_control_ui.ui.checkBox_pt, pos=self._pos_check_box)
        _click_area(plot_config._plot_control_ui.ui.radioButton_3, pos=self._pos_check_box)
        _click_area(plot_config._rotation_ui.ui.dial_rotation)

        self._plot()