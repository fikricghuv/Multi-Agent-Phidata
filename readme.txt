uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload


lsof -i :8765
kill -9 <pid>