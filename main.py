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
    password: str = Field(..., max_length=32)

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
    
    password_lower = payload.password.lower()
    username_lower = payload.username.lower()
    email_prefix = payload.email.split('@')[0].lower()
    
    # Additional check to ensure password does not contain username or email prefix
    if username_lower in password_lower or email_prefix in password_lower:
        results['score'] = 0
        results['feedback']['warning'] = "The password cannot contain your username or email."
        results['feedback']['suggestions'].append("Please choose a password completely unrelated to your personal data.")

    # Additional check to ensure password length is at least 8 characters
    if len(password_lower)<8:
        results['score'] = 0
        results['feedback']['warning'] = "The password is too short."
        results["feedback"]["suggestions"].append("Password is too short. Consider using at least 8 characters.")
        
    has_low = any(char.islower() for char in payload.password)
    has_up = any(char.isupper() for char in payload.password)
    has_num = any(char.isdigit() for char in payload.password)
    has_special = any(not char.isalnum() for char in payload.password)

    # Additional check to ensure password contains a mix of character types
    if not has_low or not has_up or not has_num or not has_special  :
        if results['score'] > 2:
            results['score'] = 2
        results["feedback"]["suggestions"].append("Consider using small and capital letters, numbers, and symbols to increase password strength.")
    
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