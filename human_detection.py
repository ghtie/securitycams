import numpy as np
import tensorflow as tf


class HumanDetector:
    def __init__(self, model_loc='model.pb', threshold=0.7):
        # Load the human detection model
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

        # Get the classification, confidence scores, and detection boxes
        self.tensor = self.graph.get_tensor_by_name('image_tensor:0')
        self.scores = self.graph.get_tensor_by_name('detection_scores:0')
        self.classes = self.graph.get_tensor_by_name('detection_classes:0')
        self.boxes = self.graph.get_tensor_by_name('detection_boxes:0')

    def detect(self, img):
        """
        Method for detecting human objects in images
        :param img: current image/frame
        :return: list of bounding boxes for each detected human in the image
        """
        image_np_expanded = np.expand_dims(img, axis=0)
        (scores, classes, boxes) = self.session.run([self.scores, self.classes, self.boxes], feed_dict={self.tensor: image_np_expanded})
        scores = scores[0].tolist()
        classes = [int(x) for x in classes[0].tolist()]

        im_height, im_width, _ = img.shape
        boxes_list = []
        for i in range(len(classes)):
            if classes[i] == 1 and scores[i] > self.threshold:  # Filter for humans only with confidence > 70%
                boxes_list.append((int(boxes[0, i, 0] * im_height),
                                 int(boxes[0, i, 1] * im_width),
                                 int(boxes[0, i, 2] * im_height),
                                 int(boxes[0, i, 3] * im_width)))
        return boxes_list

    def predict(self, img):
        """
        Method for testing model accuracy
        :param img: current image/frame
        :return: 0 if a no human is detected, and 1 if a human is detected
        """
        image_np_expanded = np.expand_dims(img, axis=0)
        (scores, classes, boxes) = self.session.run([self.scores, self.classes, self.boxes], feed_dict={self.tensor: image_np_expanded})
        scores = scores[0].tolist()
        classes = [int(x) for x in classes[0].tolist()]

        for i in range(len(classes)):
            if classes[i] == 1 and scores[i] > self.threshold:  # Filter for humans only with confidence > 70%
                return 1
        return 0

    def close(self):
        self.session.close()
        self.default_graph.close()
