import time
import json
import atexit
from bleuio_lib.bleuio_funcs import BleuIO

rssi_value = None
dongle = None  

def scan_callback(scan_input):
    global rssi_value  
    try:
        device_data = json.loads(scan_input[0])  
        if device_data.get("addr") == "[1]6B:C0:5C:BD:CF:14":
            rssi_value = device_data["rssi"]  
            print(f"\nDevice Found! Address: {device_data['addr']}, RSSI: {rssi_value}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def send_led_command(dongle, rssi):
    if rssi is not None:  
        if rssi > -40:
            print(f"RSSI: {rssi} | Sending LED Command: 50/50")
            dongle.at_led(toggle="T", on_period="50", off_period="50")
        elif -60 <= rssi <= -40:
            print(f"RSSI: {rssi} | Sending LED Command: 100/100")
            dongle.at_led(toggle="T", on_period="100", off_period="100")
        elif -90 <= rssi < -60:
            print(f"RSSI: {rssi} | Sending LED Command: 200/200")
            dongle.at_led(toggle="T", on_period="200", off_period="200")
        else:
            print(f"RSSI: {rssi} | Sending LED Command: 300/300")
            dongle.at_led(toggle="T", on_period="300", off_period="300")
    else:
        print("No RSSI value available for LED command.")


def cleanup():
    if dongle:
        print("\n--- Turning off LED and cleaning up ---")
        dongle.at_led(0)

# Main logic
def main():
    global rssi_value, dongle  
    dongle = BleuIO()

    atexit.register(cleanup)

    dongle.register_scan_cb(scan_callback)

    print("\n--- Starting BLE Task ---\n")

    print("Setting device role to Central...")
    central_response = dongle.at_central()

    try:
        while True:
            print("\nStarting scan for 2 seconds...")
            dongle.at_gapscan(2)  
            time.sleep(3)  

            send_led_command(dongle, rssi_value)

            print("\nScan cycle completed. Restarting...\n")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n--- Script Terminated by User ---")

# Run the main function
if __name__ == "__main__":
    main()
