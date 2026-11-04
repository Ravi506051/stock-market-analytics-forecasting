import streamlit as st, pandas as pd, numpy as np, plotly.express as px
st.title("Stock Market Analytics & Forecasting"); st.caption("Research demo only; not investment advice.")
up=st.file_uploader("Upload CSV containing Date and Close",type="csv"); ticker=st.text_input("Ticker for optional live download","DEMO").upper()
d=None
if up:
 d=pd.read_csv(up); d["Date"]=pd.to_datetime(d["Date"]); d["Close"]=pd.to_numeric(d["Close"],errors="coerce")
elif ticker!="DEMO":
 try:
  import yfinance as yf
  z=yf.download(ticker,period="2y",auto_adjust=True,progress=False); close=z["Close"]; close=close.iloc[:,0] if isinstance(close,pd.DataFrame) else close; d=pd.DataFrame({"Date":close.index,"Close":close.values})
 except Exception as e: st.info(f"Live data unavailable: {e}")
if d is None:
 r=np.random.default_rng(5); dates=pd.bdate_range("2023-01-01",periods=500); d=pd.DataFrame({"Date":dates,"Close":100*np.exp(np.cumsum(r.normal(.0004,.012,len(dates))))}); st.info("Synthetic sample prices shown.")
d=d.dropna().sort_values("Date"); d["return"]=d.Close.pct_change(); d["volatility_20d"]=d["return"].rolling(20).std()*np.sqrt(252)
a,b,c=st.columns(3); a.metric("Latest close",f"{d.Close.iloc[-1]:.2f}"); b.metric("Daily return",f"{d['return'].iloc[-1]:.2%}"); c.metric("20d volatility",f"{d.volatility_20d.iloc[-1]:.1%}")
st.plotly_chart(px.line(d,x="Date",y="Close"),use_container_width=True); st.plotly_chart(px.line(d,x="Date",y="volatility_20d"),use_container_width=True); st.dataframe(d.tail(20))
