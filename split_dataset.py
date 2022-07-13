import os
import numpy as np

dataset_directory = r"<Path_where_all_xml_files_are_stored>"
folder = os.path.join(os.getcwd(), dataset_directory)
print("Data Directory: ", folder)

for i in range(1,4):
    # Get all the files in the given image folder
    allFileNames = os.listdir(folder)
    np.random.shuffle(allFileNames)
    test_ratio = 0.20
    train_FileNames, test_FileNames = np.split(np.array(allFileNames),
                                               [int(len(allFileNames) * (1 - test_ratio))])
    train_FileNames = [name for name in train_FileNames.tolist()]
    test_FileNames = [name for name in test_FileNames.tolist()]
    # print("train_FileNames", train_FileNames)
    # print("test_FileNames", test_FileNames)
    print("train_FileNames", len(train_FileNames))
    print("test_FileNames", len(test_FileNames))

    split_directory = r"data_splits"
    split_folder = os.path.join(os.getcwd(), split_directory)
    train_list = str(split_folder) + "\\" + "trainlist_" + str(i) + ".txt"
    file2 = open(train_list, 'a')

    for each in train_FileNames:
        file2.write(each)
        file2.write("\n")
    file2.close()

    test_list = str(split_folder) + "\\" + "testlist_" + str(i) + ".txt"
    file3 = open(test_list, 'a')

    for each in test_FileNames:
        file3.write(each)
        file3.write("\n")
    file3.close()
