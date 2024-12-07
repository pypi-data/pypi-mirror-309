import os
from typing import List, Dict, Any
import requests
import fitz 
import json
from tqdm import tqdm
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import cycle
import re

class PDFProcessor:
    """
    Main class for processing PDFs through the Valyu AI pipeline.
    """
    
    def __init__(
        self,
        api: str = "https://srwrv3gxxfhxgnf3kfrnqqvx2u0kfouq.lambda-url.eu-west-2.on.aws/",
    ):
        """
        Initialize the PDF processor.

        Args:
            api: URL of the API Gateway endpoint
        """
        self.api = api
        self.batch_size = 5  # Fixed batch size as per requirements
        
        # Get API key from environment variable
        self.api_key = os.environ.get('VALYU_API_KEY')
        if not self.api_key:
            raise ValueError("VALYU_API_KEY environment variable not set")

    def process_folder(self, folder_path: str) -> Dict[str, Dict[str, Any]]:
        """
        Process all PDFs in a folder and save results to output.json.
        Format will be:
        {
            "pdf_name.pdf": {
                "pages": {
                    "1": { ... page 1 results ... },
                    "2": { ... page 2 results ... },
                    etc.
                },
                "total_pages": X
            }
        }
        """
        # Collect all images with their source PDF information
        all_images = []
        pdf_page_counts = {}
        total_pages = 0
        
        # Add progress bar for PDF loading
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        for filename in tqdm(pdf_files, desc="Loading PDFs"):
            pdf_path = os.path.join(folder_path, filename)
            # Get images as bytes
            images = self.convert_pdf_to_images(pdf_path)
            pdf_page_counts[filename] = len(images)
            # Convert bytes to base64 strings
            for page_num, img in enumerate(images, start=1):
                encoded_image = base64.b64encode(img).decode('utf-8')
                all_images.append({
                    'pdf_name': filename,
                    'page_num': page_num,
                    'image': encoded_image
                })
            total_pages += len(images)

        # Process all images in batches
        results = {}

        # Create batches and process
        batches = [all_images[i:i + self.batch_size] 
                   for i in range(0, len(all_images), self.batch_size)]
        
        # Split batches across 4 instances
        instance_batches = {i: [] for i in range(1, 5)}
        for batch, instance in zip(batches, cycle(range(1, 5))):
            instance_batches[instance].append(batch)

        # Process batches concurrently across instances
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Create futures for each instance's batches
            futures = []
            for instance, inst_batches in instance_batches.items():
                for batch in inst_batches:
                    futures.append(
                        executor.submit(self._process_batch, batch, instance)
                    )
            
            # Process results as they complete
            with tqdm(total=total_pages, desc="Processing pages") as pbar:
                for future in as_completed(futures):
                    batch_results = future.result()
                    # batch_results is a list of dicts with 'pdf_name', 'page_num', 'result'
                    pbar.update(len(batch_results))

                    # Update the results dictionary
                    for item in batch_results:
                        pdf_name = item['pdf_name']
                        page_num = str(item['page_num'])  # Use string as keys
                        result = item['result']

                        if pdf_name not in results:
                            results[pdf_name] = {
                                'pages': {},
                                'total_pages': pdf_page_counts[pdf_name]
                            }
                        results[pdf_name]['pages'][page_num] = result

        # Save results to output.json with nice formatting
        with open('output.json', 'w') as f:
            json.dump(results, f, indent=2, sort_keys=True)
        
        return results

    def _process_batch(self, images: List[Dict[str, Any]], instance: int) -> List[Dict[str, Any]]:
        """
        Process a batch of images.

        Args:
            images: List of dicts with 'pdf_name', 'page_num', 'image'
            instance: Instance number (1-4) to process this batch

        Returns:
            List of dicts with 'pdf_name', 'page_num', 'result'
        """
        # Extract the images from the list of dicts
        image_data = [img['image'] for img in images]

        # Prepare request payload
        payload = {
            'document': image_data,
            'instance': instance
        }

        # Prepare headers with API key
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }

        # Make API request
        response = requests.post(
            self.api,
            headers=headers,
            json=payload
        )

        # Raise exception for non-200 responses
        response.raise_for_status()

        # Get the results and clean them
        response_json = response.json()
        results = response_json['result']
        
        # Clean the results using regex to remove everything from first to last <|im_end|> token
        cleaned_results = []
        for result in results:
            # Find the first and last occurrence of <|im_end|>
            first_token = result.find('<|im_end|>')
            last_token = result.rfind('<|im_end|>')
            
            if first_token != -1 and last_token != -1:
                # Keep everything before first token and after last token
                cleaned_result = (
                    result[:first_token] + 
                    result[last_token + len('<|im_end|>'):]
                )
            else:
                cleaned_result = result
            
            cleaned_results.append(cleaned_result)
        results = cleaned_results

        # Now, we need to associate each result with the corresponding image's pdf_name and page_num
        # Assuming results is a list of results corresponding to each image in order
        batch_results = []
        for img_info, result in zip(images, results):
            batch_results.append({
                'pdf_name': img_info['pdf_name'],
                'page_num': img_info['page_num'],
                'result': result
            })

        return batch_results

    def convert_pdf_to_images(self, pdf_path: str) -> List[bytes]:
        """
        Convert PDF pages to images using PyMuPDF.
        
        Args:
            pdf_path: Path to the PDF file
        
        Returns:
            List of images as bytes
        """
        doc = fitz.open(pdf_path)
        images = []
        
        for page in doc:
            # Get the page as an image with 300 DPI resolution
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
            # Convert to PNG format in memory
            img_bytes = pix.tobytes("png")
            images.append(img_bytes)
        
        doc.close()
        return images 
