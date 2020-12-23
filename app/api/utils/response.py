from fastapi.responses import JSONResponse


def fail_response(message):
    data = dict(
        status="fail",
        message=message
    )
    return JSONResponse(data)


def success_response(data):
    return {'status': 'success', 'data': data}

# def success_response(data):
#     result = dict(
#         status="fail",
#         data=data
#     )
#     return JSONResponse(result)