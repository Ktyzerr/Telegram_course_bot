# Telegram Course Registration Bot

This is a Telegram bot for registering users to an online programming course.

## Features

- Sends a welcome message when user starts the bot
- Asks 3-5 questions to collect user data and stores answers (you can connect to your database)
- Lets user choose a course date
- Notifies the manager with user registration details
- Collects user feedback after the course

## Technologies

- Python 3.11+
- Aiogram 3.x

## Setup and Run

1. Install dependencies:

__bash__

pip install aiogram
Set your Telegram bot API key inside bot.py:

API_KEY = "YOUR_TELEGRAM_BOT_API_KEY"

Run the bot:

bash
Копировать
Редактировать
python bot.py
How to Use
Start the bot with /start

Follow the prompts to register for the course

Manager receives notifications and can approve or reject registrations

After the course, the bot collects user feedback automatically

Notes
This bot uses FSM (Finite State Machine) for managing conversation flow.

You need to add your database integration if you want to save data persistently.
