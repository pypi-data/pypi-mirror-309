# mytool.py
import argparse
from colorama import Style, Fore, Back
import keyboard
from moviepy.editor import VideoFileClip
import numpy as np
import os
from os import getcwd


def add_motion_blur(clip, blur_strength=9):
    """
    Apply a motion blur effect by blending multiple frames for each frame in the clip.
    
    Parameters:
    clip (VideoFileClip): The video clip to apply the motion blur to.
    blur_strength (int): The number of frames to blend together.
    
    Returns:
    VideoFileClip: The video clip with the motion blur effect.
    """
    
    def blur_frame(t):
        """Generate a motion blur effect by averaging frames."""
        frame_list = []
        
        # Add frames before and after the current time
        for offset in range(blur_strength):
            frame_time = max(0, t - offset / clip.fps)  # Time of previous frames
            frame = clip.get_frame(frame_time)
            frame_list.append(frame)
        
        # Average the frames to create a blur effect
        blurred_frame = np.mean(frame_list, axis=0).astype(np.uint8)
        return blurred_frame
    
    # Create a new clip by applying the blur to each frame
    new_clip = clip.fl(lambda gf, t: blur_frame(t), apply_to=['video'])
    
    return new_clip

def render(name, amount):
    """Render

    Args:
        name (str): file name
        amount (int): blur amount
    """
    # Example usage
    # input_video = "to.mp4"
    # output_video = "output_blurred_video.mp4"

    input_video = f"{getcwd()}/{name}"
    output_video = f"{getcwd()}/output_{name}"

    clip = VideoFileClip(input_video)

    # Apply the motion blur
    blurred_clip = add_motion_blur(clip, blur_strength=amount)

    # Write the output video with motion blur
    blurred_clip.write_videofile(output_video, codec='libx264', fps=clip.fps)

def greet(name):
    print(f"Hello, {name}!")

def main():
    parser = argparse.ArgumentParser(
        description="Prismio: A custom CLI tool with multiple commands",
        usage="prismio <command> [options]"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add a "greet" command
    greet_parser = subparsers.add_parser("greet", help="Greet a user by name")
    greet_parser.add_argument("name", type=str, help="The name of the person to greet")

    render_parser = subparsers.add_parser("render", help="Render a video With blur-amount")
    render_parser.add_argument("filename", type=str, help="The file / vid path it has to be in your cd")
    render_parser.add_argument("amount", type=int, help="Amount recommended 1 to 8")


    # Add a "version" command
    version_parser = subparsers.add_parser("version", help="Show the version of MyTool")

    # Parse the command-line arguments
    args = parser.parse_args()

    if args.command == "greet":
        greet(args.name)
    elif args.command == "render":
        print(Fore.GREEN + "trying to Render" + Style.RESET_ALL)
        render(args.filename, args.amount)
        print("file rendered")
    elif args.command == "version":
        print("MyTool version 1.0")
    else:
        parser.print_help()  # Show help if no command is provided

if __name__ == "__main__":
    main()
