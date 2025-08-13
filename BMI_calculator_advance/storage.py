import pandas as pd
from datetime import datetime
import os

FILE_NAME = "users.csv"

def save_bmi(username, weight, height, bmi, category):
    """Save BMI record to CSV, creating headers if the file is new or empty."""
    df = pd.DataFrame([{
        "username": username,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "weight": weight,
        "height": height,
        "bmi": bmi,
        "category": category
    }])
    
    # If file does not exist or is empty, write with headers
    if not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0:
        df.to_csv(FILE_NAME, index=False)
    else:
        df.to_csv(FILE_NAME, mode='a', header=False, index=False)


def load_user_data(username):
    """Load BMI history for a specific user, returning an empty DataFrame if not found."""
    if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
        df = pd.read_csv(FILE_NAME)
        
        # Check if 'username' column exists
        if "username" in df.columns:
            return df[df["username"] == username]
    
    # Return empty DataFrame if file is missing, empty, or invalid
    return pd.DataFrame(columns=["username", "date", "weight", "height", "bmi", "category"])
