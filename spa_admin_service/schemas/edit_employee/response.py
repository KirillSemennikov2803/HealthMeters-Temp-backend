res_schema = {
    "oneOf": [
        {
            "type": "object",
            "properties": {
                "status": {"const": "ok"}
            },
            "required": ["status"],
            "additionalProperties": False
        },
        {
            "type": "object",
            "properties": {
                "status": {"const": "error"},
                "reason": {
                    "oneOf": [
                        {"const": "wrongRoles"},
                        {"const": "usedTgAccount"},
                        {"const": "noEmployee"},
                        {"const": "licenceExpired"}
                    ]
                }
            },
            "required": ["status", "reason"],
            "additionalProperties": False
        }
    ]
}
