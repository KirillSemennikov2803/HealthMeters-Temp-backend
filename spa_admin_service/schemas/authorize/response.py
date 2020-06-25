res_schema = {
    "oneOf": [
        {
            "type": "object",
            "properties": {
                "status": {"const": "ok"},
                "session": {"$ref": "#/definitions/Guid"}
            },
            "required": ["status", "session"],
            "additionalProperties": False
        },
        {
            "type": "object",
            "properties": {
                "status": {"const": "error"},
                "reason": {
                    "oneOf": [
                        {"const": "wrongCompanyName"},
                        {"const": "wrongPassword"}
                    ]
                }
            },
            "required": ["status", "reason"],
            "additionalProperties": False
        }
    ],
    "definitions": {
        "Guid": {
            "type": "string",
            "pattern":
                "^[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[8-b][0-9a-f]{3}-[0-9a-f]{12}$"
        }
    }
}
