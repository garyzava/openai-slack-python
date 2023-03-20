# OpenAI Slack App Bot
Slack App that uses Python to call ChatGPT From OpenAI's API. The app stores the chat log in a database to retain memory and reponds to two events: mentions and direct messages.

Use this notebook is you want a simpler version here: [gpt-3.5-turbo](https://github.com/garyzava/openai-python-tools/blob/main/notebooks/gpt_3_5_turbo.ipynb)

## Contents

* [Installation]
* [Usage]

## 1. Prerequisites

### 1.a Create a Slack App

Go to https://api.slack.com/apps and create an new app, the eaisest way is by using an App Manifest such as the following template:

```yaml
display_information:
  name: OpenAI Chat
  description: An OpenAI Slack bot
features:
  app_home:
    home_tab_enabled: false
    messages_tab_enabled: true
    messages_tab_read_only_enabled: false
  bot_user:
    display_name: OpenAI Chat
    always_online: true
  shortcuts:
    - name: Summarize...
      type: message
      callback_id: summarize
      description: Summarize this thread...
    - name: Ask something...
      type: message
      callback_id: ask
      description: Ask the question in the thread
  slash_commands:
    - command: /gen_image
      description: Generate image from OpenAI
      usage_hint: "[a white siamese cat]"
      should_escape: false
oauth_config:
  scopes:
    bot:
      - app_mentions:read
      - channels:history
      - chat:write
      - chat:write.customize
      - chat:write.public
      - commands
      - files:write
      - groups:history
      - im:history
      - users:read
settings:
  event_subscriptions:
    bot_events:
      - app_mention
      - message.im
  interactivity:
    is_enabled: true
  org_deploy_enabled: false
  socket_mode_enabled: true
  token_rotation_enabled: false
```


### 1.b Enable an OpenAI's API Key

Get a OpenAI key from https://platform.openai.com/account/api-keys

### 1.c Set up an Environment File
Create a `.env` file containing your keys. Your `.env` file should look like this:

```
SLACK_BOT_TOKEN = 'xoxb-...'
SLACK_APP_TOKEN = 'xapp...'
OPENAI_API_KEY = 'sk-....'
```

## 2. Installation
It is advisable to create a virtual environment and activate it first.

`pip install -r requirements.txt`

## 3. Usage

To get the slack bot up and running start the bot by running:

`python app_bot.py`

## Helpful Resources

* Guide for creating a bot: https://www.twilio.com/blog/openai-gpt-3-chatbot-python-twilio-sms
* Inspiration from javascript slack bot: https://github.com/jack482653/openai-slack-bot
* Original Javascript template: https://gist.github.com/kvzhuang/357b83499d3edcc099512d47a4a1b646 
