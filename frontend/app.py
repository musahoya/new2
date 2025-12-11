"""
프롬프트 엔지니어링 자동화 - Flask 프론트엔드
"""
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# 백엔드 API URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


@app.route("/")
def index():
    """메인 페이지"""
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """분석 API 프록시"""
    try:
        data = request.get_json()
        response = requests.post(f"{API_BASE_URL}/api/analyze", json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요."
        }), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/generate-prompts", methods=["POST"])
def generate_prompts():
    """프롬프트 생성 API 프록시"""
    try:
        data = request.get_json()
        response = requests.post(f"{API_BASE_URL}/api/generate-prompts", json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/strategies")
def get_strategies():
    """전략 목록 조회 API 프록시"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/strategies")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    """헬스 체크"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        return jsonify({
            "frontend": "healthy",
            "backend": response.json()
        })
    except:
        return jsonify({
            "frontend": "healthy",
            "backend": "unhealthy"
        }), 503


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
