from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'FastAPI+HuggingFace app sentiment + summarize YouTube comments'}

#def test_get_comments():
#    response = client.post("/comments", json={"url_video" : "https://www.youtube.com/watch?v=ITEfXK2J3Gw"})
#    assert response.status_code == 200
