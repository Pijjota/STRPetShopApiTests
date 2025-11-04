INVENTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "approved": {"type": "integer", "minimum": 0},
        "placed": {"type": "integer", "minimum": 0},
        "delivered": {"type": "integer", "minimum": 0}
    },
    "required": ["approved", "placed", "delivered"],
    "additionalProperties": False
}