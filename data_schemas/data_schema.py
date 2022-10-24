"""generate json schema for all topics"""
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple, Type
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

    def __hash__(self):
        return hash((type(self), self.session_id, self.camera_id, self.frame_id))

    def __eq__(self, other: 'TopicBase'):
        return (self.session_id, self.camera_id, self.frame_id) == (other.session_id, other.camera_id, other.frame_id)

    def __ne__(self, other: 'TopicBase'):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

    def get_key(self) -> Tuple:
        # return (self.session_id, self.camera_id, self.frame_id)
        return TopicBase(
            srctime=self.srctime,
            camera_id=self.camera_id,
            session_id=self.session_id,
            frame_id=self.frame_id
        )


class RelativeBBox(CustomBaseModel):
    x: float = Field(ge=0, le=1.0)
    y: float = Field(ge=0, le=1.0)
    w: float = Field(ge=0, le=1.0)
    h: float = Field(ge=0, le=1.0)


def clip(value: float, min: float = 0.0, max: float = 1.0):
    """force min <= value <= max"""
    if value < min:
        return min
    if value > max:
        return max
    return value


class BBox(CustomBaseModel):
    """Bouding boxes"""
    x: float
    y: float
    w: float
    h: float

    def to_relative(self, frame_w: int, frame_h: int) -> RelativeBBox:
        return RelativeBBox(
            x=clip(self.x / frame_w, 0.0, 1.0),
            y=clip(self.y / frame_h, 0.0, 1.0),
            w=clip(self.w / frame_w, 0.0, 1.0),
            h=clip(self.h / frame_h, 0.0, 1.0),
        )

    def x1(self) -> float:
        return self.x

    def y1(self) -> float:
        return self.y

    def x2(self) -> float:
        return self.x + self.w

    def y2(self) -> float:
        return self.y + self.h


class FaceRawMeta(CustomBaseModel):
    """Face raw metadata"""
    bbox: BBox
    staff_id: str = Field(
        description="match the staff id in the database"
    )
    name: str = Field(
        description="name or any text to be display"
    )
    score: float = Field(
        description="face naming score"
    )
    feature: str = Field(
        description="base64 encoded of this face feature vector"
    )
    image: str = Field(
        description="base64 encoded of this face cropped image"
    )


class FaceMeta(FaceRawMeta):
    """Face metadata"""
    is_stranger: bool = Field(
        description="is this face a stranger?"
    )


class FaceDisplayMeta(CustomBaseModel):
    """Face for display in debug mode"""
    bbox: RelativeBBox = Field(
        description="relative bouding box"
    )
    is_stranger: bool = Field(
        description="is this face a stranger?"
    )
    name: str = Field(
        description="name of this person"
    )
    confident: float = Field(
        description="face naming confident"
    )


class MotRawMeta(CustomBaseModel):
    """MOT raw metadata"""
    bbox: BBox = Field(
        description="bouding box of this person"
    )
    object_id: int = Field(
        description="MOT object id"
    )
    embedding: str = Field(
        description="base64 encoded of the embedding of this person"
    )


class MotMeta(MotRawMeta):
    """MOT metadata object"""
    pass


class MotDisplayMeta(CustomBaseModel):
    """MOT object for display in debug mode"""
    bbox: RelativeBBox = Field(
        description="relative bouding box"
    )
    object_id: int = Field(
        description="MOT object id"
    )


class MatchedMeta(CustomBaseModel):
    """an object, which can be face and mot and both"""
    face: FaceRawMeta = Field(None, description="face")
    mot: MotRawMeta = Field(None, description="mot")


class Topic1Model(TopicBase):
    """
    event data with full information, including face feature, face cropped image, maybe human cropped image
    """

    FACE: List[FaceRawMeta] = Field(
        description="list of all faces in this frame"
    )

    MOT: List[MotRawMeta] = Field(
        description="list of all mot object in this frame"
    )

    class Config:
        title = 'RawMeta'


class Topic3Model(Topic1Model):
    """For now, it just the topic1 with changed name"""
    class Config:
        title = 'Filtered'


class Topic4Model(TopicBase):
    """event data including face feature, cropped face, and matched information between face and mot"""
    OBJ: List[MatchedMeta] = Field(
        [],
        description="list of all object in this frame"
    )

    class Config:
        title = 'Matched'


class Topic5Model(Topic4Model):
    """For now, it just the topic4 with changed name"""
    class Config:
        title = 'Mtmc'


class Topic100Model(TopicBase):
    """emit resized full frame image, without any drawing"""

    frame: str = Field(
        description="base64 encoded of the resized full frame"
    )

    frame_w: int = Field(
        description="width of the image"
    )

    frame_h: int = Field(
        description="height of the image"
    )

    class Config:
        title = 'RawImage'


class Topic101Model(Topic100Model):
    """
    Debug (resized) image with information, including face (resized) bouding boxes, human (resized) bouding boxes 
    Shoule be use to draw in UI apps.
    """
    FACE: List[FaceDisplayMeta] = Field(
        description="list of all faces in this image"
    )

    MOT: List[MotDisplayMeta] = Field(
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


if __name__ == "__main__":
    with open('schema_topic1.json', 'w') as _f:
        _f.write(Topic1Model.schema_json(indent=4))

    with open('schema_topic3.json', 'w') as _f:
        _f.write(Topic3Model.schema_json(indent=4))

    with open('schema_topic4.json', 'w') as _f:
        _f.write(Topic4Model.schema_json(indent=4))

    with open('schema_topic5.json', 'w') as _f:
        _f.write(Topic5Model.schema_json(indent=4))

    with open('schema_topic100.json', 'w') as _f:
        _f.write(Topic100Model.schema_json(indent=4))

    with open('schema_topic101.json', 'w') as _f:
        _f.write(Topic101Model.schema_json(indent=4))

    with open('schema_topic6.json', 'w') as _f:
        _f.write(Topic6Model.schema_json(indent=4))

    with open('schema_topic7.json', 'w') as _f:
        _f.write(Topic7Model.schema_json(indent=4))
