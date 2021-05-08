import os
import csv
import numpy as np
from PIL import Image
from human_detection import HumanDetector
import sklearn.metrics as metrics

human_detector = HumanDetector()


# HUMAN VS NONHUMAN DATASET: https://www.kaggle.com/aliasgartaksali/human-and-non-human
# HUMANS WITH MASKS DATASET: https://www.kaggle.com/bikashjaiswal/dataset-for-mask-nonmask-and-nonhuman-classes
def create_labels(source_dir, label_file):
    """
    Creates a CSV file of each image file name and it's corresponding image classification
    :param source_dir: directory path of the image folder
    :param label_file: file path of the csv
    """
    dir_list = ["non-humans", "humans"]
    with open(label_file, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['filename', 'label'])
        for i in range(2):
            files = os.listdir(source_dir + '/' + dir_list[i])
            for f in files:
                writer.writerow({'filename': f, 'label': i})


def create_tables(labels_file):
    """
    Creates a 2D array of each image and its classification: 0 = nonhuman, 1 = humans
    :param labels_file: path to the csv label file
    :return: 2D numpy array of each image file name and classification
    """
    file = open(labels_file, 'r')
    reader = csv.reader(file, delimiter=',')
    return np.array([row for row in reader])


def create_summary(table_list, img_dir_list, summary_file):
    """
    Prints out the accuracy and precision of the model
    :param table_list: 2D numpy array of each image file name and classification
    :param img_dir_list: directory path to the image folder
    :param summary_file: path to the summary/output text file
    """
    for (table, img_dir) in zip(table_list, img_dir_list):
        # shuffle dataset
        np.random.shuffle(table)

        # get predictions
        img_list = table.T[0]
        actual = table.T[1].astype('int32').tolist()
        predictions = []
        for img_path in img_list:
            img = Image.open(img_dir + img_path)
            predictions.append(human_detector.predict(img))

        # get metric summary
        accuracy = metrics.accuracy_score(actual, predictions)
        precision = metrics.precision_score(actual, predictions)

        file = open(summary_file, 'a')
        file.write('Accuracy: ' + str(accuracy) + os.linesep)
        file.write('Precision: ' + str(precision) + os.linesep)
    file.close()


if __name__ == "__main__":
    human_labels = "test_images/human_vs_nonhuman/labels.csv"
    mask_labels = "test_images/masks/labels.csv"
    # create_labels("test_images/masks", mask_labels)
    # human_table = create_tables(human_labels)
    mask_table = create_tables(mask_labels)
    create_summary([mask_table], ["test_images/masks/combined/"], "summary.txt")
