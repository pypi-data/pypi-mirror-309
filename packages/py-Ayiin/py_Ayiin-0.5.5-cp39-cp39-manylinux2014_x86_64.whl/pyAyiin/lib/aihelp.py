# (C) 2020-2023 by TgCatUB@Github.

from os import getenv
import openai


openai.api_key = getenv("OPENAI_API_KEY", None)


class OpenAi:
    conv = {}
    def gen_resp(self, input_text, chat_id):
        model = "gpt-3.5-turbo"
        system_message = None
        messages = self.conv.get(chat_id, [])
        if system_message and not messages:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": input_text})
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
            )
            generated_text = response.choices[0].message.content.strip()
            messages.append({"role": "assistant", "content": generated_text})
            self.conv[chat_id] = messages
        except Exception as e:
            generated_text = f"`Error generating GPT response: {str(e)}`"
        return generated_text


    def gen_edited_resp(self, input_text, instructions):
        try:
            response = openai.Edit.create(
                model="text-davinci-edit-001",
                input=input_text,
                instruction=instructions,
            )
            edited_text = response.choices[0].text.strip()
        except Exception as e:
            edited_text = f"Error generating GPT edited response`: {str(e)}`"
        return edited_text
