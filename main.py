import asyncio
import json
import random
from typing import Any, Dict, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from agents import chiku_engine, model
from database import chiku_brain 
from pycricbuzz import Cricbuzz

app = FastAPI()

# --- STEP 1: CORS SETTINGS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cb = Cricbuzz()

async def get_dynamic_match_telemetry() -> tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Live match data extraction with strict defensive checks."""
    try:
        matches = cb.matches()
        if not matches:
            return None, "Commander, no active operations. Radar clear."

        live_match = next((m for m in matches if m.get('m_status') != 'Match ended'), None)
        if not live_match:
            return None, "All battles for today have concluded."

        m_id = live_match.get('id')
        if not m_id:
            return None, "Target ID missing. Re-scanning satellite..."

        status_text = str(live_match.get('status', '')).lower()
        ls = cb.livescore(m_id)
        
        if not ls or not isinstance(ls, dict):
            return {
                "type": "PRE_MATCH",
                "prediction": f"Status: {status_text}",
                "score": "N/A",
                "status": status_text
            }, None

        batting = ls.get('batting', {})
        batsman_list = batting.get('batsman', [])
        current_batsman = batsman_list[0].get('name', 'Unknown') if (batsman_list and isinstance(batsman_list, list)) else "Loading..."
        
        score_list = ls.get('score', [])
        score_data = score_list[0] if (score_list and isinstance(score_list, list)) else {}
        runs = score_data.get('runs', '0')
        wickets = score_data.get('wickets', '0')
        
        innings_list = batting.get('innings', [])
        overs = innings_list[0].get('overs', '0.0') if (innings_list and isinstance(innings_list, list)) else '0.0'

        return {
            "type": "LIVE",
            "batsman": current_batsman,
            "score": f"{runs}/{wickets}",
            "overs": overs,
            "status": status_text
        }, None

    except Exception as e:
        return None, f"Satellite Comms Jammed: {str(e)}"

# --- STEP 2: WEBSOCKET WAR-ROOM ---
@app.websocket("/ws/chiku")
async def chiku_war_room(websocket: WebSocket):
    await websocket.accept()
    print("🚀 CRIC-COMMANDER: War-Room Link Established via /ws/chiku")
    
    try:
        while True:
            data, error = await get_dynamic_match_telemetry()
            
            # Default payload structure
            payload: Dict[str, Any] = {
                "score": "Scanning...",
                "overs": "0.0",
                "batsman": "Unknown",
                "is_live": False,
                "vibe": 50,
                "prediction": "Scanning battlefield...",
                "nextBall": "DOT",
                "twitterVibe": "NEUTRAL"
            }

            if error or not data:
                payload["alert"] = error or "Radar Clear."
                await websocket.send_text(json.dumps(payload))
                await asyncio.sleep(15)
                continue

            # Base Data
            payload["score"] = data.get('score', '0/0')
            payload["overs"] = data.get('overs', '0.0')
            payload["batsman"] = data.get('batsman', 'Unknown')
            payload["is_live"] = data.get('type') == "LIVE"

            # Check for RAIN or DELAY in status
            status = data.get('status', '')
            if "rain" in status or "delayed" in status:
                payload["alert"] = "RAIN DELAY: Satellite shows heavy clouds. DLS mode active."
                payload["twitterVibe"] = "ANXIOUS 🌧️"
                payload["vibe"] = 30
                payload["nextBall"] = "WAITING"
            
            elif data.get('type') == "LIVE":
                # 1. Get History from CSV
                history = chiku_brain.get_tactical_insight(data['batsman'])
                
                # 2. Invoke Gemini Agent for Dynamic Tactical Alert & Prediction
                context = f"Match Score: {data['score']}. Batsman: {data['batsman']}. Status: {status}."
                inputs: Any = {
                    "match_context": context, 
                    "historical_data": history, 
                    "is_exit": False
                }
                
                try:
                    result = chiku_engine.invoke(inputs)
                    res_val = result.get('prediction', '') if hasattr(result, 'get') else getattr(result, 'prediction', '')
                    payload["alert"] = res_val
                    
                    # 3. Dynamic Ball Prediction Logic (Based on Gemini's alert)
                    if "wicket" in res_val.lower(): payload["nextBall"] = "WICKET"
                    elif "six" in res_val.lower() or "boundary" in res_val.lower(): payload["nextBall"] = "SIX"
                    elif "four" in res_val.lower(): payload["nextBall"] = "FOUR"
                    else: payload["nextBall"] = random.choice(["DOT", "SINGLE", "DOT"])

                    # 4. Dynamic Twitter Vibe (Simulated via Score Momentum)
                    payload["vibe"] = random.randint(70, 95) if "SIX" in payload["nextBall"] else random.randint(40, 70)
                    payload["twitterVibe"] = "ROARING 🦁" if payload["vibe"] > 75 else "INTENSE ⚡"

                except Exception as e:
                    payload["alert"] = f"Tactical Engine Error: {str(e)}"
            
            else:
                payload["alert"] = f"Match Status: {status.upper()}"
                payload["twitterVibe"] = "HYPED 🔥"
                payload["nextBall"] = "PRE-MATCH"

            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(10) # Refresh rate
            
    except WebSocketDisconnect:
        print("❌ link severed by Commander.")
    except Exception as e:
        print(f"⚠️ System Failure: {e}")

@app.post("/chat")
async def handle_user_query(query: Dict[str, Any]):
    user_msg = query.get("text", "")
    try:
        response = model.generate_content(f"Respond as CRIC-COMMANDER AI: {user_msg}")
        return {"response": response.text}
    except Exception:
        return {"response": "Signal interference."}