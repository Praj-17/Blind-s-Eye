from DataBuilder.data_builder import Data_builder
from DataBuilder.data_builder import Augmentation


person = "Gautam"
def create_training_image_folder(person, n, augment = False, augment_n = 15):
    data_builder = Data_builder(person)
    data_builder.get_images(n)
    if augment == True:
        Augmentation(f"{data_builder.path}\\",f"{data_builder.path}\\","aug",augment_n)
    print("Images Captured Sucessfully...!")
   

