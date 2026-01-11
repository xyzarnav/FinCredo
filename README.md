# 📈 FinCredo – Indian Stock Market Data API

FinCredo is a **lightweight Python-based REST API** that provides **Indian stock market data** such as **current price, PE ratio, EPS, market cap, 52-week high/low, and other fundamentals** for NSE-listed companies.

The project uses **Yahoo Finance (`yfinance`)** as the data source and is built using **FastAPI**, making it fast, simple, and easy to extend.

---

## 🚀 Features
- ✅ Supports **NSE stocks** using `.NS` symbols (e.g. `TCS.NS`, `RELIANCE.NS`)
- ✅ Live stock price & daily range
- ✅ Valuation metrics (PE, PB, EPS, ROE, Beta)
- ✅ Company fundamentals (sector, industry, market cap)
- ✅ 52-week high & low data
- ✅ Dividend yield & debt-to-equity ratios
- ✅ Multiple API endpoints optimized for different use cases
- ✅ Built-in caching for improved performance
- ✅ CORS enabled for web applications
- ✅ Free to use (no API key required)

---

## 🛠 Tech Stack
- **Python 3.9+**
- **FastAPI** - Modern web framework
- **yfinance** - Yahoo Finance data fetcher
- **Uvicorn** - ASGI server
- **asyncio** - Async processing

---

## 📦 Installation & Setup

Follow these steps to run the project locally.

### 1️⃣ Prerequisites
Make sure you have:
- Python **3.9 or above**
- Git installed
- Internet connection (for fetching stock data)

Check versions:
```bash
python --version
git --version
```

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/xyzarnav/FinCredo.git
cd FinCredo
```

### 3️⃣ Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install fastapi uvicorn yfinance python-multipart
```

### 5️⃣ Run the API Server
```bash
uvicorn main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

### 6️⃣ Test the API
Open your browser and visit:
- **API Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health
- **Test Endpoint**: http://127.0.0.1:8000/test

---

## 🔗 API Endpoints

### Base URL
```
http://127.0.0.1:8000
```

### 📊 Main Endpoints

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/` | GET | Welcome message & API info | `/` |
| `/health` | GET | API health status | `/health` |
| `/test` | GET | Simple test endpoint | `/test` |

### 📈 Stock Data Endpoints

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/stock/{symbol}` | GET | Complete stock data | `/stock/TCS` |
| `/price/{symbol}` | GET | Price-only data (fast) | `/price/RELIANCE` |
| `/summary/{symbol}` | GET | Key metrics summary | `/summary/INFY` |

### 📋 Batch & Watchlist Endpoints

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/batch/price` | GET | Multiple stock prices | `/batch/price?symbols=TCS.NS,RELIANCE.NS` |
| `/watchlist` | GET | Watchlist data | `/watchlist?symbols=TCS.NS,INFY.NS&type=summary` |
| `/popular/indian` | GET | Popular Indian stocks | `/popular/indian` |

---

## 💡 Usage Examples

### 1. Get Complete Stock Data
```bash
curl "http://127.0.0.1:8000/stock/TCS"
```

**Response:**
```json
{
  "symbol": "TCS.NS",
  "name": "Tata Consultancy Services Limited",
  "currentPrice": 3756.25,
  "change": 45.80,
  "changePercent": 1.23,
  "peRatio": 28.5,
  "eps": 131.89,
  "dividendYield": 2.1,
  "roe": 44.2,
  "debtToEquity": 0.05,
  "bookValue": 298.7,
  "beta": 0.8,
  "marketCap": 13654000000000,
  "sector": "Information Technology",
  "industry": "Information Technology Services"
}
```

### 2. Get Quick Price Data
```bash
curl "http://127.0.0.1:8000/price/RELIANCE"
```

### 3. Get Multiple Stock Prices
```bash
curl "http://127.0.0.1:8000/batch/price?symbols=TCS.NS,RELIANCE.NS,INFY.NS"
```

### 4. Python Usage Example
```python
import requests

# Get stock data
response = requests.get("http://127.0.0.1:8000/stock/TCS")
data = response.json()

print(f"Stock: {data['name']}")
print(f"Price: ₹{data['currentPrice']}")
print(f"PE Ratio: {data['peRatio']}")
```

### 5. JavaScript/Node.js Usage
```javascript
fetch('http://127.0.0.1:8000/stock/TCS')
  .then(response => response.json())
  .then(data => {
    console.log(`Stock: ${data.name}`);
    console.log(`Price: ₹${data.currentPrice}`);
    console.log(`PE Ratio: ${data.peRatio}`);
  });
```

