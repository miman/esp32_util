## FileMgr Task
This task will do a number of file operation tasks on the ESP 32
* Write the given file content to the given file path
* Read a file path with a given name & return the content on topic ***file/content***
* Delete the file with the given file path

## Pins
The file mgr does not use any PIN's

## Eventbus messages
### file/write
Write the given file content to the given file path msgs posted to the topic ***file/write***
If the reboot flag is present & set to true the device will be rebooted after the file has been written.
This could for example be used foe remote software updates.

### Payload format
The payload for ***file/write*** is:

```
{
    "path": "dir/filename.py",
    "content": "File content",
    "reboot": false
}
```

### file/read
Read a file path with a given name msgs posted to the topic ***file/read*** & return the content on topic ***file/content***

### Payload format
The payload for ***file/read*** is:

```
{
    "path": "dir/filename.py"
}
```

### file/remove
Write the given file content to the given file path msgs posted to the topic ***file/remove***

### Payload format
The payload for ***file/remove*** is:

```
{
    "path": "dir/filename.py",
    "content": "File content"
}
```

### file/content
When asked to read a file a message with the file content will be sent to this topic ***file/content***

### Payload format
The payload for ***file/content*** is:

```
{
    "path": "dir/filename.py",
    "content": "File content"
}
```

## Configuration format
If this taks is active or not is configured in the ***file*** block

```
    "file": {
        "active": True
    },
```