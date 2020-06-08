import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from countryInfo import countrylist, countryconvert
from weatherData import data_week, data_now
import datetime


class MainWindow(QMainWindow):

    font = QFont()
    font.setFamily("Arial")
    font.setPointSize(48)

    def __init__(self):
        super().__init__()
        self.UISetup()

    def UISetup(self):
        self.setWindowTitle("The Weather Hub")
        self.resize(800, 600)
        self.setLayoutDirection(Qt.LeftToRight)
        self.setStyleSheet("background-color: rgb(215, 65, 2)")

        mainLogo = QLabel("", self)
        mainLogo.setGeometry(QRect(60, 20, 241, 281))
        mainLogo.setPixmap(QPixmap("Images/weatherLogo.png"))

        welcomeLabel = QLabel(self)
        welcomeLabel.setGeometry(QRect(350, 40, 391, 121))
        welcomeLabel.setFont(self.font)
        welcomeLabel.setText("The Weather Hub")

        APILabel = QLabel("Powered by the OpenWeatherMap API", self)
        APILabel.setGeometry(QRect(420, 140, 241, 16))

        dataSubmit = QPushButton("Submit", self)
        dataSubmit.setGeometry(QRect(502, 320, 121, 32))
        dataSubmit.setStyleSheet("border-radius: -40px\n")
        dataSubmit.clicked.connect(self.dataCheck)

        self.countryEntry = QComboBox(self)
        self.countryEntry.addItems(countrylist())
        self.countryEntry.setGeometry(QRect(580, 240, 191, 31))
        self.countryEntry.setStyleSheet("background-color: rgb(255,255,255)")

        self.cityEntry = QLineEdit(self)
        self.cityEntry.setGeometry(QRect(350, 240, 191, 31))
        self.cityEntry.setStyleSheet("background-color: rgb(255,255,255)")

        entryAidCity = QLabel("City:", self)
        entryAidCity.setGeometry(QRect(350, 220, 60, 16))
        entryAidCity.setObjectName("entryAidCity")

        entryAidCountry = QLabel("Country", self)
        entryAidCountry.setGeometry(QRect(580, 220, 60, 16))
        entryAidCountry.setObjectName("entryAidCountry")

        creditLabel = QLabel("Created by Varun Patel on June 5th, 2020", self)
        creditLabel.setGeometry(QRect(50, 530, 261, 16))

        self.show()

    def dataCheck(self):
        if data_now(self.cityEntry.text(), self.countryEntry.currentText()[:2]) != "City Not Found":
            self.page = DataWindow(self.cityEntry.text(), self.countryEntry.currentText()[:2])
            self.page.show()
            self.close()
        else:
            self.page = ErrorWindow()
            self.page.show()
            self.close()


class ErrorWindow(QDialog):

    font = QFont()
    font.setFamily("Arial")
    font.setPointSize(48)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.UISetup()

    def UISetup(self):
        self.setWindowTitle("The Weather Hub")
        self.resize(800, 600)
        self.setStyleSheet("background-color: rgb(215, 65, 2)")

        noData = QLabel("No Weather Data Found", self)
        noData.setGeometry(QRect(150, 20, 611, 171))
        noData.setFont(self.font)

        self.returnHome = QPushButton("Return Home", self)
        self.returnHome.setGeometry(QRect(360, 230, 113, 32))
        self.returnHome.clicked.connect(self.homePage)

    def homePage(self):
        self.page = MainWindow()
        self.page.show()
        self.close()


