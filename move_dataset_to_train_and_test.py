import shutil
import os

source_xml = os.path.join(os.getcwd(), r'path_where_all_xml_are_stored')
source_image = os.path.join(os.getcwd(), r'<path_where_all_images_are_stored')

if not os.path.exists(r'dataset\train'):
    os.makedirs(r'dataset\train')

if not os.path.exists(r'dataset\test'):
    os.makedirs(r'dataset\test')

dest_train = os.path.join(os.getcwd(), r'dataset\train')
dest_test = os.path.join(os.getcwd(), r'dataset\test')

trainlist = os.path.join(os.getcwd(), r'data_splits\trainlist_1.txt')
file1 = open(trainlist, 'r')
Lines = file1.readlines()
for line in Lines:
    line = line.strip("\n")
    shutil.copy(os.path.join(source_xml, line), os.path.join(dest_train, line))
    shutil.copy(os.path.join(source_image, line.replace(".xml",".bmp")), os.path.join(dest_train, line.replace(".xml",".bmp")))

trainlist = os.path.join(os.getcwd(), r'data_splits\testlist_1.txt')
file1 = open(trainlist, 'r')
Lines = file1.readlines()
for line in Lines:
    line = line.strip("\n")
    shutil.copy(os.path.join(source_xml, line), os.path.join(dest_test, line))
    shutil.copy(os.path.join(source_image, line.replace(".xml",".bmp")), os.path.join(dest_test, line.replace(".xml",".bmp")))
