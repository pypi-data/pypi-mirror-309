from .models import Chat, ChatMessage
from typing import List, Dict
from datetime import datetime
import logging
import os
from openai import OpenAI




def save_chat(user: str, agent: str, msgs:List[Dict]):
  """
  Save a new chat
  """
  try:
    chat_messages =[ChatMessage(role=msg['role'], content=msg['content']) for msg in msgs if msg['role']!='system']
    chat = Chat(user=user, agent=agent, msgs=chat_messages, ts=datetime.now())
    summary = summarize_chat(chat)
    chat.summary = summary
    chat.save()
    return chat
  except Exception as e:
    logging.error(f"Failed to save chat: {str(e)}")

def user_chats(user: str, agent: str=None):
  """
  Search for user's chat
  """
  chats = Chat.find(Chat.user==user).all()
  if agent:
    chats = [chat for chat in chats if chat.agent==agent]
  if chats: return chats


def summarize_chat(chat:Chat, max_words=100):
  """
  Summarize a chat text
  """
  assert os.environ.get('OPENAI_API_KEY')
  client = OpenAI()

  text = '\n'.join(msg.role+': '+msg.content for msg in chat.msgs)
  response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
    {
      "role": "system",
      "content": f"Extract the subject of the conversation below and summarize in max {max_words} words"
    },
    {
      "role": "user",
      "content": text
    }
    ],
    temperature=0.7,
    max_tokens=int(max_words*1.3),
    top_p=1)
  return response.choices[0].message


