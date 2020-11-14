import json

import pandas as pd
import numpy as np
import tensorflow as tf

TEST_JSON = "tests/PROCESSED_LABELSET/test_set1_frame.json"

with open(TEST_JSON) as data_file:
  data = json.load(data_file)
  df = pd.json_normalize(data['points'])

test = []
for lp in df['lane_points']:
  test.append(lp)
  
bt = tf.ragged.constant(test)

label = df.pop('label')


ft = tf.data.Dataset.from_tensor_slices(bt)
lt = tf.data.Dataset.from_tensor_slices(label.values)

print(bt)


# #dataset = tf.data.Dataset.from_tensor_slices((bt, label.values))

#for feat, labl in dataset.take(5):
#  print("Features: {}, Label: {}".format(feat, labl))