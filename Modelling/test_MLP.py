import tensorflow as tf
import numpy as np
import os


def shit ():
    feature_names = np.array([str(i) for i in range(50)])
    feature_columns = [tf.feature_column.numeric_column(k) for k in feature_names]
    vals = np.array([i for i in range(50)])
    # age = np.arange(4) * 1.0
    # height = np.arange(32, 36)
    x = dict(zip(feature_names, vals))
    # x = {'age': age, 'height': height}
    # y = np.arange(-32, -28)

    return tf.estimator.inputs.numpy_input_fn(
        x, batch_size=1, shuffle=False, num_epochs=1)


feature_names = [str(i) for i in range(50)]
feature_columns = [tf.feature_column.numeric_column(k) for k in feature_names]

my_checkpointing_config = tf.estimator.RunConfig(
    save_checkpoints_secs = 60,  # Save checkpoints every 20 minutes.
    keep_checkpoint_max = 10,       # Retain the 10 most recent checkpoints.
)

# create classifier that will be used
classifier = tf.estimator.DNNClassifier(
    feature_columns=feature_columns,                # The input features to our model
    hidden_units=[50, 50],              # Two layers, each with 10 neurons
    n_classes=2,                                    # Number of classes, currently good or bad
    optimizer=tf.train.AdamOptimizer(1e-4),         # Use Adam optimiser with default setting
    dropout=0.1,                                    # Add dropout to reduce overfitting
    config=my_checkpointing_config,
    model_dir=os.getcwd()+"/modeloutput_validation/",
    warm_start_from=os.getcwd()+"/modeloutput_validation/"
)  

evaluate_result =classifier.predict(input_fn=shit())
print(evaluate_result)

print("Evaluation results")
for key in evaluate_result:
    print(key)
    print("   {}, was: {}".format(key, evaluate_result[key]))

# tf.reset_default_graph()

# # Create some variables.
# # v1 = tf.get_variable("v1", shape=[3])
# # v2 = tf.get_variable("v2", shape=[5])

# # Add ops to save and restore all the variables.
# # saver = tf.train.Saver()

# # Later, launch the model, use the saver to restore variables from disk, and
# # do some work with the model.
# with tf.Session() as sess:
#    new_saver = tf.train.import_meta_graph('./modeloutput_validation/model.ckpt-154609.meta')
#    new_saver.restore(sess, tf.train.latest_checkpoint('./modeloutput_validation/'))
#    print("Model restored.")
#    graph = tf.get_default_graph()

#    graph.run(feed_dict={X: [1,1,1,1,]})
#    # Check the values of the variables
# #    print("v1 : %s" % v1.eval())
# #    print("v2 : %s" % v2.eval())

