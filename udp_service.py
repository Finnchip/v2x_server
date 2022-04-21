import threading
import socket
import time
import asn1tools
import sys

import util.const as const

class UdpService():

    def __init__(self):
        # Create socket for IPv6 UDP connection
        self.s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        # Bind any address to port 37008
        self.s.bind(("::", 37008))

        # Use asn specification to decode uper strings
        self.foo = asn1tools.compile_files("rsc/etsi_mapem_spatem.asn", 'uper')

        self.map_responses = []
        self.spat_responses = []

    def _handle_mapem(self, data):
        print('decode map')

        decoded = False
        try:
            # Use asn sequence 'MAPEM' with asn1tools to decode the bytestring after the MAPEM identifier
            decoded = self.foo.decode(
                'MAPEM', data[data.index(const.MAPEM_IDENTIFIER):])
        except Exception as error:
            # TODO: Error handling
            pass

        if decoded:
            if self.map_responses is None:
                self.map_responses.append(decoded)
                print("map added")
            else:
                for map in self.map_responses:
                    if decoded['header']['stationID'] == map['header']['stationID']:
                        print("map not added")
                        return
                        self.map_responses.append(decoded)
                        print("map added")

    def _handle_spatem(self, data):
        print('decode spat')
        # TODO: Decode header first?

        decoded = False
        try:
            # Use asn sequence 'SPATEM' with asn1tools to decode the bytestring after the SPATEM identifier
            decoded = self.foo.decode(
                'SPATEM', data[data.index(const.SPATEM_IDENTIFIER):])
        except Exception as error:
            pass

        if decoded:
            # TODO: implement generic decoding for all intersections
            if str(decoded['spat']['intersections'][0]['id']['id']) == str(309):

                if self.spat_responses:
                    self.spat_responses[0] = decoded
                    print("309 spat replaced")
                else:
                    self.spat_responses.append(decoded)
                    print("309 spat added")

    def resolve_udp_packets(self):

        try:
            mode = sys.argv[1]
        except IndexError:
            mode = "live"
        
        if mode == 'debug':
            datalist = []
            datalist.append(
                        b'\x01\x00\x00\x12\xf0\x01\x00\xf1\x04\x00\x00\x00\x87\n\x01\xc3\n\x01\xc8\x0c\x01\x0c\x11\x01\x00\xf2H\x00\x00H\x00\x02\x00\x00@\x00\x00\x04\xe5H\x008\x00\x02\x00\xdd\x02L\xe2\x00\x00@Q\x00\x00\x00\x00\n\x01\x86\xff\x90\xff4\xff4\xff\x11\x02\x00\x00\xad8\xac\xa4\x93\xcf\x05\x00\xa5\x02\x0c\x17M\xa7Y\xff\xf2\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x88\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\rA\x12\x19\xd4\xff\xff\xff\xff\xff\xff\xd0\xad!\x00\xaa\xaa\x03\x00\x00\x00\x89G\x11\x00\x1a\n @\x03\x00\x02G\n\x00V \x00\x00<\x00\x00\rA\x12\x19\xd4\x03\x19\x7f\x14\x1cg\x92S\x05\xa6\xd2\xa9\x80\x00\x00\x00\x1cg\x92S\x05\xa6\xd2\xa9\x03\xe8\x00\x00\x00\x00\x00\x00\x07\xd3\x07\xd3\x02\x05\x00\x12\x19\xd4\x08\x00\x03\x02\xcc\xa7\x05\x9b\x070\x03\x10\x13P&\x90c\xe3\x83\x87\x85Y0\x06\x08\x18j\x00\x00\x05(X\x90(P\x00\x00\x00\x15\x97\xb2\x1eH\x00$=\xe9\xbdq\x1d\xf3\xd2\x92\x88\x00@TT\x02\x04\xa2\x01\x102@\xb1@\x00\x00\x00\x96[\xa9\x18 \x00\x90\xf5\x86\xe9\x12\x04\xd4\xca\x00 \xcc*\xcf\xc1P\xa8\x10"\x85D\x81D\x03\x04\x80\x00\x00\x01\x19^\'LB\xe2\xdar\x19c\x99\xb4h\xc8"\xc0\x01\x00\x00\x00P\xb4?\xda \rT\x07TU\x052\x85\x03\x1a2\x88\xb0\x00@\x00\x00\x14I\xfbf\x80\x02\x08R\x90\x052\x05\x03\x92\n\x12\x00\x00\x00\x00\xb6\xee\xef\xd9\x00\x04\x91\xd4\xfb\xd4J\x0c\x03\x08QP\x18J\x8a\x84\xc2\x84\x05H\x80\x00\x00\x00\x1b\xbcw\x98H\xf9~=4\xc8"`\x00\x80\x00\x00-\x9cZ\xb4D\x01\x96\x80p\xc6@\xac\x90\xb0\xb3L\x92&\x00\x08\x00\x00\x02\xe0\x17\xa4\xb4@\x19h\x18s\xc8\n\xc8\x0b\x0c4\xca"`\x01\x00\x00\x00\r\x97\xfb\xcc\x04\x9d\xa0\x82\x8b\x02\x03L2\xc8\x98\x00@\x00\x00\x03\x7f~Y@\xf4Q\x04\x83\xc6\x80\x00\x00\x01\xab\x0e\xfdQ\x00\x04zr\x97\x1a\xb9zu\x10\x01\x05\xaew(,\xcb\xd6\xc1P\xa8 r\x83\x01\x03\xc9\x07\xcd\x00\x00\x00\x01V+pJ\x00\x08\xf4\xb1.!r\xf5\x90\x8a\x8a\x81D\x14T," @d\x00\x00\x00\x18\xb2K:\x87\xab9\x93\x0b\xc4\xa9\xecZ\xf1o\xe2\xcc>\x1c4\x833`\x00\x80\x00\x00.)\x18\xa4D\x01\xad\x01\x03b\xc0\xa8@\xc1#HC6\x00\x08\x00\x00\x02jOTD\x01\xad\x00\xfb\x9e \xa80\xc12B\x84@\x00\x00\x00\x94\xb8\xc7~\x80\x02G%\xca\x80C\x048\xa0\x02\n?D\xacT*\x0c(\xa1QARB\x94@\x00\x00\x00T\x8a$\x1a\x80\x02GX\xcd\xed\x0c+\x16\xe2\xa0\xc0qe\x06\n\x8b\x88\x15!\x00\x00\x00\x02#*#r9\xd0j\x00\xde\x02^\xf3H\xd4F\x00\x08\x00\x00\x02T\xa0\xeeD\x01\x99\x01h= \xa8\xe0\xd1\x83H\xe4F\x00\x08\x00\x00\x02\x8bAe\x11\x00f@\x14\xf2(*44d\xd0\xad\x11\x80\x04\x00\x00\x00&\x8d;P;\xe9\x08+,$h\xc0\xb1\x11\x80\x04\x00\x00\x00"\x8dk\x00?\x0b`\x9e\xb0\xe9W')
            datalist.append(
                        b'\x01\x00\x00\x12\xf0\x01\x00\xf1\x04\x00\x00\x00,\n\x01\xc1\n\x01\xc8\x0c\x01\x0c\x11\x01\x00\xf2H\x00\x00H\x00\x02\x00\x00@\x00\x00\x04\xe5H\x008\x00\x02\x00\xd1\x01\xcf\xe1\x00\x00a\xf0\x00\x00\x00\x00\n\x01\x82\xff\x90\xff4\xff4\xff\xef,\x00\x00r\xf7\x91\xa4\x93\xcf\x05\x00\x99\x01\x0c\x17\xa57\x95\xe0\xee\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x88\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\rA\x12\x19\xd4\xff\xff\xff\xff\xff\xff\xa0\xac!\x00\xaa\xaa\x03\x00\x00\x00\x89G\x11\x00\x1a\x01 P\x03\x00\x01K\x01\x00<\x00\x00\rA\x12\x19\xd4\x03\x19x[\x1cg\x92S\x05\xa6\xd2\xa9\x80\x00\x00\x00\x00\x00\x00\x00\x07\xd4\x07\xd4\x02\x04\x00\x12\x19\xd4F\xa6c\x01\x88\x01\x88\t\xa8\x10 \x06\xa6c\xc6\xe6\x1d\x00\x10CrYBk\x12b(\x00\x10!\xb9,\xa1/q.\x08\x80\x0c\x11\\\x95L\x97\xb8\x96\x82\x00\x08\x08nK\xf0L\x9aLEP\x05\x047%\x94%\xee%\xc1\x10\x03\x02+\x92\xca\x12\xf7\x12\xe0\x88\x01\xc1\r\xc9T\xc9{\x89h \x01\x00\x8a\xe4\xaad\xbd\xc4\xb4\x10\x00\x90ErYB^\xe2\\\x11\x00P!\xb9315\x894^\x00,\x10\xdc\x97\xe0\x994\x98\x8a\xa0\x18\x08\xaeK(K\xdcK\x82 \r\x047%\x94&\xb1&"\x80\x07\x02\x0b\x92\xca\x13X\x93\x11@\x03\xc1%\xc9T\xc9{\x89h \x02\x00\x82\xe4\xbf\x04\xc9\xa4\xc4U\x01\x10ArU2^\xe2Z\x08\x00\x90 \xb9*\x99/q-\x04\x00L\x10\\\x95L\x97\xb8\x96\x82\x00(\x08.J\xa6K\xdcKA\x00\x15\x04\x17%S%\xee%\xa0\x80\x0b\x02\x0b\x92\xa9\x92\xf7\x12\xd0@\x05\xc1\x05\xc9\x99\x89\xacI\xa2\xf0\x03\x00\x82\xe4\xcc\xc4\xd6$\xd1x\x01\x90Ar_\x82d\xd2b*\x80\xd0 \xb9/\xc12i1\x15@l\x10\\\x95L\x97\xb8\x96\x82\x008\x08.J\xa6K\xdcKA\x00\x1d\x04\x17%\x94&\xb1&"\x80\x0f\x02\x0b\x92\xca\x13X\x93\x11@\xa3\xab\xbe\'')
            datalist.append(
                        b'\x01\x00\x00\x12\xf0\x01\x00\xf1\x04\x00\x00\x03;\n\x01\xc4\n\x01\xc8\x0c\x01\x0c\x11\x01\x00\xf2H\x00\x00H\x00\x02\x00\x00@\x00\x00\x04\xe5H\x008\x00\x02\x00\xcd\x01\x02\xe6\x00\x00\x85\'\x00\x00\x00\x00\n\x01\x88\xff\x90\xff4\xff4\xff\x9c,\x00\x00\xa0\x04q\xa5\x93\xcf\x05\x00\x95\x01\x0c\x17K\x9f\xf8\xe5\xf8\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x88\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\rA\x12\x19\xd4\xff\xff\xff\xff\xff\xff\xa0\xb6!\x00\xaa\xaa\x03\x00\x00\x00\x89G\x11\x00\x1a\x01 P\x03\x00\x01G\x01\x00<\x00\x00\rA\x12\x19\xd4\x03\x19\xb1c\x1cg\x92S\x05\xa6\xd2\xa9\x80\x00\x00\x00\x00\x00\x00\x00\x07\xd4\x07\xd4\x02\x04\x00\x12\x19\xd4F\xa6d\x01\x88\x01\x88\t\xa8\x10 \x06\xa6d\x17\x1c\x1d\x00\x10CrY\xe2k\x12bx\x00\x10!\xb9,\xf1/q.0\x00\x0c\x10\xdc\x99\x98\x9a\xc4\x9a.\xc0\x08\x08nK\xf0L\x9aLE0\x05\x047%\x9e%\xee%\xc6\x00\x03\x02+\x92\xcf\x12\xf7\x12\xe3\x00\x01\xc1\x0c\th\xc0\x10\x08nL\xccMbM\x17`\t\x04W%\x9e%\xee%\xc6\x00\x05\x02\x1b\x933\x13X\x93E\xd8\x02\xc1\r\xc9~\t\x93I\x88\xa6\x01\x80\x86\xe4\xb3\xc4\xbd\xc4\xb8\xc0\x00\xd0CrY\xe2k\x12bx\x00p \xb9,\xf15\x891<\x00<\x10\\\x99\x98\x9a\xc4\x9a.\xc0 \x08.K\xf0L\x9aLE0\x11\x04\x17%\x9e%\xee%\xc6\x00\t\x02\x0b\x92\xcf\x12\xf7\x12\xe3\x00\x04\xc1\x05\xc9g\x89{\x89q\x80\x02\x80\x82\xe4\xb3\xc4\xbd\xc4\xb8\xc0\x01PArY\xe2^\xe2\\`\x00\xb0 \xb9,\xf1/q.0\x00\\\x10\\\x99\x98\x9a\xc4\x9a.\xc00\x08.L\xccMbM\x17`\x19\x04\x17%\xf8&M&"\x98\r\x02\x0b\x92\xfc\x13&\x93\x11L\x06\xc1\x05\xc9g\x89{\x89q\x80\x03\x80\x82\xe4\xb3\xc4\xbd\xc4\xb8\xc0\x01\xd0ArY\xe2k\x12bx\x00\xf0 \xb9,\xf15\x891<\x00h\x9f$P')

            for data in datalist:
                # TODO: Use ItsPduHeader to identify message type
                if const.MAPEM_IDENTIFIER in data:
                    with threading.Lock():
                    self._handle_mapem(data)
                if const.SPATEM_IDENTIFIER in data:
                    with threading.Lock():
                        self._handle_spatem(data)

        if mode == 'live':
            while True:
                time.sleep(.1)
                data, addr = self.s.recvfrom(4096)

                # TODO: Use ItsPduHeader to identify message type
                if const.MAPEM_IDENTIFIER in data:
                    with threading.Lock():
                        self._handle_mapem(data)
                if const.SPATEM_IDENTIFIER in data:
                    with threading.Lock():
                        self._handle_spatem(data)
