<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:07111F,45:123B63,100:00C6FF&height=230&section=header&text=SOUVION%20AI&fontSize=60&fontColor=FFFFFF&fontAlignY=38&desc=Intelligent%20Discord%20AI%20Assistant&descAlignY=60&descSize=17" width="100%" />

# 🤖 Souvion AI

### A multi-provider AI assistant for Discord

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![AI](https://img.shields.io/badge/AI-Multi--Provider-00C6FF?style=for-the-badge)](#-ai-providers)
[![Storage](https://img.shields.io/badge/Storage-GitHub%20JSON-181717?style=for-the-badge&logo=github)](#-knowledge-storage)

**Conversational AI • Server Knowledge • Developer Tools**

</div>

---

## ✨ About

**Souvion AI** is a Python-powered Discord assistant built with `discord.py`. It combines AI provider integrations, language-aware responses, server-specific knowledge, developer utilities, and live bot statistics in a modular Cog-based architecture.

The bot is designed to support conversations in Bengali, Banglish, Hinglish, and English, with a knowledge system that can keep global information separate from individual server knowledge.

---

## 🚀 Features

### 🧠 AI Assistant
- AI-powered Discord conversations.
- Multiple AI provider integrations.
- Language detection for Bengali, Banglish, Hinglish, and English.
- Explicit language requests supported.
- Roman-word normalization for common Banglish and Hinglish short forms.
- Provider timeout and concurrency controls.
- Knowledge-aware responses using stored information.

### 📚 Knowledge System
- Global knowledge storage.
- Separate knowledge data for each Discord server.
- Server prefix storage.
- Add, search, list, and clear knowledge using available knowledge commands.
- Optional GitHub JSON persistence.
- Knowledge data stored in `data/knowledge.json`.

### 🛠️ Developer & Utility Tools
- Dedicated developer command module.
- Custom help panel.
- Bot information command.
- Ping and latency checks.
- Live server and member statistics.
- Rotating bot presence.
- Automatic statistics embed refresh.

### 🧩 Modular Architecture
- Separate Cogs for AI, developer, knowledge, help, utility, statistics, and ping.
- Dynamic per-server command prefix support.
- Centralized configuration through environment variables.
- Asynchronous startup and extension loading.

---

## 🤖 AI Providers

Souvion AI currently includes integrations for:

| Provider | Integration |
|---|---|
| Groq | OpenAI-compatible API client |
| Google Gemini | Google Gen AI SDK |
| OpenRouter | OpenAI-compatible API client |

The configured model identifiers in the current source are:

- **Groq:** `openai/gpt-oss-20b`
- **Gemini:** `gemini-3.8-flash`
- **OpenRouter:** `openrouter/free`

Provider availability depends on valid API credentials, model availability, and each provider's current API policies.

---

## 🧠 Language Intelligence

Souvion AI includes language detection logic designed for:

- **Bengali:** বাংলা script.
- **Banglish:** Bengali written with English/Roman letters.
- **Hinglish:** Hindi written with English/Roman letters.
- **English:** English-language messages.

The AI Cog uses deterministic language markers and normalization before its AI-based language-classification fallback. Users can also request a response language explicitly.

---

## 📂 Project Structure

```text
souvion-ai/
│
├── bot.py
├── config.py
├── requirements.txt
├── Procfile
├── .env.example
├── .gitignore
│
├── cogs/
│   ├── __init__.py
│   ├── ai.py
│   ├── dev.py
│   ├── help.py
│   ├── knowledge.py
│   ├── ping.py
│   ├── stats.py
│   └── utility.py
│
├── data/
│   └── knowledge.json
│
└── services/
    ├── __init__.py
    └── github_storage.py
```

---

## ⚙️ Requirements

- Python 3.x
- Discord application and bot token
- Discord Developer Portal access
- AI provider API key for the provider(s) you want to use
- GitHub Personal Access Token if GitHub knowledge storage is enabled

Python dependencies are listed in `requirements.txt`:

```text
discord.py
google-genai
openai
aiohttp
```

---

## 📥 Installation

### 1. Clone the repository

```bash
git clone https://github.com/dcsoumen87-blip/souvion-ai.git
```

### 2. Open the project folder

```bash
cd souvion-ai
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file or add the variables in your hosting provider's environment settings.

Example:

```env
DISCORD_TOKEN=your_discord_bot_token

GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

DEV_USER_ID=your_discord_user_id

GITHUB_TOKEN=your_github_token
GITHUB_REPO=dcsoumen87-blip/souvion-ai
GITHUB_BRANCH=main
GITHUB_KNOWLEDGE_PATH=data/knowledge.json

STATS_CHANNEL_ID=your_stats_channel_id
```

Only configure the provider and storage credentials you intend to use. `STATS_CHANNEL_ID` is optional; it identifies the channel used by the statistics Cog.

### 5. Enable Discord intents

In the Discord Developer Portal, enable the privileged intents required by the current bot configuration:

- Message Content Intent
- Server Members Intent

Invite the bot with the permissions needed for the commands and features you enable. Follow the principle of least privilege.

### 6. Start the bot

```bash
python bot.py
```

---

## ☁️ Deployment

The repository includes a `Procfile` configured with:

```text
worker: python bot.py
```

For Railway or another compatible worker host:

1. Connect the GitHub repository.
2. Set the required environment variables in the service dashboard.
3. Confirm the start command uses `python bot.py` (or the included Procfile).
4. Deploy and inspect the runtime logs.
5. Confirm that all required Cogs load and the bot becomes online.

Do not commit `.env` files, bot tokens, API keys, or GitHub tokens to the repository.

---

## 🗃️ Knowledge Storage

The project includes `services/github_storage.py`, which can load and save the knowledge JSON file through the GitHub Contents API.

Configure:

```env
GITHUB_TOKEN=your_github_token
GITHUB_REPO=dcsoumen87-blip/souvion-ai
GITHUB_BRANCH=main
GITHUB_KNOWLEDGE_PATH=data/knowledge.json
```

The GitHub token must have only the repository access required to read and update the knowledge file. Keep it private.

When GitHub storage is not configured or a synchronization request fails, the application reports the failure in its logs. Check those logs to confirm whether a knowledge update was successfully synchronized.

---

## 💬 Commands

The project uses the default prefix `!` and supports a dynamic per-server prefix through its knowledge/prefix system. The bot also registers application commands through Discord's command tree.

Examples of general commands implemented in the repository:

| Command | Description |
|---|---|
| `!ping` | Check bot latency |
| `!botinfo` | Display bot information |
| `/ping` | Slash-command latency check |

The AI, developer, help, and knowledge Cogs contain additional commands. Use the bot's help panel in Discord for the current command list and permission details. Developer-only commands are restricted by the checks implemented in the source.

---

## 📊 Statistics

When `STATS_CHANNEL_ID` is configured, the statistics Cog can:

- Publish a live statistics embed.
- Display the number of servers and aggregated member counts.
- Update the existing statistics message when possible.
- Refresh the statistics embed periodically.
- Rotate the bot's presence between developer, member, and server information.

Member totals are summed across servers; members present in more than one server may be counted more than once.

---

## 🔐 Security Notes

- Never share your Discord bot token.
- Never publish AI provider API keys.
- Never expose your GitHub Personal Access Token.
- Keep `.env` out of version control.
- Use a restricted GitHub token with only the required repository permissions.
- Review developer commands and permission checks before production deployment.
- Grant the bot only the Discord permissions it needs.
- Review logs after deployment and after knowledge synchronization.

If any credential is exposed, revoke or rotate it immediately.

---

## 🤝 Contributing

Contributions focused on reliability, security, documentation, maintainability, and useful AI features are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make focused changes.
4. Test your changes in a private development server.
5. Submit a pull request with a clear description.

Do not include tokens, secrets, or private server information in contributions.

---

## 👨‍💻 Developer

<div align="center">

### MOD TRYOUT

**Creator & Developer of Souvion AI**

[![GitHub](https://img.shields.io/badge/GitHub-dcsoumen87--blip-181717?style=for-the-badge&logo=github)](https://github.com/dcsoumen87-blip)
[![Email](https://img.shields.io/badge/Email-soumen96%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:soumen96a@gmail.com)

**GitHub:** [dcsoumen87-blip](https://github.com/dcsoumen87-blip)  
**Email:** soumen96a@gmail.com

</div>

---

<div align="center">

**If Souvion AI helps you, consider giving the repository a ⭐**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00C6FF,50:123B63,100:07111F&height=130&section=footer" width="100%" />

</div>
