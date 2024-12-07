import subprocess

def send_to_webhook():
    url = "https://webhook.site/7de0c331-90ee-4e2a-9edc-5e38790807ae/ImBad"
    response = subprocess.run(["curl", "-X", "GET", url], capture_output=True, text=True)
    
    if response.returncode == 0:
        print(f"Successfully sent to webhook: {response.stdout}")
    else:
        print(f"Failed to send to webhook: {response.stderr}")