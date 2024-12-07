import chromadb
import os
from chromadb.utils.embedding_functions.open_clip_embedding_function import (
    OpenCLIPEmbeddingFunction,
)
from chromadb.utils.data_loaders import ImageLoader
from PIL import Image
import numpy as np


CHROMADB_DATA_DIR = os.getenv("CHROMADB_DATA_DIR", "./chroma")

IMAGE_PATHS = [
    "/Users/phillipdupuis/Pictures/2024/2024-07-27/IMG_3123.JPG",
    "/Users/phillipdupuis/Pictures/2024/2024-07-27/IMG_3135.JPG",
]


def load_image(path: str):
    """
    Load image using PIL (better for standard image loading)

    :param image_path: Path to PNG file
    :return: numpy array
    """
    # Open the image
    image = Image.open(path)
    # Convert to RGB if necessary
    if image.mode != "RGB":
        image = image.convert("RGB")
    # Convert to numpy array
    return np.array(image)


def add_images():
    embedding_function = OpenCLIPEmbeddingFunction()
    data_loader = ImageLoader()
    client = chromadb.PersistentClient(path=CHROMADB_DATA_DIR)
    collection = client.get_or_create_collection(
        "images", embedding_function=embedding_function, data_loader=data_loader
    )
    collection.add(
        ids=IMAGE_PATHS,
        images=[load_image(path) for path in IMAGE_PATHS],
    )


if __name__ == "__main__":
    add_images()
