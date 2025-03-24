# Server Monitoring Slack Bot

This repository contains a Slack bot designed to monitor server health and send real-time alerts to your Slack workspace. The bot helps ensure your infrastructure remains reliable by notifying you of critical issues.

## Features
- **Integration with Slack**: Alerts are sent directly to a specified Slack channel.
- **Scheduled Health Checks**: Periodic updates on server health.

## Using Docker

0. Modify the secrets.json:
    ```json
    {
        "slack_webhook_url": "https://hooks.slack.com/services/your/webhook/url"
    }
    ```
    Replace `your/webhook/url` with your actual Slack webhook URL.

1. Build the Docker image:
    ```bash
    docker build -t server-monitoring-slack .
    ```

2. Run the Docker container:
    ```bash
    docker run -d --name server_monitor slack-server-monitor
    ```
3. If you need to run it on a system with a GPU (NVIDIA), make sure to use NVIDIA Container Toolkit:
    ```bash
    docker run -d --gpus all --name server_monitor slack-server-monitor
    ```
## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/server_monitoring_slack.git
    cd server_monitoring_slack
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    - `SLACK_BOT_TOKEN`: Your Slack bot token.
    - `SLACK_CHANNEL_ID`: The ID of the Slack channel for notifications.

4. Configure the monitoring settings in `config.json`.

## Usage

Start the bot:
```bash
python bot.py
```

The bot will begin monitoring your servers and send alerts to the configured Slack channel.

## Configuration

Edit the `config.json` file to define:
- Server IPs or hostnames.
- Resource usage thresholds (CPU, memory, disk).
- Alert frequency.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Support

For issues or questions, please open an issue in the repository or contact the maintainer.
