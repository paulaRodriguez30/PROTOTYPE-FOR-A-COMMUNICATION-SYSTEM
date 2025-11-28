#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: GMSK_RX
# GNU Radio version: v3.10.11.0-89-ga17f69e7

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import GMSK_epy_block_0 as epy_block_0  # embedded python block
import numpy as np
import satellites
import threading



class GMSK(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "GMSK_RX", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("GMSK_RX")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "GMSK")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.samp_rate = samp_rate = 390625
        self.if_gain = if_gain = 31.5
        self.freq = freq = 437e6
        self.BT = BT = 0.5

        ##################################################
        # Blocks
        ##################################################

        self.controls = Qt.QTabWidget()
        self.controls_widget_0 = Qt.QWidget()
        self.controls_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controls_widget_0)
        self.controls_grid_layout_0 = Qt.QGridLayout()
        self.controls_layout_0.addLayout(self.controls_grid_layout_0)
        self.controls.addTab(self.controls_widget_0, 'Canal')
        self.controls_widget_1 = Qt.QWidget()
        self.controls_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controls_widget_1)
        self.controls_grid_layout_1 = Qt.QGridLayout()
        self.controls_layout_1.addLayout(self.controls_grid_layout_1)
        self.controls.addTab(self.controls_widget_1, 'Rx')
        self.top_grid_layout.addWidget(self.controls, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.transmited = Qt.QTabWidget()
        self.transmited_widget_0 = Qt.QWidget()
        self.transmited_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.transmited_widget_0)
        self.transmited_grid_layout_0 = Qt.QGridLayout()
        self.transmited_layout_0.addLayout(self.transmited_grid_layout_0)
        self.transmited.addTab(self.transmited_widget_0, 'Constellation Tx')
        self.transmited_widget_1 = Qt.QWidget()
        self.transmited_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.transmited_widget_1)
        self.transmited_grid_layout_1 = Qt.QGridLayout()
        self.transmited_layout_1.addLayout(self.transmited_grid_layout_1)
        self.transmited.addTab(self.transmited_widget_1, 'Envolvente compleja Post Canal')
        self.top_grid_layout.addWidget(self.transmited, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.satellites_nrzi_decode_0 = satellites.nrzi_decode()
        self.satellites_hdlc_deframer_0 = satellites.hdlc_deframer(check_fcs=True, max_length=10000)
        self.received = Qt.QTabWidget()
        self.received_widget_0 = Qt.QWidget()
        self.received_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.received_widget_0)
        self.received_grid_layout_0 = Qt.QGridLayout()
        self.received_layout_0.addLayout(self.received_grid_layout_0)
        self.received.addTab(self.received_widget_0, 'Constelacion Rx')
        self.top_grid_layout.addWidget(self.received, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                (1.8*(samp_rate/sps)),
                (0.2*(samp_rate/sps)),
                window.WIN_HAMMING,
                6.76))
        self._if_gain_range = qtgui.Range(0, 40, 0.01, 31.5, 200)
        self._if_gain_win = qtgui.RangeWidget(self._if_gain_range, self.set_if_gain, "'if_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.controls_grid_layout_0.addWidget(self._if_gain_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.controls_grid_layout_0.setColumnStretch(c, 1)
        self.epy_block_0 = epy_block_0.image_receiver()
        self.digital_gfsk_demod_0 = digital.gfsk_demod(
            samples_per_symbol=sps,
            sensitivity=(np.pi/sps),
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0.0,
            verbose=False,
            log=False)
        self.digital_descrambler_bb_0 = digital.descrambler_bb(0x21, 0x0, 16)
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.info)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc((-140), 1)
        self.analog_agc3_xx_0 = analog.agc3_cc((1e-3), (1e-4), 1.0, 1.0, 1, 10000)
        self._BT_range = qtgui.Range(0.0, 1, 0.01, 0.5, 200)
        self._BT_win = qtgui.RangeWidget(self._BT_range, self.set_BT, "BT", "counter_slider", float, QtCore.Qt.Horizontal)
        self.controls_grid_layout_1.addWidget(self._BT_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.controls_grid_layout_1.setColumnStretch(c, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_hdlc_deframer_0, 'out'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.satellites_hdlc_deframer_0, 'out'), (self.epy_block_0, 'msg_in'))
        self.connect((self.analog_agc3_xx_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.digital_gfsk_demod_0, 0))
        self.connect((self.digital_descrambler_bb_0, 0), (self.satellites_hdlc_deframer_0, 0))
        self.connect((self.digital_gfsk_demod_0, 0), (self.satellites_nrzi_decode_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.satellites_nrzi_decode_0, 0), (self.digital_descrambler_bb_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.analog_agc3_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "GMSK")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, (1.8*(self.samp_rate/self.sps)), (0.2*(self.samp_rate/self.sps)), window.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, (1.8*(self.samp_rate/self.sps)), (0.2*(self.samp_rate/self.sps)), window.WIN_HAMMING, 6.76))
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_BT(self):
        return self.BT

    def set_BT(self, BT):
        self.BT = BT




def main(top_block_cls=GMSK, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
