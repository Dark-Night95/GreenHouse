import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"


# Load trained model
model = joblib.load(MODEL_PATH)


def predict_water_requirement(
    temperature,
    humidity,
    light
):

    # Create DataFrame with feature names
    input_data = pd.DataFrame({
        "Temperature": [temperature],
        "Humidity": [humidity],
        "Light": [light]
    })

    # Make sure columns have exactly the same
    # order as during model training
    input_data = input_data[
        model.feature_names_in_
    ]

    # Prediction
    prediction = model.predict(input_data)

    # Prediction probability
    probability = model.predict_proba(input_data)

    # Convert prediction to integer
    result = int(prediction[0])

    # Get confidence
    confidence = float(max(probability[0]))

    # return {
    #     "water_required": result,
    #     "confidence": confidence
    # }
    if result == 1:
        return {"Water is required":confidence}
    else:
        return{"Water is not required":confidence}


# Test
# if __name__ == "__main__":
#
#     result = predict_water_requirement(30,0,900)
#     print(result)

# range of values should be according to the given training data
# Temperature: ~15–40°C
# Humidity: ~20–80%
# Light: ~100–1000