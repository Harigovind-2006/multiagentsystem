from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from pipeline import run_research_pipeline

app = FastAPI(title="Neural Research OS API")

# Allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    topic: str

@app.post("/api/research")
async def do_research(request: ResearchRequest):
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required")
        
    try:
        # Calls the existing pipeline implementation
        result_state = run_research_pipeline(request.topic)
        return {
            "status": "success",
            "topic": request.topic,
            "final_report": result_state.get("final_report", "No report generated.")
        }
    except Exception as e:
        print(f"Error during research: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting Research API on port 8000...")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