class DataWindow(QDialog):

    font = QFont()
    font.setFamily("Arial")
    font.setPointSize(31)

    def __init__(self, city, country, parent=None):
        super().__init__(parent)
        self.city = city
        self.country = country
        self.UISetup()
        self.updateUI()

    def UISetup(self):
        self.setWindowTitle("The Weather Hub")
        self.resize(800, 600)
        self.setStyleSheet("background-color: rgb(215, 65, 2)")

        topSeperator = QFrame(self)
        topSeperator.setGeometry(QRect(0, 90, 800, 16))
        topSeperator.setStyleSheet("background-color: rgb(0, 0, 0)")
        topSeperator.setFrameShadow(QFrame.Raised)
        topSeperator.setLineWidth(1)
        topSeperator.setFrameShape(QFrame.HLine)

        bottomSeperator = QFrame(self)
        bottomSeperator.setGeometry(QRect(0, 350, 800, 16))
        bottomSeperator.setStyleSheet("background-color: rgb(0,0,0)")
        bottomSeperator.setFrameShadow(QFrame.Raised)
        bottomSeperator.setLineWidth(1)
        bottomSeperator.setFrameShape(QFrame.HLine)

        self.homeButton = QPushButton("Return Home", self)
        self.homeButton.setGeometry(QRect(670, 40, 113, 32))
        self.homeButton.clicked.connect(self.homePage)

        self.locationLabel = QLabel(self)
        self.locationLabel.setGeometry(QRect(10, 10, 781, 16))
        self.locationLabel.setAlignment(Qt.AlignCenter)

        self.font.setPointSize(31)
        dateLabel = QLabel(f'{datetime.datetime.now().strftime("%A, %B %d, %Y")}', self)
        dateLabel.setGeometry(QRect(110, 30, 431, 51))
        dateLabel.setFont(self.font)
        dateLabel.setAlignment(Qt.AlignCenter)

        self.timeLabel = QLabel(f'{datetime.datetime.now().strftime("%H:%M")}', self)
        self.timeLabel.setGeometry(QRect(520, 30, 131, 51))
        self.timeLabel.setFont(self.font)
        self.timeLabel.setAlignment(Qt.AlignCenter)

        localTimeLabel = QLabel("Time at CURRENT Location:", self)
        localTimeLabel.setGeometry(QRect(20, 30, 91, 51))
        localTimeLabel.setWordWrap(True)

        self.currentTemp = QLabel(self)
        self.currentTemp.setGeometry(QRect(20, 140, 291, 181))
        self.font.setPointSize(60)
        self.currentTemp.setFont(self.font)
        self.currentTemp.setAlignment(Qt.AlignCenter)

        self.mainWeatherIcon = QLabel(self)
        self.mainWeatherIcon.setGeometry(QRect(340, 160, 111, 100))
        self.mainWeatherIcon.setAlignment(Qt.AlignCenter)

        self.mainWeatherDescription = QLabel(self)
        self.mainWeatherDescription.setGeometry(QRect(340, 240, 121, 71))
        self.mainWeatherDescription.setAlignment(Qt.AlignCenter)
        self.mainWeatherDescription.setWordWrap(True)

        self.currentWeather1 = QLabel(self)
        self.currentWeather1.setGeometry(QRect(500, 140, 141, 181))
        self.currentWeather1.setAlignment(Qt.AlignLeft)

        self.currentWeather2 = QLabel(self)
        self.currentWeather2.setGeometry(QRect(630, 140, 141, 181))
        self.currentWeather2.setAlignment(Qt.AlignCenter)

        self.pic1 = QLabel(self)
        self.pic1.setGeometry(QRect(40, 380, 61, 41))
        self.pic1.setAlignment(Qt.AlignCenter)

        self.pic2 = QLabel(self)
        self.pic2.setGeometry(QRect(200, 380, 61, 41))
        self.pic2.setAlignment(Qt.AlignCenter)

        self.pic3 = QLabel(self)
        self.pic3.setGeometry(QRect(370, 380, 61, 41))
        self.pic3.setAlignment(Qt.AlignCenter)

        self.pic4 = QLabel(self)
        self.pic4.setGeometry(QRect(540, 380, 61, 41))
        self.pic4.setAlignment(Qt.AlignCenter)

        self.pic5 = QLabel(self)
        self.pic5.setGeometry(QRect(690, 380, 61, 41))
        self.pic5.setAlignment(Qt.AlignCenter)

        self.day1 = QLabel(self)
        self.day1.setGeometry(QRect(30, 440, 81, 31))
        self.day1.setAlignment(Qt.AlignCenter)

        self.day2 = QLabel(self)
        self.day2.setGeometry(QRect(190, 440, 81, 31))
        self.day2.setAlignment(Qt.AlignCenter)

        self.day3 = QLabel(self)
        self.day3.setGeometry(QRect(360, 440, 81, 31))
        self.day3.setAlignment(Qt.AlignCenter)

        self.day4 = QLabel(self)
        self.day4.setGeometry(QRect(530, 440, 81, 31))
        self.day4.setAlignment(Qt.AlignCenter)

        self.day5 = QLabel(self)
        self.day5.setGeometry(QRect(680, 440, 81, 31))
        self.day5.setAlignment(Qt.AlignCenter)

        self.day1Info = QLabel(self)
        self.day1Info.setGeometry(QRect(30, 500, 100, 100))
        self.day1Info.setAlignment(Qt.AlignCenter)

        self.day2Info = QLabel(self)
        self.day2Info.setGeometry(QRect(190, 500, 100, 100))
        self.day2Info.setAlignment(Qt.AlignCenter)

        self.day3Info = QLabel(self)
        self.day3Info.setGeometry(QRect(360, 500, 100, 100))
        self.day3Info.setAlignment(Qt.AlignCenter)

        self.day4Info = QLabel(self)
        self.day4Info.setGeometry(QRect(540, 500, 100, 100))
        self.day4Info.setAlignment(Qt.AlignCenter)

        self.day5Info = QLabel(self)
        self.day5Info.setGeometry(QRect(680, 500, 100, 100))
        self.day5Info.setAlignment(Qt.AlignCenter)

        self.days = [self.day1, self.day2, self.day3, self.day4, self.day5]
        self.daysInfo = [self.day1Info, self.day2Info, self.day3Info, self.day4Info, self.day5Info]
        self.daysPics = [self.pic1, self.pic2, self.pic3, self.pic4, self.pic5]

    def updateUI(self):
        datasetCurrent = data_now(self.city, self.country)
        datasetWeek = data_week(self.city, self.country)

        self.locationLabel.setText(f"Showing Weather Data for {self.city.lower().title()}, {countryconvert(self.country)}")
        self.currentTemp.setText(f"{datasetCurrent['temp']}ºF")
        self.mainWeatherIcon.setPixmap(QPixmap(f"Images/{datasetCurrent['icon']}@2x.png"))
        self.mainWeatherDescription.setText(f"{datasetCurrent['description'].lower().title()}")

        table1 = ["feels_like", "temp_max", "temp_min", "wind_speed"]
        table2 = ["humidity", "sunrise", "sunset", "pressure"]
        message1 = ""
        message2 = ""
        for key in table1:
            message1 += f"- {key.replace('_', ' ').title()}: {datasetCurrent[key]}\n\n\n"
        for key in table2:
            message2 += f"- {key.title()}: {datasetCurrent[key]}\n\n\n"
        self.font.setPointSize(14)
        self.currentWeather1.setFont(self.font)
        self.currentWeather1.setText(message1)
        self.currentWeather2.setFont(self.font)
        self.currentWeather2.setText(message2)

        table3 = ["temp_max", "temp_min", "humidity"]
        for i in range(0, 5):
            self.days[i].setText(list(datasetWeek.keys())[i])
            self.daysPics[i].setPixmap(QPixmap(f"Images/{datasetWeek[list(datasetWeek.keys())[i]]['icon']}@2x.png"))

            message3 = ""
            for key in table3:
                message3 += f"{key.replace('_', ' ').title()}: {datasetWeek[list(datasetWeek.keys())[i]][key]}\n"
                self.daysInfo[i].setText(message3)

    def homePage(self):
        self.page = MainWindow()
        self.page.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


