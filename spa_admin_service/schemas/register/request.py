req_schema = {
    "type": "object",
    "properties": {
        "token": {
            "type": "string",
            "pattern": "^[0-9a-zA-Z+-]{7}$"
        },
        "companyName": {"type": "string"},
        "password": {
            "type": "string",
            "pattern": "^[0-9a-f]{32}$"
        }
    },
    "required": ["token", "companyName", "password"],
    "additionalProperties": False
}
