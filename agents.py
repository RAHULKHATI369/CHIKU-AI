import os
import pandas as pd
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import google.generativeai as genai
from ntscraper import Nitter # Free Twitter Scraper

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')
scraper = Nitter()

class ChikuState(TypedDict):
    match_context: str
    historical_data: str
    twitter_sentiment: str
    prediction: str
    is_exit: bool

def sentiment_agent(state: ChikuState):
    """Twitter se fans ka mood nikalta hai"""
    try:
        # Free scraping (searching for #IPL2026 or current match)
        tweets = scraper.get_tweets("IPL match", mode='hashtag', number=5)
        texts = [t['text'] for t in tweets['tweets']]
        state['twitter_sentiment'] = " | ".join(texts)[:500]
    except:
        state['twitter_sentiment'] = "Neutral vibes on social media."
    return state

def strategist_agent(state: ChikuState):
    """CSV + Sentiment + Score ko combine karke prediction deta hai"""
    prompt = f"""
    You are Chiku-AI, a Senior Cricket Strategist.
    Live Match: {state['match_context']}
    Historical Weakness: {state['historical_data']}
    Twitter Vibe: {state['twitter_sentiment']}
    
    Task: 
    1. Predict what happens in the next 6 balls.
    2. Recommend the best bowler to get this batsman out.
    3. Give a 'Vibe Score' (0-100).
    Keep it short and aggressive.
    """
    response = model.generate_content(prompt)
    state['prediction'] = response.text
    return state

workflow = StateGraph(ChikuState)
workflow.add_node("scout", sentiment_agent)
workflow.add_node("commander", strategist_agent)
workflow.set_entry_point("scout")
workflow.add_edge("scout", "commander")
workflow.add_edge("commander", END)
chiku_engine = workflow.compile()