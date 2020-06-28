res_schema = {
    "type": "object",
    "properties": {
        "serverTime": {
            "type": "integer",
            "minimum": 0
        },
        "activeLicencePack": {
            "oneOf": [
                {"$ref": "#/definitions/Guid"},
                {"type": "null"}
            ]
        },
        "licencePacksData": {
            "type": "array",
            "items": {"$ref": "#/definitions/LicencePack"}
        }
    },
    "required": ["serverTime", "activeLicencePack", "licencePacksData"],
    "additionalProperties": False,
    "definitions": {
        "Guid": {
            "type": "string",
            "pattern":
                "^[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[8-b][0-9a-f]{3}-[0-9a-f]{12}$"
        },
        "LicencePack": {
            "type": "object",
            "properties": {
                "licencePack": {"$ref": "#/definitions/Guid"},
                "startTime": {
                    "type": "integer",
                    "minimum": 0
                },
                "endTime": {
                    "type": "integer",
                    "minimum": 0
                },
                "employeesCount": {
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": ["licencePack", "startTime", "endTime", "employeesCount"],
            "additionalProperties": False
        }
    }
}
