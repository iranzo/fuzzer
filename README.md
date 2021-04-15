# Fuzzy

# References

- <https://github.com/LonamiWebs/Telethon/tree/master/telethon_examples>

# Setup environment and execution

```sh
tox -e fuzzy
```

Get api_hash and ID from:

https://core.telegram.org/api/obtaining_api_id

Replace the vars in the fuzzy.py:

    api_id = API_ID
    api_hash = API_HASH

And put your code for sending at:

    # YOURCODE for sending messages
    await client.send_message("CHAT,USER,ETC", "TEXT TO SEND")

Execute with tox -e fuzzy
