res_schema = {
    "type": "object",
    "properties": {
        "companyName": {"type": "string"},
        "licenceActive": {"type": "boolean"}
    },
    "required": ["companyName", "licenceActive"],
    "additionalProperties": False
}
