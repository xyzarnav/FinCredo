from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import yfinance as yf
from typing import List, Optional, Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
import os
import logging
import atexit

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a shared ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=10)

# Ensure proper cleanup on shutdown
def cleanup():
    executor.shutdown(wait=False)

atexit.register(cleanup)

app = FastAPI(
    title="FinCredo - Indian Stock Market API",
    description="Get Indian stock market data for NSE-listed companies",
    version="1.0.0"
)

# Optimized CORS for n8n
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Enhanced caching with different TTLs
cache = {}
PRICE_CACHE_DURATION = 30  # 30 seconds for price data
COMPANY_CACHE_DURATION = 3600  # 1 hour for company data
MAX_CACHE_SIZE = 1000

def get_cached_data(symbol: str, cache_type: str = "price"):
    cache_key = f"{cache_type}:{symbol}"
    if cache_key in cache:
        data, timestamp = cache[cache_key]
        duration = PRICE_CACHE_DURATION if cache_type == "price" else COMPANY_CACHE_DURATION
        if time.time() - timestamp < duration:
            return data
    return None

def set_cache_data(symbol: str, data: dict, cache_type: str = "price"):
    cache_key = f"{cache_type}:{symbol}"
    # Simple cache size management
    if len(cache) > MAX_CACHE_SIZE:
        # Remove oldest entries
        oldest_key = min(cache.keys(), key=lambda k: cache[k][1])
        del cache[oldest_key]
    
    cache[cache_key] = (data, time.time())

