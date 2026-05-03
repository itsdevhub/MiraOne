import asyncio

from qasync import asyncSlot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QByteArray

import client.api


class main_window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Mira One')

        self.label = QLabel('System ready')
        self.image_label = QLabel()
        self.btn_start = QPushButton('Start Controller')
        self.btn_stop = QPushButton('Stop Controller')
        self.btn_start_stream = QPushButton('Start Vision Stream')
        self.btn_stop_stream = QPushButton('Stop Vision Stream')

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_stop)
        layout.addWidget(self.btn_start_stream)
        layout.addWidget(self.btn_stop_stream)
        self.setLayout(layout)

        self.btn_start.clicked.connect(self.on_start)
        self.btn_stop.clicked.connect(self.on_stop)
        self.btn_start_stream.clicked.connect(self.on_start_stream)
        self.btn_stop_stream.clicked.connect(self.on_stop_stream)

        self._stream_task = None

    @asyncSlot()
    async def on_start(self):
        res = await client.api.start_controller()
        if res:
            self.label.setText(str({'status': 'starting controller'}))
        else:
            self.label.setText(str({'status': 'controller already running'}))

    @asyncSlot()
    async def on_stop(self):
        res = await client.api.stop_controller()
        if res:
            self.label.setText(str({'status': 'stopping controller'}))
        else:
            self.label.setText(str({'status': 'controller already stopped'}))

        # Stop stream also
        self.on_stop_stream()

    @asyncSlot()
    async def on_start_stream(self):
        if self._stream_task and not self._stream_task.done():
            self.label.setText("Stream already running")
            return

        async def stream():
            try:
                async for frame_bytes in client.api.vision_stream():
                    pixmap = QPixmap()
                    pixmap.loadFromData(QByteArray(frame_bytes))
                    self.image_label.setPixmap(pixmap)
            except Exception as e:
                self.label.setText(f"Stream error: {e}")

        self._stream_task = asyncio.create_task(stream())
        self.label.setText("Vision stream started")

    @asyncSlot()
    async def on_stop_stream(self):
        if self._stream_task:
            self._stream_task.cancel()
            self._stream_task = None
            self.label.setText('Vision stream stopped')
