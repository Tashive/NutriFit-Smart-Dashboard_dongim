"""
app.py의 비교 보관함 영역 들여쓰기 및 col_main/col_side 우측 칼럼 신설,
엔터프라이즈 푸터를 줄 번호 기반으로 직접 교체하는 리팩토링 스크립트.
"""

with open('app.py', encoding='utf-8') as f:
    lines = f.readlines()

print(f"총 {len(lines)}줄")
# 디버그: 1400~1420행 출력
for i in range(1399, 1420):
    print(i+1, repr(lines[i][:80]))
