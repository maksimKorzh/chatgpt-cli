#!/bin/python3

# packages
import openai
import os, time
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic, Token, Whitespace
from pygments import highlight
import colorama

# custom color scheme
COLOR_SCHEME = {
  Token:              ('gray',                 'gray'),
  Comment:            ('magenta',     'brightmagenta'),
  Comment.Preproc:    ('magenta',     'brightmagenta'),
  Keyword:            ('blue',                   '**'),
  Keyword.Type:       ('green',       '*brightgreen*'),
  Operator.Word:      ('**',                     '**'),
  Name.Builtin:       ('cyan',           'brightblue'),
  Name.Function:      ('blue',           'brightblue'),
  Name.Class:         ('_green_',        'brightblue'),
  Name.Decorator:     ('magenta',     'brightmagenta'),
  Name.Variable:      ('blue',           'brightblue'),
  String:             ('yellow',       'brightyellow'),
  Number:             ('blue',         'brightyellow')
}

# init coloros
colorama.init()

# OpenAI auth
openai.api_key = os.getenv("OPENAI_API_KEY")
messages=[{'role': 'system', 'content': 'You are a helpful assistant.'}]

# syntax highlighting
def colorize_code(code):
  lexer = guess_lexer(code)
  print('\n\nGUESSED', lexer.name)
  formatter = TerminalFormatter(bg='dark', colorscheme=COLOR_SCHEME)
  return highlight(code, lexer, formatter)

# print message letter by letter
def emulate_typing(message):
  for ch in message:
    print(ch, end='', flush=True)
    time.sleep(0.001)
  print(flush=True)

# main loop
while True:
  try:
    # get user input
    question = input(colorama.Fore.CYAN + 'You: ' + colorama.Style.RESET_ALL)
    if question == 'quit': break

    # add user message to the conversation
    messages.append({
      'role': 'user',
      'content': question
    })

    # OpenAI API response
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    # extract text from response
    answer = response['choices'][0]['message']['content']

    # add ChatGPT message to the conversation
    messages.append({
      'role': 'assistant',
      'content': answer
    })

    # print CHatGPT answer
    print(colorama.Fore.YELLOW + 'ChatGPT: ' + colorama.Style.RESET_ALL, end='')
    parse_answer = answer.split('```')
    if len(parse_answer) > 1:
      emulate_typing(parse_answer[0].strip()[:-1])
      for chunk in parse_answer:
        if len(chunk.split('\n')[0]):
          code = '\n'.join(chunk.split('\n')[1:])
          highlight_code = colorize_code(code)
          if code != "    \n    ": emulate_typing(highlight_code.strip())
        else: emulate_typing('\n' + chunk.strip())
    else: emulate_typing(answer.strip())

  # more that 3 requests per minute are not allowed
  except: print(colorama.Fore.YELLOW + "ChatGPT: I'm busy, only 3 request per minute are allowed for free accounts, please ask your question again in 20 seconds" + colorama.Style.RESET_ALL)