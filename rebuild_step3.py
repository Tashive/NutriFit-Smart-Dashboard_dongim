"""
app.py Step3 비교보관함~끝(1405~1608행)을 올바른 들여쓰기로 재구성하는 스크립트.
- 1405~1608행을 새 블록으로 교체
- col_main 안: 비교보관함
- col_side 안: 어드민 인증 + CSV/PDF + 타임라인 가이드 (유틸리티 사이드카드)
- 그리드 바깥: 식약처 가이드 + 하단 버튼 + 엔터프라이즈 푸터
"""

with open('app.py', encoding='utf-8') as f:
    lines = f.readlines()

print(f"총 {len(lines)}줄")
print(f"1405: {repr(lines[1404][:60])}")
print(f"1608: {repr(lines[1607][:60])}")

new_block = '''\
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
                                        f\'<div style="background:rgba(251,191,36,0.1);border:1px solid rgba(251,191,36,0.3);border-radius:10px;padding:10px 12px;margin-top:10px;">\'
                                        f\'<div style="font-size:0.68rem;color:#fbbf24;font-weight:700;margin-bottom:4px;">📌 시장 내 대표 인기 제품</div>\'
                                        f\'<div style="font-size:0.78rem;color:#e2e8f0;font-weight:600;">{comp_mkt["brand"]} {comp_mkt["name"]}</div>\'
                                        f\'<div style="font-size:0.8rem;color:#34d399;font-weight:700;margin-top:2px;">{comp_mkt["price"]}</div>\'
                                        f\'<a href="{comp_mkt["url"]}" target="_blank" style="font-size:0.68rem;color:#60a5fa;text-decoration:none;">🔗 네이버쇼핑 바로가기 ↗</a>\'
                                        f\'</div>\'
                                    )
                                st.markdown(f"""
                                    <div style="background:rgba(30,41,59,0.55);border:2px solid #3b82f6;border-radius:20px;padding:20px;min-height:390px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 8px 24px rgba(59,130,246,0.15);">
                                        <div>
                                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                                                <span style="font-size:0.8rem;color:#60a5fa;background:rgba(59,130,246,0.15);padding:2px 8px;border-radius:6px;font-weight:700;">⚖️ 비교 {idx_c+1}</span>
                                                <span style="font-size:0.75rem;color:#94a3b8;">{comp_platform.upper()}</span>
                                            </div>
                                            <div style="font-size:0.78rem;color:#94a3b8;margin-bottom:2px;">{comp_brand}</div>
                                            <h4 style="margin:0 0 8px 0;color:#f8fafc;font-size:0.95rem;font-weight:700;height:38px;overflow:hidden;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;">{comp_name}</h4>
                                            <div style="font-size:1.18rem;font-weight:800;color:#10b981;margin-bottom:6px;">{comp_price_str}</div>
                                            <div style="font-size:0.82rem;color:#fbbf24;margin-bottom:10px;">⭐ {comp_rating:.1f} <span style="color:#64748b;">({comp_reviews:,}개 리뷰)</span></div>
                                            <div style="font-size:0.82rem;color:#cbd5e1;margin-bottom:8px;line-height:1.3;">🧬 <strong>표준성분:</strong> `{comp_std_ing}`</div>
                                            <hr style="border:0;border-top:1px solid rgba(255,255,255,0.06);margin:10px 0;"/>
                                            <div style="font-size:0.78rem;color:#cbd5e1;height:90px;overflow-y:auto;line-height:1.4;padding-right:4px;"><strong>📜 식약처 기능성:</strong> {comp_fn_desc}</div>
                                            {mkt_badge_html}
                                        </div>
                                        <a class="buy-btn" href="{primary_url}" target="_blank" style="background:linear-gradient(135deg,#3b82f6,#1d4ed8);margin-top:15px;">🛒 제품 상세 보기 ↗</a>
                                    </div>
                                """, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"비교 처리 중 오류: {e}")

            # ==================== 우측 유틸리티 사이드카드 (col_side) ====================
            with col_side:
                # --- 유틸 카드 1: 타임라인 가이드 ---
                st.markdown(\'<div class="side-section-label">⏰ AI 복용 골든타임</div>\', unsafe_allow_html=True)
                all_std_ings = "".join(recommendations.head(12)[\'표준성분\'].dropna().tolist())
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

                tl_html = \'\'
                tl_html += \'<div style="background:rgba(59,130,246,0.07);border:1px solid rgba(59,130,246,0.18);border-radius:12px;padding:12px 14px;margin-bottom:10px;">\'\
                           \'<div style="font-size:0.78rem;font-weight:700;color:#60a5fa;margin-bottom:6px;">🌅 아침 기상 공복</div>\'
                if morning_items:
                    for it in morning_items: tl_html += f\'<div style="font-size:0.75rem;color:#e2e8f0;margin-bottom:3px;">{it}</div>\'
                else:
                    tl_html += \'<div style="font-size:0.73rem;color:#94a3b8;">따뜻한 물 한 잔으로 시작하세요 🟢</div>\'
                tl_html += \'</div>\'
                tl_html += \'<div style="background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.18);border-radius:12px;padding:12px 14px;margin-bottom:10px;">\'\
                           \'<div style="font-size:0.78rem;font-weight:700;color:#34d399;margin-bottom:6px;">☀️ 점심/오후 식후</div>\'
                if lunch_items:
                    for it in lunch_items: tl_html += f\'<div style="font-size:0.75rem;color:#e2e8f0;margin-bottom:3px;">{it}</div>\'
                else:
                    tl_html += \'<div style="font-size:0.73rem;color:#94a3b8;">수분 보충을 충분히 해주세요 ☀️</div>\'
                tl_html += \'</div>\'
                tl_html += \'<div style="background:rgba(245,158,11,0.07);border:1px solid rgba(245,158,11,0.18);border-radius:12px;padding:12px 14px;">\'\
                           \'<div style="font-size:0.78rem;font-weight:700;color:#fbbf24;margin-bottom:6px;">🌙 저녁 취침 전</div>\'
                if night_items:
                    for it in night_items: tl_html += f\'<div style="font-size:0.75rem;color:#e2e8f0;margin-bottom:3px;">{it}</div>\'
                else:
                    tl_html += \'<div style="font-size:0.73rem;color:#94a3b8;">오늘의 영양제 섭취 완료! 숙면을 취하세요 🌙</div>\'
                tl_html += \'</div>\'
                st.markdown(f\'<div class="side-util-card">{tl_html}</div>\', unsafe_allow_html=True)

                # --- 유틸 카드 2: 내보내기 ---
                st.markdown(\'<div class="side-section-label">📥 데이터 내보내기</div>\', unsafe_allow_html=True)
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
            std_ing = str(selected_row.get(\'표준성분\', \'\'))
            st.info(f"📋 **선택 제품**: {selected_row.get(\'product_name\')}\\n\\n🧬 **검출 표준 성분**: `{std_ing}`")
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
                tabs_fs = st.tabs([f"🧪 {info[\'target_token\']}" for info in foodsafety_infos])
                for tab, info in zip(tabs_fs, foodsafety_infos):
                    with tab:
                        st.success(f"**식약처 공식 승인 명칭**: `{info[\'raw_material\']}`")
                        col_tab1, col_tab2 = st.columns(2)
                        with col_tab1:
                            st.markdown("#### 🎯 기능성 내용")
                            for line in info[\'functionality\'].split(\'\\n\'):
                                if line.strip(): st.write(f"- {line.strip()}")
                        with col_tab2:
                            st.markdown("#### 🥄 권장 일일섭취량")
                            st.info(info[\'daily_intake\'])
                            st.markdown("#### ⚠️ 섭취 시 주의사항")
                            st.warning(info[\'precautions\'])

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

'''

# 1405~1608행 (0-indexed: 1404~1607)을 new_block으로 교체
result = lines[:1404] + [new_block] + lines[1608:]

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(result)

print(f"완료: {len(result)}줄 저장")
