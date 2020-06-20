req_schema = {
    "type": "object",
    "properties": {
        "session": {"$ref": "#/definitions/Guid"}
    },
    "required": ["session"],
    "additionalProperties": False
}
