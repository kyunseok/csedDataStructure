import streamlit as st
import graphviz
from abc import ABC, abstractmethod

class Page(ABC):
    @abstractmethod
    def render(self):
        pass

class Week2ListPage(Page):
    def __init__(self):
        # 상태 관리 초기화
        if 'list_data' not in st.session_state:
            st.session_state.list_data = ['a', 'b', 'c', 'd']
        self.max_size = 8

    def render(self):
        st.header("Week 2: List Implementations")
        st.markdown("자료구조 **List**를 메모리 상에 구현하는 두 가지 주요 방식을 비교합니다. 하단의 탭을 통해 배열 기반과 포인터 기반 구현의 차이를 확인해 보세요.")
        
        st.divider()

        # 데이터 제어 패널
        st.subheader("데이터 삽입 / 삭제 제어")
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            val_to_insert = st.text_input("삽입할 데이터 (x)", value="x", max_chars=1)
        with col2:
            insert_p = st.number_input("삽입 위치 (p)", min_value=1, max_value=len(st.session_state.list_data) + 1, value=3)
        with col3:
            st.write("")
            st.write("")
            if st.button("Insert(x, p, L)", use_container_width=True):
                if len(st.session_state.list_data) < self.max_size:
                    st.session_state.list_data.insert(insert_p - 1, val_to_insert)
                    st.rerun()
                else:
                    st.error("Array가 가득 찼습니다!")
        with col4:
            st.write("")
            st.write("")
            if st.button("Delete(p, L)", type="primary", use_container_width=True):
                if len(st.session_state.list_data) > 0 and 1 <= insert_p <= len(st.session_state.list_data):
                    st.session_state.list_data.pop(insert_p - 1)
                    st.rerun()

        st.divider()

        # 1. 시각화 탭 구성
        tab_array, tab_pointer = st.tabs(["📦 Array-Based Implementation", "🔗 Pointer-Based Implementation"])

        with tab_array:
            self.render_array_based()

        with tab_pointer:
            self.render_pointer_based()

    # ==========================================
    # 1. Array-Based List
    # ==========================================
    def render_array_based(self):
        st.subheader("Array-Based List")
        st.markdown("배열은 연속된 메모리 공간을 사용합니다. 삽입/삭제 시 위치에 따라 데이터의 **이동(Shifting)**이 발생하여 $O(n)$의 시간 복잡도를 가집니다.")
        
        html_code = "<div style='display: flex; flex-direction: row; align-items: center; gap: 0px; margin-top: 20px;'>"
        for i in range(self.max_size):
            if i < len(st.session_state.list_data):
                content = st.session_state.list_data[i]
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
        html_code += "</div><br>"
        
        st.markdown(html_code, unsafe_allow_html=True)

    # ==========================================
    # 2. Pointer-Based List (Option 1 & 2)
    # ==========================================
    def render_pointer_based(self):
        st.subheader("Pointer-Based List")
        st.markdown("포인터 기반 구현에서는 논리적 경계(Logical Fence)를 변수 `p`로 어떻게 가리킬 것인지가 핵심입니다.")
        
        # UI: Logical Fence 조정 및 Option 선택
        col1, col2 = st.columns([1, 1])
        with col1:
            fence_pos = st.slider(
                "📍 논리적 위치 (Logical Fence)", 
                min_value=0, max_value=len(st.session_state.list_data), value=2,
                help="값이 2이면, 2번째와 3번째 원소 사이에 Fence가 있음을 의미합니다."
            )
        with col2:
            pointer_option = st.radio(
                "포인터 p 설정 방식:",
                ("Option-1: 현재 요소(Current) 직접 지칭", "Option-2: 이전 요소(Previous) 지칭 (One-step ahead)")
            )

        # 특징 설명 박스
        if "Option-1" in pointer_option:
            st.warning("**Option-1의 한계:** `p`가 현재 위치 요소(예: 'c')를 직접 가리킵니다. 이 경우 `Insert(x, p, L)`을 수행할 때, 그 이전 요소(예: 'b')의 `link`를 수정해야 하는데 이전 요소로 거슬러 올라가기가 매우 불편합니다.")
        else:
            st.success("**Option-2의 장점:** `p`가 현재 위치의 이전 요소(예: 'b')를 가리킵니다. 이를 **One-step ahead convention**이라 하며, 이전 노드의 `link`를 즉시 수정할 수 있어 삽입 연산 구현이 훨씬 직관적입니다.")

        # Graphviz 생성
        dot = graphviz.Digraph(engine='dot')
        dot.attr(rankdir='LR', bgcolor='transparent', splines='ortho')
        dot.attr('node', shape='record', style='filled', fontname='Helvetica', color='black')

        data = st.session_state.list_data
        
        # L 포인터
        dot.node('L_ptr', 'L', shape='plaintext', fontcolor='white', fillcolor='transparent', fontsize='16')

        if not data:
            dot.node('null', 'null', shape='plaintext', fontcolor='#A0AEC0', fillcolor='transparent')
            dot.edge('L_ptr', 'null', color='white')
        else:
            prev_node = 'L_ptr'
            for i, val in enumerate(data):
                node_id = f'node_{i}'
                
                # 시각적 피드백: 이전 노드는 초록색(Option 2 강조), 현재 노드는 빨간색(Option 1 강조) 테두리
                border_color = '#4A5568'
                fill_color = '#1A202C'
                
                if i == fence_pos - 1:
                    border_color = '#48BB78' # Green (Previous Position)
                elif i == fence_pos:
                    border_color = '#F56565' # Red (Current Position)

                dot.node(node_id, f'<f0> {val} | <f1> ', color=border_color, fillcolor=fill_color, fontcolor='white', penwidth='2')
                dot.edge(prev_node if prev_node == 'L_ptr' else f'{prev_node}:f1', f'{node_id}:f0', color='white')
                prev_node = node_id
            
            # 마지막 null 처리
            dot.node('null', 'null', shape='plaintext', fontcolor='#A0AEC0', fillcolor='transparent')
            dot.edge(f'{prev_node}:f1', 'null', color='white')

            # 포인터 p 그리기
            dot.node('p_ptr', 'p', shape='box', style='filled', fillcolor='#E2E8F0', fontcolor='black')
            
            if "Option-1" in pointer_option:
                target = f'node_{fence_pos}' if fence_pos < len(data) else 'null'
            else: # Option-2
                target = f'node_{fence_pos - 1}' if fence_pos > 0 else 'L_ptr'
            
            # p에서 타겟 노드로 향하는 점선 화살표
            dot.edge('p_ptr', target, color='#E2E8F0', style='dashed', penwidth='2')

        st.graphviz_chart(dot)

# 테스트용 단독 실행 코드
if __name__ == "__main__":
    st.set_page_config(page_title="Week 2: List Visualizer", layout="wide")
    page = Week2ListPage()
    page.render()
