/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

/**
 * Types of event will be stream to UI
 * EVENT_FACE: event recognize a face or found a stranger
 * EVENT_CAMERA: a camera is be moved
 * EVENT_SYSTEM: maybe some important system messages
 * EVENT_OTHER: other
 */
export type EventType = "event_face" | "event_camera" | "event_system" | "event_other";

/**
 * Bouding boxes in relative coordinate
 */
export interface BBox {
  x: number;
  y: number;
  w: number;
  h: number;
}
/**
 * just the BaseModel without title
 */
export interface CustomBaseModel {}
/**
 * Base event
 */
export interface EventBase {
  /**
   * Time stamp of this image
   */
  srctime: string;
  /**
   * id of the camera that this event blong to
   */
  camera_id: string;
}
/**
 * Full Face metadata
 */
export interface FaceMeta {
  bbox: BBox;
  /**
   * match the staff id in the database
   */
  staff_id?: string;
  /**
   * name or any text to be display
   */
  name?: string;
  /**
   * face naming score
   */
  score?: number;
  /**
   * base64 encoded of this face feature vector
   */
  feature: string;
  /**
   * base64 encoded of this face cropped image
   */
  image: string;
  /**
   * is this face a stranger?
   */
  is_stranger: boolean;
  /**
   * displaying title
   */
  title?: string;
  /**
   * custom notes go here
   */
  note?: string;
  /**
   * direct url of saved image. Only available in topic8
   */
  image_uri?: string;
}
/**
 * Face base metadata
 */
export interface FaceMetaBase {
  bbox: BBox;
  /**
   * match the staff id in the database
   */
  staff_id?: string;
  /**
   * name or any text to be display
   */
  name?: string;
  /**
   * face naming score
   */
  score?: number;
}
/**
 * Face raw metadata
 */
export interface FaceMetaRaw {
  bbox: BBox;
  /**
   * match the staff id in the database
   */
  staff_id?: string;
  /**
   * name or any text to be display
   */
  name?: string;
  /**
   * face naming score
   */
  score?: number;
  /**
   * base64 encoded of this face feature vector
   */
  feature: string;
  /**
   * base64 encoded of this face cropped image
   */
  image: string;
}
/**
 * Multi-camera multi-tracking meta
 */
export interface MCMTMeta {}
/**
 * an object, which can be face and mot and both
 */
export interface MatchedMeta {
  /**
   * face
   */
  face?: FaceMeta;
  /**
   * mot
   */
  mot?: MotMeta;
  /**
   * mtmc meta
   */
  mtmc?: MCMTMeta;
}
/**
 * MOT full metadata
 */
export interface MotMeta {
  /**
   * bouding box of this person
   */
  bbox: BBox;
  /**
   * MOT object id
   */
  object_id: number;
  /**
   * base64 encoded of the embedding of this person
   */
  embedding: string;
  /**
   * text display on object
   */
  text?: string;
}
/**
 * MOT base metadata
 */
export interface MotMetaBase {
  /**
   * bouding box of this person
   */
  bbox: BBox;
  /**
   * MOT object id
   */
  object_id: number;
  /**
   * base64 encoded of the embedding of this person
   */
  embedding: string;
}
/**
 * MOT raw metadata
 */
export interface MotMetaRaw {
  /**
   * bouding box of this person
   */
  bbox: BBox;
  /**
   * MOT object id
   */
  object_id: number;
  /**
   * base64 encoded of the embedding of this person
   */
  embedding: string;
}
/**
 * emit resized full frame image, without any drawing
 */
export interface RawImage {
  /**
   * Time stamp of this image
   */
  srctime: string;
  /**
   * id of the camera that this event blong to
   */
  camera_id: string;
  /**
   * unique id of deepstream-app session
   */
  session_id: string;
  /**
   * frame id of this frame in this session
   */
  frame_id: number;
  /**
   * base64 encoded of the resized full frame
   */
  frame: string;
  /**
   * width of the image
   */
  frame_w: number;
  /**
   * height of the image
   */
  frame_h: number;
}
/**
 * Debug (resized) image with information, including face (resized) bouding boxes, human (resized) bouding boxes
 * Shoule be use to draw in UI apps.
 */
