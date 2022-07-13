# Convert csv to tf record files - To switch to a code based version so that the sys.exit dont take place.

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
from research.object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

#flags = tf.compat.v1.flags
#flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
#flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
#flags.DEFINE_string('image_dir', '', 'Path to images')
#LAGS = flags.FLAGS

# TO-DO replace this with label map

def class_text_to_int(row_label):
    if row_label == 'closedbook':
        return 0
    elif row_label == 'emptycup':
        return 1
    elif row_label == 'fullcup':
        return 2
    elif row_label == 'openbook':
        return 3
    else:
        None

def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

def create_tf_example(group, path):
    with tf.compat.v1.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))

    return tf_example

def main(_):
    output_path = os.path.join(os.getcwd(), 'train.record')
    input_path = os.path.join(os.getcwd(), 'train_labels.csv')
    writer = tf.io.TFRecordWriter(output_path)
    path = os.path.join(os.getcwd(), r'dataset\train')
    examples = pd.read_csv(input_path)
    grouped = split(examples, 'filename')
    for group in grouped:
      tf_example = create_tf_example(group, path)
      writer.write(tf_example.SerializeToString())
    writer.close()
    # output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords for train: {}'.format(output_path))

    output_path = os.path.join(os.getcwd(), 'test.record')
    input_path = os.path.join(os.getcwd(), 'test_labels.csv')
    writer = tf.io.TFRecordWriter(output_path)
    path = os.path.join(os.getcwd(), r'dataset\test')
    examples = pd.read_csv(input_path)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())
    writer.close()
    # output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords for test: {}'.format(output_path))

if __name__ == '__main__':
    tf.compat.v1.app.run()
