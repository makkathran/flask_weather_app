# Weather App

A web application that allows users to view current weather and air quality data based on their location.

## Features

- **User Registration & Authentication**: Users can sign up and log in.
- **Weather Data**: Display weather data post-login.
- **Air Quality Data**: Alongside weather, air quality details are also available.
- **Responsive UI**: Designed using Bootstrap for a clean interface.

## File Structure

- `app.py`: Main Flask application file.
- `models.py`: Database models.
- `forms.py`: Definitions of forms.
- `base.html`, `index.html`, `login.html`, `registers.html`: HTML templates.
- `style.css`: Styling details.
- `weather.db`: SQLite database.

## External Integrations

1. **OpenWeatherMap**: For fetching weather details.
2. **Nominatim (OpenStreetMap)**: To get city names from coordinates.
3. **AirVisual**: Sourced for fetching air quality data.

## Installation

1. Clone the repository.
2. Install the required packages.
3. Run the application: `python app.py`
4. Open a browser and navigate to: `http://localhost:5000`

## Contribution

Pull requests are welcome!
