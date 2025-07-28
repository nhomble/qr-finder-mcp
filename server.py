#!/usr/bin/env uv run

from typing import List, Dict, Any
import cv2
import pyautogui
import time
import os
import logging
from mcp.server.fastmcp import FastMCP

name = "qr-finder"
name_mcp = f"{name}-mcp"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"/tmp/{name_mcp}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(name_mcp)

# Initialize the FastMCP server
logger.info("Initializing FastMCP server...")
mcp = FastMCP(name)
logger.info("FastMCP server initialized successfully")

@mcp.tool()
def take_screenshot() -> str:
    """
    Captures a screenshot of the full desktop and returns the local file path to the saved image.

    Returns:
        The absolute path to the saved screenshot PNG file.
    """
    logger.info("take_screenshot tool called")
    try:
        # Generate a unique filename with timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        file_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
        
        logger.info(f"Taking screenshot, saving to: {file_path}")
        
        # Capture and save the screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        
        logger.info(f"Screenshot saved successfully: {file_path}")
        return os.path.abspath(file_path)
    except Exception as e:
        logger.error(f"Error taking screenshot: {e}")
        raise

@mcp.tool()
def find_qr_locations(image_path: str) -> List[Dict[str, Any]]:
    """
    Detects QR codes in the given image and returns their locations.

    Args:
        image_path: The local file path to the image (e.g., '/path/to/image.png').

    Returns:
        A list of dictionaries, each containing:
        - 'points': List of four [x, y] coordinates representing the bounding box corners.
        - 'decoded_text': The decoded QR content if successful, or None if decoding failed.
    If no QR codes are found, returns an empty list.
    """
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        return []  # Return empty list if image can't be loaded

    # Create QR Code Detector
    qcd = cv2.QRCodeDetector()

    # Detect and decode multiple QR codes
    retval, decoded_info, points, _ = qcd.detectAndDecodeMulti(img)

    if not retval:
        return []  # No QR codes detected

    # Prepare results
    results = []
    for i, point_set in enumerate(points):
        decoded = decoded_info[i] if decoded_info[i] else None
        results.append({
            'points': point_set.tolist(),  # Convert numpy array to list of [x, y] pairs
            'decoded_text': decoded
        })

    return results

# Run the server
if __name__ == "__main__":
    logger.info("Starting FastMCP server...")
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Error running MCP server: {e}")
        raise
