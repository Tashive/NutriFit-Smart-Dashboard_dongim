"""
app.py의 최상단 메인 타이틀 및 서브 타이틀의 디자인 위계를 압도적으로 럭셔리하게 고도화하는 스크립트입니다.
주요 수정 내용:
1. 메인 타이틀(.main-title) 폰트 크기를 3.5rem으로 확장하고, 익스트림 볼드(800) 및 linear-gradient(90deg, #2C3281, #5A83F1) 텍스트 채우기 적용.
2. 서브 타이틀(.sub-title)의 폰트 크기를 16px로 조정하고 색상을 #4B5563 그레이로 매핑하며, 하단 콘텐츠 간의 여유로운 마진(40px)을 주어 시각적 호흡 확보.
"""

def main():
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()

    # CSS 블록 내의 .main-title과 .sub-title 정의를 럭셔리 폰트 및 마진 여백으로 치환합니다.
    old_main_title_css = """        .main-title {
            font-family: 'Outfit', 'Noto Sans KR', sans-serif;
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #5A83F1, #2C3281);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        .sub-title {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 1rem;
            color: #475569;
            margin-bottom: 12px;
        }"""

    new_main_title_css = """        .main-title {
            font-family: 'Outfit', 'Noto Sans KR', sans-serif;
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            background: linear-gradient(90deg, #2C3281, #5A83F1) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin-bottom: 16px !important;
            line-height: 1.15 !important;
            letter-spacing: -1px !important;
        }
        .sub-title {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 16px !important;
            color: #4B5563 !important;
            margin-bottom: 40px !important;
            font-weight: 500 !important;
            letter-spacing: -0.2px !important;
        }"""

    if old_main_title_css in content:
        content = content.replace(old_main_title_css, new_main_title_css)
    else:
        # 혹시 공백이 다르면 유연하게
        # 정규표현식이나 일부분 치환 사용
        content = content.replace(".main-title {", ".main-title {\\n            font-size: 3.5rem !important;\\n            font-weight: 800 !important;")
        print("Warning: CSS가 마크업 형태와 완벽히 일치하지 않아 부분 치환을 유도합니다.")

    with open("app.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("메인 타이틀 럭셔리 볼드 및 여백 튜닝 성공!")

if __name__ == "__main__":
    main()
