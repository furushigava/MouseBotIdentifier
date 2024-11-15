# MouseBotIdentifier

This project aims to create a machine learning model capable of identifying whether mouse movement was performed by a human or a bot. The project includes both the model's creation and training, as well as a web version for testing and data collection. The web-based testing version is available at: [MouseBotIdentifier Demo](https://furushigava.github.io/MouseBotIdentifier/).

## Project Structure

- **saved_model/** - Directory for saving models and checkpoints.
- **web/** - Directory for the web application (data, static files, templates, and Flask application).
- **add_angles.py** - Script for adding angle data to mouse movement data.
- **const.py** - Configuration file for paths to data and model.
- **create_model.py** - Script for creating and training the model.
- **model_work.py** - Script for using the model (predictions and evaluation).
- **mouse_position_saver.py** - Script for saving mouse movement data.
- **random_move.py** - Script for generating random mouse movements.
- **resource_override_mouse_checker_client.js** - Script for saving mouse movement data from a browser.
- **transform_desktop_pkl_to_normal.py** - Script for normalizing data collected by mouse_position_saver.
- **transform_pkl_from_js_to_normal.py** - Script for normalizing data collected from the browser.

## Installation and Running

```bash
git clone https://github.com/furushigava/Mouse_Movement_Detection_Model
```

## Using the Model

### Web Version

Access the web version at [MouseBotIdentifier Demo](https://furushigava.github.io/MouseBotIdentifier/).
> **Note**: A value closer to 0 indicates likely human movement, while a value closer to 1 indicates bot-like movement.

To run the web version locally:
```bash
python web/app.py
```
The model testing interface will be available at http://127.0.0.1:5000/check_model.

### Terminal Version

```bash
python model_work.py --model_path saved_model/CNN_LSTM --data_files path_to_your_pkl_file
```

## Scripts

### 1. `mouse_position_saver.py`

This script is used to collect data on mouse movements. It records the mouse coordinates in a `.pkl` file.

### 2. `transform_desktop_pkl_to_normal.py`

This script converts the mouse movement data obtained with `mouse_position_saver` (saved in a `.pkl` file) into the range [0;1]. This step is necessary for normalizing the data before training the model.

### 3. `resource_override_mouse_checker_client.js`

This script handles data collection from the browser. Install the Resource Override extension and use `resource_override_mouse_checker_client.js` to collect data. Run `app.py` to receive the data on the server.

### 4. `transform_pkl_from_js_to_normal.py`

This script converts the mouse movement data collected via `resource_override_mouse_checker_client.js` and `app.py` (saved in a `.pkl` file) into the range [0;1]. This normalization is required before training the model.

### 5. `add_angles.py`

All the data collected via `mouse_position_saver`, `resource_override_mouse_checker_client.js` + `app.py`, and normalized by the corresponding transformer scripts should be processed through `add_angles.py` to add a third variable — the angle.

### 6. `random_move.py`

Generates random mouse movements on the screen.

### 7. `create_model.py`

This script builds and trains the model. The training occurs on data in the format `[Count_batches, 40, 3]`: Each sequence includes 40 mouse movements. Each movement is described by two coordinates and the angle between the current, previous, and next vectors.

## Data Collection

To collect the necessary training data, follow these steps:

1. **Install the Resource Override Extension:**
   - Install the Resource Override extension in your browser.

2. **Load the `resource_override_mouse_checker_client.js`:**
   - Load the `resource_override_mouse_checker_client.js` file into the extension.

3. **Configure the Movement Type:**
   - Modify the corresponding variable in the `resource_override_mouse_checker_client.js` file to set the movement type you want to record (either "bot" or "human").

4. **Run `web/app.py`:**
   - Run the `app.py` script to start the server.

5. **Start Data Collection:**
   - Access the clicker game at `http://127.0.0.1:5000/game` to begin collecting mouse movement data continuously.
   - You can monitor the number of saved batches at `http://127.0.0.1:5000/batch_counts`.

6. **Data Saving:**
   - The collected data will be saved in `.pkl` format by default in the `web/` directory.

7. **Normalize the Data:**
   - After data collection, use the `transform_pkl_from_js_to_normal.py` script to normalize the data.

8. **Add Angle Information:**
   - Run the `add_angles.py` script to add angle information between the mouse movements.

9. **Ready for Model Training:**
   - The data is now ready for model training.
