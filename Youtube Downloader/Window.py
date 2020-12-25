import PyQt5.QtWidgets as Qt
import PyQt5.QtGui as Qg
import PyQt5.QtCore as Qc
import urllib.request
import Downloader

vid_inform = [
    "uploader",
    "title",
    "thumbnails",
    "webpage_url",
]

class Window(Qt.QWidget):
    videoOptions = []
    audioOptions = []
    window_title = "Youtube Downloader"
    width = 800
    height = 600

    def __init__(self):
        super().__init__()
        # Youtube Downloader
        self.yt_downloader = Downloader.Downloader()
        # Api Setting
        self.api_box = Qt.QHBoxLayout()
        self.api_key = Qt.QLineEdit()
        self.api_btn = Qt.QPushButton("적용")
        # Directory to download
        self.dir_box = Qt.QHBoxLayout()
        self.dir_path = Qt.QLineEdit()
        self.dir_button = Qt.QPushButton("...")
        # Search
        self.search_label = Qt.QLabel("검색어: ")
        self.search_line = Qt.QLineEdit(self)
        self.search_btn = Qt.QPushButton("Search")
        self.search_box = Qt.QHBoxLayout()
        # Download Option
        self.opt_lb = Qt.QLabel("검색 방식: ")
        self.opt_url = Qt.QRadioButton("주소")
        self.opt_word = Qt.QRadioButton("검색어")
        # Result
        self.scrollBox = Qt.QScrollArea()
        self.download_btns = []
        self.initUI()

    def initUI(self):
        self.scrollBox.setFixedHeight(400)
        self.apiArea()
        self.dirArea()
        self.searchArea()
        self.makeLayout()
        self.createWindow()

    def createWindow(self):
        self.setWindowTitle(self.window_title)
        self.resize(self.width, self.height)
        self.setWindowToCenter()
        self.show()

    def setWindowToCenter(self):
        window_inform = self.frameGeometry()
        center_monitor = Qt.QDesktopWidget().availableGeometry().center()
        window_inform.moveCenter(center_monitor)
        self.move(window_inform.topLeft())

    def makeLayout(self):
        vbox = Qt.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(self.api_box)
        vbox.addLayout(self.dir_box)
        vbox.addLayout(self.search_box)
        vbox.addWidget(self.scrollBox)
        vbox.addStretch(1)
        self.setLayout(vbox)

    def apiArea(self):
        self.api_btn.clicked.connect(lambda : self.applyApi(self.api_key.text()))
        self.api_box.addWidget(self.api_key)
        self.api_box.addWidget(self.api_btn)

    def applyApi(self, key):
        if not self.yt_downloader.setBuildEnv(key):
            msgbox = Qt.QMessageBox()
            msgbox.critical(self, 'Api Error', 'This is unavailable api key')

    def dirArea(self):
        self.dir_button.clicked.connect(self.openDir)
        dir_lb = Qt.QLabel("Download Path: ")
        self.dir_box.addWidget(dir_lb)
        self.dir_box.addWidget(self.dir_path)
        self.dir_box.addWidget(self.dir_button)

    def openDir(self):
        path = Qt.QFileDialog.getExistingDirectory()
        self.dir_path.setText(path)

    def searchArea(self):
        self.search_btn.pressed.connect(lambda : self.setResultArea(self.search_line.text()))
        self.opt_url.setChecked(True)

        self.search_box.addStretch(1)
        self.search_box.addWidget(self.search_label)
        self.search_box.addWidget(self.search_line)
        self.search_box.addWidget(self.search_btn)
        self.search_box.addWidget(self.opt_lb)
        self.search_box.addWidget(self.opt_url)
        self.search_box.addWidget(self.opt_word)
        self.search_box.addStretch(1)

    def setResultArea(self, url):
        vid_list = self.getVidsList(url)
        # List Area
        list_box = Qt.QVBoxLayout()

        for vids in vid_list:
            # Video Area
            vid_box = Qt.QHBoxLayout()
            vid_box.addStretch(1)
            # Video's Detail Area
            detail_box = Qt.QVBoxLayout()
            detail_box.setContentsMargins(35, 0, 0, 0)
            download_btn = Qt.QPushButton("Download", self)
            for vid_key, vid_val in vids.items():
                lb = Qt.QLabel()
                if vid_key == 'thumbnails':
                    imageFromWeb = urllib.request.urlopen(vid_val[0]['url']).read()
                    thumbnail = Qg.QPixmap()
                    thumbnail.loadFromData(imageFromWeb)
                    lb.setPixmap(thumbnail)
                    vid_box.addWidget(lb)
                elif vid_key == 'webpage_url':
                    lb.setText("<a href='" + str(vid_val) + "'>Go To Webpage</a>")
                    lb.setOpenExternalLinks(True)
                    download_btn.pressed.connect(lambda : self.yt_downloader.downloadVid(str(vid_val), True, self.dir_path.text()))
                    self.download_btns.append(download_btn)
                    detail_box.addWidget(lb)
                else:
                    lb.setText(vid_key + ": " + str(vid_val))
                    detail_box.addWidget(lb)
            vid_box.addLayout(detail_box)
            vid_box.addWidget(download_btn)
            vid_box.addStretch(1)
            list_box.addLayout(vid_box)

        if len(vid_list) == 0:
            lb = Qt.QLabel("There is no video.")
            list_box.addWidget(lb)

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(list_box)
        self.scrollBox.setWidget(scroll_widget)
        self.scrollBox.setAlignment(Qc.Qt.AlignHCenter)

    def getVidsList(self, url):
        vid_list = []
        log = open("Error_Logs.txt", 'w', encoding='UTF8')
        try:
            vid = {}
            vid_informs = self.yt_downloader.downloadVid(url)
            for key, val in vid_informs.items():
                if key in vid_inform:
                    vid[key] = val
            vid_list.append(vid)
        except:
            print("There is Error in " + url, file=log)
        log.close()
        return vid_list