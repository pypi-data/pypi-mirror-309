import tensorflow as tf
from tensorflow.keras.layers import Layer, Conv2D, GlobalAveragePooling2D, GlobalMaxPooling2D, Dense, Multiply, Add, Concatenate, Activation

class GlobalAveragePooling2DCustom(Layer):
    def __init__(self, **kwargs):
        super(GlobalAveragePooling2DCustom, self).__init__(**kwargs)

    def call(self, inputs):
        return tf.reduce_mean(inputs, axis=-1, keepdims=True)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[1], input_shape[2], 1)
    
class GlobalMaxPooling2DCustom(Layer):
    def __init__(self, **kwargs):
        super(GlobalMaxPooling2DCustom, self).__init__(**kwargs)

    def call(self, inputs):
        return tf.reduce_max(inputs, axis=-1, keepdims=True)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[1], input_shape[2], 1)

# Channel Attention Block
def channel_attention(X, ratio=8):
    channel_axis = -1
    channel = X.shape[channel_axis]
    
    shared_layer_one = Dense(channel // ratio,
                             activation='relu',
                             kernel_initializer='he_normal',
                             use_bias=True,
                             bias_initializer='zeros')
    shared_layer_two = Dense(channel,
                             kernel_initializer='he_normal',
                             use_bias=True,
                             bias_initializer='zeros')
    
    avg_pool = GlobalAveragePooling2D()(X)
    avg_pool = shared_layer_one(avg_pool)
    avg_pool = shared_layer_two(avg_pool)
    
    max_pool = GlobalMaxPooling2D()(X)
    max_pool = shared_layer_one(max_pool)
    max_pool = shared_layer_two(max_pool)
    
    cbam_feature = Add()([avg_pool, max_pool])
    cbam_feature = Activation('sigmoid')(cbam_feature)
    
    return Multiply()([X, cbam_feature])

# Spatial Attention Block
def spatial_attention(X):
    avg_pool = GlobalAveragePooling2DCustom()(X)
    max_pool = GlobalMaxPooling2DCustom()(X)

    concat = Concatenate(axis=-1)([avg_pool, max_pool])
    
    cbam_feature = Conv2D(filters=1,
               kernel_size=(7,7),
               strides=(1,1),
               padding='same',
               activation='sigmoid',
               kernel_initializer='he_normal',
               use_bias=False)(concat)  # Apply convolution
    
    return Multiply()([X, cbam_feature])

# CBAM Block (Channel + Spatial Attention)
def cbam_block(input_feature, ratio=8):
    cbam_feature = channel_attention(input_feature, ratio)
    cbam_feature = spatial_attention(cbam_feature)
    return cbam_feature
