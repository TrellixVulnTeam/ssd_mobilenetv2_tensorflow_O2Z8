import shutil
import os

# You can specify the specific extension you want to move
file_extensions = ['xml']

for root, dirs, files in os.walk(r"<Path_where_all_images_and_xml_are_stored>", topdown=True):
    for name in files:
        if name.split('.')[-1] in file_extensions:
            shutil.move(os.path.join(root, name), os.path.join(r"Path_where_you_want_all_xml_to_be_stored", name))
