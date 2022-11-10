#
# Wormhole Video Streaming
#

# Import Libraries
import argparse
import cv2
import numpy as np

from wormhole import Wormhole
from wormhole.utils import (
    render_fraps_fps, 
    render_debug_info, 
    render_watermark, 
    blend_frames,
    draw_multiline_text)


def main():
    """
    Main start function for Wormhole Demo Server
    """
    
    parser = argparse.ArgumentParser(description='Wormhole Video Streaming')
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--video', type=str, default='video.webm')
    args = parser.parse_args()

    server = Wormhole(host = args.host, port = args.port, debug = args.debug)
    server.stream(args.video, 
                  print_video_fps=True, 
                  frame_modifiers=[render_fraps_fps, 
                                   render_debug_info, 
                                   render_watermark,
                                   render_welcome_message])
    
    server.join()


def render_welcome_message(video):
    """
    Renders welcome message on the video.
    """
    
    # Constants
    BOX_WIDTH = 540
    BOX_HEIGHT = 400
    BOX_X_OFFSET = video.width-640
    BOX_Y_OFFSET = video.height-480
    BOX_MARGIN = 10

    # Render a dark box around the message
    dark_rectangle = np.copy(video._frame)
    cv2.rectangle(
        dark_rectangle, 
        (BOX_X_OFFSET-BOX_MARGIN, BOX_Y_OFFSET-BOX_MARGIN),
        (BOX_X_OFFSET+BOX_WIDTH+BOX_MARGIN, BOX_Y_OFFSET+BOX_HEIGHT+BOX_MARGIN),
        (0,0,0), -1)
    blend_frames(video._frame, dark_rectangle)
    
    # Render The Text
    from wormhole.version import __version__
    draw_multiline_text(video._frame, video.width, video.height, (BOX_X_OFFSET, BOX_Y_OFFSET), [
        "========================================",
        "> Welcome to the Wormhole Realtime Video Streaming Demo! <",
        "========================================",
        "https://github.com/EdwardJXLi/Wormhole",
        "https://github.com/EdwardJXLi/WormholeExampleServer",
        "========================================",
        "",
        "Everything here, dynamic and static, is powered by Wormhole.",
        "From video loading, processing, rendering, and streaming",
        "Wormhole is simple and hackable realtime",
        "video streaming engine for prototypes and projects alike!",
        "",
        "> NOTE: A better and more robust demo is in the works,",
        "> with fully interactive elements and more.",
        "> Visit the github for more information!",
        "",
        "In the meanwhile, these following links",
        "showcase the capabilities of Wormhole:",
        "",
        ">> Demo Links <<",
        "(Add these to the end of the current url)",
        " | Original Source Material: [ (url)/original ]",
        " | Video Postprocessing Demo: [ /postprocessing ]",
        " | Webcam Demo: (not available yet)",
        " | Video Proxying & Rebroadcasting Demo: [ /proxy ]",
        " | Custom Renderer Demo: [ /custom ]",
        " | Source Code: [ /source ] or [ /github ]",
        "",
        "================================"
    ])

if __name__ == '__main__':
    main()
