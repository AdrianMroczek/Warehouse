import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "test-results/videos/",
        "viewport": {"width": 1920, "height": 1080},
    }

@pytest.fixture(scope="function", autouse=True)
def auto_screenshot(page, request):
    yield
    page.screenshot(path=f"test-results/screenshots/{request.node.name}.png")