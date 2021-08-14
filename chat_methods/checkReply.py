from chat_methods.getAllMessages import get_all_messages


def check_reply_id_in_chat(chat_id, reply_id):
    messages = get_all_messages(chat_id, 0)

    for message in messages:
        if message.get("messageId").get("S") == reply_id:
            return True

    return False
