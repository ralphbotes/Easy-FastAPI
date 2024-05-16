import uvicorn
import time
import contextlib
import threading
from fastapi import Body, FastAPI, Request, HTTPException
from utils import get_line_info, request_checker
from data_handling import getRequestData

app = FastAPI(docs_url=None, redoc_url=None)

@app.get('/')
async def root():
    return {
        "error_code": "200",
        "payload": {"message": "Connection active and secured"}
    }

@app.post('/my_request')
async def my_request(request: Request, bod: dict = Body(...)):
    request, l_headers, l_body = request_checker(request, bod)

    if not "request_type" in l_body:
        raise HTTPException(
            status_code=401,
            detail={
                "payload": {"message": "Required params not available"},
                "error_code": 101
            }
        )
    
    return getRequestData(l_body["request_type"])

if __name__ == '__main__':
    try:
        print(f'Startup FastAPI Server')
        
        class Server(uvicorn.Server):
            @contextlib.contextmanager
            def run_in_thread(self):
                thread = threading.Thread(target=self.run)
                thread.start()
                try:
                    while not self.started:
                        time.sleep(1e-4)
                    yield
                finally:
                    self.should_exit = True
                    thread.join()

        config = uvicorn.Config("main:app", host="127.0.0.1", port=80, log_level="debug", reload=True)
        server = Server(config=config)
        server.run()
    except Exception as e:
        print(f"⛔ Error: {str(e)}")
        get_line_info()