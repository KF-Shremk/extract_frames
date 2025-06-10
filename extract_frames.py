import cv2
import os
import argparse

def extract_frames(video_path, output_folder, interval_frames, offset_frames):
    os.makedirs(output_folder, exist_ok=True)

    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video.set(cv2.CAP_PROP_POS_FRAMES, offset_frames)

    frame_count = offset_frames
    saved_count = 0

    while frame_count < total_frames:
        ret, frame = video.read()
        if not ret:
            print(f"⚠️ Skipping unreadable frame at {frame_count}")
            frame_count += 1
            continue

        if (frame_count - offset_frames) % interval_frames == 0:
            filename = os.path.join(output_folder, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Captured frame #{saved_count:04d} at frame {frame_count}")
            saved_count += 1

        frame_count += 1

    video.release()
    print(f"\n✅ Done! Extracted {saved_count} frames to '{output_folder}'")

def main():
    parser = argparse.ArgumentParser(description="Extract frames from a video at regular frame intervals.")
    parser.add_argument("-i", "--input", required=True, help="Path to input video file")
    parser.add_argument("-o", "--output", required=True, help="Output folder for extracted frames")
    parser.add_argument("--interval", type=int, default=30, help="Interval between frames (in frames)")
    parser.add_argument("--offset", type=int, default=0, help="Initial offset before first frame (in frames)")

    args = parser.parse_args()
    extract_frames(args.input, args.output, args.interval, args.offset)

if __name__ == "__main__":
    main()
