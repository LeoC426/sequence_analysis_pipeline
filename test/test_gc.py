from src.main import gc_content

def test_gc_content():
    seq = "GGCC"
    assert gc_content(seq) == 100.0

def test_gc_content_zero():
    seq = "AAAA"
    assert gc_content(seq) == 0.0