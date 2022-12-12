from pydantic2ts import generate_typescript_defs
from data_schema import Topic7Model

generate_typescript_defs("data_schema", "data_schema.ts")