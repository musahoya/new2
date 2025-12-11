#!/usr/bin/env python3
"""
API 테스트 스크립트
백엔드 서버를 테스트합니다.
"""
import requests
import json
import sys


def print_header(text):
    """헤더 출력"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def test_health_check():
    """헬스 체크 테스트"""
    print_header("1. 헬스 체크")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"✅ 상태: {response.status_code}")
        print(f"응답: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ 서버 연결 실패!")
        print("백엔드 서버가 실행 중인지 확인하세요.")
        print("실행 방법: ./run_backend.sh")
        return False
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False


def test_strategies():
    """전략 목록 조회 테스트"""
    print_header("2. 프롬프팅 전략 목록 조회")
    try:
        response = requests.get("http://localhost:8000/api/strategies")
        print(f"✅ 상태: {response.status_code}")
        data = response.json()
        print(f"\n사용 가능한 전략: {len(data['strategies'])}개\n")
        for strategy in data["strategies"]:
            print(f"  {strategy['icon']} {strategy['name']}")
            print(f"     - {strategy['description']}")
            print(f"     - 최적: {strategy['best_for']}\n")
        return True
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False


def test_analyze():
    """분석 API 테스트"""
    print_header("3. 쿼리 분석 테스트")

    test_query = "제주도 3박4일 여행 계획 추천해줘"
    print(f"테스트 쿼리: '{test_query}'")

    try:
        response = requests.post(
            "http://localhost:8000/api/analyze", json={"query": test_query}
        )
        print(f"\n✅ 상태: {response.status_code}")
        data = response.json()

        print("\n📊 분석 결과:")
        print(f"  - 목적: {data['intent']['primary_intent']}")
        print(f"  - 형식: {data['intent']['output_type']}")
        print(f"  - 대상: {data['intent']['target_audience']}")
        print(f"  - 분야: {data['intent']['domain']}")
        print(f"  - 신뢰도: {data['intent']['confidence']:.1%}")

        print("\n🔥 수집된 트렌드 (상위 5개):")
        for i, trend in enumerate(data["trends"]["trends"][:5], 1):
            print(f"  {i}. {trend}")

        return data

    except Exception as e:
        print(f"❌ 오류: {e}")
        return None


def test_generate_prompts(analysis_data):
    """프롬프트 생성 테스트"""
    print_header("4. 프롬프트 생성 테스트")

    if not analysis_data:
        print("❌ 분석 데이터가 없습니다.")
        return False

    try:
        response = requests.post(
            "http://localhost:8000/api/generate-prompts", json=analysis_data
        )
        print(f"✅ 상태: {response.status_code}")
        data = response.json()

        print(f"\n✨ 생성된 프롬프트: {len(data['prompts']['prompts'])}개\n")

        for prompt in data["prompts"]["prompts"]:
            print(f"{prompt['icon']} {prompt['name']}")
            print(f"  설명: {prompt['description']}")
            print(f"  최적: {prompt['best_for']}")
            print(f"  길이: {len(prompt['prompt'])} 글자\n")

        # 첫 번째 프롬프트 미리보기
        print("=" * 60)
        print("📄 프롬프트 미리보기 (CoT 전략):")
        print("=" * 60)
        print(data["prompts"]["prompts"][0]["prompt"][:500] + "...")

        return True

    except Exception as e:
        print(f"❌ 오류: {e}")
        return False


def test_full_pipeline():
    """전체 파이프라인 테스트"""
    print_header("5. 전체 파이프라인 테스트")

    test_query = "2025년 AI 트렌드 분석 보고서 작성"
    print(f"테스트 쿼리: '{test_query}'")

    try:
        response = requests.post(
            "http://localhost:8000/api/pipeline", json={"query": test_query}
        )
        print(f"\n✅ 상태: {response.status_code}")
        data = response.json()

        print(f"✅ 파이프라인 완료: {data['status']}")
        print(f"  - 분석 완료")
        print(f"  - 프롬프트 {len(data['prompts']['prompts']['prompts'])}개 생성")

        return True

    except Exception as e:
        print(f"❌ 오류: {e}")
        return False


def main():
    """메인 함수"""
    print("\n" + "🚀 프롬프트 엔지니어링 자동화 API 테스트".center(60))
    print()

    # 1. 헬스 체크
    if not test_health_check():
        sys.exit(1)

    # 2. 전략 목록
    test_strategies()

    # 3. 분석
    analysis_result = test_analyze()

    # 4. 프롬프트 생성
    if analysis_result:
        test_generate_prompts(analysis_result)

    # 5. 전체 파이프라인
    test_full_pipeline()

    print_header("✅ 모든 테스트 완료!")
    print("\n이제 프론트엔드를 실행하세요:")
    print("  ./run_frontend.sh")
    print("\n또는 브라우저에서 직접 API를 테스트하세요:")
    print("  http://localhost:8000/docs")
    print()


if __name__ == "__main__":
    main()
