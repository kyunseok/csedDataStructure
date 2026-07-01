import streamlit as st
from basePage import Page

class Week2Page(Page):
    def __init__(self):
        super().__init__("Week 2: Lists, Stacks, Queues", "📚")

    def render(self):
        st.title(f"{self.icon} {self.title}")
        st.markdown("---")
        
        tab_list, tab_stack, tab_queue = st.tabs(["List (리스트)", "Stack (스택)", "Queue (큐)"])
        
        with tab_list:
            self._render_list_section()
            
        with tab_stack:
            st.subheader("Stack")
            st.info("추후 구현 예정 구역입니다.")
            
        with tab_queue:
            st.subheader("Queue")
            st.info("추후 구현 예정 구역입니다.")

    def _render_list_section(self):
        st.header("선형 리스트 (Linear List) 생성 및 시각화")
        
        # ==========================================
        # 🚨 [추가/수정된 부분] Session State 안전 초기화
        # 화면이 다시 그려질 때마다 변수가 없으면 기본값을 세팅합니다.
        # ==========================================
        if 'list_data' not in st.session_state:
            st.session_state.list_data = []
        if 'curr_idx' not in st.session_state:
            st.session_state.curr_idx = 0
        if 'array_capacity' not in st.session_state:
            st.session_state.array_capacity = 5  # 기본 Capacity 5로 설정
        
        # 1. 구현 방식 및 초기 설정 선택
        st.markdown("### 🛠️ 1단계: 리스트 구현 방식 선택 및 초기화")
        col_type, col_config = st.columns(2)
        
        with col_type:
            impl_type = st.radio(
                "구현 전략을 선택하세요:",
                ["Array-based (배열 기반)", "Pointer-based (현재 위치 포인터)", "Pointer-based (이전 위치/더미 헤드)"]
            )
            
        with col_config:
            if impl_type == "Array-based (배열 기반)":
                capacity = st.number_input("배열 최대 용량(Capacity) 설정", min_value=3, max_value=10, value=5)
                st.caption("⚠️ 배열은 생성 시점에 연속된 고정 크기 메모리를 미리 할당받습니다.")
            else:
                use_init = st.checkbox("샘플 데이터와 함께 생성하기", value=True)
                st.caption("⚠️ 연결 리스트는 동적으로 메모리를 할당하거나, 관리용 더미 노드를 만듭니다.")

        # ==========================================
        # 🚨 [수정된 부분] 새로 생성하기 버튼 로직 간소화
        # ==========================================
        if st.button("🔄 리스트 새로 생성하기 (Initialize)"):
            if impl_type == "Array-based (배열 기반)":
                st.session_state.list_data = [] # 실제 데이터는 비어있음
                st.session_state.array_capacity = capacity # 사용자가 입력한 capacity 저장
            else:
                st.session_state.list_data = [12, 45, 78] if use_init else []
            st.session_state.curr_idx = 0
            st.rerun() # 상태 업데이트 후 화면을 강제로 즉시 새로고침 (Streamlit 최신 권장)

        st.markdown("---")
        
        # 2. 제어 및 조작 판
        st.markdown("### 🎛️ 2단계: 리스트 조작 연산")
        col_btn1, col_btn2, col_input, col_btn3, col_btn4 = st.columns([1, 1, 2, 1, 1])
        
        data_len = len(st.session_state.list_data)
        
        with col_btn1:
            if st.button("⬅️ Previous"):
                st.session_state.curr_idx = max(0, st.session_state.curr_idx - 1)
        with col_btn2:
            if st.button("Next ➡️"):
                limit = data_len if impl_type == "Array-based (배열 기반)" else max(0, data_len - 1)
                st.session_state.curr_idx = min(limit, st.session_state.curr_idx + 1)
        
        with col_input:
            new_val = st.text_input("값 입력", value="99", label_visibility="collapsed")
        
        with col_btn3:
            if st.button("➕ Insert"):
                if impl_type == "Array-based (배열 기반)" and data_len >= st.session_state.array_capacity:
                    st.error("오버플로우! 배열 공간이 가득 찼습니다.")
                else:
                    st.session_state.list_data.insert(st.session_state.curr_idx, new_val)
                    
        with col_btn4:
            if st.button("🗑️ Delete") and st.session_state.list_data:
                # 배열 기반에서 인덱스가 마지막 빈 칸을 가리키고 있을 때 예외 처리
                if st.session_state.curr_idx < len(st.session_state.list_data):
                    st.session_state.list_data.pop(st.session_state.curr_idx)
                st.session_state.curr_idx = min(st.session_state.curr_idx, max(0, len(st.session_state.list_data) - 1))

        st.markdown("---")
        
        # 3. 상태 시각화 출력
        st.markdown("### 🖥️ 메모리 시각화 화면")
        
        # ==========================================
        # 🚨 [수정된 부분] 안전하게 array_capacity 호출
        # ==========================================
        if impl_type == "Array-based (배열 기반)":
            # Session State에서 capacity를 안전하게 가져옴
            safe_capacity = st.session_state.get('array_capacity', 5)
            self._draw_array(st.session_state.list_data, st.session_state.curr_idx, safe_capacity)
        elif impl_type == "Pointer-based (현재 위치 포인터)":
            self._draw_linked_list(st.session_state.list_data, st.session_state.curr_idx, strategy="current")
        else:
            self._draw_linked_list(st.session_state.list_data, st.session_state.curr_idx, strategy="previous")
    # ==========================================
    # HTML/CSS 기반 시각화 헬퍼 (들여쓰기 버그 완벽 제거)
    # ==========================================
    def _draw_array(self, data, curr_idx, capacity):
        st.write(f"**상태:** 현재 데이터 개수(Size) = {len(data)} / 할당된 용량(Capacity) = {capacity}")
        
        html = "<div style='display: flex; flex-wrap: wrap; gap: 6px; align-items: flex-end; padding-top: 20px;'> "
        for i in range(capacity):
            is_exist = i < len(data)
            val = data[i] if is_exist else "-"
            
            border_color = "#1E90FF" if i == curr_idx else ("#555" if is_exist else "#333")
            bg_color = "#1E90FF33" if i == curr_idx else ("transparent" if is_exist else "#111")
            text_color = "white" if is_exist else "#444"
            
            marker = "<div style='text-align: center; color: #1E90FF; font-weight: bold; margin-bottom: 5px;'>curr &darr;</div>" if i == curr_idx else "<div style='height: 24px;'></div>"
            
            html += "<div style='display: flex; flex-direction: column; align-items: center;'>"
            html += marker
            html += f"<div style='border: 2px solid {border_color}; background-color: {bg_color}; padding: 15px 20px; font-size: 20px; border-radius: 4px; color: {text_color}; min-width: 60px; text-align: center;'>{val}</div>"
            html += f"<div style='font-size: 12px; color: #aaa; margin-top: 5px;'>[{i}]</div>"
            html += "</div>"
            
        html += "</div>"
        st.html(html)

    def _draw_linked_list(self, data, curr_idx, strategy):
        html = "<div style='display: flex; flex-wrap: wrap; gap: 15px; align-items: center; padding-top: 30px;'>"
        
        # 1. Head 포인터 혹은 Dummy 노드 생성 표현
        if strategy == "current":
            # 일반 포인터 기반: Head 변수가 첫 노드를 바로 가리키거나 NULL을 가리킴
            head_border = "#1E90FF" if (not data and curr_idx == 0) else "#555"
            html += "<div style='display: flex; align-items: center;'>"
            html += f"<div style='background-color: #333; padding: 10px 15px; border-radius: 4px; border: 2px solid {head_border}; color: white;'>Head 변수</div>"
            html += "<div style='margin-left: 10px; color: #888;'>&rarr;</div>"
            html += "</div>"
        else:
            # 더미 헤드 기반: 데이터가 없어도 무조건 Dummy 노드가 메모리에 존재함
            show_head_curr = (curr_idx == 0)
            marker_color = "#FF4B4B"
            head_marker = f"<div style='position: absolute; top: -30px; left: 50%; transform: translateX(-50%); color: {marker_color}; font-weight: bold;'>curr &darr;</div>" if show_head_curr else ""
            highlight_border = f"2px solid {marker_color}" if show_head_curr else "1px solid #555"
            
            html += "<div style='position: relative; display: flex; align-items: center;'>"
            html += head_marker
            html += f"<div style='display: flex; border: {highlight_border}; border-radius: 4px; overflow: hidden;'>"
            html += "<div style='padding: 10px 15px; background-color: #1f242d; color: #666; font-style: italic;'>Dummy</div>"
            html += "<div style='padding: 10px 10px; background-color: #444; border-left: 1px solid #555; color: #ccc;'>&bull;</div>"
            html += "</div>"
            html += "<div style='margin-left: 10px; color: #888;'>&rarr;</div>"
            html += "</div>"
            
        # 2. 연결된 데이터 노드들 출력
        if not data:
            html += "<div style='color: #FF4B4B; font-weight: bold; padding: 10px;'>NULL (비어 있음)</div>"
        else:
            for i, val in enumerate(data):
                show_curr = False
                curr_color = "#1E90FF"
                
                if strategy == "current" and i == curr_idx:
                    show_curr = True
                elif strategy == "previous" and i == curr_idx - 1:
                    show_curr = True
                    curr_color = "#FF4B4B"
                    
                marker = f"<div style='position: absolute; top: -30px; left: 50%; transform: translateX(-50%); color: {curr_color}; font-weight: bold;'>curr &darr;</div>" if show_curr else ""
                highlight_border = f"2px solid {curr_color}" if show_curr else "1px solid #555"
                
                html += "<div style='position: relative; display: flex; align-items: center;'>"
                html += marker
                html += f"<div style='display: flex; border: {highlight_border}; border-radius: 4px; overflow: hidden;'>"
                html += f"<div style='padding: 10px 15px; background-color: #262730; color: white;'>{val}</div>"
                html += "<div style='padding: 10px 10px; background-color: #444; border-left: 1px solid #555; color: #ccc;'>&bull;</div>"
                html += "</div>"
                html += "<div style='margin-left: 10px; color: #888;'>&rarr;</div>"
                html += "</div>"
                
            html += "<div style='color: #aaa; font-weight: bold;'>NULL</div>"
            
        html += "</div>"
        st.html(html)
        
        # 교육용 핵심 피드백 가이드
        if not data:
            if strategy == "current":
                st.info("💡 **초기 생성 상태:** 현재 리스트가 완전히 비어 있어 `Head` 포인터가 아무것도 가리키지 않는 `NULL` 상태입니다.")
            else:
                st.info("💡 **초기 생성 상태:** 리스트가 비어 있지만, 기본 구조 유지를 위한 **Dummy 노드**가 메모리에 생성되어 있습니다. `curr` 포인터가 Dummy를 가리키므로, 첫 번째 요소를 삽입할 때 일반 노드와 동일한 코드로 처리할 수 있어 예외 처리가 줄어듭니다.")
