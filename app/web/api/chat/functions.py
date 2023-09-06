from app.web.api.tasks.core import create_reminder

function_names = {
    "create_reminder": create_reminder,
}


function_descriptions = [
    {
        "name": "create_reminder",
        "description": "This function handles the logic for creating a reminder for a "
        "generic task at a given date and time. Integer parameters should be greater "
        "than or equal to zero.",
        "parameters": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "The task to be reminded of, such as 'clean the "
                    "house'",
                },
                "days": {
                    "type": "integer",
                    "description": "The number of days until the reminder should be "
                    "triggered.",
                },
                "hours": {
                    "type": "integer",
                    "description": "The number of hours until the"
                    " reminder should be triggered.",
                },
                "minutes": {
                    "type": "integer",
                    "description": "The number of minutes until the"
                    " reminder should be triggered.",
                },
                "user_id": {
                    "type": "integer",
                    "description": "The user id of the user to be reminded.",
                },
            },
            "required": ["task", "days", "hours", "minutes", "user_id"],
        },
    },
]
