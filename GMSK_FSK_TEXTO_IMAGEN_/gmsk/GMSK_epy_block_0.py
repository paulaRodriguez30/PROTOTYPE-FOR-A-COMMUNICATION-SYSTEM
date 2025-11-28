import numpy as np
import pmt
from gnuradio import gr

class image_receiver(gr.basic_block):
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='image_receiver',
            in_sig=None,
            out_sig=None
        )
        self.message_port_register_in(pmt.intern("msg_in"))
        self.set_msg_handler(pmt.intern("msg_in"), self.handle_msg)

        self.receiving = False
        self.received = bytearray()

    def handle_msg(self, msg):
        vec = pmt.cdr(msg)
        data = bytearray(pmt.u8vector_elements(vec))

        if data == b"START":
            self.receiving = True
            self.received = bytearray()
            print("[RX] Recibiendo imagen...")

        elif data == b"END":
            if self.receiving:
                with open("/home/estudiante/Descargas/imagen_recibida.jpg", "wb") as f:
                    f.write(self.received)
                print(f"[RX] Imagen reconstruida correctamente. Total: {len(self.received)} bytes")
                self.receiving = False
            else:
                print("[RX] END recibido sin START")

        elif self.receiving:
            self.received += data
            print(f"[RX] Chunk recibido: {len(data)} bytes")
