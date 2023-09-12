from app.web.api.tasks.core import create_reminder

function_names = {
    "create_reminder": create_reminder,
}


function_descriptions = [
    {
        "name": "create_reminder",
        "description": "This function handles the logic for creating a reminder for a "
        "generic task at a given date and time.",
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
                    "description": "The number of days from now to be reminded",
                },
                "hours": {
                    "type": "integer",
                    "description": "The number of hours from now to be reminded",
                },
                "minutes": {
                    "type": "integer",
                    "description": "The number of minutes from now to be reminded",
                },
            },
            "required": ["task", "days", "hours", "minutes"],
        },
    },
]
