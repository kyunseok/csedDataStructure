import streamlit as st
from abc import ABC, abstractmethod

# ==========================================
# 1. Base Page Class (추상 클래스)
# 모든 주차별 페이지는 이 클래스를 상속받아 구현됩니다.
# ==========================================
class Page(ABC):
    def __init__(self, title, icon="📌"):
        self.title = title
        self.icon = icon

    @abstractmethod
    def render(self):
        """이 메서드 안에 각 페이지별 Streamlit UI 및 시각화 로직을 구현합니다."""
        pass


# ==========================================
# 2. Concrete Page Classes (각 주차별 구현)
# ==========================================
class Week1Page(Page):
    def __init__(self):
        super().__init__("Week 1: Algorithm Analysis", "⏱️")

    def render(self):
        st.title(f"{self.icon} {self.title}")
        st.markdown("---")
        st.subheader("Big-O 표기법 및 시간/공간 복잡도")
        st.write("여기에 입력 크기(N)에 따른 알고리즘 성능 그래프(선형, 로그, 지수 등)를 시각화하는 코드가 들어갑니다.")
        # 예시 컨트롤
        n_value = st.slider("데이터 크기 (N) 설정", 1, 100, 10)
        st.info(f"선택된 N = {n_value}. 추후 matplotlib이나 plotly를 연동하여 그래프를 렌더링하세요.")

class Week2Page(Page):
    def __init__(self):
        super().__init__("Week 2: Lists, Stacks, Queues", "📚")

    def render(self):
        st.title(f"{self.icon} {self.title}")
        st.markdown("---")
        st.subheader("선형 자료구조 시각화")
        st.write("Push/Pop, Enqueue/Dequeue 과정에서 메모리 배열이 어떻게 변하는지 애니메이션으로 보여줍니다.")

# 뼈대를 잡기 위한 임시 페이지 클래스 (아직 구현되지 않은 주차용)
class PlaceholderPage(Page):
    def __init__(self, week_num, topic, icon="🚧"):
        super().__init__(f"Week {week_num}: {topic}", icon)

    def render(self):
        st.title(f"{self.icon} {self.title}")
        st.markdown("---")
        st.info("현재 이 알고리즘의 시각화 모듈은 개발 중입니다.")


# ==========================================
# 3. Main Application Class
# 전체 사이트의 뼈대와 네비게이션을 담당합니다.
# ==========================================
class DataStructureVisualizerApp:
    def __init__(self):
        self._setup_page_config()
        self.pages = self._initialize_pages()

    def _setup_page_config(self):
        st.set_page_config(
            page_title="DS Algorithm Visualizer",
            page_icon="💻",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    def _initialize_pages(self):
        # 16주차 전체 커리큘럼 매핑 (추후 각각의 구현 클래스로 교체)
        return {
            "Week 1": Week1Page(),
            "Week 2": Week2Page(),
            "Week 3": PlaceholderPage(3, "Trees", "🌳"),
            "Week 4": PlaceholderPage(4, "Priority Queues & Heaps", "⏳"),
            "Week 5": PlaceholderPage(5, "Sorting", "🔄"),
            "Week 6": PlaceholderPage(6, "Binary Search Trees", "🌲"),
            "Week 7": PlaceholderPage(7, "AVL Trees-1", "⚖️"),
            "Week 8": PlaceholderPage(8, "AVL Trees-2", "⚖️"),
            "Week 9": PlaceholderPage(9, "2-3 Trees & B-Trees", "🗂️"),
            "Week 10": PlaceholderPage(10, "Dictionaries & Hashing", "📖"),
            "Week 11": PlaceholderPage(11, "Graph & Representations", "🕸️"),
            "Week 12": PlaceholderPage(12, "Graph Traversals", "🚶‍♂️"),
            "Week 13": PlaceholderPage(13, "Shortest Path Finding", "🗺️"),
            "Week 14": PlaceholderPage(14, "Minimum-Cost Spanning Trees", "🌉"),
            "Week 15": PlaceholderPage(15, "Tries", "🔤"),
            "Week 16": PlaceholderPage(16, "Expression Trees", "🧮"),
        }

    def _render_sidebar(self):
        st.sidebar.title("데이터 구조 커리큘럼")
        st.sidebar.markdown("---")
        
        # Selectbox나 Radio 버튼을 통해 네비게이션 구현
        page_names = list(self.pages.keys())
        
        # 사용자가 선택한 주차의 제목과 아이콘을 보기 좋게 포매팅
        selected_week = st.sidebar.radio(
            "학습할 주차를 선택하세요:",
            page_names,
            format_func=lambda x: f"{x}: {self.pages[x].title.split(': ')[-1]}" if ": " in self.pages[x].title else self.pages[x].title
        )
        
        st.sidebar.markdown("---")
        st.sidebar.caption("© 2026 CS Education Tool")
        
        return self.pages[selected_week]

    def run(self):
        # 1. 사이드바 렌더링 및 사용자가 선택한 페이지 객체 받아오기
        selected_page = self._render_sidebar()
        
        # 2. 선택된 페이지의 render() 메서드 실행 (다형성)
        selected_page.render()

# ==========================================
# Application Entry Point
# ==========================================
if __name__ == "__main__":
    app = DataStructureVisualizerApp()
    app.run()
