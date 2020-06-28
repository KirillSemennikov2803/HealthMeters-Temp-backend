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
                        {"const": "licenceExpired"},
                        {"const": "licenceEmployeesBoundaryReached"},
                        {"const": "usedTgAccount"},
                        {"const": "wrongRoles"},
                        {"const": "noEmployee"}
                    ]
                }
            },
            "required": ["status", "reason"],
            "additionalProperties": False
        }
    ]
}
