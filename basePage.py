from abc import ABC, abstractmethod

class Page(ABC):
    def __init__(self, title, icon="📌"):
        self.title = title
        self.icon = icon

    @abstractmethod
    def render(self):
        """각 주차별 파일에서 이 메서드를 오버라이딩하여 시각화 UI를 구현합니다."""
        pass
