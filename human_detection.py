import numpy as np
import tensorflow as tf


class HumanDetector:
    def __init__(self, model_loc='model.pb', threshold=0.7):
        self.model_loc = model_loc
        self.threshold = threshold
        self.graph = tf.Graph()
        with self.graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(self.model_loc, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.graph.as_default()
        self.session = tf.compat.v1.Session(graph=self.graph)
        self.tensor = self.graph.get_tensor_by_name('image_tensor:0')
        self.scores = self.graph.get_tensor_by_name('detection_scores:0')
        self.classes = self.graph.get_tensor_by_name('detection_classes:0')

    def is_human(self, img):
        image_np_expanded = np.expand_dims(img, axis=0)
        (scores, classes) = self.session.run([self.scores, self.classes], feed_dict={self.tensor: image_np_expanded})
        scores = scores[0].tolist()
        classes = [int(x) for x in classes[0].tolist()]

        # Filter for humans only with confidence scores > threshold
        return [scores[x] for x in range(len(scores)) if classes[x] == 1 and scores[x] > self.threshold] != []

    def close(self):
        self.session.close()
        self.default_graph.close()
