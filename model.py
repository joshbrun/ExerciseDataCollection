import os
import tensorflow as tf

PATH = os.getcwd()

# Fetch and store Training and Test dataset files
PATH_DATASET = PATH
FILE_TRAIN = PATH_DATASET + os.sep + "data/training/hcs_squat_front.csv" # "squat_male_front.csv"
FILE_TEST = PATH_DATASET + os.sep + "data/training/hcs_squat_front.csv"  # "tes_fem.csv" 


def train(training_file, testing_file, epochs):
    next_batch = get_dataset(training_file, True)       # Will return 32 random elements

    feature_names = [str(i) for i in range(75)]
    feature_columns = [tf.feature_column.numeric_column(k) for k in feature_names]

    # create classifier that will be used
    classifier = tf.estimator.DNNClassifier(
        feature_columns=feature_columns,                # The input features to our model
        hidden_units=[10, 10],              # Two layers, each with 10 neurons
        n_classes=2,                                    # Number of classes, currently good or bad
        optimizer=tf.train.AdamOptimizer(1e-4),         # Use Adam optimiser with default setting
        dropout=0.1,                                    # Add dropout to reduce overfitting
        model_dir=os.getcwd()+"/modeloutput/")          # Path to where checkpoints etc are stored


    classifier.train(input_fn=lambda: get_dataset(training_file, True, epochs))

    # evaluate model
    evaluate_result = classifier.evaluate(input_fn=lambda: get_dataset(testing_file, False, 4))

    print("Evaluation results")
    for key in evaluate_result:
        print("   {}, was: {}".format(key, evaluate_result[key]))


tf.logging.set_verbosity(tf.logging.INFO)

def get_dataset(file_path, perform_shuffle=False, repeat_count=1):
    def decode_csv(line):
        feature_names = [str(i) for i in range(75)]
        decoder = [[0.]] * 75
        decoder.append([0])
        parsed_line = tf.decode_csv(line, decoder)
        label = parsed_line[-1]     # Last element is the label
        del parsed_line[-1]         # Delete last element
        #parsed_line = [parsed_line[i] for i in range(75) if i % 3 != 0]
        features = parsed_line      # Everything but last elements are the features
        d = dict(zip(feature_names, features)), label
        return d
    
    dataset = (tf.data.TextLineDataset(file_path)   # Read text file
               #.skip(1)                            # Skip header row
               .map(decode_csv))                    # Transform each elem by applying decode_csv fn
    if perform_shuffle:
        dataset = dataset.shuffle(buffer_size=256)
    dataset = dataset.repeat(repeat_count)
    dataset = dataset.batch(16)
    iterator = dataset.make_one_shot_iterator()
    batch_features, batch_labels = iterator.get_next()
    return batch_features, batch_labels

train(FILE_TRAIN, FILE_TEST, 100)