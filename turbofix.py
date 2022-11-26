#
#
#
# ========================================================
# Temporary fix to performance issues on the demo website with TurboJPEG
# This will be released on the main wormhole repo soon, but for now, this will do.
# ========================================================
#
#
#


from wormhole.streamer import AbstractStreamer
from wormhole.utils import FrameController

import logging
import time
import traceback
from flask.wrappers import Response
from turbojpeg import TurboJPEG, TJFLAG_FASTUPSAMPLE, TJFLAG_FASTDCT


class TurboMJPEGStreamer(AbstractStreamer):
    def __init__(
        self,
        *args,
        boundary: str = "WORMHOLE",
        quality: int = 100,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.boundary = boundary
        self.jpeg = TurboJPEG()

        # Create Video Feed Handler for Flask
        def video_feed():
            # Render and Send Frames for each client
            def generate_next_frame():
                frame_controller = FrameController(self.max_fps, print_fps=self.print_fps)
                while True:
                    try:
                        jpg = self.jpeg.encode(self.video.get_frame(), flags=TJFLAG_FASTUPSAMPLE|TJFLAG_FASTDCT, quality = quality)
                        yield (b"--" + boundary.encode("ascii") + b"\r\nContent-Type: image/jpeg\r\n\r\n" + jpg + b"\r\n")
                        frame_controller.next_frame()
                    except Exception as e:
                        # Print Error To User
                        logging.error(f"Error While Generating JPEG for Stream! {e}")
                        traceback.print_exc()
                        time.sleep(1)

                        # Reset FPS Statistics in case the video works again
                        frame_controller.reset_fps_stats()

            return Response(
                generate_next_frame(),
                mimetype=f"multipart/x-mixed-replace; boundary={boundary}",
            )

        # Add the video feed route to the network controller
        self.controller.add_route(self.route, video_feed, strict_url=self.strict_url)
