#!/bin/bash
cd /home/kavia/workspace/code-generation/ai-chatbot-platform-140245-140263/ai_chat_bot_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

