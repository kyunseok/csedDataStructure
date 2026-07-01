import streamlit as st
from base_page import Page

class Week2Page(Page):
    def __init__(self):
        super().__init__("Week 2: Lists, Stacks, Queues", "📚")

    def render(self):
        st.title(f"{self.icon} {self.title}")
        st.markdown("---")
        
        # 탭을 이용한 서브 주제 분리 (우선 List부터 시작)
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
        st.header("선형 리스트 (Linear List)")
        st.write("리스트는 순서를 가진 원소들의 집합을 표현하는 가장 기본적인 추상 데이터 타입(ADT)입니다.")
        
        # 1. 기본 기능 ADT 소개
        st.subheader("1. 리스트의 주요 ADT 연산")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **`Insert(X, P)`**: 위치 `P`에 원소 `X`를 삽입합니다.
            - **`Delete(P)`**: 위치 `P`에 있는 원소를 삭제합니다.
            - **`Locate(X)`**: 원소 `X`가 위치한 인덱스나 포인터를 반환합니다.
            """)
        with col2:
            st.markdown("""
            - **`Next(P)`**: 현재 위치 `P` 다음의 위치를 반환합니다.
            - **`Previous(P)`**: 현재 위치 `P` 이전의 위치를 반환합니다.
            - **`Retrieve(P)`**: 위치 `P`에 있는 원소의 값을 읽습니다.
            """)
            
        st.markdown("---")
        
        # 2. 구현 방식 선택 및 개념 설명
        st.subheader("2. 리스트의 구현 방법 비교")
        impl_type = st.selectbox(
            "구현 방식을 선택하여 특징을 확인하세요:",
            ["Array-based (배열 기반)", "Pointer-based (포인터 기반)"]
        )
        
        if impl_type == "Array-based (배열 기반)":
            st.markdown("""
            ### 🔹 배열 기반 리스트 (Sequential List)
            - **특징**: 연속적인 메모리 공간에 데이터를 순차적으로 저장합니다.
            - **장점**: 인덱스를 통한 무작위 접근(`Retrieve`)이 $O(1)$로 매우 빠릅니다.
            - **단점**: 리스트 중간에 데이터를 삽입(`Insert`)하거나 삭제(`Delete`)할 때, 뒤에 있는 연속된 데이터들을 한 칸씩 이동시켜야 하므로 최악의 경우 $O(N)$의 비용이 발생합니다. 크기가 고정된다는 단점도 있습니다.
            """)
            
        else:
            st.markdown("""
            ### 🔹 포인터 기반 리스트 (Linked List)
            - **특징**: 데이터와 다음 노드를 가리키는 포인터를 포함하는 '노드(Node)'들이 연결된 형태입니다.
            - **장점**: 동적으로 크기를 조절할 수 있으며, 삽입/삭제할 위치의 포인터를 알고 있다면 주소 연결만 바꾸면 되므로 $O(1)$에 연산이 가능합니다.
            - **단점**: 특정 위치를 찾기 위해 헤드 노드부터 순차적으로 탐색해야 하므로 탐색(`Locate`) 비용이 $O(N)$입니다.
            """)
            
            st.markdown("#### 📍 탐색 포인터의 위치 지정 전략 2가지")
            pointer_strategy = st.radio(
                "포인터가 현재 위치를 가리키는 방식의 차이:",
                ["현재 위치 직접 지칭 (Current Pointer)", "현재 위치의 이전 위치 지칭 (Previous Pointer)"]
            )
            
            if pointer_strategy == "현재 위치 직접 지칭 (Current Pointer)":
                st.markdown("""
                - **개념**: `curr` 포인터가 작업 대상이 되는 노드를 **직접** 가리킵니다.
                - **특징**: 현재 노드의 데이터를 읽거나 탐색할 때는 직관적입니다.
                - **한계**: 단방향 연결 리스트(Singly Linked List)에서 현재 위치에 새로운 노드를 삽입하거나 현재 노드를 삭제하려면 **'이전 노드'의 포인터 링크를 수정**해야 합니다. 따라서 `Previous` 연산이 동반되거나 처음부터 다시 탐색해야 하는 비효율성이 존재합니다.
                """)
            else:
                st.markdown("""
                - **개념**: `curr` 포인터가 실제 작업 대상 노드의 **바로 직전(Previous) 노드**를 가리킵니다.
                - **특징**: 단방향 연결 리스트의 태생적 한계를 극복하기 위해 자주 쓰입니다. `curr`이 가리키는 노드의 `next` 공간을 대상으로 삽입/삭제를 수행하므로, 별도의 역방향 탐색 없이 즉시 링크 구조를 재조정할 수 있어 구현이 매우 매끄러워집니다. 보통 첫 번째 노드 처리를 쉽게 하기 위해 **더미 헤드 노드(Dummy Head Node)**와 함께 조합됩니다.
                """)
