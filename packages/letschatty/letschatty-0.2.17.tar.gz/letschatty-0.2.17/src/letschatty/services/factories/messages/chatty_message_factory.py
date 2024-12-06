# Fabrica principal de mensajes, que convierte mensajes de meta, frontend o BD a mensajes de Chatty
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any, List

from .child_db_message_factory import JsonMessageFactory
from .child_request_message import fromMessageDraftFactory
from .central_notification_factory import CentralNotificationFactory
from ....models.messages import ChattyMessageJson, CentralNotification
from ....models.company.assets import ChattyFastAnswer

if TYPE_CHECKING:
    from ....models.messages import ChattyMessage, MessageDraft

def from_message_json(message_json : Dict[str, Any]) -> ChattyMessage:
    chatty_message_json = ChattyMessageJson(**message_json)
    return JsonMessageFactory.from_json(chatty_message_json)
    
def from_message_draft(message_draft : MessageDraft, sent_by: str) -> ChattyMessage:
    return fromMessageDraftFactory.from_draft(message_draft, sent_by)
  
def from_notification_body(notification_body: str) -> CentralNotification:
    return CentralNotificationFactory.from_notification_body(notification_body)
    
def from_chatty_fast_answer(chatty_fast_answer: ChattyFastAnswer, sent_by: str) -> List[ChattyMessage]:
    """Returns the messages from a ChattyResponse, copying the objects, with current datetime in UTC and a new id"""
    return [fromMessageDraftFactory.from_draft(message=message, sent_by=sent_by) for message in chatty_fast_answer.messages]