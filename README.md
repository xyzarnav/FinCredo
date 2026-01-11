# 📈 FinCredo – Indian Stock Market Data API

FinCredo is a **lightweight Python-based REST API** that provides **Indian stock market data** such as **current price, PE ratio, EPS, market cap, 52-week high/low, and other fundamentals** for NSE-listed companies.

The project uses **Yahoo Finance (`yfinance`)** as the data source and is built using **FastAPI**, making it fast, simple, and easy to extend.

---

## 🚀 Features
- Supports **NSE stocks** using `.NS` symbols (e.g. `TCS.NS`, `RELIANCE.NS`)
- Live stock price & daily range
- Valuation metrics (PE, PB, EPS)
- Company fundamentals (sector, industry, market cap)
- 52-week high & low
- Free to use (no API key required)

---

## 🛠 Tech Stack
- Python
- FastAPI
- yfinance
- Uvicorn

---

## 📦 Installation & Setup

Follow these steps to run the project locally.

### 1️⃣ Prerequisites
Make sure you have:
- Python **3.9 or above**
- Git installed

Check versions:
```bash
python --version
git --version
