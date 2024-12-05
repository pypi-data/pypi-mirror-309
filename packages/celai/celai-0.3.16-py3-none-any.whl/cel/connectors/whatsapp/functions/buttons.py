import logging
import requests
from typing import Dict, Any


def create_button(button: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Method to create a button object to be used in the send_message method.

    This is method is designed to only be used internally by the send_button method.

    Args:
            button[dict]: A dictionary containing the button data
    """
    data = {"type": "list", "action": button.get("action")}
    if button.get("header"):
        data["header"] = {"type": "text", "text": button.get("header")}
    if button.get("body"):
        data["body"] = {"text": button.get("body")}
    if button.get("footer"):
        data["footer"] = {"text": button.get("footer")}
    return data


def send_button(self, button: Dict[Any, Any], recipient_id: str) -> Dict[Any, Any]:
    """
    Sends an interactive buttons message to a WhatsApp user

    Args:
        button[dict]: A dictionary containing the button data(rows-title may not exceed 20 characters)
        recipient_id[str]: Phone number of the user with country code wihout +

    check https://github.com/Neurotech-HQ/whatsapp#sending-interactive-reply-buttons for an example.
    """
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "interactive",
        "interactive": create_button(button),
    }
    logging.info(f"Sending buttons to {recipient_id}")
    r = requests.post(self.url, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Buttons sent to {recipient_id}")
        return r.json()
    logging.info(f"Buttons not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.info(f"Response: {r.json()}")
    return r.json()


def send_reply_button(
    self, button: Dict[Any, Any], recipient_id: str
) -> Dict[Any, Any]:
    """
    Sends an interactive reply buttons[menu] message to a WhatsApp user

    Args:
        button[dict]: A dictionary containing the button data
        recipient_id[str]: Phone number of the user with country code wihout +

    Note:
        The maximum number of buttons is 3, more than 3 buttons will rise an error.
    """
    if len(button["action"]["buttons"]) > 3:
        raise ValueError("The maximum number of buttons is 3.")
    
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "interactive",
        "interactive": button,
    }
    r = requests.post(self.url, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Reply buttons sent to {recipient_id}")
        return r.json()
    logging.info(f"Reply buttons not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.info(f"Response: {r.json()}")
    return r.json()




def send_cta_url(
    self, cta_url: Dict[Any, Any], recipient_id: str
) -> Dict[Any, Any]:
    """
    Sends a call to action url message to a WhatsApp user

    Args:
        cta_url[dict]: A dictionary containing the cta url data
        recipient_id[str]: Phone number of the user with country code wihout +

    check
    
    """
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "interactive",
        "interactive": cta_url,
    }
    r = requests.post(self.url, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"CTA URL sent to {recipient_id}")
        return r.json()
    logging.info(f"CTA URL not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.info(f"Response: {r.json()}")
    return r.json()