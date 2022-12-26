from django.apps import AppConfig
from keras.models import load_model
import os


models = []

class MainappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mainapp"

    def ready(self):
        if 'mainapp' in os.listdir():
            model = load_model('./mainapp/DL_model/최종_MLP.hdf5')
        else:
            model = load_model('./todays/mainapp/DL_model/최종_MLP.hdf5')
        models.append(model)
        print(models[0])
        pass