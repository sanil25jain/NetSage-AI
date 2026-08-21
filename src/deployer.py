from datetime import datetime


def deploy(
    case_id: str,
    commands: list[str]
) -> dict:
    """
    Simulate deployment of Cisco CLI commands.

    No real network device is contacted.
    """

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Validate commands
    if not commands:

        return {
            "status": "FAILED",
            "case_id": case_id,
            "commands": [],
            "timestamp": timestamp,
            "message": "No commands were provided."
        }

    # Simulate command execution
    executed_commands = []

    for command in commands:

        executed_commands.append({
            "command": command,
            "status": "SUCCESS"
        })

    return {
        "status": "SUCCESS",
        "case_id": case_id,
        "commands": executed_commands,
        "timestamp": timestamp,
        "message": "Deployment simulation completed successfully."
    }