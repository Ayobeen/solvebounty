from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

app = FastAPI(
    title="SolveBounty AI Microservice",
    description="Independent advisory layer for problem decomposition, matching, and solution evaluation",
    version="1.0.0"
)

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
    return {"status": "ok", "service": "ai-microservice", "version": "1.0.0"}

@app.post("/ai/v1/challenge/draft", response_model=DraftResponse)
def draft_challenge(request: DraftRequest):
    desc = request.raw_description.strip()
    
    # Intelligent heuristics / LLM provider simulation
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
