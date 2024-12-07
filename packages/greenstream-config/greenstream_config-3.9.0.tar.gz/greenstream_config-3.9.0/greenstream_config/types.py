from typing import List, Literal, Optional

from pydantic import BaseModel

class Offsets(BaseModel):
    # in radians in FLU
    roll: Optional[float] = None
    pitch: Optional[float] = None
    yaw: Optional[float] = None
    forward: Optional[float] = None
    left: Optional[float] = None
    up: Optional[float] = None

class PTZOffsets(Offsets):
    type: Literal["pan", "tilt"]

class Camera(BaseModel):
    # This will become the name of frame-id, ros topic and webrtc stream
    name: str
    # Used to order the stream in the UI
    order: int
    # The camera type, eg. color, ir
    type: str = "color"
    # Whether we should start the PTZ driver
    ptz: bool = False
    # The offsets from the base-link to the camera
    camera_offsets: Optional[Offsets] = None
    # The offsets from the camera to the optical frame if PTZ
    ptz_offsets: List[PTZOffsets] = []

class GreenstreamConfig(BaseModel):
    cameras: List[Camera]
    signalling_server_port: int = 8443
    namespace_vessel: str = "vessel_1"
    namespace_application: str = "greenstream"
    ui_port: int = 8000
    debug: bool = False
    diagnostics_topic: str = "diagnostics"
