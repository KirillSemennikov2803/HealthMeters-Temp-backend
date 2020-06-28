res_schema = {
    "type": "object",
    "properties": {
        "employeesCount": {
            "type": "integer",
            "minimum": 0
        }
    },
    "required": ["employeesCount"],
    "additionalProperties": False,
}
