import os
import urllib.request
import urllib.parse
import json
import streamlit as st

BOT_TOKEN = "8733784833:AAFtSekTYwJ1_tUxODOYhnbac46A8m_tkVE"

# We use session state to cache the chat_id so we don't fetch it every time
def get_chat_id():
    # If we have it in session state, return it
    if "admin_chat_id" in st.session_state:
        return st.session_state.admin_chat_id
        
    # Try to fetch from getUpdates (needs the user to have messaged the bot first)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get("ok") and data.get("result"):
                # Get the chat id of the last person who messaged the bot
                chat_id = data["result"][-1]["message"]["chat"]["id"]
                st.session_state.admin_chat_id = chat_id
                return chat_id
    except Exception as e:
        print(f"Telegram error: {e}")
    return None

def send_notification(text):
    """Sends a notification to the owner's Telegram."""
    chat_id = get_chat_id()
    if not chat_id:
        return False
        
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }).encode('utf-8')
    
    try:
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Failed to send telegram msg: {e}")
        return False
