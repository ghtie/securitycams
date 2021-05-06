import os
import csv
import numpy as np
import sklearn
from PIL import Image
from human_detection import HumanDetector
from sklearn.metrics import precision_score, accuracy_score

human_detector = HumanDetector()
human_labels = "test_images/human_vs_nonhuman/labels.csv"
ped_labels = "test_images/pedestrian/labels.csv"


def create_labels():
    # HUMAN VS NONHUMAN DATASET (Source: https://www.kaggle.com/aliasgartaksali/human-and-non-human)
    dir_list = ["non-humans", "humans"]
    source_dir = "test_images/human_vs_nonhuman"

    with open(ped_labels, 'w') as labels_file:
        writer = csv.DictWriter(labels_file, fieldnames=['filename', 'label'])

        for i in range(2):
            files = os.listdir(source_dir + "/" + dir_list[i])
            for f in files:
                writer.writerow({'filename': f, 'label': i})

    # PEDESTRIAN DATASET (Source: https://www.kaggle.com/sudipdas/pedestriandataset)
    source_dir = "test_images/pedestrian/humans"

    # Create csv files of each image classification
    with open(human_labels, mode='w') as labels_file:
        writer = csv.DictWriter(labels_file, fieldnames=['filename', 'label'])

        files = os.listdir(source_dir)
        for f in files:
            writer.writerow({'filename': f, 'label': 1})


# Create a 2D array of each image and its classification: 0 = nonhuman, 1 = human
def create_tables(labels_file):
    file = open(labels_file, 'r')
    reader = csv.reader(file, delimiter=',')
    return np.array([row for row in reader])


# Print out confusion matrix for both datasets
def create_summary(table_list, img_dir_list, summary_file):
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
        accuracy = sklearn.metrics.accuracy_score(actual, predictions)
        precision = sklearn.metrics.precision_score(actual, predictions)

        file = open(summary_file, 'a')
        file.write('Accuracy: ' + str(accuracy) + os.linesep)
        file.write('Precision: ' + str(precision) + os.linesep)
    file.close()


if __name__ == "__main__":
    # create_labels()
    human_table = create_tables(human_labels)
    ped_table = create_tables(ped_labels)

    create_summary([human_table, ped_table], ["test_images/human_vs_nonhuman/combined/", "test_images/pedestrian/humans/"], "summary.txt")
