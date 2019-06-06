import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential, load_model, Model
from keras.layers import Input, Dense, Conv2D, Flatten, BatchNormalization, Activation, LeakyReLU, add

ACTION_SIZE

class Model():
    """
    The network being created.
    Attributes:
    TODO
    """
    def __init__(self, regul_const, learning_rate, input_dim, output_dim, hidden_layers):
        self.regul_const = regul_const
        self.learning_rate = learning_rate
        self.input_dim = input_dim
        self.hidden_layers = hidden_layers
        self.model = self.build_model()
    
    def make_hidden_layers(self, inp, filters, kernal_size):
        x = Dense(
            self.output_dim,
            use_bias=False,
            activation='relu',
            kernel_regularizer = regularizers.l2(self.regul_const)       
            )(x)

    def build_model():
        main_input = Input(shape = self.input_dim, name = 'main_input')
        model = Sequential()

        # potentially add convo layer...

        if len(self.hidden_layers) > 1:
            for i in self.hidden_layers[1:]:
                model.add(Dense(self.output_dim, use_bias=False, activation='relu', kernel_regularizer = regularizers.l2(self.regul_const)))
            
        
        #policy head value head????

        model.add(Dense(ACTION_SIZE, activation='linear'))

        model.compile(model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate)))



