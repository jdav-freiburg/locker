
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import NoCardException, CardRequestTimeoutException, NoReadersException, \
    CardConnectionException
from smartcard.System import readers
from smartcard.util import toHexString, PACK

from PyQt5.QtCore import pyqtSignal, QThread

from widgets.base import exc

CMD_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]


class NFCReader(QThread):
    read_card = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        avail_readers = readers()
        if len(avail_readers) == 0:
            #raise RuntimeError("Couldn't find any readers")
            pass
        print(f"Found the following readers: {avail_readers}")

        self.running: bool = True

    @exc
    def run(self):
        last_uid: str = ""
        print("Card reader running")
        while self.running:
            try:
                request = CardRequest(timeout=1, cardType=AnyCardType())
                cardservice = request.waitforcard()
                cardservice.connection.connect()
                data, sw1, sw2 = cardservice.connection.transmit(CMD_UID)
                if sw1 != 0x90 or sw2 != 0:
                    raise ValueError(f"The requested command returned an error code: {sw1}, {sw2}")
                data_str = toHexString(data, PACK)
                if data_str == last_uid:
                    continue
                else:
                    print(f"Read card {data_str}", flush=True)
                    self.read_card.emit(data_str)
                    last_uid = data_str
                cardservice.connection.disconnect()
            except NoReadersException:
                pass
            except (NoCardException, CardRequestTimeoutException):
                # print("no card found, trying again")
                last_uid = ""
            except CardConnectionException as ex:
                print(f"Couldn't connect to card: {ex}")
            except ValueError as ex:
                print(f"One excecuted command failed:{ex}")
