import tensorflow as tf
import numpy as np
from sklearn.metrics import precision_score,recall_score,f1_score

class TextCNN(object):
    """
    A CNN for text classification.
    Uses an embedding layer, followed by a convolutional, max-pooling and softmax layer.
    """
    def __init__(
      self, sequence_length, num_classes, vocab_size,
      embedding_size, pos_vocab_size,pos_embedding_size,filter_sizes, num_filters, l2_reg_lambda=0.0):

        # Placeholders for input, output and dropout
        print('text CNN: pos_vocab_size:{},vocab_size:{}'.format(pos_vocab_size,vocab_size))
        self.input_x = tf.placeholder(tf.int32, [None, sequence_length], name="input_x")
        self.input_pos1 = tf.placeholder(tf.int32, [None, sequence_length], name="input_pos1")
        self.input_pos2 = tf.placeholder(tf.int32, [None, sequence_length], name="input_pos2")
        self.input_y = tf.placeholder(tf.float32, [None, num_classes], name="input_y")
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")

        # Keeping track of l2 regularization loss (optional)
        l2_loss = tf.constant(0.0)

        #我要在这里添加位置向量和词向量，将其拼接起来
        # Word Embedding layer
        with tf.device('/cpu:0'), tf.name_scope("embedding"):
            self.W = tf.Variable(
                tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0),
                name="W")
            self.embedded_chars = tf.nn.embedding_lookup(self.W, self.input_x)
            #self.embedded_chars_expanded = tf.expand_dims(self.embedded_chars, -1)
        #position Embedding layer
        with tf.device('/cpu:0'),tf.name_scope("pos_embedding"):
            self.pos_embedding=tf.Variable(
                tf.random_uniform([pos_vocab_size, pos_embedding_size], -1.0, 1.0),
                name="pos_embedding")
            self.embedded_pos1=tf.nn.embedding_lookup(self.pos_embedding,self.input_pos1)
            self.embedded_pos2=tf.nn.embedding_lookup(self.pos_embedding,self.input_pos2)
            print("text_cnn.py: embedded_pos1::" + str(self.embedded_pos1.shape))

            self.embedded_pos=tf.concat(values=[self.embedded_pos1,self.embedded_pos2],axis=2)
            print("text_cnn.py: embedded_pos::" + str(self.embedded_pos.shape))
        #Concat word and position
        self.embedded_x=tf.concat(values=[self.embedded_chars,self.embedded_pos],axis=2)
        print("text_cnn.py: embedded_x:"+str(self.embedded_x.shape))
        self.embedded_x_expanded=tf.expand_dims(self.embedded_x,-1)
        print("text_cnn.py: embedded_x_expanded:"+str(self.embedded_x_expanded.shape))
        # Create a convolution + maxpool layer for each filter size
        pooled_outputs = []
        for i, filter_size in enumerate(filter_sizes):
            with tf.name_scope("conv-maxpool-%s" % filter_size):
                # Convolution Layer
                filter_shape = [filter_size, embedding_size+2*pos_embedding_size, 1, num_filters]
                W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
                b = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")
                conv = tf.nn.conv2d(
                    self.embedded_x_expanded,
                    W,
                    strides=[1, 1, 1, 1],
                    padding="VALID",
                    name="conv")
                # Apply nonlinearity
                h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
                # Maxpooling over the outputs
                pooled = tf.nn.max_pool(
                    h,
                    ksize=[1, sequence_length - filter_size + 1, 1, 1],
                    strides=[1, 1, 1, 1],
                    padding='VALID',
                    name="pool")
                pooled_outputs.append(pooled)

        # Combine all the pooled features
        num_filters_total = num_filters * len(filter_sizes)
        self.h_pool = tf.concat(pooled_outputs, 3)
        self.h_pool_flat = tf.reshape(self.h_pool, [-1, num_filters_total])

        # Add dropout
        with tf.name_scope("dropout"):
            self.h_drop = tf.nn.dropout(self.h_pool_flat, self.dropout_keep_prob)

        # Final (unnormalized) scores and predictions
        with tf.name_scope("output"):
            W = tf.get_variable(
                "W",
                shape=[num_filters_total, num_classes],
                initializer=tf.contrib.layers.xavier_initializer())
            b = tf.Variable(tf.constant(0.1, shape=[num_classes]), name="b")
            l2_loss += tf.nn.l2_loss(W)
            l2_loss += tf.nn.l2_loss(b)
            self.scores = tf.nn.xw_plus_b(self.h_drop, W, b, name="scores")
            print("text_cnn.py: score:"+str(self.scores.shape))
            self.predictions = tf.argmax(self.scores, 1, name="predictions")
            self.predicted=tf.round(tf.nn.sigmoid(self.scores))

        # Calculate mean cross-entropy loss
        with tf.name_scope("loss"):
            losses = tf.nn.softmax_cross_entropy_with_logits(logits=self.scores, labels=self.input_y)
            self.loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

        # Accuracy
        with tf.name_scope("accuracy"):
            correct_predictions = tf.equal(self.predictions, tf.argmax(self.input_y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")
            
         # F1-score
        with tf.name_scope("F1score"):
            # Count true positives, true negatives, false positives and false negatives.
            self.tp = tf.count_nonzero(self.predicted* self.input_y)
            self.tn = tf.count_nonzero((self.predicted - 1) * (self.input_y - 1))
            self.fp = tf.count_nonzero(self.predicted * (self.input_y - 1))
            self.fn = tf.count_nonzero((self.predicted - 1) * self.input_y)
            # Calculate precision, recall and F1 score.
            self.precision = self.tp / (self.tp + self.fp)
            self.recall = self.tp / (self.tp + self.fn)
            self.fmeasure = (2 * self.precision * self.recall) / (self.precision + self.recall)
# 
        def print_f1score(self):
            print("f1_score,",str(f1_score(self.input_y, self.predictions, average="macro")))