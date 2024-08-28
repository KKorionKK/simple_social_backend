import uvicorn


if __name__ == '__main__':
    uvicorn.run('api.app:app', host='127.0.0.1', port=4444, reload=True, access_log=True)