import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    xml_list = []
    classes_names = []

    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    classes_names = list(set(classes_names))
    classes_names.sort()

    return xml_df, classes_names


def main():
    xml_path = os.path.join(os.getcwd(), r'datatset/train')
    xml_df, classes = xml_to_csv(xml_path)
    # print(xml_df)
    xml_df.to_csv('train_labels.csv', index=None)
    print('Successfully converted xml to csv for train')
    xml_path = os.path.join(os.getcwd(), r'datatset/test')
    xml_df, classes = xml_to_csv(xml_path)
    # print(xml_df)
    xml_df.to_csv('test_labels.csv', index=None)
    print('Successfully converted xml to csv for test')


main()
