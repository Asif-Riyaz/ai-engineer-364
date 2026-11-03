import requests
import csv
import sys
from datetime import datetime

def get_weather(city):
    """Fetches weather data using the free wttr.in API."""
    url = f"https://wttr.in/{city}?format=j1"
    try:
        # Applying a 5-second timeout and raising HTTP errors
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        temp_c = data['current_condition'][0]['temp_C']
        condition = data['current_condition'][0]['weatherDesc'][0]['value']
        return f"{temp_c}°C, {condition}"
    except requests.exceptions.Timeout:
        print("Error: Weather API request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
    return None

def get_exchange_rate(base="USD", target="INR"):
    """Fetches live exchange rates using the free Frankfurter API."""
    url = f"https://api.frankfurter.app/latest?from={base}&to={target}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data['rates'][target]
    except requests.exceptions.Timeout:
        print("Error: Currency API request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rate: {e}")
    return None

def log_to_csv(city, weather, rate):
    """Logs the fetched data into a CSV file."""
    filename = "daily_tracker_log.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Append to the CSV file
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header if file is empty
            if file.tell() == 0:
                writer.writerow(["Timestamp", "City", "Weather", "USD to INR Rate"])
            writer.writerow([timestamp, city, weather, rate])
        print(f"Successfully logged data to {filename}")
    except IOError as e:
        print(f"Error writing to CSV: {e}")

def main():
    print("--- CLI Weather & Currency Tracker ---")
    city = input("Enter a city for weather (e.g., Delhi): ").strip()
    
    print("\nFetching data...")
    weather = get_weather(city)
    rate = get_exchange_rate()
    
    if weather and rate:
        print(f"\nResults:\n- Weather in {city}: {weather}\n- 1 USD = {rate} INR")
        log_to_csv(city, weather, rate)
    else:
        print("\nFailed to retrieve complete data. Logging aborted.")

if __name__ == "__main__":
    main()