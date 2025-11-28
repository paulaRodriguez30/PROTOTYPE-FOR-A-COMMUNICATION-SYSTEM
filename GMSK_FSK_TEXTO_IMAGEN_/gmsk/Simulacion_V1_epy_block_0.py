import numpy as np
import pmt
from gnuradio import gr

class image_sender(gr.basic_block):
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='image_sender',
            in_sig=None,
            out_sig=None
        )
        self.message_port_register_out(pmt.intern('msg_out'))

        with open("/home/estudiante/Descargas/a.jpg", "rb") as f:
            self.image_data = f.read()

        self.chunks = [self.image_data[i:i+256] for i in range(0, len(self.image_data), 256)]

    def send_chunk(self, data):
        vec = pmt.init_u8vector(len(data), list(data))
        meta = pmt.make_dict()
        pdu = pmt.cons(meta, vec)
        self.message_port_pub(pmt.intern("msg_out"), pdu)

    def start(self):
        # Enviar señal de inicio
        self.send_chunk(b"START")
        print("[TX] Enviando encabezado START")

        # Enviar imagen por chunks
        for chunk in self.chunks:
            self.send_chunk(chunk)
            print(f"[TX] Enviando chunk: {len(chunk)} bytes")

        # Enviar señal de fin
        self.send_chunk(b"END")
        print("[TX] Enviando final END")
        return True
