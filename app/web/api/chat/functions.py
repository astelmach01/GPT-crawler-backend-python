from app.tasks.reminder import create_reminder

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
                "date": {
                    "type": "string",
                    "description": "The date and time to be reminded at as a datetime "
                    "string in the format %Y-%m-%d %H:%M:%S, such as "
                    "'2021-08-01 12:00:00'",
                },
            },
            "required": ["task", "date"],
        },
    },
]
