import joblib
import pandas as pd


# Load trained model
model = joblib.load("model.pkl")


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
#     result = predict_water_requirement(
#         30,
#         35,
#         700
#     )
#
#     print(result)