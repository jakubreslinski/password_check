from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from zxcvbn import zxcvbn

app = FastAPI(
    title="Password Strength API",
    description="Microservice for evaluating password strength"
)

# Class defining the request model for password evaluation
class PasswordRequest(BaseModel):
    username: str = Field(..., max_length=32)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)

# Class defining the response model for password evaluation
class PasswordResponse(BaseModel):
    score: int
    strength: str
    feedback: dict

# Endpoint for evaluating password strength
@app.post("/api/v1/evaluate", response_model=PasswordResponse)
async def evaluate_password(payload: PasswordRequest):
    
    user_inputs = [payload.username, payload.email]
    
    # Evaluating password with zxcvbn, considering username and email
    results = zxcvbn(payload.password, user_inputs=user_inputs)
    
    # Mapping score to strength description
    strength_mapping = {
        0: "Very Weak", # guessable after < 10^3 guesses
        1: "Weak",      # guessable after < 10^6 guesses
        2: "Fair",      # guessable after < 10^8 guesses
        3: "Good",      # guessable after < 10^10 guesses
        4: "Strong"     # strong, practically unguessable
    }
    
    return PasswordResponse(
        score=results['score'],
        strength=strength_mapping[results['score']],
        feedback=results['feedback']
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)