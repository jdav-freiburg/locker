
import qrcode
import qrcode.image.base

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap



class QRCodePixmap(qrcode.image.base.BaseImage):
    needs_drawrect = False
    needs_processing = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def new_image(self, **_) -> QPixmap:
        total_size = self.box_size * self.width + 2 * self.border
        pixmap = QPixmap(total_size, total_size)
        pixmap.fill(Qt.GlobalColor.white)
        return pixmap

    def process(self):
        painter = QPainter(self._img)
        for r in range(self.width):
            for c in range(self.width):
                if self.modules[r][c]:
                    painter.fillRect(
                        c * self.box_size + self.border,
                        r * self.box_size + self.border,
                        self.box_size,
                        self.box_size,
                        Qt.GlobalColor.black,
                    )

    def save(self, stream, kind=None):
        pass
