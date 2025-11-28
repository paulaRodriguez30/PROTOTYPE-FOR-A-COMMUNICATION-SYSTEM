#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Transmisor GMSK
# GNU Radio version: v3.10.11.0-89-ga17f69e7

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
import Simulacion_V1_epy_block_0 as epy_block_0  # embedded python block
import osmosdr
import time
import satellites
import threading



class Simulacion_V1(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Transmisor GMSK ", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Transmisor GMSK ")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Simulacion_V1")

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
        self.samp_rate = samp_rate = 2000000
        self.gain = gain = 42
        self.freq = freq = 437e6
        self.excess_bw = excess_bw = 0.5

        ##################################################
        # Blocks
        ##################################################

        self.controls = Qt.QTabWidget()
        self.controls_widget_0 = Qt.QWidget()
        self.controls_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controls_widget_0)
        self.controls_grid_layout_0 = Qt.QGridLayout()
        self.controls_layout_0.addLayout(self.controls_grid_layout_0)
        self.controls.addTab(self.controls_widget_0, '')
        self.top_grid_layout.addWidget(self.controls, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._samp_rate_range = qtgui.Range(100000, 20000000, 1000000, 2000000, 200)
        self._samp_rate_win = qtgui.RangeWidget(self._samp_rate_range, self.set_samp_rate, "'samp_rate'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.controls_grid_layout_0.addWidget(self._samp_rate_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.controls_grid_layout_0.setColumnStretch(c, 1)
        self._freq_range = qtgui.Range(1e6, 3000e6, 10, 437e6, 200)
        self._freq_win = qtgui.RangeWidget(self._freq_range, self.set_freq, "'freq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.controls_grid_layout_0.addWidget(self._freq_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.controls_grid_layout_0.setColumnStretch(c, 1)
        self.satellites_nrzi_encode_0_0 = satellites.nrzi_encode()
        self.satellites_hdlc_framer_0_0 = satellites.hdlc_framer(preamble_bytes=100, postamble_bytes=14)
        self.pdu_pdu_to_tagged_stream_0_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.osmosdr_sink_1 = osmosdr.sink(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_sink_1.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
        self.osmosdr_sink_1.set_sample_rate(samp_rate)
        self.osmosdr_sink_1.set_center_freq(freq, 0)
        self.osmosdr_sink_1.set_freq_corr(0, 0)
        self.osmosdr_sink_1.set_gain(10, 0)
        self.osmosdr_sink_1.set_if_gain(20, 0)
        self.osmosdr_sink_1.set_bb_gain(0, 0)
        self.osmosdr_sink_1.set_antenna('', 0)
        self.osmosdr_sink_1.set_bandwidth(0, 0)
        self._gain_range = qtgui.Range(1, 45, 1, 42, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "'gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.controls_grid_layout_0.addWidget(self._gain_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.controls_grid_layout_0.setColumnStretch(c, 1)
        self.epy_block_0 = epy_block_0.image_sender()
        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x21, 0x0, 16)
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
            samples_per_symbol=4,
            bt=excess_bw,
            verbose=False,
            log=False,
            do_unpack=True)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_pack_k_bits_bb_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.5)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'msg_out'), (self.satellites_hdlc_framer_0_0, 'in'))
        self.msg_connect((self.satellites_hdlc_framer_0_0, 'out'), (self.pdu_pdu_to_tagged_stream_0_0, 'pdus'))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0, 0), (self.digital_gmsk_mod_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.osmosdr_sink_1, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_scrambler_bb_0, 0), (self.satellites_nrzi_encode_0_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0, 0), (self.digital_scrambler_bb_0, 0))
        self.connect((self.satellites_nrzi_encode_0_0, 0), (self.blocks_pack_k_bits_bb_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Simulacion_V1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.osmosdr_sink_1.set_sample_rate(self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_sink_1.set_center_freq(self.freq, 0)

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw




def main(top_block_cls=Simulacion_V1, options=None):

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
