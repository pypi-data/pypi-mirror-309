# ops-py-reports

## Payloads

### Slack App  
Creates Slack payload(s) from the provided *title* and *body*.
  
The title will be formatted as **bold**, while the body will be formatted as a  ```Code block```:            
``` [{"text": f"*{title}*\n```{body}```"}]```  
  
- If the payload is too large it will be split into multiple parts (individual posts).  
  - If spilt, the provided *title* will be used for *all* posts.
    - The *part number* will be appended to the *title* on each post.  
  

---

## Reports

### SlackMessages  
Accepts a list of dicts and returns Slack Markdown formatted rows.  
  
The `get_ssl_report()` method creates a message with a provided title in bold (defaults to `SSL certificates report`) .    
If any of the provided rows of dicts contains a *status* key, the value of this key will be formatted according to the status value. Defaults to the following config:   

```
{
  "ok": {
    "emoji": ":white_check_mark:",
    "txt": "OK"
  },
  "warning": {
    "emoji": ":warning:",
    "txt": "WARNING"
  },
  "critical": {
    "emoji": ":bangbang:",
    "txt": "CRITICAL!"
  },
  "expired": {
    "emoji": ":rotating_light:",
    "txt": "EXPIRED!!"
  },
  "error": {
    "emoji": ":no_entry:",
    "txt": "ERROR"
  },
  "unknown": {
    "emoji": ":question:",
    "txt": "UNKNOWN"
  }
}

```

The status will use the provided config to apply corresponding emoji and status text.  
  
### Markdown  
Creates a plain text Markdown table from a list (rows) of lists (columns). The header is the first list in the list of rows.  
  
### HTMLTable
Creates a HTML table from a list (rows) of lists (columns). The header is the first list in the list of rows. 

*Styles*
```
"grey": " style='background-color: Grey; color: White; font-weight:bold'"
"purple": " style='background-color: Purple; color: White; font-weight:bold'"
"yellow": " style='background-color: Yellow; color: Black; font-weight:bold'"
"red": " style='background-color: Red; color: White; font-weight:bold'"
"green": " style='background-color: Green; color: White; font-weight:bold'"

```

will be added to the cells which equals the following *values*:
```
"disabled": "grey"  
"unknown": "grey"  
"warning": "yellow"  
"critical": "red"  
"ok": "green"  
"error": "red"  
"expired": "red"  
```


---

## Functions 

### dict_to_rows
Converts a list of dicts to a list of a header and rows.

### dict_to_csv
Converts a list of dicts to a comma separated csv text, with a header and rows.
