import streamlit as st
import graphviz
from abc import ABC, abstractmethod

# ==========================================
# Page Interface (기존 앱 구조와 호환)
# ==========================================
class Page(ABC):
    @abstractmethod
    def render(self):
        pass

# ==========================================
# Week 2: List Visualization Page
# ==========================================
class Week2ListPage(Page):
    def __init__(self):
        # 1. 상태 관리 초기화 (강의 슬라이드의 예시 데이터 <a, b, c, d> 사용) [cite: 94]
        if 'list_data' not in st.session_state:
            st.session_state.list_data = ['a', 'b', 'c', 'd']
        self.max_size = 8 # Array-Based 한계 시각화를 위한 최대 크기 설정

    def render(self):
        st.header("Week 2: List (배열 vs 포인터 구현)")
        st.markdown("자료구조 **List**는 유한하고 순서가 있는 원소들의 집합입니다 ($L=<a_1, a_2, ..., a_n>$)[cite: 23, 24]. 새로운 원소를 추가하거나 삭제할 때 내부 구조가 어떻게 변하는지 확인해 보세요.")
        
        st.divider()

        # 2. List Operations Control (Insert & Delete) [cite: 71]
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            val_to_insert = st.text_input("삽입할 데이터 (x)", value="x", max_chars=1)
        with col2:
            # Insert position parameter 'p' [cite: 72]
            insert_p = st.number_input("삽입 위치 (p)", min_value=1, max_value=len(st.session_state.list_data) + 1, value=3)
        with col3:
            st.write("") # 수직 정렬을 위한 여백
            st.write("")
            if st.button("Insert(x, p, L)", use_container_width=True):
                if len(st.session_state.list_data) < self.max_size:
                    st.session_state.list_data.insert(insert_p - 1, val_to_insert)
                    st.rerun()
                else:
                    st.error("Array가 가득 찼습니다 (Max Size 초과)!")
        
        with col4:
            st.write("") # 수직 정렬을 위한 여백
            st.write("")
            if st.button("Delete(p, L)", type="primary", use_container_width=True):
                if len(st.session_state.list_data) > 0 and 1 <= insert_p <= len(st.session_state.list_data):
                    st.session_state.list_data.pop(insert_p - 1)
                    st.rerun()
                else:
                    st.warning("유효하지 않은 삭제 위치입니다.")

        st.divider()

        # 3. 탭을 활용한 두 가지 구현 방식 동시 비교
        tab_array, tab_pointer = st.tabs(["1. Array-Based List", "2. Pointer-Based List"])

        with tab_array:
            self.render_array_based()

        with tab_pointer:
            self.render_pointer_based()

    # ==========================================
    # Array-Based List 시각화 (HTML/CSS 활용)
    # ==========================================
    def render_array_based(self):
        st.subheader("Array-Based List Implementation")
        st.markdown("배열 기반 구현에서는 원소를 삽입하거나 삭제할 때 위치에 따라 데이터의 **이동(Shifting)**이 발생하여 $O(n)$의 시간 복잡도를 가집니다[cite: 136, 138, 140]. 또한 `max` 크기가 고정되어 있습니다[cite: 95].")
        
        # HTML을 이용한 연속적인 메모리 블록(배열) 시각화
        html_code = f"<div style='display: flex; flex-direction: row; align-items: center; gap: 0px; margin-top: 20px;'>"
        
        for i in range(self.max_size):
            if i < len(st.session_state.list_data):
                content = st.session_state.list_data[i]
                bg_color = "#3B82F6" # 테마 포인트 컬러 (파란색)
                border = "border: 2px solid #60A5FA;"
            else:
                content = "" # 빈 공간
                bg_color = "#1A202C" # 빈 공간 어두운 색
                border = "border: 2px dashed #4A5568;"
                
            html_code += f"""
                <div style='{border} background-color: {bg_color}; width: 60px; height: 60px; 
                            display: flex; justify-content: center; align-items: center; 
                            font-size: 24px; font-weight: bold; color: white;'>
                    {content}
                </div>
            """
        html_code += "</div>"
        
        # 인덱스 라벨 (1, 2, 3, 4 ... max) [cite: 100]
        html_code += f"<div style='display: flex; flex-direction: row; gap: 0px; margin-top: 5px;'>"
        for i in range(self.max_size):
            label = str(i + 1) if i < self.max_size - 1 else "max"
            html_code += f"<div style='width: 60px; text-align: center; color: #A0AEC0; font-size: 14px;'>{label}</div>"
        html_code += "</div>"
        
        st.markdown(html_code, unsafe_allow_html=True)
        st.info(f"현재 Size: **{len(st.session_state.list_data)}** / {self.max_size}")

    # ==========================================
    # Pointer-Based List 시각화 (Graphviz 활용)
    # ==========================================
    def render_pointer_based(self):
        st.subheader("Pointer-Based List Implementation")
        st.markdown("포인터 기반 구현(Singly-Linked List)은 데이터를 포함하는 `info`와 다음 노드를 가리키는 `link`로 구성됩니다[cite: 146, 147, 152]. 삽입 시 리스트가 비어있거나 맨 앞부분을 다룰 때 발생하는 예외 처리를 피하기 위해 **Dummy Header** 노드를 사용하기도 합니다[cite: 205, 218].")
        
        use_dummy = st.checkbox("Dummy Header 노드 사용하기", value=False)
        
        # Graphviz 방향성 그래프 생성
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR', bgcolor='transparent') # 가로 방향 배치, 배경 투명화
        dot.attr('node', shape='record', style='filled', fillcolor='#1A202C', color='#3B82F6', fontcolor='white')
        dot.attr('edge', color='#60A5FA', penwidth='2')

        # 리스트 시작점(L) 포인터
        dot.node('L', 'L', shape='plaintext', fillcolor='transparent', fontcolor='white')

        data = st.session_state.list_data
        prev_node = 'L'

        # Dummy Header 로직 
        if use_dummy:
            dot.node('header', '{ <info> null | <link> }', fillcolor='#4A5568') # 더미 노드는 회색
            dot.edge(prev_node, 'header')
            prev_node = 'header'

        if not data:
            if not use_dummy:
                dot.node('null', 'null', shape='plaintext', fillcolor='transparent', fontcolor='#A0AEC0')
                dot.edge(prev_node, 'null')
        else:
            for i, val in enumerate(data):
                node_id = f'node_{i}'
                # 노드 구조: info | link (화살표 연결용 포트)
                dot.node(node_id, f'{{ <info> {val} | <link> }}')
                dot.edge(prev_node if prev_node == 'L' else f'{prev_node}:link', node_id)
                prev_node = node_id
            
            # 마지막 노드는 끝(null)을 가리킴
            dot.node('null', 'null', shape='plaintext', fillcolor='transparent', fontcolor='#A0AEC0')
            dot.edge(f'{prev_node}:link', 'null')

        # Streamlit에 그래프 렌더링
        st.graphviz_chart(dot)

# 테스트용 단독 실행 코드
if __name__ == "__main__":
    st.set_page_config(page_title="Week 2: List Visualizer", layout="wide")
    page = Week2ListPage()
    page.render()
