from fastapi import FastAPI

from settings import Settings
from api import create_api
from data_manager import DataManager

app = FastAPI()
settings = Settings()
data_manager = DataManager(settings)

create_api(app, settings, data_manager)


# Run by using fastapi dev in the python env terminal
if __name__ == '__main__':
    print('Henlo')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
