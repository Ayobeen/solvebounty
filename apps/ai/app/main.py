import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Automatically load root .env or local .env
root_env = Path(__file__).resolve().parents[3] / ".env"
if root_env.exists():
    load_dotenv(dotenv_path=root_env, override=True)
else:
    load_dotenv(override=True)

app = FastAPI(
    title="SolveBounty AI Microservice",
    description="Independent advisory layer for problem decomposition, matching, and solution evaluation",
    version="1.0.0"
)

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock").lower()
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

def call_groq_json(system_prompt: str, user_prompt: str) -> Optional[dict]:
    if LLM_PROVIDER != "groq" or not LLM_API_KEY:
        return None
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)
        else:
            print(f"Groq API error HTTP {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"Groq API exception: {e}")
    return None

class DraftRequest(BaseModel):
    raw_description: str = Field(..., min_length=10, description="Raw problem text entered by challenge creator")

class PrizeEstimate(BaseModel):
    currency: str = "NGN"
    min: int
    recommended: int
    max: int

class DraftResponse(BaseModel):
    title: str
    category: str
    skills: List[str]
    deliverables: List[str]
    requirements: List[str]
    suggested_prize: PrizeEstimate
    confidence: float

class MatchRequest(BaseModel):
    challenge_skills: List[str]
    solver_skills: List[str]
    solver_reputation: float
    solver_completed: int

class MatchResponse(BaseModel):
    final_score: float
    skill_match: float
    reputation_component: float
    recommendation: str

class EvaluateRequest(BaseModel):
    requirements: List[str]
    submission_content: str

class EvaluateResponse(BaseModel):
    overall_score: float
    requirement_coverage_percent: int
    technical_completeness: int
    documentation_quality: int
    originality_risk: str
    strengths: List[str]
    potential_weaknesses: List[str]
    recommendation: str

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-microservice",
        "version": "1.0.0",
        "llm_provider": LLM_PROVIDER,
        "groq_configured": LLM_PROVIDER == "groq" and bool(LLM_API_KEY)
    }

@app.post("/ai/v1/challenge/draft", response_model=DraftResponse)
def draft_challenge(request: DraftRequest):
    desc = request.raw_description.strip()
    
    # Attempt Groq LLM provider if configured
    if LLM_PROVIDER == "groq" and LLM_API_KEY:
        system_prompt = (
            "You are an expert AI Challenge Architect for SolveBounty marketplace in Nigeria. "
            "Analyze the raw problem statement and return a valid JSON object matching this exact schema:\n"
            "{\n"
            '  "title": "Concise title starting with Build:, Design:, or Create:",\n'
            '  "category": "One of: Software Engineering, Data Analytics, Mobile Development, Design, AI & ML, Content & Marketing, General",\n'
            '  "skills": ["Skill 1", "Skill 2"],\n'
            '  "deliverables": ["Deliverable 1", "Deliverable 2"],\n'
            '  "requirements": ["Requirement 1", "Requirement 2"],\n'
            '  "suggested_prize": {"currency": "NGN", "min": 50000, "recommended": 150000, "max": 500000},\n'
            '  "confidence": 0.95\n'
            "}"
        )
        llm_res = call_groq_json(system_prompt, f"Problem Statement: {desc}")
        if llm_res and "title" in llm_res and "suggested_prize" in llm_res:
            try:
                sp = llm_res["suggested_prize"]
                return DraftResponse(
                    title=llm_res.get("title", f"Build: {desc[:40]}"),
                    category=llm_res.get("category", "Software Engineering"),
                    skills=llm_res.get("skills", ["Problem Solving"]),
                    deliverables=llm_res.get("deliverables", ["Working solution"]),
                    requirements=llm_res.get("requirements", ["Address specifications"]),
                    suggested_prize=PrizeEstimate(
                        currency=sp.get("currency", "NGN"),
                        min=int(sp.get("min", 50000)),
                        recommended=int(sp.get("recommended", 125000)),
                        max=int(sp.get("max", 250000))
                    ),
                    confidence=float(llm_res.get("confidence", 0.95))
                )
            except Exception as e:
                print(f"Error parsing Groq challenge draft response: {e}")

    # Fallback heuristics
    words = desc.lower()
    if any(k in words for k in ["dashboard", "sales", "analytics", "power bi", "tableau", "bi"]):
        category = "Data Analytics"
        skills = ["Power BI", "SQL", "Data Visualization", "Data Analysis"]
        deliverables = ["Interactive sales dashboard", "Clean ETL SQL scripts", "User documentation guide"]
        requirements = ["Monthly revenue breakdown", "Customer segmentation filter", "Exportable summary PDF"]
        min_p, rec_p, max_p = 75000, 125000, 200000
    elif any(k in words for k in ["app", "flutter", "react native", "mobile", "ios", "android"]):
        category = "Mobile Development"
        skills = ["React Native", "TypeScript", "Mobile UI", "API Integration"]
        deliverables = ["Working APK/TestFlight build", "Clean GitHub repository", "Setup walkthrough video"]
        requirements = ["Responsive mobile layout", "Offline caching support", "Push notification integration"]
        min_p, rec_p, max_p = 150000, 250000, 450000
    elif any(k in words for k in ["logo", "brand", "design", "ui", "ux", "figma"]):
        category = "Design"
        skills = ["UI/UX Design", "Figma", "Graphic Design", "Logo Design"]
        deliverables = ["Figma design system file", "Vector SVG & PNG exports", "Brand style guide"]
        requirements = ["Modern minimalist aesthetic", "Dark & light mode variants", "Full component tokens"]
        min_p, rec_p, max_p = 40000, 80000, 150000
    else:
        category = "Software Engineering"
        skills = ["Python", "Django", "PostgreSQL", "REST API"]
        deliverables = ["Complete source code repository", "Comprehensive test suite", "Deployment instructions"]
        requirements = ["Strict adhering to specification", "Clean modular structure", "High unit test coverage"]
        min_p, rec_p, max_p = 100000, 180000, 300000

    title = f"Build: {desc[:50].strip().title()}"

    return DraftResponse(
        title=title,
        category=category,
        skills=skills,
        deliverables=deliverables,
        requirements=requirements,
        suggested_prize=PrizeEstimate(currency="NGN", min=min_p, recommended=rec_p, max=max_p),
        confidence=0.91
    )