---

## 📊 Supported Stock Symbols

FinCredo supports **NSE-listed stocks**. Use the stock symbol with `.NS` suffix:

### Popular Stocks
- **TCS.NS** - Tata Consultancy Services
- **RELIANCE.NS** - Reliance Industries
- **HDFCBANK.NS** - HDFC Bank
- **INFY.NS** - Infosys
- **ICICIBANK.NS** - ICICI Bank
- **HINDUNILVR.NS** - Hindustan Unilever
- **SBIN.NS** - State Bank of India
- **BHARTIARTL.NS** - Bharti Airtel
- **ITC.NS** - ITC Limited
- **KOTAKBANK.NS** - Kotak Mahindra Bank

### Auto-Detection
The API automatically adds `.NS` suffix if not provided:
- `/stock/TCS` → `/stock/TCS.NS`
- `/stock/RELIANCE` → `/stock/RELIANCE.NS`

---

## ⚡ Performance Features

### Caching System
- **Price data**: 30-second cache
- **Company data**: 1-hour cache
- **Automatic cache cleanup**

### Optimized Endpoints
- **`/price/{symbol}`** - Ultra-fast price updates
- **`/summary/{symbol}`** - Key metrics only
- **`/stock/{symbol}`** - Complete data

### Concurrent Processing
- **Batch requests** support up to 20 stocks
- **Async processing** with ThreadPoolExecutor
- **Timeout handling** prevents hanging requests

---

## 🔧 Configuration

### Environment Variables (Optional)
```bash
# Set log level
export LOG_LEVEL=INFO

# Set cache duration (seconds)
export PRICE_CACHE_DURATION=30
export COMPANY_CACHE_DURATION=3600
```

### Custom Port
```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

---

## 🛠 Development

### Project Structure
```
FinCredo/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Add your endpoint in `main.py`
4. Test thoroughly
5. Submit a pull request

---

## 🚨 Troubleshooting

### Common Issues

**1. Server won't start**
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install --upgrade fastapi uvicorn yfinance
```

**2. Stock data not loading**
- Check internet connection
- Verify stock symbol exists on NSE
- Try with `.NS` suffix explicitly

**3. Timeout errors**
- Wait a few seconds and retry
- Yahoo Finance might be temporarily unavailable
- Check if symbol is correct

**4. CORS issues**
- API already has CORS enabled
- Check browser console for specific errors

### Debug Mode
```bash
# Run with debug logging
uvicorn main:app --reload --log-level debug
```

---

## 📄 API Response Fields

### Complete Stock Data Fields
| Field | Description | Example |
|-------|-------------|---------|
| `symbol` | Stock symbol with exchange | "TCS.NS" |
| `name` | Company name | "Tata Consultancy Services" |
| `currentPrice` | Current stock price | 3756.25 |
| `change` | Price change | 45.80 |
| `changePercent` | Percentage change | 1.23 |
| `peRatio` | Price-to-Earnings ratio | 28.5 |
| `eps` | Earnings per share | 131.89 |
| `dividendYield` | Dividend yield % | 2.1 |
| `roe` | Return on Equity % | 44.2 |
| `debtToEquity` | Debt-to-Equity ratio | 0.05 |
| `bookValue` | Book value per share | 298.7 |
| `beta` | Stock volatility measure | 0.8 |
| `marketCap` | Market capitalization | 13654000000000 |
| `sector` | Business sector | "Information Technology" |
| `industry` | Industry category | "IT Services" |
| `volume` | Trading volume | 2500000 |
| `fiftyTwoWeekHigh` | 52-week high price | 4000.0 |
| `fiftyTwoWeekLow` | 52-week low price | 2800.0 |

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs** - Open an issue with details
2. **Suggest Features** - Share your ideas
3. **Submit PRs** - Fix bugs or add features
4. **Improve Documentation** - Help others understand better

### Development Setup
```bash
git clone https://github.com/xyzarnav/FinCredo.git
cd FinCredo
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 📜 License

This project is **open-source** and available under the [MIT License](LICENSE).

---

## ⭐ Support

If you find FinCredo helpful:
- **Star this repository** ⭐
- **Share with others** 📤
- **Report issues** 🐛
- **Contribute improvements** 🚀

---

## 📞 Contact

- **GitHub**: [@xyzarnav](https://github.com/xyzarnav)
- **Issues**: [GitHub Issues](https://github.com/xyzarnav/FinCredo/issues)

---

**Happy Trading! 📈**
