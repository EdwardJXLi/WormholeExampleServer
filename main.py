#
# Wormhole Video Streaming
#

# Import Libraries
import argparse
import cv2
import numpy as np
import math

from wormhole import Wormhole
from wormhole.streamer import MJPEGStreamer
from wormhole.video import FileVideo, SoftCopy, HardCopy, CustomVideo
from wormhole.utils import (
    render_fraps_fps, 
    render_full_fps,
    render_debug_info, 
    render_watermark,
    draw_overlay,
    blend_frames,
    draw_text)

# Move message rendering to another file to save space
from render_messages import (
    render_welcome_message,
    render_low_res_message,
    render_grayscale_message,
    render_inverted_message,
    render_advanced_message,
    render_overlay_message,
    render_webcam_message,
    render_proxy_message,
    render_custom_message
)


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
    
    """
    Load Video From File
    """
     
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
    lowres_video = HardCopy(video, 640, 360, max_fps=1, frame_modifiers = [render_full_fps, render_fraps_fps, render_low_res_message])
    
    # Here, we stream with custom imencode configs passed to the MJPEGStreamer.
    # In this instance, we are significantly dropping the quality of the video
    # to add to the crusty:tm: feel.
    server.create_stream(MJPEGStreamer, lowres_video, '/lowres', imencode_config=[cv2.IMWRITE_JPEG_QUALITY, 50])
    
    """
    Postprocessed Video Streams - Grayscale
    """
    
    # Here is where the fun starts.
    # Wormhole supports many advanced postprocessing features.
    
    # Here, we create a basic filter
    def grayscale_filter(video):
        video._frame = cv2.cvtColor(video._frame, cv2.COLOR_BGR2GRAY)
        video._frame = cv2.cvtColor(video._frame, cv2.COLOR_GRAY2BGR)  # Make sure image is still 3 channel
    
    # then, we create a realtime "Soft Copy" of the original video
    # so that any modifications dont modify the original
    # Soft copies are realtime copies of the original video using
    # frame subscribes and publishers. This is better for light weight video modifications
    grayscale_video = SoftCopy(video, frame_modifiers = [render_debug_info, render_fraps_fps, grayscale_filter, render_grayscale_message])
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
    inverted_video.add_frame_modifier(render_inverted_message)
    
    """
    Advanced Postprocessed Video Streams
    """
    
    # Here is an example of a computationally heavy postprocessed video stream
    from advanced_video_effect import circle_video_filter, wavy_image_filter
    
    # We first create a hard copy of the video with half the resolution
    # This makes it so that the video is somewhat useable.
    # postprocessing_test_video = HardCopy(
    #     video, 
    #     video.width//2, 
    #     video.height//2, 
    #     frame_modifiers = [
    #         circle_video_filter, 
    #         wavy_image_filter, 
    #         render_debug_info, 
    #         render_fraps_fps,
    #         render_advanced_message
    #     ]) 
    # server.create_stream(MJPEGStreamer, postprocessing_test_video, '/postprocessing')
    
    """
    Video Overlaying Demo
    """
    
    # In this example, we are drawing two other live video feeds on top of the original video.
    # This is done by creating a new video stream that is a hard copy of the original video.
    # and adding frame modifiers that will draw on top of the original video.
    
    # Here is a helper function that will draw a video feed on top of the original video.
    def render_overlay_feeds(video):
        # In this example, we will the grayscale and inverted video feeds
        grayscale_frame = grayscale_video.get_frame()
        inverted_frame = inverted_video.get_frame()
        
        # First, overlay the grayscale video with a moving offset
        draw_overlay(
            video._frame, 
            grayscale_frame, 
            (video.width//4 + int(math.sin(video.frame_controller.frames_rendered/10)*video.width//8), 32), 
            (video.width//4, video.height//4))
        
        # Draw Description Text
        draw_text(video._frame, "Moving Video Demo", (video.width//4, 300), font_size=2)
        
        # Then, draw the inverted video with a transparency
        # Render the watermark onto a copy of the frame
        transparent_frame = draw_overlay(video._frame.copy(), inverted_frame, (video.width//4, 440), (video.width//4, video.height//4))

        # Render the watermark with the new width and height
        blend_frames(video._frame, transparent_frame, transparency=0.2)
        
        # Draw Description Text
        draw_text(video._frame, "Transparent Video Demo", (video.width//4, 700), font_size=2)

    # Here we create a hard copy of the original video
    overlay_video = HardCopy(
        video, 
        video.width, 
        video.height, 
        frame_modifiers = [
            render_overlay_feeds,
            render_debug_info, 
            render_fraps_fps,
            render_overlay_message])
    server.create_stream(MJPEGStreamer, overlay_video, '/overlay')
    
    """
    Webcam Demo
    """
    
    # TODO
    
    """
    Video Proxying Demo
    """
    
    # TODO
    
    """
    Custom Video Demo
    """
    
    # Here, we dont use any video source. We generate new image frames during runtime!
    
    # Here is a helper function that will generate a new image frame
    # def frame_generator(video):
    #     new_frame = np.zeros((video.height, video.width, 3), np.uint8)
    #     new_frame[:] = (video.frame_controller.frames_rendered % 196, 255, 255)
    #     new_frame = cv2.cvtColor(new_frame, cv2.COLOR_HSV2BGR)
        
    #     video.set_frame(new_frame)

    # custom_video = CustomVideo(1920, 804, 100, frame_generator, frame_modifiers = [
    #     render_debug_info, 
    #     render_fraps_fps,
    #     render_custom_message
    # ])
    # server.create_stream(MJPEGStreamer, custom_video, '/custom')
    
    """
    Error Handling Demo
    """
    
    # Things don't always go to plan! Here is an example of an error while generating frames
    def error_generator(video):
        raise Exception("This Is A Test Error! "
                        "This error is intentional and is used to demonstrate error handling. "
                        "In this example, Wormhole gracefully captures the error "
                        "and continues processing all other video streams with no issues.")

    # Wormhole gracefully handles such error and continues on with all other streams
    error_video = CustomVideo(1920, 804, 100, error_generator)
    server.create_stream(MJPEGStreamer, error_video, '/error')
    
    """
    Static Webpage Demo
    """
    
    # Here is a basic example of serving a static webpage through Wormhole.
    # It's not too exciting, but it's a good starting point for more complex webpages.
    def serve_static():
        return "This is just a plain static page hosted with Flask. " \
               "The only difference is that this is served through the " \
               "Wormhole network server."

    server.controller.add_route("/static", serve_static, methods=["GET"], strict_slashes=False)
    
    """
    Redirect to Github Page
    """
    
    # Here, we use some more advanced flask routing features
    # to redirect users to the source code of Wormhole
    from flask import redirect
    
    def serve_source():
        return redirect("https://github.com/EdwardJXLi/Wormhole")

    server.controller.add_route("/source", serve_source, methods=["GET"], strict_slashes=False)
    server.controller.add_route("/github", serve_source, methods=["GET"], strict_slashes=False)
    
    """
    Generate (hidden) debug page
    """
    
    # Cool debug page thats not publicly listed. Should be safe, i think...
    def serve_debug():
        return server.generate_debug_html()

    server.controller.add_route("/debug", serve_debug, methods=["GET"], strict_slashes=False)
    
    # Join server thread to keep process alive
    server.join()

if __name__ == '__main__':
    main()
