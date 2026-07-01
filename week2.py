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
        st.header("선형 리스트 (Linear List) 시각화 도구")
        st.write("버튼을 눌러 리스트의 상태를 변경하고, 내부 메모리 구조가 어떻게 변하는지 확인해 보세요.")
        
        # 1. Session State 초기화 (상태 유지를 위함)
        if 'list_data' not in st.session_state:
            st.session_state.list_data = [12, 45, 78]
        if 'curr_idx' not in st.session_state:
            st.session_state.curr_idx = 0

        # 2. 제어판 (Controls)
        st.markdown("### 🎛️ 리스트 컨트롤")
        col_btn1, col_btn2, col_input, col_btn3, col_btn4 = st.columns([1, 1, 2, 1, 1])
        
        with col_btn1:
            if st.button("⬅️ Previous"):
                st.session_state.curr_idx = max(0, st.session_state.curr_idx - 1)
        with col_btn2:
            if st.button("Next ➡️"):
                st.session_state.curr_idx = min(len(st.session_state.list_data) - 1, st.session_state.curr_idx + 1)
        
        with col_input:
            new_val = st.text_input("삽입할 값", value="99", label_visibility="collapsed")
        
        with col_btn3:
            if st.button("➕ Insert"):
                st.session_state.list_data.insert(st.session_state.curr_idx, new_val)
        with col_btn4:
            if st.button("🗑️ Delete") and st.session_state.list_data:
                st.session_state.list_data.pop(st.session_state.curr_idx)
                # 삭제 후 인덱스 초과 방지
                st.session_state.curr_idx = min(st.session_state.curr_idx, max(0, len(st.session_state.list_data) - 1))

        st.markdown("---")
        
        # 3. 구현 방식 선택 및 렌더링
        st.markdown("### 🖥️ 시각화 화면")
        impl_type = st.radio(
            "구현 방식을 선택하세요:",
            ["Array-based (배열 기반)", "Pointer-based (현재 위치 포인터)", "Pointer-based (이전 위치 포인터)"],
            horizontal=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)

        if impl_type == "Array-based (배열 기반)":
            self._draw_array(st.session_state.list_data, st.session_state.curr_idx)
        elif impl_type == "Pointer-based (현재 위치 포인터)":
            self._draw_linked_list(st.session_state.list_data, st.session_state.curr_idx, strategy="current")
        else:
            self._draw_linked_list(st.session_state.list_data, st.session_state.curr_idx, strategy="previous")

    def _draw_array(self, data, curr_idx):
        st.write("**[ 배열 메모리 구조 ]** - 연속된 메모리 공간에 할당됨")
        
        html = "<div style='display: flex; flex-wrap: wrap; gap: 4px; align-items: flex-end;'>"
        for i, val in enumerate(data):
            border_color = "#1E90FF" if i == curr_idx else "#555"
            bg_color = "#1E90FF33" if i == curr_idx else "transparent"
            marker = "<div style='text-align: center; color: #1E90FF; font-weight: bold; margin-bottom: 5px;'>curr &darr;</div>" if i == curr_idx else "<div style='height: 24px;'></div>"
            
            # 파이썬 코드의 들여쓰기가 HTML 문자열에 들어가지 않도록 라인별로 붙임
            html += "<div style='display: flex; flex-direction: column; align-items: center;'>"
            html += marker
            html += f"<div style='border: 2px solid {border_color}; background-color: {bg_color}; padding: 15px 20px; font-size: 20px; border-radius: 4px; color: white;'>{val}</div>"
            html += f"<div style='font-size: 12px; color: #aaa; margin-top: 5px;'>Index {i}</div>"
            html += "</div>"
            
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

    def _draw_linked_list(self, data, curr_idx, strategy):
        st.write(f"**[ 연결 리스트 구조 ]** - 포인터 전략: {strategy.capitalize()}")
        
        html = "<div style='display: flex; flex-wrap: wrap; gap: 15px; align-items: center; padding-top: 30px;'>"
        
        # Head 노드 (더미)
        head_marker = ""
        if strategy == "previous" and curr_idx == 0:
            head_marker = "<div style='position: absolute; top: -30px; left: 50%; transform: translateX(-50%); color: #FF4B4B; font-weight: bold;'>curr &darr;</div>"
            
        html += "<div style='position: relative; display: flex; align-items: center;'>"
        html += head_marker
        html += "<div style='background-color: #333; padding: 10px 15px; border-radius: 20px; border: 2px solid #555; color: white;'>Head</div>"
        html += "<div style='margin-left: 10px; color: #888;'>&rarr;</div>"
        html += "</div>"
        
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
            
            # 노드 렌더링
            html += "<div style='position: relative; display: flex; align-items: center;'>"
            html += marker
            html += f"<div style='display: flex; border: {highlight_border}; border-radius: 4px; overflow: hidden;'>"
            html += f"<div style='padding: 10px 15px; background-color: #262730; color: white;'>{val}</div>"
            html += "<div style='padding: 10px 10px; background-color: #444; border-left: 1px solid #555; color: #ccc;'>&bull;</div>"
            html += "</div>"
            html += "<div style='margin-left: 10px; color: #888;'>&rarr;</div>"
            html += "</div>"
            
        # NULL 끝부분
        html += "<div style='color: #aaa; font-weight: bold;'>NULL</div>"
        html += "</div>"
        
        st.markdown(html, unsafe_allow_html=True)
        
        st.info(f"💡 **현재 상태 분석:** `Insert`나 `Delete`를 누르면 " + 
                ("가리키는 노드 그 자체를 조작하기 때문에 단방향 링크에서는 이전 노드의 Next 주소를 변경하기 어렵습니다." if strategy == "current" else "`curr`이 가리키는 노드의 **Next** 공간에 접근하여 쉽게 새로운 노드를 연결하거나 삭제할 수 있습니다."))