export interface Display {
  /**
   * Time stamp of this image
   */
  srctime: string;
  /**
   * id of the camera that this event blong to
   */
  camera_id: string;
  /**
   * unique id of deepstream-app session
   */
  session_id: string;
  /**
   * frame id of this frame in this session
   */
  frame_id: number;
  /**
   * list of all object in this frame
   */
  OBJ?: MatchedMeta[];
  /**
   * base64 encoded of the resized full frame
   */
  frame: string;
  /**
   * width of the image
   */
  frame_w: number;
  /**
   * height of the image
   */
  frame_h: number;
}
/**
 * MOT event metadata
 */
export interface RawMeta {
  /**
   * Time stamp of this image
   */
  srctime: string;
  /**
   * id of the camera that this event blong to
   */
  camera_id: string;
  /**
   * unique id of deepstream-app session
   */
  session_id: string;
  /**
   * frame id of this frame in this session
   */
  frame_id: number;
  /**
   * list of all mot object in this frame
   */
  MOT?: MotMetaRaw[];
}
/**
 * Face event metadata
 */
export interface Topic2Model {
  /**
   * Time stamp of this image
   */
  srctime: string;
  /**
   * id of the camera that this event blong to
   */
  camera_id: string;
  /**
   * unique id of deepstream-app session
   */
  session_id: string;
  /**
   * frame id of this frame in this session
   */
  frame_id: number;
  /**
   * Face event raw metadata
   */
  face: FaceMetaRaw;
}
/**
 * Filter faces frop topic2
 */
export interface Filtered {
  /**
   * Time stamp of this image
   */
  srctime: string;
  /**
   * id of the camera that this event blong to
   */
  camera_id: string;
  /**
   * unique id of deepstream-app session
   */
  session_id: string;
  /**
   * frame id of this frame in this session
   */
  frame_id: number;
  /**
   * Face event raw metadata
   */
  face: FaceMetaRaw;
}
/**
 * event data including face feature, cropped face, and matched information between face and mot
 */
export interface Matched {
  /**
   * Time stamp of this image
   */
  srctime: string;
  /**
   * id of the camera that this event blong to
   */
  camera_id: string;
  /**
   * unique id of deepstream-app session
   */
  session_id: string;
  /**
   * frame id of this frame in this session
   */
  frame_id: number;
  /**
   * list of all object in this frame
   */
  OBJ?: MatchedMeta[];
}
/**
 * For now, it just the topic4 with changed name
 */
export interface Mtmc {
  /**
   * Time stamp of this image
   */
  srctime: string;
  /**
   * id of the camera that this event blong to
   */
  camera_id: string;
  /**
   * unique id of deepstream-app session
   */
  session_id: string;
  /**
   * frame id of this frame in this session
   */
  frame_id: number;
  /**
   * list of all object in this frame
   */
  OBJ?: MatchedMeta[];
}
/**
 * event data with minimum, only-for-display information
 */
export interface Event {
  /**
   * Time stamp of this image
   */
  srctime: string;
  /**
   * id of the camera that this event blong to
   */
  camera_id: string;
  /**
   * type of this event
   */
  event_type: EventType;
  /**
   * only face_meat for now
   */
  face_meta: FaceMeta;
}
/**
 * event data with full information, including face feature, face cropped image, maybe human cropped image
 */
export interface Forsave {
  /**
   * Time stamp of this image
   */
  srctime: string;
  /**
   * id of the camera that this event blong to
   */
  camera_id: string;
  /**
   * unique id of deepstream-app session
   */
  session_id: string;
  /**
   * frame id of this frame in this session
   */
  frame_id: number;
  /**
   * list of all object in this frame
   */
  OBJ?: MatchedMeta[];
}
/**
 * event data with full information, including face feature, face cropped image, maybe human cropped image
 */
export interface Saved {
  /**
   * Time stamp of this image
   */
  srctime: string;
  /**
   * id of the camera that this event blong to
   */
  camera_id: string;
  /**
   * unique id of deepstream-app session
   */
  session_id: string;
  /**
   * frame id of this frame in this session
   */
  frame_id: number;
  /**
   * list of all object in this frame
   */
  OBJ?: MatchedMeta[];
}
/**
 * Base topic
 */
export interface TopicBase {
  /**
   * Time stamp of this image
   */
  srctime: string;
  /**
   * id of the camera that this event blong to
   */
  camera_id: string;
  /**
   * unique id of deepstream-app session
   */
  session_id: string;
  /**
   * frame id of this frame in this session
   */
  frame_id: number;
}
