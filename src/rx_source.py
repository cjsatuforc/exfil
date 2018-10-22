# This module instantiates one of a number of possible
# sources of IQ data.

import rf_mgt as rfm
import zmq_utils as zmqu
from gnuradio import gr
from gnuradio import uhd
from gnuradio import zeromq

class rx_source(gr.hier_block2):

    def __init__(self,
                 rf_params,
                 tcp_test,
                 sdr_sel):
        gr.hier_block2.__init__(
            self,
            "RX Source Block",
            gr.io_signature(0, 0, 0), # no inputs
            gr.io_signature(1, 1, gr.sizeof_gr_complex * 1)  # single out
        )

        # parameters
        self.rf_params = rf_params
        self.tcp_test = tcp_test
        self.sdr_sel = sdr_sel

        # instantiate the IQ source
        ## use the ZeroMQ Pull Source for loopback connection to TX
        if self.sdr_sel == rfm.HW_TEST:
            self.src = zeromq.pull_source(
                gr.sizeof_gr_complex,
                1,
                self.tcp_test,
                100,
                False,
                -1)

        elif self.sdr_sel == rfm.HW_UHD:
            self.src = uhd.usrp_source(
                ",".join(("", "")),
                uhd.stream_args(
                        cpu_format="fc32",
                        channels=range(1),
                ),
            )
            self.src.set_antenna('TX/RX', 0)
            self.src.set_center_freq(rf_params.center_freq, 0)
            self.src.set_gain(rf_params.rx_gain, 0)
            self.src.set_samp_rate(rf_params.samp_rate)

        self.connect((self.src, 0), (self,0))
