import os
import sys
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(PROJECT_PATH, "..", "aus_weather_data")
print(SOURCE_PATH)
sys.path.append(SOURCE_PATH)
