# AI-Personal-News-Assistant-
A conversational AI assistant that fetches live global news by topic and country, summarizes it using Claude AI, and delivers it to your Gmail inbox on request. Built with Python using NewsAPI, Claude, and Gmail OAuth. Features persistent memory, natural language understanding, and a chatbot interface.
You type: "show me tech news from us"
        ↓
Claude understands your intent
        ↓
NewsAPI fetches live articles from global sources
        ↓
Claude reads all articles and writes a clean digest
        ↓
You say: "send it to my email"
        ↓
Gmail API delivers it to your inbox


What is inside

File	Job
main.py	Runs the chat loop
news_helper.py	Fetches news from NewsAPI
ai_helper.py	Intent detection + summarization
email_helper.py	Sends email via Gmail OAuth
memory.py	Remembers conversations across sessions



Built on top of

Project	What it contributed
Project 1	Gmail API OAuth authentication
Project 2	Chatbot + persistent memory
Project 3 NEW	Live internet data, intent detection, virtual environment, Git
