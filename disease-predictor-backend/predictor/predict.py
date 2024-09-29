import pickle
import numpy as np
import tensorflow as tf
from keras.models import load_model

#model_cnn = tf.keras.models.load_model('./predictor/models/model_cnn.h5')

# Load the model
model_cnn = load_model('./predictor/models/model_cnn.keras')


# Load the label_encoder using pickle
with open('./predictor/models/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)


def get_top_5_predictions(input):
    # Convert input to a NumPy array and reshape
    input_array = np.array(input)
    # Predict the probabilities
    #predicted_probabilities = model_cnn.predict(input.reshape(1, -1))
    predicted_probabilities = model_cnn.predict(input_array.reshape(1, input_array.shape[0], 1))

    # Get the top 5 indices with the highest probabilities
    top_5_indices = np.argsort(-predicted_probabilities[0])[:5]

    # Retrieve the class labels and their corresponding probabilities
    top_5_predictions = [
        {"label": label_encoder.classes_[i], "probability": float(predicted_probabilities[0][i])}
        for i in top_5_indices
    ]

    return top_5_predictions
