"""
batch_extract.py
================
Extract frames from all videos in videos/ folder.
Automatically handles hammer, screwdriver, wrench folders.
"""

import cv2
from pathlib import Path

# ============================================================================
# SETTINGS - Adjust these as needed
# ============================================================================

FRAMES_PER_VIDEO = 200          # How many frames to extract per video
ROTATE_FRAMES = True            # Set to False if rotation not needed
VIDEOS_FOLDER = Path("videos")  
OUTPUT_FOLDER = Path("dataset")


# ============================================================================
# MAIN EXTRACTION
# ============================================================================

def extract_frames(video_path, output_folder, num_frames=200):
    """Extract evenly-spaced frames from a video."""
    
    cap = cv2.VideoCapture(str(video_path))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames == 0:
        print(f"    ❌ Error: No frames found in video")
        cap.release()
        return 0
    
    # Calculate which frames to extract (evenly spaced)
    if total_frames < num_frames:
        frame_indices = list(range(total_frames))
    else:
        step = total_frames / num_frames
        frame_indices = [int(i * step) for i in range(num_frames)]
    
    # Extract and save frames
    saved = 0
    video_name = video_path.stem  # e.g., "video1" from "video1.mp4"
    
    for frame_num in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        success, frame = cap.read()
        
        if success:
            # Rotate if needed
            if ROTATE_FRAMES:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            
            # Save with unique name: {video_name}_{frame_number}.png
            output_file = output_folder / f"{video_name}_{saved:04d}.png"
            cv2.imwrite(str(output_file), frame)
            saved += 1
            
            # Progress indicator every 50 frames
            if saved % 50 == 0:
                print(f"    Progress: {saved}/{num_frames} frames")
    
    cap.release()
    return saved


def main():
    """Process all videos in hammer, screwdriver, and wrench folders."""
    
    print("="*70)
    print("BATCH FRAME EXTRACTION")
    print("="*70)
    print(f"\nSettings:")
    print(f"  Frames per video: {FRAMES_PER_VIDEO}")
    print(f"  Rotation: {'Enabled' if ROTATE_FRAMES else 'Disabled'}")
    print()
    
    # Check if videos folder exists
    if not VIDEOS_FOLDER.exists():
        print(f"❌ Error: '{VIDEOS_FOLDER}' folder not found!")
        return
    
    # Find all videos organized by object
    objects = ['hammer', 'screwdriver', 'wrench']
    videos_found = {}
    
    for obj in objects:
        obj_folder = VIDEOS_FOLDER / obj
        if obj_folder.exists():
            # Find all video files (.mp4, .avi, .mov, etc.)
            videos = list(obj_folder.glob("*.mp4")) + \
                     list(obj_folder.glob("*.MP4")) + \
                     list(obj_folder.glob("*.avi")) + \
                     list(obj_folder.glob("*.mov"))
            
            if videos:
                videos_found[obj] = sorted(videos)
    
    # Show what was found
    if not videos_found:
        print("❌ No videos found in any object folder!")
        print("\nMake sure you have videos in:")
        print("  videos/hammer/")
        print("  videos/screwdriver/")
        print("  videos/wrench/")
        return
    
    total_videos = sum(len(vids) for vids in videos_found.values())
    print(f"Found {total_videos} video(s):")
    for obj, videos in videos_found.items():
        print(f"  • {obj}: {len(videos)} video(s)")
    print()
    
    # Process each object's videos
    total_frames = 0
    
    for obj_name, videos in videos_found.items():
        print(f"{'='*70}")
        print(f"Processing: {obj_name.upper()}")
        print(f"{'='*70}")
        
        # Create output folder for this object
        output_folder = OUTPUT_FOLDER / obj_name
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Process each video
        for i, video_path in enumerate(videos, 1):
            print(f"\n[{i}/{len(videos)}] {video_path.name}")
            
            frames_saved = extract_frames(
                video_path, 
                output_folder, 
                FRAMES_PER_VIDEO
            )
            
            print(f"    ✓ Saved {frames_saved} frames")
            total_frames += frames_saved
        
        print()
    
    # Summary
    print("="*70)
    print("EXTRACTION COMPLETE")
    print("="*70)
    print(f"Total videos processed: {total_videos}")
    print(f"Total frames extracted: {total_frames}")
    print(f"\nFrames saved to: {OUTPUT_FOLDER}/")
    for obj in videos_found.keys():
        print(f"  • {OUTPUT_FOLDER}/{obj}/")
    print("="*70)


if __name__ == "__main__":
    main()
