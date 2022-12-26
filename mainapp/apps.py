from django.apps import AppConfig
from keras.models import load_model

models = []

class MainappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mainapp"

    def ready(self):
        model = load_model('./todays/mainapp/DL_model/최종_MLP.hdf5') 
        models.append(model)
        print(models[0])
        pass