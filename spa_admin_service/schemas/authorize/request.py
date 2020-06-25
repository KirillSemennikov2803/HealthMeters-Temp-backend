req_schema = {
    "type": "object",
    "properties": {
        "companyName": {"type": "string"},
        "password": {
            "type": "string",
            "pattern": "^[0-9a-f]{32}$"
        }
    },
    "required": ["companyName", "password"],
    "additionalProperties": False
}
