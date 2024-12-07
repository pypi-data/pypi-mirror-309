import requests
import json
import base64

def invoke_lambda(image_path):
    LAMBDA_URL = "https://srwrv3gxxfhxgnf3kfrnqqvx2u0kfouq.lambda-url.eu-west-2.on.aws/"

    # Load and encode the image
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    # Prepare payload
    payload = {
        "document": [image_base64]
    }

    # Make request to Lambda URL
    response = requests.post(LAMBDA_URL, json=payload)
    
    # Print status code and response
    print(f"Status Code: {response.status_code}")
    print("\nResponse:")
    print(json.dumps(response.json(), indent=2))

    return response.json()

if __name__ == "__main__":
    # Replace with your image path
    image_path = "image.png"
    invoke_lambda(image_path) 