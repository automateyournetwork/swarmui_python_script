import requests
import json
import subprocess
from PIL import Image
from datetime import datetime
# Enable debug logging for requests
import logging
import http.client as http_client

current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

http_client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# Step 1: Get a usable session ID
session_url = "http://localhost:7801/API/GetNewSession"
headers = {
    "Content-Type": "application/json"
}
response = requests.post(session_url, headers=headers, data=json.dumps({}))
if response.status_code == 200:
    session_data = response.json()
    session_id = session_data["session_id"]
    print(f"Session ID: {session_id}")
else:
    print(f"Failed to get session ID, status code: {response.status_code}")
    print(response.text)
    exit()

# Step 2: Generate the image
models = ["Juggernaut_X_RunDiffusion", "sd3_medium", "sd3_medium_incl_clips_t5xxlfp16"]
for model in models: 
    generate_url = "http://localhost:7801/API/GenerateText2Image"
    payload = {
        "session_id": session_id,
        "images": 1,
        "prompt": "A hyperrealistic depiction of a wizard inside a futuristic data center from the year 3000. The wizard, dressed in modern high-tech robes adorned with glowing symbols, stands in the middle of a vast room filled with sleek, advanced servers and holographic interfaces. The environment is illuminated by the blue and purple glow of the technology surrounding him. The wizard is casting a spell, with swirling magical energy integrating seamlessly with the digital elements around him, creating a blend of mysticism and advanced technology. The overall scene should feel both fantastical and cutting-edge, highlighting the fusion of magic and futuristic technology.",
        "model": model,
        "width": 1024,
        "height": 576
    }
    response = requests.post(generate_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        generate_data = response.json()
        print("Response from GenerateText2Image:", generate_data)
        if "images" in generate_data and generate_data["images"]:
            image_url = f"http://localhost:7801/{generate_data['images'][0]}"
            print(f"Image URL: {image_url}")
        else:
            print("No images found in the response")
            exit()
    else:
        print(f"Failed to generate image, status code: {response.status_code}")
        print(response.text)
        exit()

# Step 3: Download the image using wget

    image_filename = f"{current_datetime}_{ model }_image.png"
    subprocess.run(["wget", image_url, "-O", image_filename])

    # Step 4: Display the image using Pillow
    image = Image.open(image_filename)
    image.show()
