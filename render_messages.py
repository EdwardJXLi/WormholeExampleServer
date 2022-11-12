import cv2
import numpy as np

from wormhole.utils import blend_frames, draw_multiline_text

def render_welcome_message(video):
    """
    Renders welcome message on the video.
    """
    
    # Constants
    BOX_MARGIN = 10
    BOX_WIDTH = 540
    BOX_HEIGHT = video.height - 24*2
    BOX_X_OFFSET = video.width-640
    BOX_Y_OFFSET = 24

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
        " | Video Proxying & Rebroadcasting Demo: (WIP)",
        " | Custom Renderer Demo: [ /custom ]",
        " | Error Handling Demo: [ /error ]",
        " | Static Webpage Demo: [ /static ]",
        " | Source Code: [ /source ] or [ /github ]",
        "",
        "All streams shown above are processed, rendered, and served",
        "all from the same Wormhole instance.",
        "",
        "================================"
    ])

    
def render_low_res_message(video):
    """
    Renders description for the low res video feed.
    """
    
    # Constants
    BOX_MARGIN = 10
    BOX_WIDTH = 240
    BOX_HEIGHT = 360
    BOX_X_OFFSET = 360
    BOX_Y_OFFSET = 10

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
        "================",
        "Low Resolution Video Demo",
        "================",
        "",
        "This is one of many demos",
        "of Wormhole' realtime",
        "video manipulation.",
        "",
        "Video frames from",
        "the source video are being",
        "resized and reformatted",
        "to fit a low bitrate.",
        "",
        "================"
    ])

def render_grayscale_message(video):
    """
    Renders description for the grayscale video feed.
    """
    
    # Constants
    BOX_MARGIN = 10
    BOX_WIDTH = 540
    BOX_HEIGHT = 280
    BOX_X_OFFSET = video.width-640
    BOX_Y_OFFSET = 24

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
        "> Wormhole Grayscale Video Demo <",
        "========================================",
        "",
        "This demo shows Wormhole's real-time ",
        "video manipulation using the frame_modifiers.",
        "In this case, raw frames from the source video",
        "are edited and modified in realtime to be grayscale.",
        "",
        "This is just one of the many demos showcasing Wormhole's",
        "real-time video processing and manipulation.",
        "",
        "Go to [ / ] to check out other examples!",
        "",
        "========================================"
    ])
    # This demo shows Wormhole's realtime video manipulation using the frame_modifiers feature. In this case, frames from the source video are being manipulated in realtime to be grayscale.
    # This is just one of the many demos showcasing Wormhole's real-time video processing and manipulation.

def render_inverted_message(video):
    """
    Renders description for the inverted video feed.
    """
    
    # Constants
    BOX_MARGIN = 10
    BOX_WIDTH = 540
    BOX_HEIGHT = 200
    BOX_X_OFFSET = video.width-640
    BOX_Y_OFFSET = 24

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
        "> Wormhole Inverted Video Demo <",
        "========================================",
        "",
        "Here is another example of Wormhole's",
        "realtime video manipulation.",
        "",
        "Go to [ / ] to check out other examples!",
        "",
        "========================================"
    ])

def render_advanced_message(video):
    """
    Renders description for the advanced video feed.
    """
    
    # Constants
    BOX_MARGIN = 12
    BOX_WIDTH = 460
    BOX_HEIGHT = video.height - BOX_MARGIN * 2
    BOX_X_OFFSET = video.width-490
    BOX_Y_OFFSET = 12

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
        "==================================",
        "> Wormhole Advanced Video Postprocessing Demo <",
        "==================================",
        "",
        "Here's an example of advanced video processing with",
        "Wormhole's video pipeline. Raw frames from the",
        "source video are first into both circle and wave",
        "filters, both tasks requiring advanced processing.",
        "",
        "With computationally heavy tasks like this, we can see",
        "how Wormhole handles both heavy and light video",
        "processing tasks simultaneously with ease.",
        "",
        "This showcase demonstrates some cool video effects,",
        "but this could very well be AI Annotation output",
        "and other advanced video processing tasks.",
        "",
        "Go to [ / ] to check out other examples!",
        "",
        "=================================="
    ])
    
def render_overlay_message(video):
    """
    Renders description for the video overlaying feed.
    """
    
    # Constants
    BOX_MARGIN = 10
    BOX_WIDTH = 540
    BOX_HEIGHT = 440
    BOX_X_OFFSET = video.width-640
    BOX_Y_OFFSET = 24

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
        "> Wormhole Real-time Video Overlay Demo <",
        "========================================",
        "",
        "This is another awesome demo of Wormhole's realtime",
        "video manipulation capabilities. Here, we bring back", 
        "the grayscale and inverted video feeds from before",
        "to demonstrate realtime video composition with Wormhole.",
        "",
        "We can do much more than overlay static images and assets.",
        "In this example, frames from three separate video streams",
        "are dynamically composed on top of one another, with one",
        "moving from left to right as time goes on and another",
        "with a 50% transparency effect applied.",
        "",
        "Years ago, this would have required a bulky and complicated",
        "video manipulation libraries to achieve, but today,",
        "all this powerful video manipulation technology is available",
        "in just a dozen lines of code with the power of Wormhole.",
        "",
        "Go to [ / ] to check out other examples!",
        "",
        "========================================"
    ])

def render_webcam_message(video):
    """
    Renders description for the webcam video feed.
    """
    pass

def render_proxy_message(video):
    """
    Renders description for the proxied video feed.
    """
    pass
    
def render_custom_message(video):
    """
    Renders description for the custom video feed.
    """
    
    # Constants
    BOX_MARGIN = 10
    BOX_WIDTH = 540
    BOX_HEIGHT = 280
    BOX_X_OFFSET = video.width-640
    BOX_Y_OFFSET = 24

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
        "> Wormhole Custom Video Demo <",
        "========================================",
        "",
        "Wormhole not only works with just file or camera streams,",
        "but also custom-rendered frames. In this simple demo,",
        "we cycle through different coloured background.",
        "",
        "All of these frames are being rendered in real-time without",
        "a reference video source. This shows that Wormhole works great",
        "with dynamic video content generated on the fly!",
        "",
        "Go to [ / ] to check out other examples!",
        "",
        "========================================"
    ])
