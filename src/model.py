import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential, load_model, Model
from keras.layers import Input, Dense, Conv2D, Flatten, BatchNormalization, Activation, LeakyReLU, add
from keras.optimizers import Adam

ACTION_SIZE = 3


class NNet():
    """
    The network being created.
    Attributes:
    TODO
    """

    def __init__(self, learning_rate, input_dim, output_dim, hidden_layers):
        # self.regul_const = regul_const
        self.learning_rate = learning_rate
        self.input_dim = input_dim
        self.output_dim = input_dim
        self.hidden_layers = hidden_layers
        self.model = self.build_model()


    def build_model(self):
        """
        Builds the keras model
        """
        model = Sequential()
        model.add(Dense(24, input_dim=self.input_dim, activation='relu'))

        for _ in range(0,self.hidden_layers):
            model.add(
                Dense(
                    self.output_dim,
                    use_bias=False,
                    activation='relu',
                    # kernel_regularizer=keras.regularizers.l2(
                        # self.regul_const)
                )
            )
        model.add(Dense(ACTION_SIZE, activation='linear'))
        #  model.compile(optimizer='adam', loss=tf.keras.losses.mse, metrics=['accuracy'])
        model.compile(
             loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model