@app.post("/ai/v1/challenge/match", response_model=MatchResponse)
def match_solver(req: MatchRequest):
    if not req.challenge_skills:
        skill_score = 0.8
    else:
        matched = set(s.lower() for s in req.solver_skills).intersection(set(s.lower() for s in req.challenge_skills))
        skill_score = len(matched) / len(req.challenge_skills)

    rep_score = min(req.solver_reputation / 5.0, 1.0) if req.solver_reputation else 0.5
    history_score = min(req.solver_completed / 10.0, 1.0)

    # Hybrid matching formula from spec
    final_score = round((skill_score * 0.45) + (rep_score * 0.35) + (history_score * 0.20), 2)

    return MatchResponse(
        final_score=final_score,
        skill_match=round(skill_score, 2),
        reputation_component=round(rep_score, 2),
        recommendation="High Match" if final_score >= 0.75 else "Moderate Match"
    )

@app.post("/ai/v1/submission/evaluate", response_model=EvaluateResponse)
def evaluate_submission(req: EvaluateRequest):
    # Attempt Groq LLM provider if configured
    if LLM_PROVIDER == "groq" and LLM_API_KEY:
        system_prompt = (
            "You are an expert technical submission evaluator for SolveBounty marketplace. "
            "Analyze the solver submission against the challenge requirements and return a JSON object:\n"
            "{\n"
            '  "overall_score": 88.5,\n'
            '  "requirement_coverage_percent": 90,\n'
            '  "technical_completeness": 85,\n'
            '  "documentation_quality": 80,\n'
            '  "originality_risk": "LOW",\n'
            '  "strengths": ["Strength 1", "Strength 2"],\n'
            '  "potential_weaknesses": ["Weakness 1"],\n'
            '  "recommendation": "Strong candidate for human review."\n'
            "}"
        )
        user_prompt = f"Requirements: {json.dumps(req.requirements)}\nSubmission: {req.submission_content}"
        llm_res = call_groq_json(system_prompt, user_prompt)
        if llm_res and "overall_score" in llm_res:
            try:
                return EvaluateResponse(
                    overall_score=float(llm_res.get("overall_score", 85.0)),
                    requirement_coverage_percent=int(llm_res.get("requirement_coverage_percent", 80)),
                    technical_completeness=int(llm_res.get("technical_completeness", 80)),
                    documentation_quality=int(llm_res.get("documentation_quality", 80)),
                    originality_risk=str(llm_res.get("originality_risk", "LOW")),
                    strengths=llm_res.get("strengths", ["Clear solution outline"]),
                    potential_weaknesses=llm_res.get("potential_weaknesses", ["Further testing recommended"]),
                    recommendation=str(llm_res.get("recommendation", "Candidate for review"))
                )
            except Exception as e:
                print(f"Error parsing Groq submission evaluation: {e}")

    # Fallback heuristic evaluation
    content_len = len(req.submission_content.strip())
    coverage = 92 if content_len > 150 else 75
    completeness = 88 if content_len > 100 else 60

    return EvaluateResponse(
        overall_score=89.5,
        requirement_coverage_percent=coverage,
        technical_completeness=completeness,
        documentation_quality=85,
        originality_risk="LOW",
        strengths=[
            "Direct alignment with posted technical constraints",
            "Clear deliverable structure with accessible source repositories"
        ],
        potential_weaknesses=[
            "Ensure full verification under load"
        ],
        recommendation="Strong candidate for human review."
    )

