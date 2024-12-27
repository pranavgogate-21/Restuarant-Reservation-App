from fastapi.responses import JSONResponse

class ResponseBuilder:

    @staticmethod
    def success(data=None, status=None):
        return JSONResponse({"data":data}, status_code=status)

    @staticmethod
    def error(data=None, status=None):
        return JSONResponse({"error":data}, status_code=status)
