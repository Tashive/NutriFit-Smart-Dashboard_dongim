"""
app.py 내부의 f-string HTML 템플릿들에서 공백 들여쓰기(Indentation)를 제거하여
Streamlit Markdown 파서가 이를 코드 블록으로 오인해 HTML 태그(</div> 등)가 생텍스트로 렌더링되던 결함을 완벽히 해결하는 스크립트입니다.
"""

import textwrap

def main():
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. render_nutrient_ring_svg 및 render_hero_nutrient_card 함수 내부 들여쓰기 제거
    # textwrap.dedent를 활용하여 반환되는 HTML에서 공백을 완전히 정돈합니다.
    
    old_ring_func = """def render_nutrient_ring_svg(label: str, percent: int, color: str) -> str:
    \"\"\"단일 영양소 섭취율을 나타내는 도넛 링 SVG를 반환.\"\"\"
    radius = 26
    circumference = 2 * 3.14159265 * radius
    offset = circumference * (1 - min(percent, 100) / 100)
    return f\"\"\"
        <div class="nutrient-ring-item">
            <svg width="64" height="64" viewBox="0 0 64 64">
                <circle cx="32" cy="32" r="{radius}" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="6"></circle>
                <circle cx="32" cy="32" r="{radius}" fill="none" stroke="{color}" stroke-width="6"
                    stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{offset:.1f}"
                    stroke-linecap="round" transform="rotate(-90 32 32)"></circle>
                <text x="32" y="37" text-anchor="middle" class="nutrient-ring-value">{percent}%</text>
            </svg>
            <div class="nutrient-ring-label">{label}</div>
        </div>
    \"\"\""""

    new_ring_func = """def render_nutrient_ring_svg(label: str, percent: int, color: str) -> str:
    \"\"\"단일 영양소 섭취율을 나타내는 도넛 링 SVG를 반환.\"\"\"
    radius = 26
    circumference = 2 * 3.14159265 * radius
    offset = circumference * (1 - min(percent, 100) / 100)
    import textwrap
    html_str = f\"\"\"
<div class="nutrient-ring-item">
    <svg width="64" height="64" viewBox="0 0 64 64">
        <circle cx="32" cy="32" r="{radius}" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="6"></circle>
        <circle cx="32" cy="32" r="{radius}" fill="none" stroke="{color}" stroke-width="6"
            stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{offset:.1f}"
            stroke-linecap="round" transform="rotate(-90 32 32)"></circle>
        <text x="32" y="37" text-anchor="middle" class="nutrient-ring-value">{percent}%</text>
    </svg>
    <div class="nutrient-ring-label">{label}</div>
</div>
\"\"\"
    return textwrap.dedent(html_str).strip()"""

    old_hero_card_func = """def render_hero_nutrient_card() -> str:
    \"\"\"히어로 섹션 우측에 배치할 영양소 섭취율 미리보기 글래스 카드.\"\"\"
    sample_nutrients = [
        ("비타민D", 62, "#8FC3A2"),
        ("마그네슘", 78, "#FFD166"),
        ("오메가3", 45, "#F4A261"),
        ("아연", 90, "#E9F5EC"),
    ]
    rings_html = "".join(
        render_nutrient_ring_svg(label, pct, color) for label, pct, color in sample_nutrients
    )
    return f\"\"\"
        <div class="hero-glass-card">
            <div class="glass-title">🌿 내 영양소 섭취율 미리보기</div>
            <div class="nutrient-ring-row">
                {rings_html}
            </div>
        </div>
    \"\"\""""

    new_hero_card_func = """def render_hero_nutrient_card() -> str:
    \"\"\"히어로 섹션 우측에 배치할 영양소 섭취율 미리보기 글래스 카드.\"\"\"
    sample_nutrients = [
        ("비타민D", 62, "#8FC3A2"),
        ("마그네슘", 78, "#FFD166"),
        ("오메가3", 45, "#F4A261"),
        ("아연", 90, "#E9F5EC"),
    ]
    rings_html = "".join(
        render_nutrient_ring_svg(label, pct, color) for label, pct, color in sample_nutrients
    )
    import textwrap
    html_str = f\"\"\"
<div class="hero-glass-card">
    <div class="glass-title">🌿 내 영양소 섭취율 미리보기</div>
    <div class="nutrient-ring-row">
        {rings_html}
    </div>
</div>
\"\"\"
    return textwrap.dedent(html_str).strip()"""

    # 2. 메인 히어로 배너 st.markdown 들여쓰기 제거
    old_hero_markdown = """    st.markdown(f\"\"\"
        <div class="hero-panel">
            <div class="hero-flex">
                <div class="hero-flex-text">
                    <span class="hero-badge">🌿 Beta 오픈 중</span>
                    <div class="main-title">나에게 꼭 맞는<br>영양 <span class="accent-italic">밸런스</span>를 찾아드립니다</div>
                    <div class="sub-title">식약처 공인 데이터베이스 및 초개인화 가중 스코어링 기반 웰니스 큐레이션</div>
                </div>
                <div class="hero-flex-visual">
                    {render_hero_nutrient_card()}
                </div>
            </div>
        </div>
    \"\"\", unsafe_allow_html=True)"""

    new_hero_markdown = """    import textwrap
    hero_html = f\"\"\"
<div class="hero-panel">
    <div class="hero-flex">
        <div class="hero-flex-text">
            <span class="hero-badge">🌿 Beta 오픈 중</span>
            <div class="main-title">나에게 꼭 맞는<br>영양 <span class="accent-italic">밸런스</span>를 찾아드립니다</div>
            <div class="sub-title">식약처 공인 데이터베이스 및 초개인화 가중 스코어링 기반 웰니스 큐레이션</div>
        </div>
        <div class="hero-flex-visual">
            {render_hero_nutrient_card()}
        </div>
    </div>
</div>
\"\"\"
    st.markdown(textwrap.dedent(hero_html).strip(), unsafe_allow_html=True)"""

    # 치환 작업 실행
    modified = False
    
    if old_ring_func in content:
        content = content.replace(old_ring_func, new_ring_func)
        modified = True
        print("render_nutrient_ring_svg 치환 성공")
    else:
        print("render_nutrient_ring_svg 치환 실패 (포맷 다름)")
        
    if old_hero_card_func in content:
        content = content.replace(old_hero_card_func, new_hero_card_func)
        modified = True
        print("render_hero_nutrient_card 치환 성공")
    else:
        print("render_hero_nutrient_card 치환 실패 (포맷 다름)")
        
    if old_hero_markdown in content:
        content = content.replace(old_hero_markdown, new_hero_markdown)
        modified = True
        print("st.markdown(hero_html) 치환 성공")
    else:
        print("st.markdown(hero_html) 치환 실패 (포맷 다름)")

    if modified:
        with open("app.py", "w", encoding="utf-8") as f:
            f.write(content)
        print("app.py의 공백 들여쓰기 렌더링 이슈 수정 및 저장 완료!")
    else:
        print("수정 사항이 감지되지 않았습니다.")

if __name__ == "__main__":
    main()
