import cv2
import numpy as np
import os
import argparse

def inpaint_images(input_folder, output_folder, top_left, bottom_right):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(input_folder, filename)
        img = cv2.imread(path)

        if img is None:
            print(f"[!] Skipped (couldn't load): {filename}")
            continue

        # Create binary mask
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv2.rectangle(mask, top_left, bottom_right, 255, -1)

        # Inpaint
        inpainted = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
        out_path = os.path.join(output_folder, filename)
        cv2.imwrite(out_path, inpainted)

        print(f"[✓] Inpainted: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove static watermark or text using inpainting.")
    parser.add_argument("input_folder", help="Path to folder with input images")
    parser.add_argument("output_folder", help="Path to folder where processed images will be saved")
    parser.add_argument("--x1", type=int, required=True, help="Top-left x of the text area")
    parser.add_argument("--y1", type=int, required=True, help="Top-left y of the text area")
    parser.add_argument("--x2", type=int, required=True, help="Bottom-right x of the text area")
    parser.add_argument("--y2", type=int, required=True, help="Bottom-right y of the text area")

    args = parser.parse_args()
    top_left = (args.x1, args.y1)
    bottom_right = (args.x2, args.y2)

    inpaint_images(args.input_folder, args.output_folder, top_left, bottom_right)
