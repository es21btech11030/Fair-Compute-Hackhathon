# fair_compute_llava_gui.py

import tkinter as tk
from tkinter import filedialog
import requests
import base64

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read())
    return encoded_string.decode('utf-8')

def send_request_to_llava(encoded_image):
    endpoint_url = "http://8.12.5.48:11434/api/generate"
    print(encoded_image)
    payload = {
        "model": "llava:7b-v1.6-mistral-q5_K_M",
        "prompt": "What is in this picture?",
        "stream": False,
        "images": [encoded_image]


    }
    try:
        response = requests.post(endpoint_url, json=payload)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        encoded_image = encode_image_to_base64(file_path)
        result = send_request_to_llava(encoded_image)
        if "error" in result:
            result_text.delete(1.0, tk.END)  # Clear previous result
            result_text.insert(tk.END, "Error: " + result["error"])
        else:
            result_text.delete(1.0, tk.END)  # Clear previous result
            result_text.insert(tk.END, str(result))

# Create the GUI
root = tk.Tk()
root.title("Fair Compute Llava Image Analysis")

upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack()

result_text = tk.Text(root, height=10, width=50)
result_text.pack()

root.mainloop()