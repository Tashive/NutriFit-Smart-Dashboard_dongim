"""
app.py의 UI/UX 완성도를 하이엔드 수준으로 끌어올리기 위한 리팩토링 스크립트입니다.
주요 변경 사항:
1. 전역 테마 독립형 프리미엄 컬러칩 (#5A83F1 계열 및 화이트 배경) 고정
2. 4열 카드 및 비교 보관함의 HTML 들여쓰기를 제거하여 HTML 코드 노출 결함 제거
3. 사이드바의 로그인/관리자 인증 기능을 최상단 GNB와 통합 인증 패널로 이관
"""

import re
import os

def run_fix():
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. render_product_grid 함수 개편 (L199 ~ L404)
    # card_html과 cols[c].markdown 내부에 들여쓰기가 있어서 HTML 코드가 그대로 노출되는 문제를 해결합니다.
    # 배경은 #FAFBFF, 테두리는 #E5EFFF, 주색 #5A83F1, 보조색 #2C3281, 텍스트 #1F2937로 통일합니다.
    
    new_render_grid = '''def render_product_grid(df_to_render, selected_row, db_data, survey):
    if df_to_render.empty:
        st.info("해당 카테고리에 추천된 맞춤 상품이 없습니다.")
        return
        
    recommendations_count = len(df_to_render)
    rows_needed = (recommendations_count + 3) // 4
    
    # 최초 진입 시 스트리밍 미완료 상태인 경우: 0.18초 간격 순차 드로잉 연출
    if not st.session_state.get('streaming_done', False):
        grid_containers = []
        for r in range(rows_needed):
            cols = st.columns(4)
            for c in range(4):
                grid_containers.append(cols[c].empty())
                
        for idx_in_rec in range(recommendations_count):
            row = df_to_render.iloc[idx_in_rec]
            
            platform = str(row.get('platform') or 'Unknown')
            name = str(row.get('product_name') or row.get('displayName') or '이름 없음')
            brand = str(row.get('brandName') or row.get('brand') or '브랜드 정보 없음')
            rating = row.get('rating', 0.0)
            reviews = int(row.get('review_count', 0))
            score = row['score']
            std_ing = str(row.get('표준성분', ''))
            bonus = row.get('wellness_bonus', 0.0)
            
            # 이미지 Fallback
            img_url = row.get('image_url') or row.get('img_url')
            if pd.isna(img_url) or not isinstance(img_url, str) or not img_url.strip():
                img_url = "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400"
                
            # 가격 포맷
            price_val = row.get('price')
            if pd.isna(price_val):
                price_val = row.get('discountPrice') or row.get('price_cur') or 0.0
            price_str = f"{int(price_val):,}원" if price_val > 0 else "가격 정보 없음"
            
            first_goal = survey['health_goals'][0] if survey.get('health_goals') else "건강관리"
            prod_form = str(row.get('productForm') or row.get('productForm') or '정제')
            if prod_form == 'nan':
                prod_form = '정제'
                
            detail_url = get_product_detail_url(row)
            
            # 선택 강조 표시
            is_selected = (row.name == selected_row.name)
            card_style = "border: 2px solid #5A83F1; background: #E5EFFF; box-shadow: 0 10px 25px rgba(90, 131, 241, 0.15);" if is_selected else ""
            rank_prefix = f"🔥 선택됨" if is_selected else f"추천"
            
            # 식약처 가이드 요약 추출
            row_foodsafety = find_foodsafety_info(std_ing, db_data)
            fn_desc = "표준 고시 기준 규격 적용 원료"
            if row_foodsafety:
                fn_desc = row_foodsafety[0]['functionality'][:45] + "..." if len(row_foodsafety[0]['functionality']) > 45 else row_foodsafety[0]['functionality']
            
            # 시장 대표 인기 제품 매핑
            _mkt = get_market_top_product(std_ing)
            if _mkt:
                market_product_html = f\'\'\'<hr style="border:0;border-top:1px solid #E5EFFF;margin:8px 0;"/>
<div style="background:#FAFBFF;border:1px solid #E5EFFF;border-radius:8px;padding:8px 10px;margin-top:4px;">
<div style="font-size:0.7rem;color:#2C3281;font-weight:700;margin-bottom:4px;">📌 시장 내 대표 인기 제품</div>
<div style="font-size:0.75rem;color:#1F2937;font-weight:600;">{_mkt["brand"]} {_mkt["name"]}</div>
<div style="font-size:0.75rem;color:#5A83F1;font-weight:700;margin-top:2px;">{_mkt["price"]}</div>
<a href="{_mkt["url"]}" target="_blank" style="font-size:0.68rem;color:#5A83F1;text-decoration:none;font-weight:700;">🔗 네이버쇼핑 바로가기 ↗</a>
</div>\'\'\'
            else:
                market_product_html = ""

            # 마크다운 렌더링 시 들여쓰기로 인한 HTML 태그 노출 방지를 위해 문자열 앞의 들여쓰기를 원천 제거합니다.
            card_html = f\'\'\'<div class="ecommerce-card" style="{card_style}">
<div>
<div style="position: relative; width: 100%; height: 160px; overflow: hidden; border-radius: 12px; margin-bottom: 12px; background: #FAFBFF; display: flex; justify-content: center; align-items: center;">
<img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.src=\\\'https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400\\\'"/>
</div>
<div style="margin-bottom: 8px; line-height: 1.8;">
<span class="card-badge badge-goal">🎯 {first_goal}</span>
<span class="card-badge badge-platform">{platform.upper()}</span>
<span class="card-badge badge-form">💊 {prod_form}</span>
</div>
<div style="font-size: 0.8rem; color: #475569; margin-bottom: 2px;">{brand}</div>
<h4 style="margin: 0 0 6px 0; color: #1F2937; font-size: 1rem; font-weight: 700; height: 42px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; line-height: 1.3;">{rank_prefix}. {name}</h4>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
<span style="font-size: 1.15rem; font-weight: 800; color: #5A83F1;">{price_str}</span>
<div>
<span class="rating-star">⭐ {rating:.1f}</span>
<span style="font-size: 0.75rem; color: #64748b;">({reviews})</span>
</div>
</div>
<div style="font-size: 0.75rem; color: #2C3281;">가산점 반영: +{bonus:.2f}점</div>
<hr style="border: 0; border-top: 1px solid #E5EFFF; margin: 10px 0;"/>
<div style="font-size: 0.75rem; color: #1F2937; height: 36px; overflow: hidden; line-height: 1.3;">
<strong>💡 기능성 요약:</strong> {fn_desc}
</div>
{market_product_html}
</div>
<a class="buy-btn" href="{detail_url}" target="_blank">
🛒 제품 상세 보기 ↗
</a>
</div>\'\'\'
            
            # 극적 연출을 위한 딜레이 (지연 없이 매끄럽게 흐르도록 0.03초 설정)
            time.sleep(0.03)
            grid_containers[idx_in_rec].markdown(card_html, unsafe_allow_html=True)
            
    else:
        # 스트리밍 완료 상태: 딜레이 없이 한 번에 렌더링
        for r in range(rows_needed):
            cols = st.columns(4)
            for c in range(4):
                idx_in_rec = r * 4 + c
                if idx_in_rec < recommendations_count:
                    row = df_to_render.iloc[idx_in_rec]
                    
                    platform = str(row.get('platform') or 'Unknown')
                    name = str(row.get('product_name') or row.get('displayName') or '이름 없음')
                    brand = str(row.get('brandName') or row.get('brand') or '브랜드 정보 없음')
                    rating = row.get('rating', 0.0)
                    reviews = int(row.get('review_count', 0))
                    score = row['score']
                    std_ing = str(row.get('표준성분', ''))
                    bonus = row.get('wellness_bonus', 0.0)
                    
                    # 이미지 Fallback
                    img_url = row.get('image_url') or row.get('img_url')
                    if pd.isna(img_url) or not isinstance(img_url, str) or not img_url.strip():
                        img_url = "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400"
                        
                    # 가격 포맷
                    price_val = row.get('price')
                    if pd.isna(price_val):
                        price_val = row.get('discountPrice') or row.get('price_cur') or 0.0
                    price_str = f"{int(price_val):,}원" if price_val > 0 else "가격 정보 없음"
                    
                    first_goal = survey['health_goals'][0] if survey.get('health_goals') else "건강관리"
                    prod_form = str(row.get('productForm') or row.get('productForm') or '정제')
                    if prod_form == 'nan':
                        prod_form = '정제'
                        
                    detail_url = get_product_detail_url(row)

                    # 시장 대표 인기 제품 매핑 (static)
                    _mkt_s = get_market_top_product(std_ing)
                    if _mkt_s:
                        market_product_html_s = f\'\'\'<hr style="border:0;border-top:1px solid #E5EFFF;margin:8px 0;"/>
<div style="background:#FAFBFF;border:1px solid #E5EFFF;border-radius:8px;padding:8px 10px;margin-top:4px;">
<div style="font-size:0.7rem;color:#2C3281;font-weight:700;margin-bottom:4px;">📌 시장 내 대표 인기 제품</div>
<div style="font-size:0.75rem;color:#1F2937;font-weight:600;">{_mkt_s["brand"]} {_mkt_s["name"]}</div>
<div style="font-size:0.75rem;color:#5A83F1;font-weight:700;margin-top:2px;">{_mkt_s["price"]}</div>
<a href="{_mkt_s["url"]}" target="_blank" style="font-size:0.68rem;color:#5A83F1;text-decoration:none;font-weight:700;">🔗 네이버쇼핑 바로가기 ↗</a>
</div>\'\'\'
                    else:
                        market_product_html_s = ""

                    # 선택 강조 표시
                    is_selected = (row.name == selected_row.name)
                    card_style = "border: 2px solid #5A83F1; background: #E5EFFF; box-shadow: 0 10px 25px rgba(90, 131, 241, 0.15);" if is_selected else ""
                    rank_prefix = f"🔥 선택됨" if is_selected else f"추천"
                    
                    # 식약처 가이드 요약 추출
                    row_foodsafety = find_foodsafety_info(std_ing, db_data)
                    fn_desc = "표준 고시 기준 규격 적용 원료"
                    if row_foodsafety:
                        fn_desc = row_foodsafety[0]['functionality'][:45] + "..." if len(row_foodsafety[0]['functionality']) > 45 else row_foodsafety[0]['functionality']
                    
                    static_card_html = f\'\'\'<div class="ecommerce-card" style="{card_style}">
<div>
<div style="position: relative; width: 100%; height: 160px; overflow: hidden; border-radius: 12px; margin-bottom: 12px; background: #FAFBFF; display: flex; justify-content: center; align-items: center;">
<img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.src=\\\'https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400\\\'"/>
</div>
<div style="margin-bottom: 8px; line-height: 1.8;">
<span class="card-badge badge-goal">🎯 {first_goal}</span>
<span class="card-badge badge-platform">{platform.upper()}</span>
<span class="card-badge badge-form">💊 {prod_form}</span>
</div>
<div style="font-size: 0.8rem; color: #475569; margin-bottom: 2px;">{brand}</div>
<h4 style="margin: 0 0 6px 0; color: #1F2937; font-size: 1rem; font-weight: 700; height: 42px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; line-height: 1.3;">{rank_prefix}. {name}</h4>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
<span style="font-size: 1.15rem; font-weight: 800; color: #5A83F1;">{price_str}</span>
<div>
<span class="rating-star">⭐ {rating:.1f}</span>
<span style="font-size: 0.75rem; color: #64748b;">({reviews})</span>
</div>
</div>
<div style="font-size: 0.75rem; color: #2C3281;">가산점 반영: +{bonus:.2f}점</div>
<hr style="border: 0; border-top: 1px solid #E5EFFF; margin: 10px 0;"/>
<div style="font-size: 0.75rem; color: #1F2937; height: 36px; overflow: hidden; line-height: 1.3;">
<strong>💡 기능성 요약:</strong> {fn_desc}
</div>
{market_product_html_s}
</div>
<a class="buy-btn" href="{detail_url}" target="_blank">
🛒 제품 상세 보기 ↗
</a>
</div>\'\'\'
                    cols[c].markdown(static_card_html, unsafe_allow_html=True)
'''

    # app.py에서 render_product_grid 함수 추출 및 교체
    start_str = "def render_product_grid"
    end_str = "def main():"
    
    start_idx = content.find(start_str)
    end_idx = content.find(end_str, start_idx)
    
    if start_idx == -1 or end_idx == -1:
        print("Error: render_product_grid 영역을 찾을 수 없습니다.")
        return
        
    content = content[:start_idx] + new_render_grid + "\n" + content[end_idx:]

    # 2. CSS 및 GNB 영역 교체 (L407 ~ L707에 해당하는 영역을 교체합니다.)
    # 전역 화이트 테마 강제, #5A83F1 프리미엄 컬러칩, GNB 아래 로그인 통합센터 마운트.
    
    new_css_gnb_center = '''    # 프리미엄 CSS 스타일 커스텀 주입
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+KR:wght@300;400;700&display=swap');

        /* ========== 전역 테마 하드 고정 (화이트 모드 및 블루 계열) ========== */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
        }
        h1, h2, h3, h4, h5, h6, p, span, label, li, div, button {
            color: #1F2937 !important;
            font-family: 'Outfit', 'Noto Sans KR', sans-serif !important;
        }
        [data-testid="stSidebar"] {
            background-color: #FAFBFF !important;
            border-right: 1px solid #E5EFFF !important;
        }
        
        /* ========== GNB 헤더 (화이트 테마 조화) ========== */
        .gnb-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #FFFFFF;
            border-bottom: 2px solid #E5EFFF;
            padding: 14px 32px;
            position: sticky;
            top: 0;
            z-index: 999;
            backdrop-filter: blur(14px);
            margin-bottom: 24px;
            border-radius: 0 0 16px 16px;
            box-shadow: 0 4px 24px rgba(90, 131, 241, 0.06);
        }
        .gnb-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 1.35rem;
            font-weight: 800;
            background: linear-gradient(135deg, #5A83F1, #2C3281);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        .gnb-nav {
            display: flex;
            gap: 6px;
            align-items: center;
        }
        .gnb-link {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.82rem;
            font-weight: 600;
            color: #475569;
            padding: 6px 14px;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.22s ease;
            border: 1px solid transparent;
            cursor: pointer;
        }
        .gnb-link:hover {
            color: #2C3281;
            background: #E5EFFF;
            border-color: #E5EFFF;
        }
        .gnb-link-highlight {
            color: #5A83F1;
            border: 1px solid rgba(90, 131, 241, 0.35);
            background: rgba(90, 131, 241, 0.07);
        }
        .gnb-link-highlight:hover {
            background: rgba(90, 131, 241, 0.15);
            border-color: #5A83F1;
            color: #2C3281;
        }

        /* ========== 기존 카드/타이틀 (화이트 및 블루칩 기반 개편) ========== */
        .main-title {
            font-family: 'Outfit', 'Noto Sans KR', sans-serif;
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #5A83F1, #2C3281);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 4px;
        }
        .sub-title {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 1rem;
            color: #475569;
            margin-bottom: 5px;
        }
        .rating-star {
            color: #fbbf24;
            font-weight: bold;
            font-size: 1.1rem;
        }
        .ecommerce-card {
            background: #FAFBFF !important;
            border: 1px solid #E5EFFF !important;
            border-radius: 20px;
            padding: 18px;
            margin-bottom: 24px;
            transition: transform 0.28s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.28s ease, border-color 0.28s ease;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 580px;
            box-shadow: 0 6px 20px rgba(90, 131, 241, 0.04);
        }
        .ecommerce-card:hover {
            transform: translateY(-9px);
            box-shadow: 0 22px 40px rgba(90, 131, 241, 0.12) !important;
            border-color: #5A83F1 !important;
        }
        .card-badge {
            font-size: 0.7rem;
            padding: 3px 7px;
            border-radius: 5px;
            font-weight: 600;
            margin-right: 4px;
            display: inline-block;
            transition: all 0.18s ease;
        }
        .card-badge:hover { opacity: 0.8; transform: scale(1.04); }
        .badge-goal { background: #E5EFFF; color: #2C3281; }
        .badge-platform { background: rgba(90, 131, 241, 0.15); color: #5A83F1; }
        .badge-form { background: #FAFBFF; color: #475569; border: 1px solid #E5EFFF; }
        .buy-btn {
            display: block;
            width: 100%;
            text-align: center;
            background: linear-gradient(135deg, #5A83F1, #2C3281);
            color: white !important;
            padding: 10px 0;
            border-radius: 10px;
            font-weight: 700;
            text-decoration: none;
            font-size: 0.88rem;
            transition: all 0.22s ease;
            margin-top: 10px;
            box-shadow: 0 4px 12px rgba(90, 131, 241, 0.2);
        }
        .buy-btn:hover {
            opacity: 0.88;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(90, 131, 241, 0.35);
        }

        /* ========== 유틸리티 사이드카드 ========== */
        .side-util-card {
            background: #FAFBFF !important;
            border: 1px solid #E5EFFF !important;
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 18px;
            box-shadow: 0 6px 20px rgba(90, 131, 241, 0.04);
            transition: box-shadow 0.25s ease, border-color 0.25s ease;
        }
        .side-util-card:hover {
            box-shadow: 0 10px 30px rgba(90, 131, 241, 0.1);
            border-color: #5A83F1;
        }
        .side-section-label {
            font-size: 0.72rem;
            font-weight: 700;
            color: #2C3281;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        /* ========== 아웃링크 트리플 버튼 덱 ========== */
        .outlink-deck {
            display: flex;
            gap: 6px;
            margin-top: 8px;
        }
        .outlink-btn {
            flex: 1;
            text-align: center;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 6px 4px;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.2s ease;
        }
        .outlink-btn-coupang {
            background: rgba(255, 93, 0, 0.07);
            color: #ff7a30;
            border: 1px solid rgba(255, 93, 0, 0.2);
        }
        .outlink-btn-coupang:hover { background: rgba(255, 93, 0, 0.15); transform: translateY(-2px); }
        .outlink-btn-naver {
            background: rgba(3, 199, 90, 0.07);
            color: #03c75a;
            border: 1px solid rgba(3, 199, 90, 0.2);
        }
        .outlink-btn-naver:hover { background: rgba(3, 199, 90, 0.15); transform: translateY(-2px); }
        .outlink-btn-iherb {
            background: rgba(91, 192, 79, 0.07);
            color: #5bc04f;
            border: 1px solid rgba(91, 192, 79, 0.2);
        }
        .outlink-btn-iherb:hover { background: rgba(91, 192, 79, 0.15); transform: translateY(-2px); }

        /* ========== 엔터프라이즈 푸터 ========== */
        .enterprise-footer {
            background: #FAFBFF !important;
            border-top: 2px solid #E5EFFF;
            border-radius: 20px 20px 0 0;
            padding: 28px 40px;
            margin-top: 40px;
            text-align: center;
        }
        .footer-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 1.1rem;
            font-weight: 800;
            background: linear-gradient(135deg, #5A83F1, #2C3281);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        .footer-text {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.78rem;
            color: #475569;
            line-height: 1.7;
        }
        .footer-divider {
            border: 0;
            border-top: 1px solid #E5EFFF;
            margin: 14px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # ===== 최상단 브랜드 GNB 헤더 네비게이션 =====
    st.markdown("""
        <div class="gnb-header">
            <div class="gnb-logo">&#x1F957; NutriFit</div>
            <div class="gnb-nav">
                <span class="gnb-link">&#x1F4CB; 소개</span>
                <span class="gnb-link gnb-link-highlight">&#x1FA7A; AI 맞춤 추천</span>
                <span class="gnb-link">&#x26A0;&#xFE0F; 내 영양제 초과 진단</span>
                <span class="gnb-link">&#x1F512; 백오피스</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ===== 최상단 GNB 연동 백오피스 & 멤버십 로그인 통합 인증 센터 =====
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False
    if 'logged_in_username' not in st.session_state:
        st.session_state.logged_in_username = ""
    if 'admin_password_val' not in st.session_state:
        st.session_state.admin_password_val = ""

    with st.expander("🔑 멤버십 로그인 & 🔒 백오피스 관리자 인증 패널", expanded=False):
        tab_login, tab_register, tab_admin = st.tabs(["🔑 로그인 데모", "📝 회원가입 데모", "🔒 시스템 관리자 인증"])
        with tab_login:
            if not st.session_state.user_logged_in:
                login_id_val = st.text_input("아이디:", key="login_id")
                login_pw_val = st.text_input("비밀번호:", type="password", key="login_pw")
                if st.button("로그인", key="login_btn"):
                    if login_id_val.strip() and login_pw_val.strip():
                        st.session_state.user_logged_in = True
                        st.session_state.logged_in_username = login_id_val.strip()
                        st.success(f"🎉 {login_id_val}님 로그인 성공!")
                        st.rerun()
                    else:
                        st.error("아이디와 비밀번호를 입력해 주세요.")
            else:
                st.markdown(f"**👤 현재 로그인 계정: `{st.session_state.logged_in_username}`님**")
                st.write("✅ 장바구니 실시간 동기화 상태 활성화")
                if st.button("로그아웃", key="logout_btn"):
                    st.session_state.user_logged_in = False
                    st.session_state.logged_in_username = ""
                    st.rerun()
        with tab_register:
            reg_id_val = st.text_input("가입할 아이디:", key="reg_id")
            reg_pw_val = st.text_input("비밀번호 설정:", type="password", key="reg_pw")
            reg_pw_confirm_val = st.text_input("비밀번호 확인:", type="password", key="reg_pw_confirm")
            if st.button("간이 회원가입", key="register_btn"):
                if reg_id_val.strip() and reg_pw_val.strip():
                    if reg_pw_val == reg_pw_confirm_val:
                        st.success("회원가입 성공! 로그인 탭에서 입력해 주세요.")
                    else:
                        st.error("비밀번호가 일치하지 않습니다.")
                else:
                    st.error("모든 정보를 올바르게 기입해 주세요.")
        with tab_admin:
            admin_password_input = st.text_input("시스템 관리자 인증 비밀번호:", type="password", value=st.session_state.admin_password_val, help="우리 팀원 전용 백오피스 인증 창입니다.", key="admin_pwd_input")
            if admin_password_input != st.session_state.admin_password_val:
                st.session_state.admin_password_val = admin_password_input
                st.rerun()
            if st.session_state.admin_password_val == "nutrifit2026!":
                st.success("🔑 관리자 인증 성공! 백오피스 메뉴가 활성화되었습니다.")
            elif st.session_state.admin_password_val:
                st.error("비밀번호가 일치하지 않습니다.")

    admin_mode = (st.session_state.admin_password_val == "nutrifit2026!")
    if admin_mode:
        st.sidebar.success("🔑 관리자 인증 성공! 백오피스가 활성화되었습니다.")
        
    menu_options = ["🥗 개인별 맞춤 큐레이션"]
    if admin_mode:
        menu_options.append("📊 뉴트리핏 데이터 인사이트 (Admin)")
        
    selected_menu = st.sidebar.radio("🧭 메뉴 바로가기", menu_options, index=0)'''

    # L407 ~ L706 부근까지의 매칭 문자열
    # main함수의 st.markdown("""\n        <style> 부터 selected_menu = st.sidebar.radio("🧭 메뉴 바로가기", menu_options, index=0) 까지 치환
    css_start_marker = '    # 프리미엄 CSS 스타일 커스텀 주입\n    st.markdown("""\n        <style>'
    # selected_menu = st.sidebar.radio("🧭 메뉴 바로가기", menu_options, index=0) 문자열을 찾음
    menu_radio_marker = '    selected_menu = st.sidebar.radio("🧭 메뉴 바로가기", menu_options, index=0)'
    
    css_start_idx = content.find(css_start_marker)
    menu_radio_idx = content.find(menu_radio_marker)
    
    if css_start_idx == -1 or menu_radio_idx == -1:
        # 혹시 공백이 다르면 유연하게
        css_start_marker = 'st.markdown("""\n        <style>'
        css_start_idx = content.find(css_start_marker)
        
    if css_start_idx != -1 and menu_radio_idx != -1:
        # 치환 영역 설정
        content = content[:css_start_idx] + new_css_gnb_center + content[menu_radio_idx + len(menu_radio_marker):]
    else:
        print("Error: CSS & GNB 영역 치환 마커를 찾지 못했습니다.")
        return

    # 3. 비교 보관함의 들여쓰기 제거
    # L1451 부근 st.markdown(f"""\n                                    <div style="background:rgba(30,41,59,0.55);...
    # 이 부분의 들여쓰기를 제거한 버전을 빌드하고, app.py 내 비교보관함 영역만 직접 수정합니다.
    
    matrix_target = 'st.markdown(f"""\\n                                    <div style="background:rgba(30,41,59,0.55);'
    # app.py 내의 비교 보관함 markdown 호출 부분을 찾습니다.
    # 안전하게 dynamic 치환을 위해 정규표현식이나 정확한 슬라이싱을 이용
    
    # st.markdown(f"""\n                                    <div style="background:rgba(30,41,59,0.55);...
    # 부분을 들여쓰기가 완전히 제거된 HTML 블록으로 교체
    
    new_matrix_markdown = '''                                st.markdown(f\'\'\'<div style="background:#FAFBFF;border:2px solid #5A83F1;border-radius:20px;padding:20px;min-height:390px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 8px 24px rgba(90,131,241,0.06);">
<div>
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
<span style="font-size:0.8rem;color:#2C3281;background:#E5EFFF;padding:2px 8px;border-radius:6px;font-weight:700;">⚖️ 비교 {idx_c+1}</span>
<span style="font-size:0.75rem;color:#475569;">{comp_platform.upper()}</span>
</div>
<div style="font-size:0.78rem;color:#475569;margin-bottom:2px;">{comp_brand}</div>
<h4 style="margin:0 0 8px 0;color:#1F2937;font-size:0.95rem;font-weight:700;height:38px;overflow:hidden;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;">{comp_name}</h4>
<div style="font-size:1.18rem;font-weight:800;color:#5A83F1;margin-bottom:6px;">{comp_price_str}</div>
<div style="font-size:0.82rem;color:#fbbf24;margin-bottom:10px;">⭐ {comp_rating:.1f} <span style="color:#64748b;">({comp_reviews:,}개 리뷰)</span></div>
<div style="font-size:0.82rem;color:#1F2937;margin-bottom:8px;line-height:1.3;">🧬 <strong>표준성분:</strong> `{comp_std_ing}`</div>
<hr style="border:0;border-top:1px solid #E5EFFF;margin:10px 0;"/>
<div style="font-size:0.78rem;color:#1F2937;height:90px;overflow-y:auto;line-height:1.4;padding-right:4px;"><strong>📜 식약처 기능성:</strong> {comp_fn_desc}</div>
{mkt_badge_html}
</div>
<a class="buy-btn" href="{primary_url}" target="_blank" style="background:linear-gradient(135deg,#5A83F1,#2C3281);margin-top:15px;">🛒 제품 상세 보기 ↗</a>
</div>\'\'\', unsafe_allow_html=True)'''

    # 치환 영역 검색
    # cols_compare[idx_c] 아래의 st.markdown(f""" ... """, unsafe_allow_html=True) 전체를 교체
    matrix_start_marker = '                                st.markdown(f"""'
    matrix_end_marker = '""", unsafe_allow_html=True)'
    
    # compare_matrix_selector 부근부터 탐색
    selector_idx = content.find("compare_matrix_selector")
    if selector_idx != -1:
        m_start = content.find(matrix_start_marker, selector_idx)
        m_end = content.find(matrix_end_marker, m_start)
        if m_start != -1 and m_end != -1:
            content = content[:m_start] + new_matrix_markdown + content[m_end + len(matrix_end_marker):]
        else:
            print("Error: 비교보관함 st.markdown 영역을 찾을 수 없습니다.")
    else:
        print("Error: compare_matrix_selector를 찾을 수 없습니다.")

    with open("app.py", "w", encoding="utf-8") as f:
        f.write(content)
        
    print("app.py 리팩토링 및 덮어쓰기 완료!")

if __name__ == "__main__":
    run_fix()
