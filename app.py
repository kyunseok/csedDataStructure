import streamlit as st
from abc import ABC, abstractmethod

# ==========================================
# 1. Page Interface (추상 클래스)
# ==========================================
class Page(ABC):
    @abstractmethod
    def render(self):
        """각 페이지의 UI와 시각화 로직을 렌더링하는 메서드"""
        pass

# ==========================================
# 2. 개별 주차 페이지 구현
# ==========================================
class Week1Page(Page):
    def render(self):
        st.header("Week 1: Algorithm Analysis")
        st.write("이곳에는 시간 복잡도(Time Complexity)와 공간 복잡도를 비교하는 그래프나 시각화 자료가 들어갈 예정입니다.")
        # 추후 matplotlib, plotly 등을 이용한 시각화 코드 추가

class Week2Page(Page):
    def render(self):
        st.header("Week 2: Lists, Stacks, Queues")
        st.write("스택(Stack)의 Push/Pop 및 큐(Queue)의 Enqueue/Dequeue 과정을 애니메이션 또는 단계별 상태로 시각화합니다.")
        
        # UI 레이아웃 예시 (컬럼 활용)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Stack")
            st.info("LIFO (Last In First Out) 구조")
        with col2:
            st.subheader("Queue")
            st.info("FIFO (First In First Out) 구조")

# 필요에 따라 Week3, Week4 등 16주차까지 클래스를 확장하여 생성합니다.
class PlaceholderPage(Page):
    def __init__(self, title):
        self.title = title

    def render(self):
        st.header(self.title)
        st.write(f"추후 구현될 {self.title} 시각화 페이지입니다.")

# ==========================================
# 3. Main Application Manager
# ==========================================
class VisualizerApp:
    def __init__(self):
        # 16주차 커리큘럼 라우팅 딕셔너리
        self.pages = {
            "Week 1: Algorithm Analysis": Week1Page(),
            "Week 2: Lists, Stacks, Queues": Week2Page(),
            "Week 3: Trees": PlaceholderPage("Week 3: Trees"),
            "Week 4: Priority Queues & Heaps": PlaceholderPage("Week 4: Priority Queues & Heaps"),
            "Week 5: Sorting": PlaceholderPage("Week 5: Sorting"),
            "Week 6: Binary Search Trees": PlaceholderPage("Week 6: Binary Search Trees"),
            # 7~16주차도 동일한 방식으로 연결 가능
        }

    def apply_theme(self):
        """검은색/파란색 테마를 위한 CSS 주입"""
        theme_css = """
        <style>
            /* 전체 배경을 어두운 검은색 계열로 설정 */
            .stApp {
                background-color: #0E1117;
                color: #E2E8F0;
            }
            /* 헤더 텍스트를 파란색 포인트 컬러로 설정 */
            h1, h2, h3 {
                color: #3B82F6 !important; 
            }
            /* 사이드바 색상 미세 조정 */
            [data-testid="stSidebar"] {
                background-color: #1A202C;
            }
        </style>
        """
        st.markdown(theme_css, unsafe_allow_html=True)

    def run(self):
        # 페이지 기본 설정
        st.set_page_config(
            page_title="Data Structures Visualizer", 
            page_icon="💻", 
            layout="wide"
        )
        
        # 테마 적용
        self.apply_theme()

        # 왼쪽 사이드바 UI
        st.sidebar.title("데이터구조 커리큘럼")
        st.sidebar.markdown("---")
        
        # 사용자가 선택한 탭(주차)
        selection = st.sidebar.radio("학습할 주차를 선택하세요:", list(self.pages.keys()))

        # 선택된 페이지 렌더링 (다형성 활용)
        page = self.pages[selection]
        page.render()

# ==========================================
# 4. 앱 실행
# ==========================================
if __name__ == "__main__":
    app = VisualizerApp()
    app.run()
