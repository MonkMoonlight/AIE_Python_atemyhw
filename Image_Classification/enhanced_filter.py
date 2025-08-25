from PIL import Image, ImageFilter, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import os

# --------- Filters ---------
def filter_bw(img, threshold=128):
    """Pure black & white (binary) with a threshold."""
    gray = ImageOps.grayscale(img)
    bw = gray.point(lambda x: 255 if x >= threshold else 0, mode='L')
    return bw.convert("RGB")

def filter_sepia(img):
    """Classic warm sepia tone."""
    arr = np.array(img.convert("RGB")).astype(np.float32)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    tr = 0.393*r + 0.769*g + 0.189*b
    tg = 0.349*r + 0.686*g + 0.168*b
    tb = 0.272*r + 0.534*g + 0.131*b
    sep = np.clip(np.stack([tr, tg, tb], axis=-1), 0, 255).astype(np.uint8)
    return Image.fromarray(sep, mode="RGB")

def filter_posterize(img, bits=3):
    """Reduce color depth for a flat pop-art look."""
    return ImageOps.posterize(img.convert("RGB"), bits)

def filter_sketch(img):
    """Light pencil-sketch style via edges + grayscale blend."""
    gray = ImageOps.grayscale(img)
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges = ImageOps.invert(edges)
    sketch = ImageOps.autocontrast(Image.blend(gray, edges, alpha=0.5))
    return sketch.convert("RGB")

def filter_ripple(img, amplitude=6, wavelength=18):
    """Horizontal sine-wave ripple distortion."""
    arr = np.array(img.convert("RGB"))
    h, w = arr.shape[:2]
    out = np.empty_like(arr)
    y_idx = np.arange(h)
    # shift each row by a sine based on its y position
    shifts = (amplitude * np.sin(2 * np.pi * y_idx / max(1, wavelength))).astype(int)
    for y in range(h):
        out[y] = np.roll(arr[y], shifts[y], axis=0)  # roll along width
    return Image.fromarray(out, mode="RGB")

FILTERS = {
    # black & white
    "bw": filter_bw,
    # stylize / artistic
    "sepia": filter_sepia,
    "posterize": filter_posterize,
    "sketch": filter_sketch,
    # distortion
    "ripple": filter_ripple,
}

def apply_filter(image_path, filter_name, output_path):
    img = Image.open(image_path)
    # Example: small safety resize if you want consistent processing (optional)
    # img = img.resize((512, 512), Image.LANCZOS)

    if filter_name not in FILTERS:
        raise ValueError(f"Unknown filter '{filter_name}'. "
                         f"Choose from: {', '.join(FILTERS.keys())}")

    processed = FILTERS[filter_name](img)

    # Save using matplotlib so we preserve an axis-free image (like your original)
    plt.imshow(processed)
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

# --------- CLI loop ---------
if __name__ == "__main__":
    print("Image Filter Processor (type 'exit' to quit)\n")
    print("Available filters:")
    print("  bw  | sepia | posterize | sketch | ripple\n")

    while True:
        image_path = input("Enter image filename (or 'exit'): ").strip()
        if image_path.lower() == "exit":
            print("Goodbye!")
            break
        if not os.path.isfile(image_path):
            print(f"File not found: {image_path}")
            continue

        filter_name = input("Choose filter (bw/sepia/posterize/sketch/ripple): ").strip().lower()
        base, ext = os.path.splitext(image_path)
        ext = ext if ext else ".png"
        output_file = f"{base}_{filter_name}{ext}"

        try:
            apply_filter(image_path, filter_name, output_file)
            print(f"Processed image saved as '{output_file}'.")
        except Exception as e:
            print(f"Error: {e}")
