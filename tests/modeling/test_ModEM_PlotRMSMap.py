# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 13:13:29 2016

@author: Alison Kirkby, YG


Plot RMS at each station as a map

"""
import os
from unittest import TestCase

from mtpy.modeling.modem import Plot_RMS_Maps
from tests import _plt_wait, _plt_close, TEST_TEMP_DIR, SAMPLE_DIR


class Test_PlotRMSMap(TestCase):
    def tearDown(self):
        _plt_wait(1)
        _plt_close()


    def test_fun(self):
        """
        test function
        :return: T/F
        """

        # directory where files are located
        wd = os.path.join(SAMPLE_DIR, 'ModEM')

        # directory to save to
        save_path = TEST_TEMP_DIR

        # file stem for inversion result
        filestem = 'Modular_MPI_NLCG_004'

        # period index to plot (0 plots the first (shortest) period, 1 for the second, etc)
        period_index = 0

        # plot map
        rmsmap = Plot_RMS_Maps(residual_fn=os.path.join(wd, filestem + '.res'), period_index=period_index,
                               xminorticks=50000, yminorticks=50000, save_plots='y')

        rmsmap.save_figure(save_path)  # this will save a file to
