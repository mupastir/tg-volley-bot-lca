# Telegram Beach Volleyball Bot for Larnaca

A Telegram bot designed to support the beach volleyball community in Larnaca, Cyprus. This bot provides translation services, AI-powered Q&A, and community information.

## Features

- **Automatic Translation**: Translates messages from Russian to English to facilitate communication in the international community
- **AI Assistant**: Answers questions about beach volleyball, sports, nutrition, and community topics
- **Community Knowledge Base**: Shares random facts and information about community members
- **Command Interface**: Provides helpful information through intuitive commands

## Commands

- `/start` - Get an introduction to the bot
- `/help` - Display available commands and usage instructions
- `fact!` or `oneliner!` - Get a random fact about community members
- `ping` - Simple response to check if the bot is active
- `ai!`, `gpt!`, `openai!`, `чат!` - Ask the AI assistant a question

## Usage Limits

- Regular users: 5 AI questions per day
- Super users: Unlimited usage (configured via environment variables)

## Tech Stack

- **Python 3.12+**
- **minigram-py**: Lightweight Telegram bot framework
- **OpenAI API**: Provides AI responses (GPT models)
- **AWS Lambda**: Serverless hosting
- **AWS DynamoDB**: Stores conversation history
- **Translation API**: Handles message translation

## Installation

### Prerequisites

- Python 3.12 or higher
- An OpenAI API key
- A Telegram bot token (obtained from [@BotFather](https://t.me/BotFather))
- AWS account (for production deployment)

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd tg-volley-bot-lca
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following variables:
   ```
   openai_api_key=your_openai_api_key
   openai_model=gpt-4o-mini
   tg_bot_token=your_telegram_bot_token
   super_users=["username1", "username2"]
   ```

4. Run the bot locally:
   ```bash
   python -m app.main
   ```

### AWS Deployment

1. Create a DynamoDB table named `tg_volley_bot_openai_requests`

2. Deploy the Lambda function:
   - Zip the project files
   - Upload to AWS Lambda
   - Set the handler to `lambda_function.lambda_handler`
   - Configure environment variables in the Lambda console

3. Set up a webhook connecting Telegram to your Lambda function

## Project Structure

```
app/
├── __init__.py
├── bot.py            # Core bot logic
├── gateways/         # External API connections
├── handlers/         # Message handling logic
├── main.py           # Application initialization
├── misc/             # Utility functions
├── models/           # Data models
└── settings.py       # Configuration
data/
├── basic.data        # Help text
└── bvlarnaca.json    # Community facts
lambda_function.py    # AWS Lambda entry point
```

## Testing

Run tests with pytest:
```bash
pytest
```

## License

This project is licensed under the terms of the LICENSE file included in the repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.