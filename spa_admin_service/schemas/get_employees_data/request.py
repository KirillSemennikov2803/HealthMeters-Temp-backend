req_schema = {
    "type": "object",
    "properties": {
        "session": {"$ref": "#/definitions/Guid"},
        "employees": {
            "type": "array",
            "items": {"$ref": "#/definitions/Guid"}
        }
    },
    "required": ["session"],
    "additionalProperties": False,
    "definitions": {
        "Guid": {
            "type": "string",
            "pattern":
                "^[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[8-b][0-9a-f]{3}-[0-9a-f]{12}$"
        }
    }
}
