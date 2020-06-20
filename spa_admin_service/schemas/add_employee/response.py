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
                        {"const": "usedTgAccount"},
                        {"const": "licenceExpired"},
                        {"const": "licenceEmployeesBoundaryReached"}
                    ]
                }
            },
            "required": ["status", "reason"],
            "additionalProperties": False
        }
    ]
}
