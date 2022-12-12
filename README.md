# Checkout wiki

## Usage

- When create services using python, one can use `data_schemas/data_schema.py` to easily create/parse topic messages
- When setup a new kafka system, use `data_schemas/create_topics.py` to create topics

## Data flow (copied from the wiki)

```mermaid
graph TD
    Camera --> B(Deepstream app)
    B -->|2| C(Filtering)
    C -->|3| D(Matcher)
    B -->|1| D
    D -->|4| E(MTMC)
    E -->|5| F(Event Manager)
    B -->|100| F
    F -->|6| Q(Qt app)
    F -->|101| Q(Qt app)
    F -->|7| S(Storage Manager)
    S --> S3(Storage)
    S -->|8| G(Database Kafka Connect)
    G --> DB(Database)
```

## class diagram of schemas

```mermaid
classDiagram
    FaceMetaBase <|-- FaceMetaRaw
    FaceMetaRaw <|-- FaceMeta
    class FaceMetaBase {
        +BBox bbox
        +Optional[str] staff_id
        +Optional[str] name
        +Optional[float] score
    }

    class FaceMetaRaw {
        +base64_string feature
        +base64_string image
    }

    class FaceMeta {
        +bool is_stranger
        +str title
        +str note
    }

    MotMetaBase <|-- MotMetaRaw
    MotMetaRaw <|-- MotMeta
    class MotMetaBase {
        +BBox bbox
        +int object_id
        +base64_string embedding
    }

    class MotMetaRaw {
        +base64_string embedding
    }

    class MotMeta {
        +str text
    }

    class MCMTMeta {
        +FaceMeta face
    }

    class MatchedMeta {

    }

    class EventBase {
        +datetime srctime
        +str camera_id
    }

    class TopicBase {
        +str session_id
        +int frame_id
        +get_key() abcdef
    }

    class Topic4Model {
        +List[MatchedMeta] OBJ
    }

    EventBase <|-- TopicBase
    TopicBase <|-- Topic4Model
    TopicBase <|-- Topic100Model
    TopicBase <|-- Topic2Model
    Topic2Model <|-- Topic3Model
    TopicBase <|-- Topic1Model
    Topic4Model <|-- Topic5Model
    Topic5Model <|-- Topic7Model
    Topic7Model <|-- Topic8Model

    Topic100Model <|-- Topic101Model
    Topic5Model <|-- Topic101Model

    EventBase <|-- Topic6Model

    FaceMeta <.. MatchedMeta : Dependency
    MotMeta  <.. MatchedMeta : Dependency
    MCMTMeta <.. MatchedMeta : Dependency
    %% MotMetaRaw <.. Topic1Model : Dependency
    %% FaceMetaRaw <.. Topic2Model : Dependency
    MatchedMeta <.. Topic4Model : Dependency
```
