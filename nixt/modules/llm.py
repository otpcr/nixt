# This file is placed in the Public Domain.


import select
import sys


OLLAMA = True


try:
    from ollama import chat
    from ollama import ChatResponse
except ModuleNotFoundError:
    OLLAMA = False


def api(txt):
    response: ChatResponse = chat(model='deepseek-coder:6.7b-instruct', messages=[
      {
        'role': 'system',
        'content': """
                     You are {Config.name}, a modern python3 expert coder and expected to give short, precise answers.
                     Reply with yes or no where possible. Your are not to help, but to give expert python3 advise.
                   """
      },
      {
        'role': 'user',
        'content': txt,
      },
    ])
    return response.message.content.strip()


def ask(event):
    if not OLLAMA:
        event.reply("ollama is not installed.")
        return
    if event.rest:
        text = event.rest +"\n\n"
    if not select.select(
                         [sys.stdin, ],
                         [],
                         [],
                         0.0
                        )[0]:
        if not event.rest:
            event.reply("ask <text>")
        else:
            event.reply(api(text))
        return
    size = 0
    while 1:
        try:
            (input, _output, error) = select.select(
                                             [sys.stdin,],
                                             [],
                                             [sys.stderr,]
                                            )
        except KeyboardInterrupt:
            return
        if error:
            break
        stop = False
        for sock in input:
            txt = sock.readline()
            if not txt:
                stop = True
                break
            text += txt + "\n"
            size += len(txt)
        if stop:
            break
    event.reply(api(text))
