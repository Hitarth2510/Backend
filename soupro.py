import numpy as np
import librosa
from scipy.signal import correlate
import math
from pymongo import MongoClient
from datetime import datetime

# Step 1: Load Audio Data from Microphones
def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    return y, sr

# Step 2: Compute Time Delay between two signals
# TDOA 
def compute_time_delay(signal1, signal2, sr):
    correlation = correlate(signal1, signal2, mode='full')
    lag = np.argmax(correlation) - len(signal2) + 1
    time_delay = lag / sr  # Time delay in seconds
    return time_delay

# Step 3: Convert angle to cardinal direction
def angle_to_cardinal(angle):
    if angle >= 337.5 or angle < 22.5:
        return "N", angle
    elif angle >= 22.5 and angle < 67.5:
        return "NE", angle
    elif angle >= 67.5 and angle < 112.5:
        return "E", angle
    elif angle >= 112.5 and angle < 157.5:
        return "SE", angle
    elif angle >= 157.5 and angle < 202.5:
        return "S", angle
    elif angle >= 202.5 and angle < 247.5:
        return "SW", angle
    elif angle >= 247.5 and angle < 292.5:
        return "W", angle
    elif angle >= 292.5 and angle < 337.5:
        return "NW", angle

# Step 4: Estimate the direction of gunshot based on time differences
def estimate_direction(time_delays, mic_positions):
    # For simplicity, assuming microphones are arranged in a circle
    angle_sum = 0
    # Iterate only over available time delays
    for i in range(len(time_delays)):
        x, y = mic_positions[i + 1]  # Skip the first mic (reference mic)
        angle = math.atan2(y, x)  # Calculate angle based on mic position
        angle_sum += angle * time_delays[i]  # Weight angle with the time delay
    
    avg_angle = angle_sum / sum(time_delays)
    return math.degrees(avg_angle) % 360  # Convert to degrees and normalize to 0-360

# Step 5: Store output in MongoDB
def store_in_mongo(direction, angle):
    # Replace this with your actual MongoDB connection string
    client = MongoClient("mongodb://localhost:27017/")  # Or your MongoDB URI
    db = client["gunshot_db"]  # Database name
    collection = db["gunshot_directions"]  # Collection name
    
    # Prepare the data to insert
    data = {
        "timestamp": datetime.utcnow(),
        "direction": direction,
        "angle": angle
    }
    
    # Insert data into MongoDB
    collection.insert_one(data)
    print("Data inserted into MongoDB successfully!")

# Step 6: Main process for gunshot direction detection
def main():
    # Assuming relative positions of microphones in a circle around the origin (arbitrary units)
    mic_positions = [
        (1, 0),   # Mic 1 (x=1, y=0)
        (0.5, 0.87),  # Mic 2 (x=0.5, y=0.87)
        (-0.5, 0.87),  # Mic 3 (x=-0.5, y=0.87)
        (-1, 0),   # Mic 4 (x=-1, y=0)
        (-0.5, -0.87),  # Mic 5 (x=-0.5, y=-0.87)
        (0.5, -0.87)  # Mic 6 (x=0.5, y=-0.87)
    ]

    # Audio file paths for gunshot recordings
    file_paths = [
        'mic1_gunshot.wav', 'mic2_gunshot.wav', 'mic3_gunshot.wav',
        'mic4_gunshot.wav', 'mic5_gunshot.wav', 'mic6.wav'
    ]

    # Load audio from each microphone
    signals = [load_audio(file)[0] for file in file_paths]  # Load signals
    sample_rate = load_audio(file_paths[0])[1]  # Get sample rate (assuming same for all)

    # Calculate Time Difference of Arrival (TDOA) for microphone pairs
    time_delays = []
    for i in range(1, len(signals)):  # Compare each mic's signal with the first mic
        time_delays.append(compute_time_delay(signals[0], signals[i], sample_rate))
    
    # Estimate direction based on time delays and mic positions
    estimated_angle = estimate_direction(time_delays, mic_positions)
    
    # Convert angle to cardinal direction
    cardinal_direction, angle = angle_to_cardinal(estimated_angle)
    
    print(f"Estimated gunshot direction: {cardinal_direction} ({angle:.2f} degrees)")

    # Store result in MongoDB
    store_in_mongo(cardinal_direction, angle)

if __name__ == "__main__":
    main()