def fetch_optimized_stock_data(symbol: str, data_type: str = "full"):
    """Optimized data fetching with selective fields"""
    try:
        # Add .NS suffix if not present
        if not symbol.endswith('.NS'):
            symbol += '.NS'
            
        stock = yf.Ticker(symbol)
        data = stock.info
        
        if data_type == "price_only":
            # Minimal data for high-frequency price updates
            result = {
                "symbol": symbol,
                "currentPrice": data.get("currentPrice") or data.get("regularMarketPrice"),
                "change": data.get("regularMarketChange"),
                "changePercent": data.get("regularMarketChangePercent"),
                "volume": data.get("volume") or data.get("regularMarketVolume"),
                "timestamp": int(time.time())
            }
        elif data_type == "summary":
            # Key metrics for n8n workflows
            result = {
                "symbol": symbol,
                "name": data.get("longName"),
                "currentPrice": data.get("currentPrice") or data.get("regularMarketPrice"),
                "change": data.get("regularMarketChange"),
                "changePercent": data.get("regularMarketChangePercent"),
                "peRatio": data.get("trailingPE") or data.get("forwardPE"),
                "eps": data.get("trailingEps") or data.get("forwardEps"),
                "priceToBook": data.get("priceToBook"),
                "dividendYield": data.get("dividendYield"),
                "sector": data.get("sector"),
                "marketCap": data.get("marketCap"),
                "volume": data.get("volume") or data.get("regularMarketVolume"),
                "fiftyTwoWeekHigh": data.get("fiftyTwoWeekHigh"),
                "fiftyTwoWeekLow": data.get("fiftyTwoWeekLow"),
                "timestamp": int(time.time())
            }
        else:
            # Full data (your existing comprehensive data)
            hist = stock.history(period="1y")
            year_high = float(hist['High'].max()) if not hist.empty else None
            year_low = float(hist['Low'].min()) if not hist.empty else None
            
            result = {
                # Basic Price Data
                "symbol": symbol,
                "name": data.get("longName"),
                "currentPrice": data.get("currentPrice") or data.get("regularMarketPrice"),
                "open": data.get("open") or data.get("regularMarketOpen"),
                "dayHigh": data.get("dayHigh") or data.get("regularMarketDayHigh"),
                "dayLow": data.get("dayLow") or data.get("regularMarketDayLow"),
                "previousClose": data.get("previousClose") or data.get("regularMarketPreviousClose"),
                "change": data.get("regularMarketChange"),
                "changePercent": data.get("regularMarketChangePercent"),
                
                # Volume & Market Data
                "volume": data.get("volume") or data.get("regularMarketVolume"),
                "averageVolume": data.get("averageVolume") or data.get("averageVolume10days"),
                "marketCap": data.get("marketCap"),
                "currency": data.get("currency"),
                
                # 52-Week Data
                "fiftyTwoWeekHigh": data.get("fiftyTwoWeekHigh") or year_high,
                "fiftyTwoWeekLow": data.get("fiftyTwoWeekLow") or year_low,
                "fiftyTwoWeekChange": data.get("52WeekChange"),
                
                # Valuation Metrics
                "peRatio": data.get("trailingPE") or data.get("forwardPE"),
                "pegRatio": data.get("pegRatio"),
                "priceToBook": data.get("priceToBook"),
                "priceToSales": data.get("priceToSalesTrailing12Months"),
                "enterpriseValue": data.get("enterpriseValue"),
                "evToRevenue": data.get("enterpriseToRevenue"),
                "evToEbitda": data.get("enterpriseToEbitda"),
                
                # Financial Metrics
                "eps": data.get("trailingEps") or data.get("forwardEps"),
                "beta": data.get("beta"),
                "bookValue": data.get("bookValue"),
                "profitMargins": data.get("profitMargins"),
                "returnOnAssets": data.get("returnOnAssets"),
                "returnOnEquity": data.get("returnOnEquity"),
                
                # Dividend Information
                "dividendYield": data.get("dividendYield"),
                "dividendRate": data.get("dividendRate"),
                "exDividendDate": data.get("exDividendDate"),
                "payoutRatio": data.get("payoutRatio"),
                "fiveYearAvgDividendYield": data.get("fiveYearAvgDividendYield"),
                
                # Company Information
                "sector": data.get("sector"),
                "industry": data.get("industry"),
                "country": data.get("country"),
                "exchange": data.get("exchange"),
                "quoteType": data.get("quoteType"),
                "website": data.get("website"),
                "employees": data.get("fullTimeEmployees"),
                
                # Moving Averages
                "fiftyDayAverage": data.get("fiftyDayAverage"),
                "twoHundredDayAverage": data.get("twoHundredDayAverage"),
                
                # Additional Metrics
                "totalCash": data.get("totalCash"),
                "totalDebt": data.get("totalDebt"),
                "debtToEquity": data.get("debtToEquity"),
                "currentRatio": data.get("currentRatio"),
                "quickRatio": data.get("quickRatio"),
                "grossMargins": data.get("grossMargins"),
                "operatingMargins": data.get("operatingMargins"),
                
                # Revenue & Growth
                "totalRevenue": data.get("totalRevenue"),
                "revenuePerShare": data.get("revenuePerShare"),
                "revenueGrowth": data.get("revenueGrowth"),
                "earningsGrowth": data.get("earningsGrowth"),
                
                # Analyst Recommendations
                "recommendationMean": data.get("recommendationMean"),
                "recommendationKey": data.get("recommendationKey"),
                "numberOfAnalystOpinions": data.get("numberOfAnalystOpinions"),
                "targetHighPrice": data.get("targetHighPrice"),
                "targetLowPrice": data.get("targetLowPrice"),
                "targetMeanPrice": data.get("targetMeanPrice"),
                
                # Additional Info
                "sharesOutstanding": data.get("sharesOutstanding"),
                "floatShares": data.get("floatShares"),
                "heldPercentInsiders": data.get("heldPercentInsiders"),
                "heldPercentInstitutions": data.get("heldPercentInstitutions"),
                "shortRatio": data.get("shortRatio"),
                "shortPercentOfFloat": data.get("shortPercentOfFloat"),
                
                # Timestamps
                "timestamp": int(time.time()),
                "lastMarketUpdate": data.get("regularMarketTime")
            }
        
        set_cache_data(symbol, result, "price" if data_type == "price_only" else "company")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {str(e)}")
        return {"error": f"Stock {symbol} not found: {str(e)}"}

@app.get("/")
async def root():
    return {
        "message": "Welcome to FinCredo API",
        "status": "running",
        "docs": "Visit /docs for API documentation"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FinCredo API"}

@app.get("/stock/{symbol}")
async def get_stock(symbol: str):
    """Full comprehensive stock data"""
    try:
        # Add .NS suffix if not present
        if not symbol.endswith('.NS'):
            symbol += '.NS'
            
        cached_data = get_cached_data(symbol, "company")
        if cached_data:
            cached_data["cached"] = True
            return JSONResponse(content=cached_data)
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, fetch_optimized_stock_data, symbol, "full")
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
            
        result["cached"] = False
        return JSONResponse(content=result)
    except asyncio.CancelledError:
        logger.info(f"Request cancelled for {symbol}")
        raise HTTPException(status_code=408, detail="Request cancelled")
    except Exception as e:
        logger.error(f"Error in get_stock: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# OPTIMIZED ENDPOINTS FOR N8N

@app.get("/price/{symbol}")
async def get_price_only(symbol: str):
    """
    Ultra-fast price-only endpoint for n8n bots
    Returns only essential price data with 30-second cache
    Perfect for high-frequency price monitoring
    """
    try:
        cached_data = get_cached_data(symbol, "price")
        if cached_data:
            cached_data["cached"] = True
            return JSONResponse(content=cached_data)
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, fetch_optimized_stock_data, symbol, "price_only")
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
            
        result["cached"] = False
        return JSONResponse(content=result)
    except asyncio.CancelledError:
        logger.info(f"Request cancelled for {symbol}")
        raise HTTPException(status_code=408, detail="Request cancelled")
    except Exception as e:
        logger.error(f"Error in get_price_only: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/summary/{symbol}")
