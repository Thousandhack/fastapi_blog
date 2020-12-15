from fastapi.responses import JSONResponse


def fail_response(message):
    data = dict(
        status="fail",
        message=message
    )
    return JSONResponse(data)
