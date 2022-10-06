"""generate json schema for all topics"""
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Type
from pydantic import BaseModel, Field

class CustomBaseModel(BaseModel):
    """just the BaseModel without title"""
    class Config:
        @staticmethod
        def schema_extra(schema: Dict[str, Any], model: Type['CustomBaseModel']) -> None:
            for prop in schema.get('properties', {}).values():
                prop.pop('title', None)

class EventBase(CustomBaseModel):
    """Base event"""
    srctime: datetime = Field(
        description="Time stamp of this image"
    )
    camera_id: str = Field(
        description="id of the camera that this event blong to"
    )

class TopicBase(EventBase):
    """Base topic"""
    session_id: str = Field(
        description="unique id of deepstream-app session"
    )
    frame_id: int = Field(
        description="frame id of this frame in this session"
    )
    image: str = Field(
        None,
        description="base64 encoded of this face cropped image"
    )

class BBox(CustomBaseModel):
    """Bouding boxes"""
    x: float
    y: float
    w: float
    h: float

class FaceMeta(CustomBaseModel):
    """Face message"""
    bbox: BBox
    is_stranger: bool = Field(
        description="is this face a stranger?"
    )
    staff_id: int = Field(
        description="match the staff id in the database"
    )
    confident: float = Field(
        description="face naming confident"
    )
    feature: str = Field(
        description="base64 encoded of this face feature vector"
    )
    image: str = Field(
        description="base64 encoded of this face cropped image"
    )

class MotMeta(CustomBaseModel):
    """MOT metadata object"""
    bbox: BBox = Field(
        description="bouding box of this person"
    )
    object_id: int = Field(
        description="MOT object id"
    )
    embedding: str = Field(
        description="base64 encoded of the embedding of this person"
    )


class Topic101Model(TopicBase):
    """
    event data with full information, including face feature, face cropped image, maybe human cropped image
    """
    image: str = Field(
        description="base64 encoded of the full image"
    )

    FACE: List[FaceMeta] = Field(
        description="list of all faces in this image"
    )

    MOT: List[MotMeta] = Field(
        description="list of all mot object in this image"
    )

    class Config:
        title = 'Display'

class EventType(str, Enum):
    """
    Types of event will be stream to UI
    EVENT_FACE: event recognize a face or found a stranger
    EVENT_CAMERA: a camera is be moved
    EVENT_SYSTEM: maybe some important system messages
    EVENT_OTHER: other
    """
    EVENT_FACE = 'event_face',
    EVENT_CAMERA = 'event_camera'
    EVENT_SYSTEM = 'event_system'
    EVENT_OTHER = 'event_other'

class Topic6Model(EventBase):
    """event data with minimum, only-for-display information"""
    event_type: EventType = Field(
        description="type of this event"
    )
    face_meta: FaceMeta = Field(
        description="only face_meat for now"
    )

    class Config:
        title = 'Event'

class Topic7Model(TopicBase):
    """event data with full information, including face feature, face cropped image, maybe human cropped image"""
    FACE: List[FaceMeta] = Field(
        description="list of all faces in this frame"
    )

    MOT: List[MotMeta] = Field(
        description="list of all mot object in this frame"
    )

    # TODO: add MTMC information

    class Config:
        title = 'Forsave'

with open('schema_topic101.json', 'w') as _f:
    _f.write(Topic101Model.schema_json(indent=4))

with open('schema_topic6.json', 'w') as _f:
    _f.write(Topic6Model.schema_json(indent=4))

with open('schema_topic7.json', 'w') as _f:
    _f.write(Topic7Model.schema_json(indent=4))