async def get_summary_optimized(symbol: str):
    """
    Optimized summary endpoint for n8n workflows
    Returns key metrics with smart caching
    """
    try:
        cached_data = get_cached_data(symbol, "company")
        if cached_data:
            cached_data["cached"] = True
            return JSONResponse(content=cached_data)
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, fetch_optimized_stock_data, symbol, "summary")
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
            
        result["cached"] = False
        return JSONResponse(content=result)
    except asyncio.CancelledError:
        logger.info(f"Request cancelled for {symbol}")
        raise HTTPException(status_code=408, detail="Request cancelled")
    except Exception as e:
        logger.error(f"Error in get_summary_optimized: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/batch/price")
async def get_batch_prices(symbols: str):
    """
    Batch price endpoint optimized for n8n
    Usage: /batch/price?symbols=TCS.NS,RELIANCE.NS,INFY.NS
    """
    try:
        symbol_list = [s.strip() for s in symbols.split(',')[:20]]  # Limit to 20 symbols
        
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, fetch_optimized_stock_data, symbol, "price_only")
            for symbol in symbol_list
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful_results = [r for r in results if isinstance(r, dict) and "error" not in r]
        errors = [str(r) if isinstance(r, Exception) else r.get("error", "Unknown error") 
                 for r in results if isinstance(r, Exception) or (isinstance(r, dict) and "error" in r)]
        
        return JSONResponse(content={
            "count": len(symbol_list),
            "successful": len(successful_results),
            "prices": successful_results,
            "errors": errors,
            "timestamp": int(time.time())
        })
    except asyncio.CancelledError:
        logger.info("Batch request cancelled")
        raise HTTPException(status_code=408, detail="Request cancelled")
    except Exception as e:
        logger.error(f"Error in get_batch_prices: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/watchlist")
async def get_watchlist_data(symbols: str, type: str = "summary"):
    """
    Optimized watchlist endpoint for n8n
    Usage: /watchlist?symbols=TCS.NS,RELIANCE.NS&type=price
    """
    try:
        symbol_list = [s.strip() for s in symbols.split(',')[:15]]  # Limit to 15 symbols
        data_type = "price_only" if type == "price" else "summary"
        
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, fetch_optimized_stock_data, symbol, data_type)
            for symbol in symbol_list
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful_results = [r for r in results if isinstance(r, dict) and "error" not in r]
        
        return JSONResponse(content={
            "watchlist": successful_results,
            "count": len(successful_results),
            "type": type,
            "timestamp": int(time.time())
        })
    except asyncio.CancelledError:
        logger.info("Watchlist request cancelled")
        raise HTTPException(status_code=408, detail="Request cancelled")
    except Exception as e:
        logger.error(f"Error in get_watchlist_data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/popular/indian")
async def get_popular_indian_stocks():
    """Popular Indian stocks for quick access"""
    popular_stocks = {
        "nifty50_top10": [
            "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
            "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "KOTAKBANK.NS"
        ],
        "sectors": {
            "IT": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS"],
            "Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS"],
            "Energy": ["RELIANCE.NS", "ONGC.NS", "NTPC.NS"],
            "Auto": ["MARUTI.NS", "TATAMOTORS.NS", "BAJAJ-AUTO.NS"]
        }
    }
    return JSONResponse(content=popular_stocks)

@app.get("/health")
def health_check():
    """Health check with cache stats"""
    return JSONResponse(content={
        "status": "healthy",
        "cache_size": len(cache),
        "timestamp": int(time.time()),
        "version": "2.0.0"
    })

@app.get("/metrics")
def get_metrics():
    """API metrics for monitoring"""
    return JSONResponse(content={
        "cache_size": len(cache),
        "cache_hit_ratio": "N/A",  # You can implement this
        "timestamp": int(time.time())
    })

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down FinCredo API...")
    executor.shutdown(wait=False)
