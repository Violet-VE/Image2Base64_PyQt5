from Ui_Image2Base64 import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import base64


class ImageToBase64(QtWidgets.QMainWindow):
    # 全局变量

    def __init__(self):
        super(ImageToBase64, self).__init__()
        global pixMap
        global fileName
        self.initUI()
        fileName = ""
        pixMap = QtGui.QPixmap()
        # 设置信号槽
        self.openBtn.clicked.connect(self.openImage)
        self.actionOpen.triggered.connect(self.openImage)
        self.convertBtn.clicked.connect(self.convertImage)
        self.actionConverToBase64.triggered.connect(self.convertImage)

# 设置界面
    def initUI(self):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.resize(386, 277)
        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.openBtn = QtWidgets.QPushButton(self.frame)
        self.gridLayout.addWidget(self.openBtn, 1, 1, 1, 1)
        self.openBtn.setFont(font)
        self.verticalLayout_2.addWidget(self.frame)
        self.base64View = QtWidgets.QTextEdit(self.centralwidget)
        self.base64View.grabKeyboard()
        self.base64View.setMaximumHeight(71)
        self.verticalLayout_2.addWidget(self.base64View)
        self.convertBtn = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout_2.addWidget(self.convertBtn)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 386, 22))
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(self)
        self.actionConverToBase64 = QtWidgets.QAction(self)
        self.image = QtWidgets.QLabel(self.frame)
        self.gridLayout.addWidget(self.image, 1, 1, 1, 1)
        self.image.hide()
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionConverToBase64)
        self.menubar.addAction(self.menuFile.menuAction())

        self.setWindowTitle("MainWindow")
        self.openBtn.setText("打开图片或者拖动、复制均可")
        self.convertBtn.setText("开始转换")
        self.menuFile.setTitle("文件")
        self.actionOpen.setText("打开图片")
        self.actionConverToBase64.setText("转换到Base64")

# 打开图片
    def openImage(self):
        global pixMap
        global fileName
        # 打开一张图片，会返回两个值，第一个是文件名，第二个是文件类型
        fileName = QtWidgets.QFileDialog.getOpenFileName(
            None, "选取文件", "./",
            "Image Files(*.jpg *.png *.jpeg *.gif *.webp *.TIFF *.TIFF *.tga)"
        )[0]
        if fileName == '':
            return
        pixMap=QtGui.QPixmap(fileName)
        self.showPixmap(pixMap)

# 转换图片
    def convertImage(self):
        byte_array = QtCore.QByteArray()
        buffer = QtCore.QBuffer(byte_array)
        buffer.open(QtCore.QIODevice.WriteOnly)
        if fileName == '':
            print("111111111")
            if pixMap.toImage().isNull() is True:
                print("2222222")
                return
            else:
                print("3333333")
                pixMap.save(buffer, "jpg")
        else:
            print("44444")
            pixMap.save(buffer, fileName.split('.')[-1])
        ls_f = base64.b64encode(bytes(buffer.data()))
        self.base64View.setText("[base64str]:data:image/png;base64," +
                                ls_f.decode("utf-8"))

# 检测按下了ctrl+v
    def keyReleaseEvent(self, event):
        global pixMap
        if (event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_V):
            pixMap = QtGui.QGuiApplication.clipboard().pixmap()
            if (pixMap.toImage().isNull() is True):
                return
            else:
                self.showPixmap(pixMap)

    def showPixmap(self, pixmap):
        self.openBtn.hide()
        self.image.show()
        newWidth = 0
        if pixmap.width() > 320:
            newWidth = pixmap.width() / 20
            pixmap = pixmap.scaledToWidth(newWidth)
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = ImageToBase64()
    widget.show()
    sys.exit(app.exec_())
