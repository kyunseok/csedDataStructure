import streamlit as st
import graphviz
import time
from abc import ABC, abstractmethod

class Page(ABC):
    @abstractmethod
    def render(self):
        pass

class Week2ListPage(Page):
    def __init__(self):
        # 상태 관리 초기화
        if 'array_data' not in st.session_state:
            st.session_state.array_data = ['a', 'b', 'c', 'd']
        if 'pointer_data' not in st.session_state:
            st.session_state.pointer_data = ['a', 'b', 'c', 'd']
        
        self.max_size = 8

    def render(self):
        st.header("Week 2: List Implementations")
        st.markdown("자료구조 **List**를 메모리 상에 구현하는 두 가지 주요 방식을 비교합니다. 각 방식의 동작 원리와 한계를 시각적으로 확인해 보세요.")
        st.divider()

        tab_array, tab_pointer = st.tabs(["📦 Array-Based Implementation", "🔗 Pointer-Based Implementation"])

        with tab_array:
            self.render_array_based()

        with tab_pointer:
            self.render_pointer_based()

    # ==========================================
    # HTML 렌더링 헬퍼 함수 (배열 그리기)
    # ==========================================
    def draw_array(self, current_data, highlight_idx=-1, action_type=""):
        html_code = "<div style='display: flex; flex-direction: row; align-items: center; gap: 0px; margin-top: 10px;'>"
        for i in range(self.max_size):
            if i < len(current_data):
                content = current_data[i]
                # 하이라이트 처리를 위한 색상 로직
                if i == highlight_idx:
                    bg_color = "#F56565" if action_type == "delete" else "#48BB78" # 삭제면 빨간색, 삽입/이동이면 초록색
                    border = f"border: 2px solid {bg_color};"
                else:
                    bg_color = "#3B82F6" 
                    border = "border: 2px solid #60A5FA;"
            else:
                content = "" 
                bg_color = "#1A202C" 
                border = "border: 2px dashed #4A5568;"
                
            html_code += f"""
                <div style='{border} background-color: {bg_color}; width: 60px; height: 60px; 
                            display: flex; justify-content: center; align-items: center; 
                            font-size: 24px; font-weight: bold; color: white;'>
                    {content}
                </div>
            """
        html_code += "</div>"
        
        html_code += "<div style='display: flex; flex-direction: row; gap: 0px; margin-top: 5px;'>"
        for i in range(self.max_size):
            label = str(i + 1) if i < self.max_size - 1 else "max"
            html_code += f"<div style='width: 60px; text-align: center; color: #A0AEC0; font-size: 14px;'>{label}</div>"
        html_code += "</div>"
        return html_code

    # ==========================================
    # 1. Array-Based List
    # ==========================================
    def render_array_based(self):
        st.subheader("Array-Based List")
        st.markdown("배열은 연속된 메모리 공간을 사용합니다. 삽입/삭제 시 빈 공간을 만들거나 채우기 위해 데이터의 **이동(Shifting)**이 발생합니다.")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            val_to_insert = st.text_input("삽입 데이터 (x)", value="x", max_chars=1, key="arr_val")
        with col2:
            insert_p = st.number_input("위치 (p)", min_value=1, max_value=len(st.session_state.array_data) + 1, value=3, key="arr_pos")
        
        # 애니메이션을 렌더링할 빈 컨테이너
        ui_container = st.empty()
        # 초기 상태 렌더링
        ui_container.markdown(self.draw_array(st.session_state.array_data), unsafe_allow_html=True)
        
        st.write("")
        col_btn1, col_btn2, _ = st.columns([1, 1, 2])
        
        # 삽입 애니메이션 로직
        if col_btn1.button("Insert(x, p, L)", key="arr_ins"):
            if len(st.session_state.array_data) >= self.max_size:
                st.error("Array가 가득 찼습니다! (최대 크기 도달)")
            else:
                target_idx = insert_p - 1
                temp_data = st.session_state.array_data.copy()
                temp_data.append("") # 임시 빈 공간 추가
                
                # 끝에서부터 타겟 인덱스까지 데이터를 한 칸씩 오른쪽으로 이동 (Shifting)
                for i in range(len(temp_data) - 1, target_idx, -1):
                    temp_data[i] = temp_data[i - 1]
                    temp_data[i - 1] = "" # 이전 자리를 비움
                    ui_container.markdown(self.draw_array(temp_data, highlight_idx=i, action_type="shift"), unsafe_allow_html=True)
                    time.sleep(0.5) # 이동 과정을 볼 수 있도록 0.5초 대기
                
                # 타겟 위치에 새로운 데이터 삽입
                temp_data[target_idx] = val_to_insert
                ui_container.markdown(self.draw_array(temp_data, highlight_idx=target_idx, action_type="insert"), unsafe_allow_html=True)
                
                st.session_state.array_data = temp_data
                st.rerun()

        # 삭제 애니메이션 로직
        if col_btn2.button("Delete(p, L)", type="primary", key="arr_del"):
            if len(st.session_state.array_data) > 0 and 1 <= insert_p <= len(st.session_state.array_data):
                target_idx = insert_p - 1
                temp_data = st.session_state.array_data.copy()
                
                # 삭제 대상 하이라이트
                ui_container.markdown(self.draw_array(temp_data, highlight_idx=target_idx, action_type="delete"), unsafe_allow_html=True)
                time.sleep(0.5)
                
                # 타겟 인덱스부터 끝까지 데이터를 한 칸씩 왼쪽으로 이동 (Shifting)
                for i in range(target_idx, len(temp_data) - 1):
                    temp_data[i] = temp_data[i + 1]
                    temp_data[i + 1] = ""
                    ui_container.markdown(self.draw_array(temp_data, highlight_idx=i, action_type="shift"), unsafe_allow_html=True)
                    time.sleep(0.5)
                
                temp_data.pop() # 마지막 빈 공간 제거
                st.session_state.array_data = temp_data
                st.rerun()

    # ==========================================
    # 2. Pointer-Based List
    # ==========================================
    def render_pointer_based(self):
        st.subheader("Pointer-Based List")
        st.markdown("포인터 기반 구현에서는 논리적 경계(Logical Fence)를 변수 `p`로 어떻게 가리킬 것인지가 핵심입니다.")
        
        # Pointer용 독립적인 데이터 제어
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            val_to_insert = st.text_input("삽입 데이터 (x)", value="y", max_chars=1, key="ptr_val")
        with col2:
            insert_p = st.number_input("위치 (p)", min_value=1, max_value=len(st.session_state.pointer_data) + 1, value=3, key="ptr_pos")
        with col3:
            st.write("")
            st.write("")
            if st.button("Insert(x, p, L)", key="ptr_ins"):
                st.session_state.pointer_data.insert(insert_p - 1, val_to_insert)
                st.rerun()
        with col4:
            st.write("")
            st.write("")
            if st.button("Delete(p, L)", type="primary", key="ptr_del"):
                if len(st.session_state.pointer_data) > 0 and 1 <= insert_p <= len(st.session_state.pointer_data):
                    st.session_state.pointer_data.pop(insert_p - 1)
                    st.rerun()

        st.divider()
        
        # UI: Logical Fence 조정 및 Option 선택
        col_slider, col_radio = st.columns([1, 1])
        with col_slider:
            fence_pos = st.slider(
                "📍 논리적 위치 (Logical Fence)", 
                min_value=0, max_value=len(st.session_state.pointer_data), value=2
            )
        with col_radio:
            pointer_option = st.radio(
                "포인터 p 설정 방식:",
                ("Option-1: 현재 요소(Current) 직접 지칭", "Option-2: 이전 요소(Previous) 지칭")
            )

        # Graphviz 시각화 로직
        dot = graphviz.Digraph(engine='dot')
        dot.attr(rankdir='LR', bgcolor='transparent', splines='ortho')
        dot.attr('node', shape='record', style='filled', fontname='Helvetica', color='black')

        data = st.session_state.pointer_data
        
        dot.node('L_ptr', 'L', shape='plaintext', fontcolor='white', fillcolor='transparent', fontsize='16')

        if not data:
            dot.node('null', 'null', shape='plaintext', fontcolor='#A0AEC0', fillcolor='transparent')
            dot.edge('L_ptr', 'null', color='white')
        else:
            prev_node = 'L_ptr'
            for i, val in enumerate(data):
                node_id = f'node_{i}'
                
                border_color = '#4A5568'
                fill_color = '#1A202C'
                
                if i == fence_pos - 1:
                    border_color = '#48BB78' # Previous Position (초록색)
                elif i == fence_pos:
                    border_color = '#F56565' # Current Position (빨간색)

                dot.node(node_id, f'<f0> {val} | <f1> ', color=border_color, fillcolor=fill_color, fontcolor='white', penwidth='2')
                dot.edge(prev_node if prev_node == 'L_ptr' else f'{prev_node}:f1', f'{node_id}:f0', color='white')
                prev_node = node_id
            
            dot.node('null', 'null', shape='plaintext', fontcolor='#A0AEC0', fillcolor='transparent')
            dot.edge(f'{prev_node}:f1', 'null', color='white')

            dot.node('p_ptr', 'p', shape='box', style='filled', fillcolor='#E2E8F0', fontcolor='black')
            
            if "Option-1" in pointer_option:
                target = f'node_{fence_pos}' if fence_pos < len(data) else 'null'
            else:
                target = f'node_{fence_pos - 1}' if fence_pos > 0 else 'L_ptr'
            
            dot.edge('p_ptr', target, color='#E2E8F0', style='dashed', penwidth='2')

        st.graphviz_chart(dot)

if __name__ == "__main__":
    st.set_page_config(page_title="Week 2: List Visualizer", layout="wide")
    page = Week2ListPage()
    page.render()
