import pyautogui
import pickle
import os
import time
import argparse

def save_data(new_data, filename):
    # Check if the file exists
    if os.path.exists(filename):
        # Load existing data
        with open(filename, 'rb') as file:
            existing_data = pickle.load(file)
    else:
        # If file doesn't exist, start with an empty list
        existing_data = []

    # Append new data to existing data
    existing_data.extend(new_data)

    # Save the combined data back to the file
    with open(filename, 'wb') as file:
        pickle.dump(existing_data, file)

def main(num_samples, num_batches, num_stationary_checks, delay, file_name):
    all_data = []
    batch = []

    last_positions = [None] * num_stationary_checks
    last_index = 0

    try:
        while True:
            x, y = pyautogui.position()
            current_position = (x, y)
            
            # Save the current position in the list
            last_positions[last_index % num_stationary_checks] = current_position
            last_index += 1

            # Check if all last positions are the same
            if len(set(last_positions)) == 1:
                # Mouse is stationary
                continue

            # If the required number of positions are collected, add to the current batch
            if len(batch) < num_samples:
                batch.append(current_position)
            else:
                # If the required number of positions are collected, add the batch to all data
                if len(batch) == num_samples:
                    if len(all_data) % num_batches == 0 and len(all_data) > 0:
                        save_data(all_data, file_name)
                    all_data.append(batch)
                # Start a new batch
                batch = [current_position]
            time.sleep(delay)
    except KeyboardInterrupt:
        # Save remaining data on exit
        if len(batch) == num_samples:
            if len(all_data) % num_batches == 0 and len(all_data) > 0:
                save_data(all_data, file_name)
            all_data.append(batch)
        save_data(all_data, file_name)
        print("Data saved to file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to record mouse positions and save them to a file.")
    parser.add_argument('--num_samples', type=int, default=40, help='Number of samples per batch')
    parser.add_argument('--num_batches', type=int, default=10, help='Number of batches before saving to file')
    parser.add_argument('--num_stationary_checks', type=int, default=30, help='Number of last positions to check for stationarity')
    parser.add_argument('--delay', type=float, default=0.01, help='Delay between position checks in seconds')
    parser.add_argument('--file_name', type=str, default='mouse_positions_bot_my.pkl', help='File name to save mouse positions')

    args = parser.parse_args()

    main(args.num_samples, args.num_batches, args.num_stationary_checks, args.delay, args.file_name)
