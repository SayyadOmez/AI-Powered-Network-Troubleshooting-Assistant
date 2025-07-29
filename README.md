# 🤖 AI-Powered Network Troubleshooting Assistant

Say goodbye to spending hours digging through network logs! This tool helps network engineers, students, and anyone in IT troubleshoot faster — using the power of GPT-4 and intelligent document search.

## ✨ What It Does

Have a confusing log file? Just paste it into the web app.

Our assistant:
- Understands your log
- Pulls in helpful info from vendor docs (like Cisco or Huawei)
- Gives you a clear answer: **what’s wrong**, **why it’s happening**, and **how to fix it**
- Lets you ask follow-up questions too — like chatting with an expert!

## 🛠️ What We Used

This project is built with:
- **Python** & **Flask** – For the backend and web app
- **OpenAI’s GPT-4 API** – To read and explain logs in plain English
- **LangChain** – To connect everything smoothly
- **FAISS** – To search through relevant documents and troubleshooting guides
- **Bootstrap 5 + HTML/CSS + Jinja2** – For a clean, chat-like interface

## 💡 Why We Built It

Troubleshooting networks is hard — logs come from so many tools: ping, traceroute, DNS lookups, firewall alerts… And they’re not easy to read. We wanted a tool that:
- Works fast during outages
- Makes sense of logs for beginners
- Reinforces learning with clear answers
- Is simple enough to demo in a classroom


## 🚀 How to Run It

1. Clone the repo  
   ```bash
   git clone https://github.com/your-username/network-troubleshooting-assistant.git
   cd network-troubleshooting-assistant
