res_schema = {
    "oneOf": [
        {
            "type": "object",
            "properties": {
                "status": {"const": "ok"},
                "employeesData": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "employee": {"$ref": "#/definitions/Guid"},
                            "employeeData": {
                                "oneOf": [
                                    {"$ref": "#/definitions/Worker"},
                                    {"$ref": "#/definitions/Manager"}
                                ]
                            }
                        },
                        "required": ["employee", "employeeData"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["status", "employees"],
            "additionalProperties": False
        },
        {
            "type": "object",
            "properties": {
                "status": {"const": "error"},
                "reason": {
                    "oneOf": [
                        {"const": "licenceExpired"},
                        {"const": "licenceEmployeesBoundaryReached"}
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
        },
        "Worker": {
            "type": "object",
            "properties": {
                "initials": {
                    "type": "string",
                    "pattern": "^([A-Za-zА-Яа-я]+[ ])*([A-Za-zА-Яа-я]+)$"
                },
                "tgUsername": {
                    "type": "string",
                    "pattern": "^\\w+$"
                },
                "role": {
                    "const": "worker"
                },
                "attachedManager": {"$ref": "#/definitions/Guid"}
            },
            "required": ["initials", "tgUsername", "role", "attachedManager"],
            "additionalProperties": False
        },
        "Manager": {
            "type": "object",
            "properties": {
                "initials": {
                    "type": "string",
                    "pattern": "^([A-Za-zА-Яа-я]+[ ])*([A-Za-zА-Яа-я]+)$"
                },
                "tgUsername": {
                    "type": "string",
                    "pattern": "^\\w+$"
                },
                "role": {
                    "const": "manager"
                }
            },
            "required": ["initials", "tgUsername", "role"],
            "additionalProperties": False
        }
    }
}
