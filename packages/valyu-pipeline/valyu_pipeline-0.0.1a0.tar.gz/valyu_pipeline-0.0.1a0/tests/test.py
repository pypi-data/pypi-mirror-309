import boto3
import threading
import json
import base64
import time

# Initialize the SageMaker runtime client
sagemaker_runtime = boto3.client('sagemaker-runtime')

# Define the endpoint name
endpoint_name = 'OCR-Model-V14'

def send_request(batch_data):
    start_time = time.time()
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=json.dumps(batch_data)
    )
    result = response['Body'].read()
    end_time = time.time()
    print(f"Request completed in {end_time - start_time:.2f} seconds")
    print("Response:", result.decode('utf-8'))
    time.sleep(1)

# Function to read and encode images
def encode_images(image_paths):
    encoded_images = []
    for path in image_paths:
        with open(path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            encoded_images.append(encoded_string)
    return encoded_images

# Prepare 4 batches of image data (replace with your actual image paths)
batch1_images = ['image.png']
batch2_images = ['image.png']
batch3_images = ['image.png']
batch4_images = ['image.png']    

# Encode images for each batch
batch1 = {'images': encode_images(batch1_images)}
batch2 = {'images': encode_images(batch2_images)}
batch3 = {'images': encode_images(batch3_images)}
batch4 = {'images': encode_images(batch4_images)}

# Use threading to send requests in parallel
threads = []
for batch in [batch1, batch2, batch3, batch4]:
    t = threading.Thread(target=send_request, args=(batch,))
    threads.append(t)
    t.start()
    # time.sleep(2)  # Add 1-second delay between starting threads

# Wait for all threads to finish
for t in threads:
    t.join()