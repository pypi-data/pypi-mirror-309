import os
from typing import List, Dict, Any, Optional
import requests
import fitz 
import json
from tqdm import tqdm
import base64

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
        pdf_image_counts = {}
        total_pages = 0
        
        # Add progress bar for PDF loading
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        for filename in tqdm(pdf_files, desc="Loading PDFs"):
            pdf_path = os.path.join(folder_path, filename)
            # Get images as bytes
            images = self.convert_pdf_to_images(pdf_path)
            # Convert bytes to base64 strings
            encoded_images = [base64.b64encode(img).decode('utf-8') for img in images]
            pdf_image_counts[filename] = len(encoded_images)
            all_images.extend(encoded_images)
            total_pages += len(images)

        # Process all images in batches
        results = {}
        current_pdf = None
        current_page = 0
        processed_images = 0

        # Create batches and process
        batches = [all_images[i:i + self.batch_size] 
                  for i in range(0, len(all_images), self.batch_size)]
        
        # Process batches with progress bar showing total pages
        with tqdm(total=total_pages, desc="Processing pages") as pbar:
            for batch in batches:
                batch_results = self._process_batch(batch)
                pbar.update(len(batch))
                
                # Handle the batch results - ensure it's a list
                if isinstance(batch_results, dict) and 'result' in batch_results:
                    # If single result is wrapped in dict
                    batch_results = [batch_results['result']]
                elif isinstance(batch_results, list):
                    # If list of results, extract 'result' from each if needed
                    batch_results = [r['result'] if isinstance(r, dict) and 'result' in r else r 
                                   for r in batch_results]
                
                # For each result in the batch
                for batch_result in batch_results:
                    # Each batch result contains multiple pages
                    for page_result in batch_result:
                        processed_images += 1
                        
                        # Find which PDF this result belongs to
                        images_so_far = 0
                        for pdf_name, image_count in pdf_image_counts.items():
                            if processed_images <= images_so_far + image_count:
                                # Initialize new PDF in results if needed
                                if pdf_name != current_pdf:
                                    current_pdf = pdf_name
                                    current_page = 0
                                    if pdf_name not in results:
                                        results[pdf_name] = {
                                            "pages": {},
                                            "total_pages": image_count
                                        }
                                
                                # Increment page counter and store individual result
                                current_page += 1
                                results[current_pdf]["pages"][str(current_page)] = page_result
                                break
                            images_so_far += image_count

        # Save results to output.json with nice formatting
        with open('output.json', 'w') as f:
            json.dump(results, f, indent=2, sort_keys=True)
        
        return results

    def _process_batch(self, images: List[bytes]) -> List[Dict[str, Any]]:
        """
        Process a batch of images.

        Args:
            images: List of base64 encoded images to process

        Returns:
            List of processing results
        """
        # Prepare request payload
        payload = {
            'document': images
        }
        
        # Calculate and log payload size
        import sys
        import json
        payload_json = json.dumps(payload)
        size_mb = sys.getsizeof(payload_json) / (1024 * 1024)  # Convert to MB
        print(f"Request payload size: {size_mb:.2f} MB")
        
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
        
        return response.json()

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