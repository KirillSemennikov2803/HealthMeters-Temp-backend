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
                        {"const": "invalidToken"},
                        {"const": "activatedToken"},
                        {"const": "usedCompanyName"}
                    ]
                }
            },
            "required": ["status", "reason"],
            "additionalProperties": False
        }
    ]
}
