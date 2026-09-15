import requests

import sys
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import (QApplication , QWidget , 
                             QLabel , QLineEdit , QPushButton , QVBoxLayout)

from PyQt6.QtCore import Qt





class WeatherApp(QWidget):
    load_dotenv()
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name",self)
        self.city_input = QLineEdit(self)
        self.get_button = QPushButton("Get Weather",self)
        self.temperature_label = QLabel()
        self.emoji_label = QLabel()
        self.description_label = QLabel()
        self.initUI()

        
    def initUI(self):

        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.get_button.setObjectName("get_button")

        self.setStyleSheet("""
            QLabel,QPushButton{
            font-family:calibri;
            }
            QLabel#city_label{
            font-size:40px;
            font-style:italic;
            }
            QLineEdit#city_input{
            font-size:40px;
            }
            QPushButton#get_button{
            font-size:30px;
            font-weight:bold;
            }
            QLabel#temperature_label{
            font-size:75px;
            }
            QLabel#emoji_label{
            font-size:100px;
            font-family:Segoe UI emoji;           
            }
            QLabel#description_label{
            font-size:50px;
            font-family:Segoe UI emoji;           
            }

""")
        self.get_button.clicked.connect(self.get_weather)


    def get_weather(self):
        api_key = os.environ["OPENWEATHER_API_KEY"]
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request\n Please Check Your Input")
                case 401:
                    self.display_error("Unautorized\n Invalid API Key")
                case 403:
                        self.display_error("Forbidden\n Access is denied")
                case 404:
                        self.display_error("Not Found\n City Not Found")
                case 500:
                        self.display_error("Internal Server Error\n Please Try Again Later")
                case 502:
                        self.display_error("Bad Gateway\n Invalid response from server")
                case 503:
                        self.display_error("Service Unavailable\n Server is down")
                case 504:
                        self.display_error("Gateway Timeout\nNo response from the Server ")
                case _:
                        self.display_error(f"HTTP Error Occured {http_error}")

        except requests.exceptions.ConnectionError:
            print("Connection Error:\nCheck your Internet Connection")
        except requests.exceptions.Timeout:
            print("Timeout error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects:\nCheck the url")
        except requests.exceptions.RequestException as req_error:
            print(f"Request Error:\n{req_error}")
  
    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size:30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size:75px;")
        temperature = data["main"]["temp"]
        temp_f = (temperature * 9/5) - 459.67
        weather_id = data["weather"][0]["id"]
        self.temperature_label.setText(f"{temp_f:.0f}°F")
        weather_description = data["weather"][0]["description"]
        self.description_label.setText(weather_description)
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
    @staticmethod
    def get_weather_emoji(weather_id):

         if  200 <=  weather_id <= 232:
              return "💭"
         elif 300 <= weather_id <= 321:
              return "☁️"
         elif 500 <= weather_id <= 531:
              return "🌦️"
         elif 600 <= weather_id <= 632:
              return "❄️"
         elif 701 <= weather_id <= 741:
              return "❄️"
         elif weather_id == 762:
              return "❄️"
         elif weather_id == 771:
               return "❄️"
         elif weather_id == 781:
               return "❄️"
         elif weather_id == 781:
               return "❄️"
         elif weather_id == 800:
               return "☀️"
         elif  801 <=  weather_id <= 804:
                       return "💭"
         
          


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())