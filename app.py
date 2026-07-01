import streamlit as st
# 각 주차별 모듈에서 페이지 클래스 로드
from week1 import Week1Page
from week2 import Week2Page

class DataStructureVisualizerApp:
    def __init__(self):
        self._setup_page_config()
        self.pages = self._initialize_pages()

    def _setup_page_config(self):
        st.set_page_config(
            page_title="자료구조 시각화 도구",
            page_icon="💻",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    def _initialize_pages(self):
        # 모듈화된 페이지 객체들을 딕셔너리로 관리
        return {
            "Week 1": Week1Page(),
            "Week 2": Week2Page(),
        }

    def _render_sidebar(self):
        st.sidebar.title("데이터 구조 커리큘럼")
        st.sidebar.markdown("---")
        
        page_names = list(self.pages.keys())
        selected_week = st.sidebar.radio(
            "학습할 주차를 선택하세요:",
            page_names,
            format_func=lambda x: f"{x}: {self.pages[x].title.split(': ')[-1]}"
        )
        
        st.sidebar.markdown("---")
        st.sidebar.caption("© 2026 자료구조 교육 보조도구")
        return self.pages[selected_week]

    def run(self):
        selected_page = self._render_sidebar()
        selected_page.render()

if __name__ == "__main__":
    app = DataStructureVisualizerApp()
    app.run()
