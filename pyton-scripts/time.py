from datetime import datetime
import pytz

# Function to convert IST time to Australian time (Sydney)
def convert_ist_to_australia(ist_time_str):
    # Define the IST time zone
    ist_tz = pytz.timezone('Asia/Kolkata')
    
    # Define the Australian time zone (Sydney)
    aus_tz = pytz.timezone('Australia/Sydney')
    
    # Parse the input time string to a datetime object
    ist_time = datetime.strptime(ist_time_str, '%Y-%m-%d %H:%M:%S')
    
    # Localize the IST time to the IST time zone
    ist_time = ist_tz.localize(ist_time)
    
    # Convert the IST time to the Australian time zone
    aus_time = ist_time.astimezone(aus_tz)
    
    return aus_time

# Example usage
ist_time_str = '2024-07-01 14:30:00'  # Input IST time as a string
aus_time = convert_ist_to_australia(ist_time_str)
print(f"IST Time: {ist_time_str}")
print(f"Australian Time (Sydney): {aus_time.strftime('%Y-%m-%d %H:%M:%S')}")