
from widgets import widgets
from PyQt4 import QtCore, QtGui


class Widget(QtGui.QWidget):

    def __init__(self, parent, config):
        super(Widget, self).__init__(parent)
        self.config = config

        # temporary coloring until display widgets get implemented
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtGui.QColor(255, 255, 255, 50))
        self.setPalette(palette)

        # make the context menu
        self.menu = QtGui.QMenu()
        self.menu.addAction(self.config.command.name).setDisabled(True)
        self.menu.addAction("Delete Widget", self.delete)

        # make the requested graphics object
        self.graphics = widgets[config.class_name](self, config)

        self.move(self.position())
        self.show()


    def sizeHint(self):
        if self.config.dimensions is not None:
            size = QtCore.QSize(self.config.dimensions['x'], self.config.dimensions['y'])
            self.graphics.setFixedSize(size)
            return size
        else:
            return self.graphics.sizeHint()


    def position(self):
        if self.config.position is not None:
            return QtCore.QPoint(self.config.position['x'], self.config.position['y'])
        else:
            return QtCore.QPoint(0, 0)


    def moveEvent(self, e):
        pos = e.pos()
        self.config.position = { 'x':pos.x(), 'y':pos.y() }
        self.config.save()


    def delete(self):
        self.parent().delete_widget(self)


    def mouseMoveEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:

            mimeData = QtCore.QMimeData()
            mimeData.setText('%d,%d' % (e.x(), e.y()))

            # show the ghost image while dragging
            pixmap = QtGui.QPixmap.grabWidget(self)
            painter = QtGui.QPainter(pixmap)
            painter.fillRect(pixmap.rect(), QtGui.QColor(0, 0, 0, 127))
            painter.end()

            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData)
            drag.setPixmap(pixmap)
            drag.setHotSpot(e.pos())

            drag.exec_(QtCore.Qt.MoveAction)


    def contextMenuEvent(self, e):
        action = self.menu.exec_(self.mapToGlobal(e.pos()))


    def get_command(self):
        return self.config.command


    def render(self, response):
        if not response.is_null():
            self.graphics.render(response.value)
