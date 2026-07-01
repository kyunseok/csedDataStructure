import streamlit as st
from base_page import Page

class Week1Page(Page):
    def __init__(self):
        super().__init__("Week 1: Algorithm Analysis", "⏱️")

    def render(self):
        st.title(f"{self.icon} {self.title}")
        st.markdown("---")
        st.header("알고리즘 분석 기초")
        st.write("알고리즘의 효율성을 평가하기 위해 시간 복잡도와 공간 복잡도를 분석합니다.")
        
        # 간단한 개념 소개 및 안내
        st.info("1주차 코드가 성공적으로 분리되어 로드되었습니다.")
