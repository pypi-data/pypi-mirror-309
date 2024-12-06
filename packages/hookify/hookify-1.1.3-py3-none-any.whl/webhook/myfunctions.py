import subprocess

def send(webhook_url, content=None, username=None, avatar_url=None, embeds=None):
    """
    ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n
    `hookify.send()` sends a **POST** request to the Discord API.\n
    ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n
     • `webhook_url` | Link to the webhook. (Required)\n

     • `content` | Content of the message. (Required)\n

     • `username` | Overrides the predefined username.\n

     • `avatar_url` | Overrides the predefined avatar URL.\n
    ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n
    Sending a message, which contains **embeds**.\n
    ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n
    • `embeds` | A **list of arrays** containing embeds and their properties.\n
    Webhook arguments could be found [here](https://birdie0.github.io/discord-webhooks-guide/discord_webhook.html) or in the official Discord documentation.\n
    ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n
    *Example use of `embeds` (check the [argument documentation](https://birdie0.github.io/discord-webhooks-guide/discord_webhook.html))*
    ```hookify.send(URL, 'Hello!', embeds=[{"title": "Embed 1!", "description": "Hello!"}, {"title": "Embed 2!"}])\n
    """

    try:
        if content == None:
            content = ''

        payload = {
            "content": content
        }

        ##############################

        if username != None:
            payload["username"] = username
        if avatar_url != None:
            payload["avatar_url"] = avatar_url
        if embeds != None:
            payload["embeds"] = embeds
        if len(content) == 0 and embeds == None:
            print('Hookify | Content may not be empty!')
            return ''

        ##############################

        command = [
            "curl",
            "-X", "POST",
            "-H", "Content-Type: application/json",
            "-d", str(payload).replace("'", '"'),
            webhook_url
        ]

    except:
        print('Hookify | Provided arguments are incorrect!')

    try:
        subprocess.check_call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return 'Hookify | Operation successfully executed!'
    except:
        print('Hookify | Provided arguments are incorrect!')
        return ''