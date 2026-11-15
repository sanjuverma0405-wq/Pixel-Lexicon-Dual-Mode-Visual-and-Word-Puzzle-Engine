import json
import urllib.request


class WordValidator:

  def __init__(self):
    # Core offline dictionary for instant lookups
    self.dictionary = {
        "cat",
        "dog",
        "pixel",
        "lexicon",
        "puzzle",
        "code",
        "engine",
        "python",
        "tkinter",
        "game",
        "desktop",
        "interface",
        "aesthetic",
        "cozy",
        "pastel",
        "matcha",
        "lavender",
        "cocoa",
        "board",
        "tile",
        "slide",
        "word",
        "search",
        "trie",
        "merge",
        "sort",
        "inversion",
        "solvable",
        "matrix",
        "binary",
        "bitmask",
        "data",
        "structure",
        "function",
        "class",
        "object",
        "render",
        "canvas",
        "button",
        "frame",
        "window",
        "app",
        "craft",
        "whimsical",
        "sparkle",
        "star",
        "flower",
        "leaf",
        "tea",
        "coffee",
        "sugar",
        "honey",
        "cookie",
        "cherry",
        "peach",
        "berry",
        "cloud",
        "breeze",
        "paper",
        "pen",
        "ink",
        "book",
        "library",
        "reader",
        "story",
        "magic",
        "test",
        "hello",
        "world",
    }

  def check_real_world_api(self, word: str) -> bool:
    """Queries a free public dictionary API to check if any real English word exists."""
    try:
      url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
      req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
      with urllib.request.urlopen(req, timeout=2) as response:
        if response.status == 200:
          data = json.loads(response.read().decode())
          return isinstance(data, list) and len(data) > 0
    except Exception:
      # If offline or request times out, it gracefully skips to returning False
      pass
    return False

  def check(self, word: str) -> bool:
    """Checks locally first, then falls back to the real-world dictionary API."""
    cleaned_word = word.strip().lower()
    if not cleaned_word:
      return False

    # 1. Check local offline set first
    if cleaned_word in self.dictionary:
      return True

    # 2. If not local, check live real-world dictionary API
    return self.check_real_world_api(cleaned_word)


# Standalone test when running this file directly
if __name__ == "__main__":
  validator = WordValidator()

  test_words = ["serendipity", "tcboooooo", "pixel", "mexl"]
  for w in test_words:
    result = validator.check(w)
    print(f"Word: '{w}' -> Real English Word? {result}")
