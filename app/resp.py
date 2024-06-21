from fastapi.responses import JSONResponse

def respond(content: dict, status: bool = True, cause: str = ""):
    mod_content = content
    mod_content["status"] = status

    if not status:
        mod_content["cause"] = cause
    
    return JSONResponse(mod_content, 200 if status else 404)