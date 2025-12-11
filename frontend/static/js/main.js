// 전역 변수
let currentStep = 1;
let analysisResult = null;
let promptsResult = null;
let selectedPrompt = null;

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    console.log('프롬프트 엔지니어링 자동화 시작');
});

// 단계 이동
function goToStep(step) {
    // 현재 단계 비활성화
    document.querySelector(`#step-${currentStep}`).classList.remove('active');
    document.querySelector(`#step-indicator-${currentStep}`).classList.remove('active');

    // 새 단계 활성화
    currentStep = step;
    document.querySelector(`#step-${currentStep}`).classList.add('active');
    document.querySelector(`#step-indicator-${currentStep}`).classList.add('active');

    // 이전 단계들 completed 표시
    for (let i = 1; i < currentStep; i++) {
        document.querySelector(`#step-indicator-${i}`).classList.add('completed');
    }

    // 페이지 최상단으로 스크롤
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 로딩 표시
function showLoading(message = '처리 중...') {
    const overlay = document.getElementById('loading-overlay');
    const loadingMessage = document.getElementById('loading-message');
    loadingMessage.textContent = message;
    overlay.classList.add('active');
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    overlay.classList.remove('active');
}

// 에러 표시
function showError(message) {
    alert('❌ ' + message);
}

// 1단계: 쿼리 분석
async function analyzeQuery() {
    const query = document.getElementById('user-query').value.trim();

    if (!query) {
        showError('내용을 입력해주세요!');
        return;
    }

    showLoading('🔍 AI가 분석하고 최신 트렌드를 수집하고 있습니다...');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || '분석 실패');
        }

        analysisResult = await response.json();
        displayAnalysisResult(analysisResult);
        goToStep(2);

    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// 분석 결과 표시
function displayAnalysisResult(result) {
    const intent = result.intent;
    const trends = result.trends;

    // 의도 분석 표시
    const intentHtml = `
        <p><strong>입력:</strong> ${result.query}</p>
        <p><strong>목적:</strong> ${intent.primary_intent}</p>
        <p><strong>형식:</strong> ${intent.output_type}</p>
        <p><strong>대상:</strong> ${intent.target_audience}</p>
        <p><strong>분야:</strong> ${intent.domain}</p>
        <p><strong>신뢰도:</strong> ${(intent.confidence * 100).toFixed(0)}%</p>
    `;
    document.getElementById('intent-result').innerHTML = intentHtml;

    // 트렌드 표시
    const trendsHtml = trends.trends.map((trend, index) =>
        `<div class="trend-item">${index + 1}. ${trend}</div>`
    ).join('');
    document.getElementById('trends-result').innerHTML = trendsHtml;

    // 요약 표시
    document.getElementById('trends-summary').textContent = trends.summary;
}

// 2단계: 프롬프트 생성
async function generatePrompts() {
    if (!analysisResult) {
        showError('분석 결과가 없습니다.');
        return;
    }

    showLoading('🎨 5가지 프롬프팅 전략을 생성하고 있습니다...');

    try {
        const response = await fetch('/api/generate-prompts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(analysisResult)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || '프롬프트 생성 실패');
        }

        promptsResult = await response.json();
        displayPrompts(promptsResult.prompts.prompts);
        goToStep(3);

    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// 프롬프트 표시
function displayPrompts(prompts) {
    const container = document.getElementById('prompts-container');

    const promptsHtml = prompts.map(prompt => `
        <div class="prompt-card">
            <div class="prompt-card-header">
                <div>
                    <div class="prompt-card-title">${prompt.icon} ${prompt.name}</div>
                    <div class="prompt-card-description">${prompt.description}</div>
                    <div class="prompt-card-best-for">💡 최적: ${prompt.best_for}</div>
                </div>
            </div>

            <details>
                <summary style="cursor: pointer; padding: 0.5rem; background: #f3f4f6; border-radius: 6px; margin: 1rem 0;">
                    📋 프롬프트 미리보기 (클릭)
                </summary>
                <div class="prompt-preview">${escapeHtml(prompt.prompt)}</div>
            </details>

            <button class="btn btn-primary" onclick='selectPrompt(${JSON.stringify(prompt).replace(/'/g, "&#39;")})'>
                ✅ 이 전략 선택
            </button>
        </div>
    `).join('');

    container.innerHTML = promptsHtml;
}

// HTML 이스케이프
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 프롬프트 선택
function selectPrompt(prompt) {
    selectedPrompt = prompt;
    displayFinalPrompt(prompt);
    goToStep(4);
}

// 최종 프롬프트 표시
function displayFinalPrompt(prompt) {
    document.getElementById('selected-strategy-name').innerHTML =
        `✅ <strong>${prompt.name}</strong> 전략을 선택하셨습니다!`;

    document.getElementById('final-prompt').textContent = prompt.prompt;
}

// 프롬프트 복사
function copyPrompt() {
    const promptText = document.getElementById('final-prompt').textContent;

    // 클립보드에 복사
    navigator.clipboard.writeText(promptText).then(() => {
        // 성공 메시지
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '✅ 복사됨!';
        btn.style.background = '#10b981';

        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.background = '';
        }, 2000);
    }).catch(err => {
        showError('복사에 실패했습니다.');
    });
}

// 재시작
function restart() {
    // 변수 초기화
    analysisResult = null;
    promptsResult = null;
    selectedPrompt = null;

    // 입력 필드 초기화
    document.getElementById('user-query').value = '';

    // 1단계로 이동
    goToStep(1);

    // 모든 단계 인디케이터 초기화
    for (let i = 1; i <= 4; i++) {
        document.querySelector(`#step-indicator-${i}`).classList.remove('completed');
    }
}
