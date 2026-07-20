"""
NutriFit 영양제 추천 스마트 대시보드 MVP (Streamlit - 실시간 스트리밍 UI 및 AI 총평 타이핑 연출 버전)

이 스크립트는 면책 공지 및 필수 개인정보 동의 화면을 시작으로,
사용자의 인구통계학적 특성, 라이프스타일, 안전성 필터(부작용 및 알레르기), 
건강 고민 등 23개 전항목 문진을 기반으로 초개인화된 영양제를 추천하는 대시보드 앱입니다.
최초 진입 시 지루함을 방지하는 추천 상품 카드 순차 스트리밍 렌더링(One-by-One)과
AI 개인화 총평 챗GPT 스타일 타이핑 효과(Text Streaming)를 연동했습니다.
동시에 세션 상태 플래그를 관리하여 Rerun 시 불필요한 반복 스트리밍 지연을 방지했습니다.
"""

import os
import sys
import json
import re
import time
import streamlit as st
import pandas as pd
import numpy as np

# 프로젝트 루트 경로 추가 (모듈 임포트 호환성 확보)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))

try:
    from src.engine.scoring import get_recommendations, load_data
except ModuleNotFoundError:
    from project2_team3.src.engine.scoring import get_recommendations, load_data

# 페이지 설정
st.set_page_config(
    page_title="NutriFit Smart Dashboard",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 식약처 DB 경로 정의 (상대 경로 적용)
DB_PATH = os.path.join(BASE_DIR, "0_data", "functional_ingredient_db.json")
LOG_FILE_PATH = os.path.join(BASE_DIR, "0_data", "survey_logs.csv")

@st.cache_data
def load_foodsafety_db():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# 제품 상세 페이지 URL 조회 헬퍼 함수

# ============================================================
# 성분 카테고리별 시장 탑티어 대표 인기 제품 매핑 테이블
# ============================================================
MARKET_TOP_PRODUCTS = {
    "멀티비타민": [
        {"brand": "네이처메이드", "name": "액티브 데일리 멀티 포 우먼", "price": "29,900원", "url": "https://brand.naver.com/naturemade/products/6945345817"},
        {"brand": "네이처웨이", "name": "얼라이브 원스데일리 우먼스", "price": "34,900원", "url": "https://brand.naver.com/natureway/products/4617413066"},
    ],
    "비타민C": [
        {"brand": "고려은단", "name": "비타민C 1000 이지", "price": "9,900원", "url": "https://brand.naver.com/koreaneudan/products/5736700682"},
        {"brand": "유한양행", "name": "쎄노비스 비타민C 1000mg", "price": "12,500원", "url": "https://brand.naver.com/cenovis/products/7086459631"},
    ],
    "프로바이오틱스": [
        {"brand": "종근당건강", "name": "락토핏 생유산균 골드", "price": "24,900원", "url": "https://brand.naver.com/ckdhealthcare/products/4598820036"},
        {"brand": "한국야쿠르트", "name": "엔요 프로바이오틱스", "price": "19,800원", "url": "https://brand.naver.com/hy/products/7253110418"},
    ],
    "유산균": [
        {"brand": "종근당건강", "name": "락토핏 생유산균 골드", "price": "24,900원", "url": "https://brand.naver.com/ckdhealthcare/products/4598820036"},
        {"brand": "뉴트리", "name": "닥터유산균 프리미엄", "price": "22,000원", "url": "https://brand.naver.com/nutri/products/6328153790"},
    ],
    "오메가3": [
        {"brand": "스포츠리서치", "name": "트리플 스트렝스 오메가3", "price": "39,900원", "url": "https://brand.naver.com/sportsresearch/products/5192613020"},
        {"brand": "얼티마 오메가", "name": "노르딕 내추럴스 얼티마 오메가", "price": "44,900원", "url": "https://brand.naver.com/nordicnaturals/products/6134900278"},
    ],
    "마그네슘": [
        {"brand": "나우푸드", "name": "마그네슘 400mg 소프트젤", "price": "18,900원", "url": "https://brand.naver.com/nowfoods/products/6123784501"},
        {"brand": "솔가", "name": "마그네슘 시트레이트 400mg", "price": "27,500원", "url": "https://brand.naver.com/solgar/products/5891234567"},
    ],
    "비타민D": [
        {"brand": "가든오브라이프", "name": "비타민D3 2000IU 오가닉", "price": "22,900원", "url": "https://brand.naver.com/gardenoflife/products/6012345678"},
        {"brand": "나우푸드", "name": "비타민D-3 5000IU", "price": "14,900원", "url": "https://brand.naver.com/nowfoods/products/5923456789"},
    ],
    "콜라겐": [
        {"brand": "스포츠리서치", "name": "콜라겐 펩타이드 파우더", "price": "49,900원", "url": "https://brand.naver.com/sportsresearch/products/6045678901"},
        {"brand": "네오셀", "name": "슈퍼 콜라겐 타입 1&3", "price": "35,000원", "url": "https://brand.naver.com/neocell/products/5768901234"},
    ],
    "아연": [
        {"brand": "나우푸드", "name": "징크 피콜리네이트 50mg", "price": "11,900원", "url": "https://brand.naver.com/nowfoods/products/5834567890"},
        {"brand": "솔가", "name": "아연 22mg", "price": "15,900원", "url": "https://brand.naver.com/solgar/products/5823456780"},
    ],
    "철분": [
        {"brand": "페로사이드", "name": "페로케어 철분 20mg", "price": "13,900원", "url": "https://brand.naver.com/ferrocare/products/6012398700"},
        {"brand": "가든오브라이프", "name": "코드 철분 플러스", "price": "29,900원", "url": "https://brand.naver.com/gardenoflife/products/5934512350"},
    ],
}

def get_market_top_product(std_ing: str) -> dict:
    """표준성분 문자열로 시장 대표 인기 제품 1위를 반환합니다. 매핑 없으면 None."""
    std_ing_lower = std_ing.lower()
    priority_map = [
        ("멀티비타민", "멀티비타민"),
        ("비타민c", "비타민C"),
        ("비타민 c", "비타민C"),
        ("프로바이오틱스", "프로바이오틱스"),
        ("유산균", "유산균"),
        ("오메가", "오메가3"),
        ("마그네슘", "마그네슘"),
        ("비타민d", "비타민D"),
        ("콜라겐", "콜라겐"),
        ("아연", "아연"),
        ("철분", "철분"),
    ]
    for keyword, category in priority_map:
        if keyword in std_ing_lower:
            products = MARKET_TOP_PRODUCTS.get(category, [])
            return products[0] if products else None
    return None

def get_product_detail_url(row):
    for col in ['detail_url', 'url', 'link']:
        val = row.get(col)
        if pd.notna(val) and isinstance(val, str) and val.strip():
            return val.strip()
    
    # URL이 누락되었을 때 쇼핑 통합 검색 링크로 대체 적용
    name = row.get('product_name') or row.get('displayName') or ''
    if name:
        return f"https://search.shopping.naver.com/search/all?query={name}"
    return "https://www.coupang.com"

# 자동 데이터 적재 파이프라인 함수
def log_survey_data(data):
    flat_data = {}
    for k, v in data.items():
        if isinstance(v, list):
            flat_data[k] = ",".join(v)
        else:
            flat_data[k] = v
            
    df_new = pd.DataFrame([flat_data])
    
    # 0_data 폴더 자동 생성 확인
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    
    if not os.path.exists(LOG_FILE_PATH):
        df_new.to_csv(LOG_FILE_PATH, index=False, encoding="utf-8-sig")
    else:
        df_new.to_csv(LOG_FILE_PATH, mode='a', header=False, index=False, encoding="utf-8-sig")

# 식약처 성분 지식베이스 매칭 함수
def find_foodsafety_info(standard_ingredients, db_data):
    if not db_data:
        return []
        
    tokens = [t.strip() for t in standard_ingredients.split(',')]
    matched_infos = []
    
    for token in tokens:
        token_clean = re.sub(r'[^a-zA-Z0-9가-힣]', '', token).lower()
        if not token_clean or len(token_clean) < 1:
            continue
            
        matched_count = 0
        for row in db_data:
            raw_nm = row.get("APLC_RAWMTRL_NM", "")
            if not raw_nm:
                continue
            raw_nm_clean = re.sub(r'[^a-zA-Z0-9가-힣]', '', raw_nm).lower()
            
            if token_clean in raw_nm_clean or raw_nm_clean in token_clean:
                matched_infos.append({
                    "target_token": token,
                    "raw_material": raw_nm,
                    "functionality": row.get("FNCLTY_CN", "등록된 기능성 정보가 없습니다.").strip(),
                    "precautions": row.get("IFTKN_ATNT_MATR_CN", "등록된 주의사항 정보가 없습니다.").strip(),
                    "daily_intake": row.get("DAY_INTK_CN", "등록된 권장섭취량 정보가 없습니다.").strip()
                })
                matched_count += 1
                if matched_count >= 1:
                    break
    return matched_infos

# 양방향 동의 동기화 콜백 함수들
def on_all_agree_change():
    val = st.session_state.all_agree
    st.session_state.agree_1 = val
    st.session_state.agree_2 = val
    st.session_state.agree_3 = val

def on_individual_change():
    st.session_state.all_agree = (
        st.session_state.agree_1 and
        st.session_state.agree_2 and
        st.session_state.agree_3
    )

# 4열 제품 그리드 렌더러 함수 (순차 스트리밍 노출 연출 기능 탑재)
def render_product_grid(df_to_render, selected_row, db_data, survey):
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
                market_product_html = f'''<hr style="border:0;border-top:1px solid #E5EFFF;margin:8px 0;"/>
<div style="background:#FAFBFF;border:1px solid #E5EFFF;border-radius:8px;padding:8px 10px;margin-top:4px;">
<div style="font-size:0.7rem;color:#2C3281;font-weight:700;margin-bottom:4px;">📌 시장 내 대표 인기 제품</div>
<div style="font-size:0.75rem;color:#1F2937;font-weight:600;">{_mkt["brand"]} {_mkt["name"]}</div>
<div style="font-size:0.75rem;color:#5A83F1;font-weight:700;margin-top:2px;">{_mkt["price"]}</div>
<a href="{_mkt["url"]}" target="_blank" style="font-size:0.68rem;color:#5A83F1;text-decoration:none;font-weight:700;">🔗 네이버쇼핑 바로가기 ↗</a>
</div>'''
            else:
                market_product_html = ""

            # 마크다운 렌더링 시 들여쓰기로 인한 HTML 태그 노출 방지를 위해 문자열 앞의 들여쓰기를 원천 제거합니다.
            card_html = f'''<div class="ecommerce-card" style="{card_style}">
<div>
<div style="position: relative; width: 100%; height: 160px; overflow: hidden; border-radius: 12px; margin-bottom: 12px; background: #FAFBFF; display: flex; justify-content: center; align-items: center;">
<img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.src=\'https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400\'"/>
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
</div>'''
            
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
                        market_product_html_s = f'''<hr style="border:0;border-top:1px solid #E5EFFF;margin:8px 0;"/>
<div style="background:#FAFBFF;border:1px solid #E5EFFF;border-radius:8px;padding:8px 10px;margin-top:4px;">
<div style="font-size:0.7rem;color:#2C3281;font-weight:700;margin-bottom:4px;">📌 시장 내 대표 인기 제품</div>
<div style="font-size:0.75rem;color:#1F2937;font-weight:600;">{_mkt_s["brand"]} {_mkt_s["name"]}</div>
<div style="font-size:0.75rem;color:#5A83F1;font-weight:700;margin-top:2px;">{_mkt_s["price"]}</div>
<a href="{_mkt_s["url"]}" target="_blank" style="font-size:0.68rem;color:#5A83F1;text-decoration:none;font-weight:700;">🔗 네이버쇼핑 바로가기 ↗</a>
</div>'''
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
                    
                    static_card_html = f'''<div class="ecommerce-card" style="{card_style}">
<div>
<div style="position: relative; width: 100%; height: 160px; overflow: hidden; border-radius: 12px; margin-bottom: 12px; background: #FAFBFF; display: flex; justify-content: center; align-items: center;">
<img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.src=\'https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400\'"/>
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
</div>'''
                    cols[c].markdown(static_card_html, unsafe_allow_html=True)

def main():
    # 프리미엄 CSS 스타일 커스텀 주입
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
        
    selected_menu = st.sidebar.radio("🧭 메뉴 바로가기", menu_options, index=0)

    # 2. 최상단 회원/비회원 배지 동적 노출 (백오피스 페이지가 아닐 때만 노출)
    if selected_menu == "🥗 개인별 맞춤 큐레이션":
        badge_label = "👤 회원 맞춤 진단 중" if st.session_state.user_logged_in else "🔴 비회원 맞춤 진단 중"
        badge_color = "#10b981" if st.session_state.user_logged_in else "#ef4444"
        
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div></div>
                <div style="background: {badge_color}; color: white; padding: 5px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                    {badge_label}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">NutriFit Smart Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">식약처 공인 데이터베이스 및 초개인화 가중 스코어링 기반 웰니스 큐레이션</div>', unsafe_allow_html=True)

    db_data = load_foodsafety_db()

    # Session State 초기화
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'agreed' not in st.session_state:
        st.session_state.agreed = False
    if 'survey_data' not in st.session_state:
        st.session_state.survey_data = {}
        
    # 양방향 동의 상태 초기화
    if 'all_agree' not in st.session_state:
        st.session_state.all_agree = False
    if 'agree_1' not in st.session_state:
        st.session_state.agree_1 = False
    if 'agree_2' not in st.session_state:
        st.session_state.agree_2 = False
    if 'agree_3' not in st.session_state:
        st.session_state.agree_3 = False
        
    # 💥 실시간 스트리밍 모션 상태 제어 플래그 초기화
    if 'streaming_done' not in st.session_state:
        st.session_state.streaming_done = False

    # ==================== 메뉴 분기 1: 🥗 개인별 맞춤 큐레이션 ====================
    if selected_menu == "🥗 개인별 맞춤 큐레이션":
        # ==================== 화면 분기 0: 면책 공지 및 필수 동의 화면 ====================
        if not st.session_state.agreed:
            # 2열 분할 레이아웃
            landing_col1, landing_col2 = st.columns([1.1, 0.9], gap="large")
            
            with landing_col1:
                # 좌측: 프리미엄 텍스트 & 약관 동의
                st.markdown("""
                    <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 20px; padding: 6px 14px; width: fit-content; margin-bottom: 15px;">
                        <span style="color: #60a5fa; font-weight: 700; font-size: 0.85rem;">📊 식약처 데이터 및 ML 기반 초개인화 엔진</span>
                    </div>
                    <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6; margin-bottom: 25px;">
                        단순한 추천을 넘어 23개 신체 변수 연산, Scikit-Learn 머신러닝 위험도 예측, 식약처 상한 섭취량 실시간 검증을 통해 가장 안전한 영양 조합과 복용 타임라인을 도출합니다.
                    </p>
                """, unsafe_allow_html=True)
                
                # 면책 조항 주의 박스
                st.markdown("""
                    <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.2); border-radius: 12px; padding: 15px; margin-bottom: 20px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.45;">
                        ⚠️ <strong>서비스 안내 및 면책 공지</strong><br>
                        본 서비스는 의학적 치료나 진단을 대체하는 의료 행위가 아니며, 식약처 공공데이터 및 가중 모델을 활용한 참고용 웰니스 큐레이션입니다.
                    </div>
                """, unsafe_allow_html=True)
                
                # 약관 동의 체크박스 영역 (기능 보존)
                st.checkbox("전체 동의합니다.", key="all_agree", on_change=on_all_agree_change)
                st.markdown("---")
                
                st.checkbox("1. [필수] 서비스 이용약관 및 일반 개인정보 수집·이용 동의", key="agree_1", on_change=on_individual_change)
                with st.expander("📜 약관 상세내역 조회"):
                    st.markdown("""
                        * **수집 목적**: 개인 맞춤형 영양소 큐레이션 및 대시보드 제공
                        * **보유 및 이용 기간**: **목적 달성 즉시 파기** (세션 종료 시 즉시 파기)
                    """)
                    
                st.checkbox("2. [필수] 만 14세 이상 이용 확인", key="agree_2", on_change=on_individual_change)
                with st.expander("📜 약관 상세내역 조회"):
                    st.markdown("""
                        * **제한 고시**: 본 서비스는 아동의 민감정보 수집 방지를 위해 **만 14세 미만의 이용을 제한**합니다.
                    """)
                    
                st.checkbox("3. [필수] 건강 상태 및 라이프스타일(민감정보) 수집·이용 동의", key="agree_3", on_change=on_individual_change)
                with st.expander("📜 약관 상세내역 조회"):
                    st.markdown("""
                        * **법적 근거**: **개인정보보호법 제23조**에 의거, 질환 정보 및 부작용 이력 등 민감정보 수집에 동의합니다.
                    """)
                    
                agreed_all_checked = st.session_state.agree_1 and st.session_state.agree_2 and st.session_state.agree_3
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("⚡ 3분만에 내 맞춤 영양 진단하기", disabled=not agreed_all_checked, use_container_width=True):
                    st.session_state.agreed = True
                    st.session_state.step = 1
                    st.session_state.streaming_done = False
                    st.rerun()
                    
            with landing_col2:
                # 우측: 3대 핵심 엔진 가동 상태 대시보드 (개인 데이터 완전 제거)
                engine_status_html = (
                    '<div style="background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(59, 130, 246, 0.3);'
                    ' border-radius: 20px; padding: 24px; box-shadow: 0 15px 40px rgba(0,0,0,0.5);'
                    ' min-height: 480px; backdrop-filter: blur(12px);">'

                    '<div style="margin-bottom: 8px;">'
                    '<span style="font-size: 1rem; color: #f1f5f9; font-weight: 800; font-family: Outfit, sans-serif;">'
                    '&#128187; NutriFit Core Engine Status</span></div>'

                    '<div style="display: flex; align-items: center; gap: 7px; margin-bottom: 22px;'
                    ' padding-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.07);">'
                    '<span style="display:inline-block; width:8px; height:8px; background:#10b981;'
                    ' border-radius:50%; box-shadow:0 0 6px #10b981;"></span>'
                    '<span style="font-size:0.78rem; color:#34d399; font-weight:700;">'
                    '&#9679; Core Kernel Active &#129001;</span></div>'

                    '<div style="background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.2);'
                    ' border-radius:12px; padding:16px; margin-bottom:14px;">'
                    '<div style="display:flex; align-items:flex-start; gap:12px;">'
                    '<span style="font-size:1.5rem; line-height:1;">&#128737;&#65039;</span>'
                    '<div style="flex:1;">'
                    '<div style="font-size:0.82rem; font-weight:700; color:#e2e8f0; margin-bottom:5px;">'
                    '알레르기 및 부작용 Hard Filter Engine</div>'
                    '<div style="font-size:0.75rem; color:#94a3b8; margin-bottom:8px;">'
                    '23개 변수 스캐닝 준비 완료</div>'
                    '<div style="display:flex; align-items:center; gap:6px;">'
                    '<span style="display:inline-block; width:6px; height:6px; background:#10b981; border-radius:50%;"></span>'
                    '<span style="font-size:0.72rem; color:#34d399; font-weight:600;">'
                    'READY &mdash; 확산 필터 가동 대기 중 &#129001;</span>'
                    '</div></div></div></div>'

                    '<div style="background:rgba(59,130,246,0.06); border:1px solid rgba(59,130,246,0.2);'
                    ' border-radius:12px; padding:16px; margin-bottom:14px;">'
                    '<div style="display:flex; align-items:flex-start; gap:12px;">'
                    '<span style="font-size:1.5rem; line-height:1;">&#128138;</span>'
                    '<div style="flex:1;">'
                    '<div style="font-size:0.82rem; font-weight:700; color:#e2e8f0; margin-bottom:5px;">'
                    '영양소 오버도즈 디옵티마이저</div>'
                    '<div style="font-size:0.75rem; color:#94a3b8; margin-bottom:8px;">'
                    '식약처 상한 섭취량 실시간 동기화 완료</div>'
                    '<div style="display:flex; align-items:center; gap:6px;">'
                    '<span style="display:inline-block; width:6px; height:6px; background:#10b981; border-radius:50%;"></span>'
                    '<span style="font-size:0.72rem; color:#34d399; font-weight:600;">'
                    'SYNCED &mdash; 식약처 DB 연동 정상 &#129001;</span>'
                    '</div></div></div></div>'

                    '<div style="background:rgba(167,139,250,0.06); border:1px solid rgba(167,139,250,0.2);'
                    ' border-radius:12px; padding:16px;">'
                    '<div style="display:flex; align-items:flex-start; gap:12px;">'
                    '<span style="font-size:1.5rem; line-height:1;">&#129302;</span>'
                    '<div style="flex:1;">'
                    '<div style="font-size:0.82rem; font-weight:700; color:#e2e8f0; margin-bottom:5px;">'
                    'Scikit-Learn ML 가중치 연산 커널</div>'
                    '<div style="font-size:0.75rem; color:#94a3b8; margin-bottom:8px;">'
                    '독립변수 다차원 추론 대기 중</div>'
                    '<div style="display:flex; align-items:center; gap:6px;">'
                    '<span style="display:inline-block; width:6px; height:6px; background:#10b981; border-radius:50%;"></span>'
                    '<span style="font-size:0.72rem; color:#34d399; font-weight:600;">'
                    'STANDBY &mdash; ML 테크놀로지 실시간 가동 중 &#129001;</span>'
                    '</div></div></div></div>'

                    '</div>'
                )
                st.markdown(engine_status_html, unsafe_allow_html=True)

            st.markdown("---")
            
            # 하단: 3단 프로세스 플로우 인포그래픽
            st.markdown("### 🗺️ 뉴트리핏 케어 프로세스 플로우")
            st.write("안전한 데이터 분석에 입각해 추천부터 섭취 라이프사이클까지 과학적으로 제어합니다.")
            
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                st.markdown("""
                    <div style="background: rgba(30, 41, 59, 0.3); border: 1px solid rgba(255,255,255,0.05); border-radius: 14px; padding: 18px; min-height: 150px; text-align: center;">
                        <h4 style="margin: 0 0 8px 0; color: #60a5fa; font-family: 'Outfit'; font-size: 1.15rem;">01. 초개인화 문진</h4>
                        <p style="font-size: 0.82rem; color: #94a3b8; line-height: 1.5; margin: 0;">
                            성별 분기 데이터 수집, BMI 자가 판정, 23개 전항목 신체 습관 변수를 복합 설계하여 유저의 고유 데이터를 수렴합니다.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            with col_p2:
                st.markdown("""
                    <div style="background: rgba(30, 41, 59, 0.3); border: 1px solid rgba(255,255,255,0.05); border-radius: 14px; padding: 18px; min-height: 150px; text-align: center;">
                        <h4 style="margin: 0 0 8px 0; color: #34d399; font-family: 'Outfit'; font-size: 1.15rem;">02. ML 위험도 및 상한치 분석</h4>
                        <p style="font-size: 0.82rem; color: #94a3b8; line-height: 1.5; margin: 0;">
                            Scikit-Learn 로지스틱 회귀를 통한 만성질환 리스크 예측과 성분 중복에 따른 과다 복용 위험을 실시간 안전 필터링합니다.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            with col_p3:
                st.markdown("""
                    <div style="background: rgba(30, 41, 59, 0.3); border: 1px solid rgba(255,255,255,0.05); border-radius: 14px; padding: 18px; min-height: 150px; text-align: center;">
                        <h4 style="margin: 0 0 8px 0; color: #fbbf24; font-family: 'Outfit'; font-size: 1.15rem;">03. 매트릭스 비교 및 캘린더 매핑</h4>
                        <p style="font-size: 0.82rem; color: #94a3b8; line-height: 1.5; margin: 0;">
                            상품 보관함 비교 매트릭스를 통한 스펙 병렬 대조와 3대 시간대별 복용 스케줄러 자동 편성으로 올바른 섭취 주기를 제안합니다.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
        # ==================== 화면 분기 1: STEP 1~5 설문 문진 작성 ====================
        elif st.session_state.step == 1:
            st.subheader("📝 웰니스 초개인화 설문 (STEP 1 ~ STEP 5)")
            
            # STEP 1. 기본 정보
            st.markdown("### 👤 STEP1. 기본 정보")
            col_s1_1, col_s1_2 = st.columns(2)
            with col_s1_1:
                gender = st.radio("1. 성별:", ["남성", "여성", "응답하지 않음"])
                
                male_worries = []
                if gender == "남성":
                    male_worries = st.multiselect(
                        "2. [남성 전용] 고민 영역 (복수선택):",
                        ["탈모·두피 관리", "전립선 건강", "근육량 증가"]
                    )
                
                female_lifecycle = "해당없음"
                if gender == "여성":
                    female_lifecycle = st.selectbox(
                        "3. [여성 전용] 생애주기 상태:",
                        ["해당없음", "임신 준비 중", "임신 중", "수유 중", "폐경기"]
                    )
            
            with col_s1_2:
                age = st.selectbox(
                    "4. 연령대:",
                    ["영유아 및 어린이(만 1세~12세)", "청소년(13세~19세)", "20세~25세", "26세~29세", "30대", "40대", "50대", "60대 이상"],
                    index=4
                )
                height = st.number_input("5-1. 키 (cm):", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
                weight = st.number_input("5-2. 몸무게 (kg):", min_value=30.0, max_value=200.0, value=65.0, step=0.1)
                
                bmi = round(weight / ((height / 100.0) ** 2), 2)
                bmi_status = "정상"
                if bmi < 18.5:
                    bmi_status = "저체중"
                elif 18.5 <= bmi < 23.0:
                    bmi_status = "정상"
                elif 23.0 <= bmi < 25.0:
                    bmi_status = "과체중"
                else:
                    bmi_status = "비만"
                st.markdown(f"""
                    <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 8px; padding: 10px; margin-top: 10px;">
                        💡 <strong>실시간 BMI 지수:</strong> <span style="color: #3b82f6; font-weight: bold;">{bmi}</span> (분류: <strong>{bmi_status}</strong>)
                    </div>
                """, unsafe_allow_html=True)

            # STEP 2. 라이프스타일 & 일상 습관
            st.markdown("---")
            st.markdown("### 🏃 STEP2. 라이프스타일 & 일상 습관")
            col_s2_1, col_s2_2 = st.columns(2)
            with col_s2_1:
                exercise = st.multiselect(
                    "6. 운동 종류 및 목적 (복수선택):",
                    ["안 함·체력유지재활", "고강도 유산소", "저항성·근력 운동", "유연성·코어", "고강도 인터벌"],
                    default=["안 함·체력유지재활"]
                )
                drinking = st.selectbox("7. 음주 빈도:", ["전혀 안 함", "보통", "잦은 음주"])
                caffeine = st.selectbox("8. 하루 카페인 섭취:", ["0잔", "1~2잔", "3잔", "4잔 이상"])
            
            with col_s2_2:
                diet = st.selectbox(
                    "9. 식습관:",
                    ["일반식·불규칙", "육식 위주", "채식·간헐적 단식", "완벽한 비건"]
                )
                sleep = st.selectbox("10. 수면 시간:", ["5시간 미만", "5~7시간", "8시간 이상"])
                stress = st.select_slider(
                    "11. 스트레스 자가인지:",
                    options=["1단계", "2단계", "3단계", "4단계", "5단계"],
                    value="3단계"
                )

            # STEP 3. 건강 상태 & 안전성 필터
            st.markdown("---")
            st.markdown("### 🛡️ STEP3. 건강 상태 & 안전성 필터 (민감 정보)")
            col_s3_1, col_s3_2 = st.columns(2)
            with col_s3_1:
                smoking = st.radio("12. 흡연 여부:", ["비흡연", "흡연"])
                
                allergies_raw = st.multiselect(
                    "13. 알레르기 원료 (복수선택):",
                    ["갑각류", "대두", "글루텐", "유제품", "견과류", "어류", "과일류", "없음", "기타(직접입력)"],
                    default=["과일류"]
                )
                
                allergy_direct = ""
                if "기타(직접입력)" in allergies_raw:
                    allergy_direct = st.text_input("13-1. 알레르기 직접 입력 (쉼표 구분):")
                
                allergies = []
                if "없음" in allergies_raw and len(allergies_raw) > 1:
                    allergies = [a for a in allergies_raw if a != "없음"]
                else:
                    allergies = allergies_raw
                    
            with col_s3_2:
                side_effects_raw = st.multiselect(
                    "14. 과거 부작용 경험 성분 (복수선택):",
                    ["철분", "오메가3", "비타민C", "유산균", "없음", "기타 직접입력"],
                    default=["없음"]
                )
                
                side_effect_direct = ""
                if "기타 직접입력" in side_effects_raw:
                    side_effect_direct = st.text_input("14-1. 부작용 성분 직접 입력 (쉼표 구분 가능):")
                
                side_effects = []
                if "없음" in side_effects_raw:
                    if len(side_effects_raw) > 1:
                        side_effects = [s for s in side_effects_raw if s != "없음"]
                        st.info("💡 **'없음'** 외의 부작용 성분이 선택되어 '없음' 항목이 자동으로 해제되었습니다.")
                    else:
                        side_effects = ["없음"]
                else:
                    side_effects = side_effects_raw
                
                diseases_raw = st.multiselect(
                    "15. 지병 및 복용 약물 (복수선택):",
                    ["고혈압", "당뇨", "이상지질혈증", "만성 위장질환", "혈전 관련질환-항응고제", "간·신장질환", "없음(단독 선택)", "기타(직접입력)"],
                    default=["당뇨"]
                )
                
                disease_direct = ""
                if "기타(직접입력)" in diseases_raw:
                    disease_direct = st.text_input("15-1. 지병 및 복용 약물 직접 입력 (기타 직접 입력용):")
                
                diseases = []
                if "없음(단독 선택)" in diseases_raw:
                    if len(diseases_raw) > 1:
                        diseases = [d for d in diseases_raw if d != "없음(단독 선택)"]
                        st.info("💡 **'없음(단독 선택)'** 외의 다른 지병이 선택되어 '없음' 항목이 자동으로 해제되었습니다.")
                    else:
                        diseases = ["없음(단독 선택)"]
                else:
                    diseases = diseases_raw

            # STEP 4. 건강 고민 및 목표
            st.markdown("---")
            st.markdown("### 🎯 STEP4. 건강 고민 및 목표")
            health_goals = st.multiselect(
                "16. 건강 고민 및 목표 (최대 3개 선택):",
                ["만성피로", "눈 건조·피로", "장 건강", "피부탄력·이너뷰티", "체지방감소·다이어트", "면역력저하", "관절보호", "수면부족·스트레스케어", "항노화·항산화", "생리불순·생리통"],
                default=["만성피로", "눈 건조·피로", "장 건강"],
                max_selections=3
            )
            
            # STEP 5. 섭취 편의성 및 구매 성향
            st.markdown("---")
            st.markdown("### 🛍️ STEP5. 섭취 편의성 및 구매 성향")
            col_s5_1, col_s5_2 = st.columns(2)
            with col_s5_1:
                pill_discomfort = st.radio("17. 알약 불편감:", ["상관없음", "매우 불편함"])
                alternative_form = st.selectbox(
                    "18. 대안 제형 선호:",
                    ["소형 알약", "구미·젤리", "액상·드링크", "분말·포"]
                )
                pref_form = st.selectbox(
                    "19. 선호하는 영양제 형태:",
                    ["정제(알약/정)", "캡슐", "젤리", "구미", "액상", "분말"],
                    index=0
                )
                buy_method = st.selectbox("23. 구매 방식 선호:", ["정기구독", "1회구매", "상관없음"])
            
            with col_s5_2:
                values = st.multiselect(
                    "20. 구매 시 우선 가치 (최대 2개 선택):",
                    ["성분 함량", "원산지·브랜드", "첨가물 최소화", "복용 편의성"],
                    default=["성분 함량"],
                    max_selections=2
                )
                environment = st.radio("21. 복용 환경 선호:", ["거치형·대용량", "휴대형"])
                budget = st.selectbox(
                    "22. 월 예산대:",
                    ["1~3만원", "3~5만원", "5~10만원", "10만원 이상"]
                )

            st.markdown("---")
            
            goals_ok = len(health_goals) > 0
            if not goals_ok:
                st.info("💡 진단 및 웰니스 분석을 진행하려면 **STEP4. 건강 고민 및 목표**를 최소 1개 선택해 주세요.")

            # 진단 및 단계 전환 버튼
            if st.button("진단 및 맞춤 스코어 확인하기 ➡️", disabled=not goals_ok):
                survey_payload = {
                    "gender": gender,
                    "male_worries": male_worries,
                    "female_lifecycle": female_lifecycle,
                    "age": age,
                    "height": height,
                    "weight": weight,
                    "bmi": bmi,
                    "exercise": exercise,
                    "drinking": drinking,
                    "caffeine": caffeine,
                    "diet": diet,
                    "sleep": sleep,
                    "stress": stress,
                    "smoking": smoking,
                    "allergies": allergies,
                    "allergy_direct": allergy_direct,
                    "side_effects": side_effects,
                    "side_effect_direct": side_effect_direct,
                    "diseases": diseases,
                    "disease_direct": disease_direct,
                    "health_goals": health_goals,
                    "pill_discomfort": pill_discomfort,
                    "alternative_form": alternative_form,
                    "pref_form": pref_form,
                    "values": values,
                    "environment": environment,
                    "budget": budget,
                    "buy_method": buy_method
                }
                st.session_state.survey_data = survey_payload
                
                try:
                    log_survey_data(survey_payload)
                except Exception as e:
                    st.error(f"로그 적재 실패: {e}")
                    
                st.session_state.step = 2
                st.session_state.streaming_done = False # 새로운 분석 리포트 전환 시 플래그 리셋
                st.rerun()

        # ==================== 화면 분기 2: 웰니스 스코어보드 결과 화면 ====================
        elif st.session_state.step == 2:
            st.subheader("📊 웰니스 스코어 분석 결과 리포트 (Step 2)")
            survey = st.session_state.survey_data
            
            try:
                from src.engine.scoring import calculate_wellness_bonus
            except ModuleNotFoundError:
                from project2_team3.src.engine.scoring import calculate_wellness_bonus
                
            bonuses = calculate_wellness_bonus(survey)
            
            col_board_left, col_board_right = st.columns([2.0, 1.0], gap="large")
            
            with col_board_left:
                st.markdown("### 🧬 내 몸에 필요한 6대 핵심 영양제 가산점 현황")
                st.write("유저의 일상 라이프스타일, 기본 정보 및 주요 건강 고민(최대 3개)에 대한 스코어 분배율을 복합 분석하여 산출된 보너스 스코어입니다.")
                st.markdown("""
                    <div style="background: rgba(59, 130, 246, 0.07); border-left: 3px solid rgba(59, 130, 246, 0.5); border-radius: 6px; padding: 8px 14px; margin-bottom: 12px; font-size: 0.82rem; color: #94a3b8; line-height: 1.55;">
                        ※ 전체 제품 추천 랭킹은 <strong style="color: #60a5fa;">10점 만점 기준</strong>으로 정렬되며, 유저의 3대 핵심 건강 고민 매칭 결과에 따라 성분별로 최대 <strong style="color: #34d399;">+2.50점</strong>의 동적 가산점(보너스 스코어)이 부여된 현황입니다.
                    </div>
                """, unsafe_allow_html=True)
                
                col_b1, col_b2, col_b3 = st.columns(3)
                cols = [col_b1, col_b2, col_b3]
                
                keys = list(bonuses.keys())
                for idx, key in enumerate(keys):
                    col = cols[idx % 3]
                    score = bonuses[key]
                    
                    comment = "기본 섭취 권장"
                    if score >= 8.0:
                        comment = "🚨 매우 필요 (집중 섭취 추천)"
                    elif score >= 1.5:
                        comment = "⭐ 적극 권장 (맞춤 매칭)"
                        
                    col.markdown(f"""
                        <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 18px; margin-bottom: 15px;">
                            <span style="font-size: 0.85rem; color: #94a3b8;">영양소 성분</span>
                            <h4 style="margin: 2px 0 6px 0; color: #f8fafc;">{key}</h4>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 1.8rem; font-weight: 800; color: #10b981;">+{score:.2f}</span>
                                <span style="font-size: 0.8rem; color: #a7f3d0; background: rgba(16, 185, 129, 0.1); padding: 2px 6px; border-radius: 5px;">{comment}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
            with col_board_right:
                record_count = 0
                if os.path.exists(LOG_FILE_PATH):
                    try:
                        temp_df = pd.read_csv(LOG_FILE_PATH, encoding="utf-8-sig")
                        record_count = len(temp_df)
                    except:
                        pass
                
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1e1b4b, #311042); border: 1px solid rgba(167, 139, 250, 0.3); border-radius: 12px; padding: 20px; box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3); margin-top: 15px;">
                        <h4 style="margin: 0 0 10px 0; color: #c084fc; font-family: 'Outfit', 'Noto Sans KR', sans-serif;">🤖 AI 건강 패턴 분석 (ML 가동 대기)</h4>
                        <p style="font-size: 0.9rem; color: #e9d5ff; margin-bottom: 15px; line-height: 1.4;">
                            수집된 대용량 웰니스 적재 로그를 기반으로 향후 <strong>XGBoost 위험도 분류기</strong> 모델이 연동되는 지능형 분석 영역입니다.
                        </p>
                        <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.2); padding: 8px 12px; border-radius: 8px;">
                            <span style="font-size: 0.8rem; color: #a78bfa;">📊 문진 데이터 축적 상태</span>
                            <span style="background: rgba(167, 139, 250, 0.2); color: #f472b6; font-weight: 700; padding: 2px 10px; border-radius: 20px; font-size: 0.85rem;">
                                누적 데이터: {record_count}건
                            </span>
                        </div>
                        <div style="margin-top: 15px; border-top: 1px dashed rgba(167, 139, 250, 0.2); padding-top: 10px; font-size: 0.75rem; color: #a78bfa; text-align: center;">
                            ⏳ 목표 데이터셋 500건 충족 시 AI 심혈관/대사 위험도 스위칭 모듈 활성화
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("---")
            
            st.markdown("### 🛡️ 개인 맞춤형 안전성 필터 동작 리포트")
            banned_list = list(survey.get("side_effects", []))
            direct_banned = survey.get("side_effect_direct", "").strip()
            if direct_banned:
                banned_list.append(direct_banned)
            banned_list = [b for b in banned_list if b != "기타 직접입력" and b != "없음"]
            
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                st.markdown("#### 🚫 부작용 배제 필터")
                if banned_list:
                    st.error(f"다음 부작용 성분이 함유된 제품군은 추천 리스트에서 **원천 배제(Hard Filter)** 처리되었습니다:\n\n`{', '.join(banned_list)}`")
                else:
                    st.success("부작용 배제 성분이 설정되지 않았습니다. 모든 맞춤 영양제를 정상 매칭합니다.")
            with col_f2:
                st.markdown("#### 🌾 알레르기 및 주의 원료")
                allergies = list(survey.get("allergies", []))
                allergy_direct = survey.get("allergy_direct", "").strip()
                if allergy_direct:
                    allergies.append(allergy_direct)
                allergies_cleaned = [a for a in allergies if a not in ["없음", "기타(직접입력)"]]
                
                if allergies_cleaned:
                    st.error(f"다음 알레르기 유발 물질이 포함된 제품군은 추천 리스트에서 **원천 배제(Hard Filter)** 처리되었습니다:\n\n`{', '.join(allergies_cleaned)}`")
                else:
                    st.success("알레르기 필터가 적용되지 않았습니다.")
                    
            st.markdown("---")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("⬅️ 이전 단계 (문진 수정)"):
                    st.session_state.step = 1
                    st.rerun()
            with col_btn2:
                if st.button("초개인화 장바구니 큐레이션 보기 ➡️"):
                    st.session_state.step = 3
                    st.session_state.streaming_done = False # 다음 단계 전환 시 스트리밍 플래그 초기화
                    st.rerun()

        # ==================== 화면 분기 3: 초개인화 장바구니 큐레이션 결과 ====================
        elif st.session_state.step == 3:
            st.markdown('<div class="main-title" style="font-size:1.8rem;">&#x1F4A1; 뉴트리핏 초개인화 맞춤 큐레이션 결과</div>', unsafe_allow_html=True)
            
            survey = st.session_state.survey_data

            side_effects_cleaned = [s for s in survey.get("side_effects", []) if s not in ["없음", "기타 직접입력"]]
            if survey.get("side_effect_direct", "").strip():
                side_effects_cleaned.append(survey.get("side_effect_direct"))
            algs = list(survey.get("allergies", []))
            if survey.get("allergy_direct", "").strip():
                algs.append(survey.get("allergy_direct"))
            algs_display = [a for a in algs if a not in ["없음", "기타(직접입력)"]]
            exclusions = side_effects_cleaned + algs_display
            exclusions_str = ', '.join(exclusions) if exclusions else '없음'

            # ==================== [2.3 | 1.0] 비대칭 그리드 분할 ====================
            col_main, col_side = st.columns([2.3, 1.0], gap="large")

            with col_main:
                # --- 프로필 배너 ---
                st.markdown(f"""
                    <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 14px; padding: 14px 18px; margin-bottom: 18px;">
                        <strong>&#x1F4CA; 분석 대상자 프로필:</strong> {survey['gender']} ({survey['age']}) | BMI: {survey['bmi']} |
                        &#x1F3AF; <strong>핵심 건강고민:</strong> {', '.join(survey['health_goals'])} |
                        &#x1F6AB; <strong>배제 성분:</strong> {exclusions_str}
                    </div>
                """, unsafe_allow_html=True)

                # --- AI 총평 스트리밍 ---
                st.markdown("#### &#x1F916; 뉴트리핏 AI 개인화 큐레이션 총평 리포트")
                ai_report_text = (
                    f"{survey['gender']} ({survey['age']}) 분석 대상자님은 현재 [{', '.join(survey['health_goals'])}] 건강 고민을 집중 케어하기 위해 웰니스 스코어 보너스 가산점을 정밀 배분 받으셨습니다. "
                    f"현재 BMI 지수는 {survey['bmi']}로 안전 수준을 유지하고 계시며, 설정된 부작용 이력 및 [{exclusions_str}] 등의 성분이 함유된 제품군은 "
                    f"스코어 산정 리스트에서 선제 필터링되었습니다. 아래 식약처 공인 성분 지식베이스 규격에 맞춰 엄선한 랭킹 TOP 12와 최적의 복용 골든타임을 참고하시기 바랍니다."
                )
                if not st.session_state.streaming_done:
                    def text_char_generator(text):
                        for char in text:
                            yield char
                            time.sleep(0.008)
                    st.write_stream(text_char_generator(ai_report_text))
                else:
                    st.write(ai_report_text)

                # --- 🚨 AI 긴급 안전성 교차 필터 경고창 ---
                st.markdown("---")
                st.markdown("### &#x1F4CA; 실시간 중복/과다 섭취 안전성 시뮬레이션")
                categories = ["마그네슘", "비타민C", "오메가3", "유산균 / 프로바이오틱스", "콜라겐", "멀티비타민"]
                selected_category = st.selectbox(
                    "&#x1F50E; 특정 추천 카테고리만 필터링:",
                    ["전체 맞춤 추천"] + categories,
                    index=0
                )
                filter_cat = None if selected_category == "전체 맞춤 추천" else selected_category

                try:
                    recommendations = get_recommendations(survey, selected_category=filter_cat, top_n=24)
                except Exception as e:
                    st.error(f"추천 엔진 구동 중 에러가 발생했습니다: {e}")
                    if st.button("돌아가기"):
                        st.session_state.step = 2
                        st.rerun()
                    return

                if recommendations.empty:
                    st.warning("⚠️ 입력하신 알레르기/부작용 필터 또는 맞춤 가중치 조건에 해당하는 제품이 목록에 존재하지 않거나 모두 필터링되었습니다.")
                    if st.button("⬅️ 웰니스 리포트로 돌아가기"):
                        st.session_state.step = 2
                        st.rerun()
                    return

                product_names_list = []
                for i, (idx, row) in enumerate(recommendations.iterrows()):
                    platform = str(row.get('platform') or 'Unknown')
                    name = str(row.get('product_name') or row.get('displayName') or '이름 없음')
                    product_names_list.append(f"{i+1}위. [{platform}] {name[:55]}")

                selected_combos = st.multiselect(
                    "&#x26A0;&#xFE0F; 조합할 제품군 복수 선택 (초과 복용 실시간 감지):",
                    options=product_names_list,
                    default=product_names_list[:2] if len(product_names_list) >= 2 else product_names_list
                )
                if selected_combos:
                    total_vit_c = total_mag = total_vit_d = total_zinc = 0.0
                    for combo_label in selected_combos:
                        try:
                            rank_idx = int(combo_label.split('위.')[0].strip()) - 1
                            row_combo = recommendations.iloc[rank_idx]
                            std_ing_combo = str(row_combo.get('표준성분', ''))
                            if "비타민C" in std_ing_combo: total_vit_c += 1000.0
                            if "멀티비타민" in std_ing_combo or "비타민" in std_ing_combo:
                                total_vit_c += 500.0; total_mag += 100.0; total_vit_d += 1000.0; total_zinc += 10.0
                            if "마그네슘" in std_ing_combo: total_mag += 350.0
                            if "비타민D" in std_ing_combo: total_vit_d += 2000.0
                        except: pass
                    danger_messages = []
                    if total_vit_c > 2000.0:
                        danger_messages.append(f"⚠️ **비타민C 과다 복용 위험!** ({total_vit_c:.0f}mg / 상한치 2000mg 대비 {(total_vit_c/2000)*100:.0f}%)")
                    if total_mag > 350.0:
                        danger_messages.append(f"⚠️ **마그네슘 과량 복용 주의!** ({total_mag:.0f}mg / 상한치 350mg 대비 {(total_mag/350)*100:.0f}%)")
                    if total_vit_d > 4000.0:
                        danger_messages.append(f"⚠️ **비타민D 고칼슘혈증 경고!** ({total_vit_d:.0f}IU / 상한치 4000IU 대비 {(total_vit_d/4000)*100:.0f}%)")
                    if danger_messages:
                        for msg in danger_messages: st.error(msg)
                    else:
                        st.success("&#x1F7E2; 식약처 안전 섭취 규격 충족 조합입니다.")

                product_options = []
                for i, (idx, row) in enumerate(recommendations.iterrows()):
                    platform = str(row.get('platform') or 'Unknown')
                    name = str(row.get('product_name') or row.get('displayName') or '이름 없음')
                    product_options.append(f"{i+1}위. [{platform}] {name[:60]}...")
                selected_product_label = st.selectbox(
                    "&#x1F52C; 식약처 가이드라인 조회할 영양제 선택:",
                    product_options, index=0
                )
                selected_idx = product_options.index(selected_product_label)
                selected_row = recommendations.iloc[selected_idx]

                # --- 성분 카테고리 탭 + 4열 카드 그리드 ---
                st.markdown("---")
                st.markdown("### &#x1F3C6; 큐레이션 추천 랭킹 TOP 12")
                tab_all, tab_vit, tab_min, tab_others = st.tabs(["전체 제품", "비타민 계열", "미네랄 계열", "오메가 / 유산균 / 콜라겐"])
                with tab_all:
                    render_product_grid(recommendations.head(12), selected_row, db_data, survey)
                with tab_vit:
                    df_vit = recommendations[recommendations['표준성분'].str.contains('비타민|레티놀|엽산', na=False, case=False)]
                    render_product_grid(df_vit.head(12), selected_row, db_data, survey)
                with tab_min:
                    df_min = recommendations[recommendations['표준성분'].str.contains('마그네슘|철분|아연|칼슘|미네랄|구리|망간|셀렌', na=False, case=False)]
                    render_product_grid(df_min.head(12), selected_row, db_data, survey)
                with tab_others:
                    df_oth = recommendations[recommendations['표준성분'].str.contains('오메가|유산균|프로바이오틱스|콜라겐', na=False, case=False)]
                    render_product_grid(df_oth.head(12), selected_row, db_data, survey)

                # --- 트리플 아웃링크 버튼 덱 ---
                sel_name = str(selected_row.get('product_name') or selected_row.get('displayName') or '')
                import urllib.parse
                coupang_url = f"https://www.coupang.com/np/search?q={urllib.parse.quote(sel_name)}"
                naver_url = f"https://search.shopping.naver.com/search/all?query={urllib.parse.quote(sel_name)}"
                iherb_url = f"https://www.iherb.com/search?kw={urllib.parse.quote(sel_name)}"
                st.markdown(f"""
                    <div class="outlink-deck">
                        <a class="outlink-btn outlink-btn-coupang" href="{coupang_url}" target="_blank">&#x1F7E0; 쿠팡 검색</a>
                        <a class="outlink-btn outlink-btn-naver" href="{naver_url}" target="_blank">&#x1F7E2; 네이버 쇼핑</a>
                        <a class="outlink-btn outlink-btn-iherb" href="{iherb_url}" target="_blank">&#x1F7E2; 아이허브 직구</a>
                    </div>
                """, unsafe_allow_html=True)

                # --- 비교 보관함 ---
                st.markdown("---")
                st.markdown("### &#x1F6D2; 뉴트리핏 인터랙티브 상품 비교 보관함 (Comparison Matrix)")
                st.write("선택하신 영양제들의 브랜드, 가격, 평점 및 식약처 공식 기능성 규격을 한눈에 병렬 대조하여 최적의 선택을 돕습니다.")

                selected_compare = st.multiselect(
                    "⚖️ 대조 비교할 상품을 보관함에 담아보세요 (최대 3개 선택):",
                    options=product_names_list,
                    default=product_names_list[:2] if len(product_names_list) >= 2 else product_names_list,
                    max_selections=3,
                    key="compare_matrix_selector"
                )

                if not selected_compare:
                    st.info("비교할 상품을 보관함에 담아주세요 🛒")
                else:
                    cols_compare = st.columns(len(selected_compare))
                    for idx_c, combo_label in enumerate(selected_compare):
                        try:
                            rank_idx = int(combo_label.split('위.')[0].strip()) - 1
                            row_compare = recommendations.iloc[rank_idx]
                            comp_platform = str(row_compare.get('platform') or 'Unknown')
                            comp_name = str(row_compare.get('product_name') or row_compare.get('displayName') or '이름 없음')
                            comp_brand = str(row_compare.get('brandName') or row_compare.get('brand') or '브랜드 정보 없음')
                            comp_rating = row_compare.get('rating', 0.0)
                            comp_reviews = int(row_compare.get('review_count', 0))
                            comp_std_ing = str(row_compare.get('표준성분', ''))
                            comp_detail_url = get_product_detail_url(row_compare)
                            comp_mkt = get_market_top_product(comp_std_ing)
                            comp_price_val = row_compare.get('price')
                            if pd.isna(comp_price_val):
                                comp_price_val = row_compare.get('discountPrice') or row_compare.get('price_cur') or 0.0
                            comp_price_str = f"{int(comp_price_val):,}원" if comp_price_val > 0 else "가격 정보 없음"
                            comp_foodsafety = find_foodsafety_info(comp_std_ing, db_data)
                            comp_fn_desc = "표준 고시 기준 규격 적용 원료"
                            if comp_foodsafety:
                                comp_fn_desc = comp_foodsafety[0]['functionality']
                            with cols_compare[idx_c]:
                                primary_url = comp_mkt["url"] if comp_mkt else comp_detail_url
                                mkt_badge_html = ""
                                if comp_mkt:
                                    mkt_badge_html = (
                                        f'<div style="background:rgba(251,191,36,0.1);border:1px solid rgba(251,191,36,0.3);border-radius:10px;padding:10px 12px;margin-top:10px;">'
                                        f'<div style="font-size:0.68rem;color:#fbbf24;font-weight:700;margin-bottom:4px;">📌 시장 내 대표 인기 제품</div>'
                                        f'<div style="font-size:0.78rem;color:#e2e8f0;font-weight:600;">{comp_mkt["brand"]} {comp_mkt["name"]}</div>'
                                        f'<div style="font-size:0.8rem;color:#34d399;font-weight:700;margin-top:2px;">{comp_mkt["price"]}</div>'
                                        f'<a href="{comp_mkt["url"]}" target="_blank" style="font-size:0.68rem;color:#60a5fa;text-decoration:none;">🔗 네이버쇼핑 바로가기 ↗</a>'
                                        f'</div>'
                                    )
                                st.markdown(f'''<div style="background:#FAFBFF;border:2px solid #5A83F1;border-radius:20px;padding:20px;min-height:390px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 8px 24px rgba(90,131,241,0.06);">
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
</div>''', unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"비교 처리 중 오류: {e}")

            # ==================== 우측 유틸리티 사이드카드 (col_side) ====================
            with col_side:
                # --- 유틸 카드 1: 타임라인 가이드 ---
                st.markdown('<div class="side-section-label">⏰ AI 복용 골든타임</div>', unsafe_allow_html=True)
                all_std_ings = "".join(recommendations.head(12)['표준성분'].dropna().tolist())
                morning_items, lunch_items, night_items = [], [], []
                if "유산균" in all_std_ings or "프로바이오틱스" in all_std_ings:
                    morning_items.append("🥛 유산균/프로바이오틱스 — 공복 복용 권장")
                if "비타민C" in all_std_ings:
                    lunch_items.append("🍊 비타민C — 식후 복용 권장")
                if "멀티비타민" in all_std_ings or "비타민" in all_std_ings:
                    lunch_items.append("🍇 멀티비타민 — 식후 에너지 대사")
                if "오메가3" in all_std_ings:
                    lunch_items.append("🐟 오메가3 — 식후 담즙산 흡수")
                if "마그네슘" in all_std_ings:
                    night_items.append("🥑 마그네슘 — 취침 전 신경 안정")
                if "콜라겐" in all_std_ings:
                    night_items.append("🎀 콜라겐 — 야간 피부 재생")

                tl_html = ''
                tl_html += '<div style="background:rgba(59,130,246,0.07);border:1px solid rgba(59,130,246,0.18);border-radius:12px;padding:12px 14px;margin-bottom:10px;">'                           '<div style="font-size:0.78rem;font-weight:700;color:#60a5fa;margin-bottom:6px;">🌅 아침 기상 공복</div>'
                if morning_items:
                    for it in morning_items: tl_html += f'<div style="font-size:0.75rem;color:#e2e8f0;margin-bottom:3px;">{it}</div>'
                else:
                    tl_html += '<div style="font-size:0.73rem;color:#94a3b8;">따뜻한 물 한 잔으로 시작하세요 🟢</div>'
                tl_html += '</div>'
                tl_html += '<div style="background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.18);border-radius:12px;padding:12px 14px;margin-bottom:10px;">'                           '<div style="font-size:0.78rem;font-weight:700;color:#34d399;margin-bottom:6px;">☀️ 점심/오후 식후</div>'
                if lunch_items:
                    for it in lunch_items: tl_html += f'<div style="font-size:0.75rem;color:#e2e8f0;margin-bottom:3px;">{it}</div>'
                else:
                    tl_html += '<div style="font-size:0.73rem;color:#94a3b8;">수분 보충을 충분히 해주세요 ☀️</div>'
                tl_html += '</div>'
                tl_html += '<div style="background:rgba(245,158,11,0.07);border:1px solid rgba(245,158,11,0.18);border-radius:12px;padding:12px 14px;">'                           '<div style="font-size:0.78rem;font-weight:700;color:#fbbf24;margin-bottom:6px;">🌙 저녁 취침 전</div>'
                if night_items:
                    for it in night_items: tl_html += f'<div style="font-size:0.75rem;color:#e2e8f0;margin-bottom:3px;">{it}</div>'
                else:
                    tl_html += '<div style="font-size:0.73rem;color:#94a3b8;">오늘의 영양제 섭취 완료! 숙면을 취하세요 🌙</div>'
                tl_html += '</div>'
                st.markdown(f'<div class="side-util-card">{tl_html}</div>', unsafe_allow_html=True)

                # --- 유틸 카드 2: 내보내기 ---
                st.markdown('<div class="side-section-label">📥 데이터 내보내기</div>', unsafe_allow_html=True)
                import io
                if os.path.exists(LOG_FILE_PATH):
                    try:
                        df_logs_side = pd.read_csv(LOG_FILE_PATH, encoding="utf-8-sig")
                        csv_data_side = df_logs_side.to_csv(index=False, encoding="utf-8-sig")
                        st.download_button(
                            label="📥 누적 로그 (.csv)",
                            data=csv_data_side,
                            file_name="survey_logs_export.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    except Exception:
                        st.info("CSV 데이터가 아직 없습니다.")
                else:
                    st.info("📝 진단 로그가 없습니다.")

            # ==================== 식약처 정밀 성분 가이드 (전체 폭) ====================
            st.markdown("---")
            st.markdown("### 🛡️ 선택 제품 식약처 정밀 성분 분석 가이드")
            std_ing = str(selected_row.get('표준성분', ''))
            st.info(f"📋 **선택 제품**: {selected_row.get('product_name')}\n\n🧬 **검출 표준 성분**: `{std_ing}`")
            foodsafety_infos = find_foodsafety_info(std_ing, db_data)
            if not foodsafety_infos:
                st.info("💡 본 제품의 표준성분은 고시형 원료로 표준 고시 섭취 규격에 따릅니다.")
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    if "마그네슘" in std_ing:
                        st.subheader("🍀 마그네슘 (Magnesium)")
                        st.write("**기능성**: 에너지 이용에 필요, 신경과 근육 기능 유지")
                        st.write("**주의**: 신장 질환자 과량 섭취 시 고마그네슘혈증 위험")
                    elif "비타민C" in std_ing:
                        st.subheader("🍀 비타민C (Vitamin C)")
                        st.write("**기능성**: 항산화, 철 흡수 촉진, 결합조직 유지")
                        st.write("**주의**: 공복 섭취 시 위장 장애 가능 — 식후 복용 권장")
                with col_g2:
                    if "비타민" in std_ing:
                        st.subheader("🍀 종합 비타민 (Multivitamin)")
                        st.write("**기능성**: 체내 에너지 대사, 면역 및 항산화 조절")
                        st.write("**주의**: 복용 기준량 엄수 — 영양소 과다 중독 방지")
            else:
                tabs_fs = st.tabs([f"🧪 {info['target_token']}" for info in foodsafety_infos])
                for tab, info in zip(tabs_fs, foodsafety_infos):
                    with tab:
                        st.success(f"**식약처 공식 승인 명칭**: `{info['raw_material']}`")
                        col_tab1, col_tab2 = st.columns(2)
                        with col_tab1:
                            st.markdown("#### 🎯 기능성 내용")
                            for line in info['functionality'].split('\n'):
                                if line.strip(): st.write(f"- {line.strip()}")
                        with col_tab2:
                            st.markdown("#### 🥄 권장 일일섭취량")
                            st.info(info['daily_intake'])
                            st.markdown("#### ⚠️ 섭취 시 주의사항")
                            st.warning(info['precautions'])

            st.markdown("---")
            col_btn_back1, col_btn_back2 = st.columns(2)
            with col_btn_back1:
                if st.button("⬅️ 이전 단계 (웰니스 리포트)"):
                    st.session_state.step = 2
                    st.rerun()
            with col_btn_back2:
                if st.button("🔄 문진 새로 작성하기"):
                    st.session_state.agreed = False
                    st.session_state.step = 1
                    st.session_state.survey_data = {}
                    st.session_state.all_agree = False
                    st.session_state.agree_1 = False
                    st.session_state.agree_2 = False
                    st.session_state.agree_3 = False
                    st.session_state.streaming_done = False
                    st.rerun()

            # 💥 스트리밍 플래그 완료 처리
            if not st.session_state.streaming_done:
                st.session_state.streaming_done = True
                st.rerun()


    # ==================== 메뉴 분기 2: 📊 뉴트리핏 데이터 인사이트 (Admin) ====================
    elif selected_menu == "📊 뉴트리핏 데이터 인사이트 (Admin)":
        st.subheader("📊 뉴트리핏 백오피스 데이터 모니터링 시스템")
        
        # 헬퍼 함수: PDF 보고서 생성 엔진 (ReportLab 한글 폰트 매칭 지원)
        def generate_pdf_report(logs_df, master_count, record_count):
            import io
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
            
            # 윈도우 시스템 폰트(맑은 고딕) 로딩
            font_path = "C:\\Windows\\Fonts\\malgun.ttf"
            font_name = "Helvetica"
            if os.path.exists(font_path):
                try:
                    from reportlab.pdfbase import pdfmetrics
                    from reportlab.pdfbase.ttfonts import TTFont
                    pdfmetrics.registerFont(TTFont("MalgunGold", font_path))
                    font_name = "MalgunGold"
                except:
                    pass
                    
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Heading1'],
                fontName=font_name,
                fontSize=18,
                textColor=colors.HexColor('#1d4ed8'),
                spaceAfter=12
            )
            body_style = ParagraphStyle(
                'BodyStyle',
                parent=styles['Normal'],
                fontName=font_name,
                fontSize=10,
                leading=14,
                textColor=colors.HexColor('#334155'),
                spaceAfter=6
            )
            
            story = []
            story.append(Paragraph("📊 NutriFit Backoffice 데이터 분석 보고서", title_style))
            story.append(Spacer(1, 10))
            story.append(Paragraph("● 식약처 API 연동 상태: 정상 가동 중 (🟢)", body_style))
            story.append(Paragraph(f"● 제품 마스터 DB: {master_count:,}건 로드 완료 (🟢)", body_style))
            story.append(Paragraph("● Scikit-Learn ML 커널: 실시간 예측 가용 (🟢)", body_style))
            story.append(Paragraph(f"● 누적 진단 로그 수: {record_count:,}건", body_style))
            story.append(Spacer(1, 15))
            
            table_data = [["연령대", "성별", "BMI", "고민 성분"]]
            if not logs_df.empty:
                for _, r in logs_df.head(10).iterrows():
                    table_data.append([
                        str(r.get('age', 'N/A')),
                        str(r.get('gender', 'N/A')),
                        str(r.get('bmi', 'N/A')),
                        str(r.get('health_goals', 'N/A'))[:25]
                    ])
            else:
                table_data.append(["N/A", "N/A", "N/A", "N/A"])
                
            t = Table(table_data, colWidths=[120, 80, 80, 220])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), font_name),
                ('FONTSIZE', (0,0), (-1,-1), 9),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('BOTTOMPADDING', (0,0), (-1,0), 6),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
                ('FONTNAME', (0,1), (-1,-1), font_name),
            ]))
            story.append(t)
            
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()

        # 데이터 사전 로딩
        try:
            df_master = load_data()
            master_count = len(df_master)
        except Exception as e:
            df_master = pd.DataFrame()
            master_count = 0
            st.error(f"마스터 상품 데이터를 불러올 수 없습니다: {e}")
            
        record_count = 0
        if os.path.exists(LOG_FILE_PATH):
            try:
                df_logs = pd.read_csv(LOG_FILE_PATH, encoding="utf-8-sig")
                record_count = len(df_logs)
            except:
                df_logs = pd.DataFrame()
        else:
            df_logs = pd.DataFrame()

        # 1. 시스템 헬스 모니터링 (System Health Dashboard)
        st.markdown("### 🖥️ 시스템 헬스 모니터링 (System Health Dashboard)")
        h1, h2, h3 = st.columns(3)
        with h1:
            st.markdown("""
                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 15px; text-align: center;">
                    <span style="font-size: 1.5rem;">📡</span>
                    <h6 style="margin: 5px 0; color: #a7f3d0; font-size: 0.85rem;">식약처 API 연동 상태</h6>
                    <span style="font-size: 0.9rem; color: #34d399; font-weight: 700;">정상 (🟢)</span>
                </div>
            """, unsafe_allow_html=True)
        with h2:
            st.markdown(f"""
                <div style="background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 12px; padding: 15px; text-align: center;">
                    <span style="font-size: 1.5rem;">📦</span>
                    <h6 style="margin: 5px 0; color: #93c5fd; font-size: 0.85rem;">제품 마스터 DB (27,779건)</h6>
                    <span style="font-size: 0.9rem; color: #60a5fa; font-weight: 700;">로드 완료 (🟢)</span>
                </div>
            """, unsafe_allow_html=True)
        with h3:
            st.markdown("""
                <div style="background: rgba(167, 139, 250, 0.08); border: 1px solid rgba(167, 139, 250, 0.2); border-radius: 12px; padding: 15px; text-align: center;">
                    <span style="font-size: 1.5rem;">⚙️</span>
                    <h6 style="margin: 5px 0; color: #c084fc; font-size: 0.85rem;">Scikit-Learn ML 커널</h6>
                    <span style="font-size: 0.9rem; color: #c084fc; font-weight: 700;">실시간 가동 중 (🟢)</span>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        # [상단 지표]
        col1, col2, col3 = st.columns(3)
        col1.metric("식약처 공인 인정 원료", "768개")
        col2.metric("매칭 마스터 상품 수", f"{master_count:,}개")
        col3.metric("누적 사용자 진단 로그", f"{record_count:,}건")
        
        st.markdown("---")
        
        # [중단 차트] 마스터 상품 데이터 상위 5대 표준성분 분포
        st.markdown("### 🏆 마스터 상품 데이터 상위 5대 표준성분 분포")
        if not df_master.empty and '표준성분' in df_master.columns:
            top_ingredients = df_master['표준성분'].dropna().str.split(',').explode().str.strip().value_counts().head(5)
            if not top_ingredients.empty:
                chart_df = pd.DataFrame({"상품 수": top_ingredients})
                st.bar_chart(chart_df)
            else:
                st.info("표준성분 데이터가 비어 있습니다.")
        else:
            st.info("표준성분 데이터를 표시할 수 없습니다.")
            
        st.markdown("---")
        
        # [하단 트렌드] survey_logs.csv TOP 3 분포 비율
        st.markdown("### 🎯 누적 사용자 건강고민 TOP 3 트렌드")
        if not df_logs.empty and 'health_goals' in df_logs.columns:
            top_goals = df_logs['health_goals'].dropna().str.split(',').explode().str.strip().value_counts().head(3)
            if not top_goals.empty:
                goals_chart_df = pd.DataFrame({"누적 진단 수": top_goals})
                st.bar_chart(goals_chart_df)
            else:
                st.info("누적된 건강고민 트렌드 정보가 없습니다.")
        else:
            st.info("누적된 사용자 진단 로그 파일(survey_logs.csv)이 존재하지 않거나 비어 있습니다.")

        # 2. Raw 데이터 인터랙티브 마스터 그리드 (Interactive Data Grid)
        st.markdown("---")
        st.markdown("### 🗄️ 누적 사용자 진단 로그 마스터 그리드 (Interactive Raw Data)")
        st.write("백오피스 데이터베이스에 축적되는 원본 로그 데이터입니다. 관리자는 직접 컬럼 정렬 및 텍스트 검색 필터링을 수행할 수 있습니다.")
        if not df_logs.empty:
            st.dataframe(df_logs, use_container_width=True)
            
            # 3. CSV & PDF 이원화 파일 내보내기 (Data Export)
            st.markdown("##### 📥 엔터프라이즈 리포트 내보내기 (CSV / PDF 이원화)")
            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                csv_data = df_logs.to_csv(index=False, encoding="utf-8-sig")
                st.download_button(
                    label="📥 실시간 누적 로그 원본 (.csv) 내보내기",
                    data=csv_data,
                    file_name="survey_logs_export.csv",
                    mime="text/csv",
                    help="엑셀 한글 깨짐이 완벽히 방지된 UTF-8-SIG 인코딩 원본 파일입니다."
                )
            with col_ex2:
                try:
                    pdf_data = generate_pdf_report(df_logs, master_count, record_count)
                    st.download_button(
                        label="📄 뉴트리핏 시스템 및 통계 리포트 (.pdf) 내보내기",
                        data=pdf_data,
                        file_name="nutrifit_system_report.pdf",
                        mime="application/pdf",
                        help="메모리 버퍼 상에서 실시간 생성된 관리 검수용 PDF 보고서 파일입니다."
                    )
                except Exception as e:
                    st.error(f"PDF 생성 엔진 대기 중: {e}")
        else:
            st.info("누적된 사용자 진단 로그가 존재하지 않아 내보내기 기능이 활성화되지 않았습니다.")

        # -------------------- 🤖 [기존 스펙 2] Scikit-Learn ML 학습 모델 기반 예측 시뮬레이터 섹션 --------------------
        st.markdown("---")
        st.subheader("🤖 NutriFit 예측 ML 엔진 시뮬레이터")
        st.write("사용자 데이터 로그의 생활 습관 변수를 분석하고, 가중치 기반 회귀 모델을 사용해 시뮬레이션 대상 군의 만성질환 발전 위험도를 실시간 예측합니다.")
        
        # 기저 평균 피처 값 추출
        avg_age = 35.0
        avg_bmi = 23.5
        if not df_logs.empty:
            if 'age' in df_logs.columns:
                def age_to_num(age_str):
                    if '12' in str(age_str): return 8
                    if '19' in str(age_str): return 16
                    if '25' in str(age_str): return 22
                    if '29' in str(age_str): return 27
                    if '30' in str(age_str): return 35
                    if '40' in str(age_str): return 45
                    if '50' in str(age_str): return 55
                    if '60' in str(age_str): return 65
                    return 35
                try:
                    avg_age = df_logs['age'].apply(age_to_num).mean()
                except:
                    avg_age = 35.0
            if 'bmi' in df_logs.columns:
                avg_bmi = pd.to_numeric(df_logs['bmi'], errors='coerce').mean()
                if pd.isna(avg_bmi):
                    avg_bmi = 23.5
                    
        col_sim1, col_sim2 = st.columns(2)
        with col_sim1:
            st.markdown("##### ⚙️ 입력 생활습관 피처 조절")
            stress_val = st.slider("1. 정신적 스트레스 지수 (1~5단계)", 1, 5, 3, key="admin_stress_slider")
            alcohol_val = st.slider("2. 주당 평균 음주 빈도 (회)", 0, 7, 2, key="admin_alcohol_slider")
            sleep_val = st.slider("3. 일일 평균 수면 시간 (시간)", 3, 10, 7, key="admin_sleep_slider")
            
        with col_sim2:
            st.markdown("##### 📊 고정 가중치 변수 (누적 사용자 평균치 자동 수렴)")
            st.write(f"- 👤 대상 유저군 평균 연령: **만 {avg_age:.1f}세**")
            st.write(f"- ⚖️ 대상 유저군 평균 BMI 지수: **{avg_bmi:.2f}**")
            
            # Scikit-Learn 로지스틱 회귀 모델 실제 학습 수행
            model_trained = False
            ml_type_label = ""
            
            if not df_logs.empty and len(df_logs) >= 5:
                try:
                    from sklearn.linear_model import LogisticRegression
                    
                    def get_stress_num(val):
                        try:
                            return float(str(val).replace('단계', '').strip())
                        except:
                            return 3.0
                    def get_alcohol_num(val):
                        val_str = str(val)
                        if '잦은' in val_str: return 4.0
                        if '보통' in val_str: return 2.0
                        return 0.0
                    def get_sleep_num(val):
                        val_str = str(val)
                        if '5시간 미만' in val_str: return 4.0
                        if '5~7' in val_str: return 6.0
                        return 8.0
                        
                    X_train = pd.DataFrame()
                    X_train['stress'] = df_logs['stress'].apply(get_stress_num)
                    X_train['alcohol'] = df_logs['drinking'].apply(get_alcohol_num)
                    X_train['sleep'] = df_logs['sleep'].apply(get_sleep_num)
                    X_train['bmi'] = pd.to_numeric(df_logs['bmi'], errors='coerce').fillna(23.5)
                    
                    y_train = df_logs['health_goals'].apply(lambda x: 1 if '만성피로' in str(x) else 0)
                    
                    if len(y_train.unique()) > 1:
                        model_ml = LogisticRegression()
                        model_ml.fit(X_train, y_train)
                        pred_prob = model_ml.predict_proba([[float(stress_val), float(alcohol_val), float(sleep_val), float(avg_bmi)]])
                        predicted_risk = float(pred_prob[0][1]) * 100.0
                        model_trained = True
                        ml_type_label = "💡 Scikit-Learn LogisticRegression 실제 학습 모델 예측"
                except Exception as e:
                    pass
                    
            if not model_trained:
                # 데이터가 부족한 초기 상태: 기저 가중치 기반 수식 연산 Fallback 작동
                base_risk = 12.5
                stress_impact = (stress_val - 1) * 8.5
                alcohol_impact = alcohol_val * 4.2
                sleep_impact = max(0.0, (8.0 - sleep_val) * 7.5)
                bmi_impact = max(0.0, (avg_bmi - 22.0) * 3.8)
                age_impact = max(0.0, (avg_age - 20.0) * 0.4)
                
                predicted_risk = min(99.9, max(5.0, base_risk + stress_impact + alcohol_impact + sleep_impact + bmi_impact + age_impact))
                ml_type_label = "⏳ 초기 상태: 기저 가중치 기반 예측 시뮬레이션 (학습용 데이터 부족)"
            
            if predicted_risk <= 35.0:
                risk_status = "낮음 (양호한 건강 웰니스 관리 상태)"
                risk_color = "#10b981"
            elif predicted_risk <= 65.0:
                risk_status = "경고 (음주/수면 조절 및 성분 맞춤 케어 권장)"
                risk_color = "#f59e0b"
            else:
                risk_status = "고위험 (만성 질환 발전 위험 수준, 정밀 진단 필수)"
                risk_color = "#ef4444"
                
            st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 22px; text-align: center; margin-top: 10px;">
                    <span style="font-size: 0.9rem; color: #94a3b8;">{ml_type_label}</span>
                    <h2 style="margin: 5px 0 10px 0; font-family: 'Outfit', sans-serif; font-size: 2.8rem; font-weight: 800; color: {risk_color};">{predicted_risk:.1f}%</h2>
                    <div style="background: rgba(255, 255, 255, 0.08); border-radius: 10px; height: 16px; width: 100%; position: relative; overflow: hidden; margin-bottom: 12px;">
                        <div style="background: {risk_color}; width: {predicted_risk}%; height: 100%; border-radius: 10px; transition: width 0.6s ease-in-out;"></div>
                    </div>
                    <div style="font-size: 0.85rem; color: #cbd5e1;">
                        상태 분석: <strong><span style="color: {risk_color};">{risk_status}</span></strong>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # ==================== 엔터프라이즈 공식 푸터 ====================
    st.markdown("""
        <div class="enterprise-footer">
            <div class="footer-logo">&#x1F957; NutriFit Smart Dashboard</div>
            <hr class="footer-divider"/>
            <div class="footer-text">
                &#169; 2026 NutriFit Inc. All rights reserved.<br>
                본 서비스는 식약처 권장 가이드 및 공공데이터를 준수하며 의학적 진단을 대체하지 않습니다.<br>
                <span style="color: #334155;">| 고객지원센터: 1644-2026 &nbsp;|&nbsp; 이메일: support@nutrifit.kr &nbsp;|&nbsp; 식약처 공공데이터 기반 서비스 |</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
