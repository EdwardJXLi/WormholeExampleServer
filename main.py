#
# Wormhole Video Streaming
#

# Import Libraries
import argparse
import cv2
import numpy as np

from wormhole import Wormhole
from wormhole.streamer import MJPEGStreamer
from wormhole.video import FileVideo, SoftCopy, HardCopy
from wormhole.utils import (
    render_fraps_fps, 
    render_full_fps,
    render_debug_info, 
    render_watermark)

# Move message rendering to another file to save space
from render_messages import render_welcome_message


def main():
    """
    Main start function for Wormhole Demo Server
    """
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Wormhole Video Streaming')
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--video', type=str, default='video.webm')
    args = parser.parse_args()

    # Create Wormhole Instance
    server = Wormhole(host = args.host, port = args.port, debug = args.debug, welcome_screen = False)
    
    """
    Stream Main Video Stream
    """
    
    server.stream(
        args.video, 
        print_video_fps=True, 
        frame_modifiers=[
            render_fraps_fps, 
            render_debug_info, 
            render_watermark,
            render_welcome_message])
    
    # This creates an alias to the "managed" default video stream.
    server.create_stream(MJPEGStreamer, server.managed_streams.get("default", (None,))[0], '/')
    
    # Load Video From File
    # The reason why we dont use this above is because
    # I'm trying to show the basic server.stream method
    # of streaming a video file. Everything down here 
    # are more advanced features that Wormhole supports.
    video = FileVideo(args.video)
    
    """
    Stream Original Video
    """
    
    # This is all the code needed to stream to a custom url!
    # Raw unprocessed video stream as simple as that!
    server.create_stream(MJPEGStreamer, video, '/original')
    
    """
    Low Resolution Stream Demo
    """
    
    # Here, we create a realtime "Hard Copy" of the original video.
    # This creates a brand new video thread that implements its own 
    # frame rate controller, with frames being pulled directly from 
    # the original video.
    # We use this to create a low resolution and frame rate copy of
    # the original stream.
    lowres_video = HardCopy(video, 640, 360, max_fps=1, frame_modifiers = [render_full_fps, render_fraps_fps])
    
    # Here, we stream with custom imencode configs passed to the MJPEGStreamer.
    # In this instance, we are significantly dropping the quality of the video
    # to add to the crusty:tm: feel.
    server.create_stream(MJPEGStreamer, lowres_video, '/lowres', imencode_config=[cv2.IMWRITE_JPEG_QUALITY, 5])
    
    """
    Postprocessed Video Streams - Grayscale
    """
    
    # Here is where the fun starts.
    # Wormhole supports many advanced postprocessing features.
    
    # Here, we create a basic filter
    def grayscale_filter(video):
        cv2.cvtColor(video._frame, cv2.COLOR_BGR2GRAY)
    
    # then, we create a realtime "Soft Copy" of the original video
    # so that any modifications dont modify the original
    # Soft copies are realtime copies of the original video using
    # frame subscribes and publishers. This is better for light weight video modifications
    grayscale_video = SoftCopy(video, frame_modifiers = [render_debug_info, render_fraps_fps, grayscale_filter])
    server.create_stream(MJPEGStreamer, grayscale_video, '/grayscale')
    
    """
    Postprocessed Video Streams - Inverted
    """
    
    # Here is another example of a video filter. This one is applied during runtime!
    # (After initializing the video stream)
    def invert_filter(video):
        video._frame = (255 - video._frame)
        
    inverted_video = SoftCopy(video, frame_modifiers = [render_debug_info, render_fraps_fps]) 
    server.create_stream(MJPEGStreamer, inverted_video, '/inverted')
    # This filter is added in realtime!
    inverted_video.add_frame_modifier(invert_filter)
    
    """
    Advanced Postprocessed Video Streams
    """
    
    # Here is an example of a computationally heavy postprocessed video stream
    from advanced_video_effect import circle_video_filter, wavy_image_filter
    
    # We first create a hard copy of the video with half the resolution
    # This makes it so that the video is somewhat useable.
    postprocessing_test_video = HardCopy(video, video.width//2, video.height//2, frame_modifiers = [circle_video_filter, wavy_image_filter, render_debug_info, render_fraps_fps]) 
    server.create_stream(MJPEGStreamer, postprocessing_test_video, '/postprocessing')
    
    # Join server thread to keep process alive
    server.join()

if __name__ == '__main__':
    main()
