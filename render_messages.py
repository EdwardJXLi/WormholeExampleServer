import cv2
import numpy as np

from wormhole.utils import blend_frames, draw_multiline_text

def render_welcome_message(video):
    """
    Renders welcome message on the video.
    """
    
    # Constants
    BOX_WIDTH = 540
    BOX_HEIGHT = 740
    BOX_X_OFFSET = video.width-640
    BOX_Y_OFFSET = 24
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
        " | Original Source Material: [ /original ]",
        " | Low Quality Video Demo: [ /lowres ]",
        " | Grayscale (Simple Postprocessing) Demo: [ /grayscale ]",
        " | Inverted (Simple Postprocessing) Demo: [ /inverted ]",
        " | Advanced Video Postprocessing Demo: [ /postprocessing ]",
        " | Live Video Overlaying Demo: [ /overlay ]",
        " | Webcam Demo: (not available yet)",
        " | Video Proxying & Rebroadcasting Demo: [ /proxy ]",
        " | Custom Renderer Demo: [ /custom ]",
        " | Error Handling Demo: [ /error ]",
        " | Static Webpage Demo: [ /static ]",
        " | Source Code: [ /source ] or [ /github ]",
        "",
        "================================"
    ])
