import pytest

from m6rclib.metaphor_lexer import MetaphorLexer
from m6rclib.metaphor_token import Token, TokenType

@pytest.fixture
def empty_lexer():
    return MetaphorLexer("", "test.txt")


@pytest.fixture
def basic_lexer():
    input_text = \
        "Role: TestRole\n" \
        "    This is a test role description\n" \
        "Context: TestContext\n" \
        "    This is a test context\n" \
        "    Context: Nested\n" \
        "        This is nested\n" \
        "Action: TestAction\n" \
        "    Do something\n"
    return MetaphorLexer(input_text, "test.txt")


def test_lexer_initialization(empty_lexer):
    """Test basic lexer initialization"""
    assert empty_lexer.filename == "test.txt"
    assert empty_lexer.in_text_block is False
    assert empty_lexer.indent_column == 1
    assert empty_lexer.current_line == 1


def test_empty_input_tokenization(empty_lexer):
    """Test tokenization of empty input"""
    token = empty_lexer.get_next_token()
    assert token.type == TokenType.END_OF_FILE


def test_comment_handling():
    """Test handling of comment lines"""
    lexer = MetaphorLexer("# This is a comment\nRole: Test", "test.txt")
    token = lexer.get_next_token()
    assert token.type == TokenType.ROLE
    assert token.value == "Role:"


def test_tab_character_handling():
    """Test handling of tab characters"""
    lexer = MetaphorLexer("\tRole: Test", "test.txt")
    token = lexer.get_next_token()
    assert token.type == TokenType.TAB
    token = lexer.get_next_token()
    assert token.type == TokenType.ROLE


def test_keyword_detection(basic_lexer):
    """Test detection of keywords"""
    tokens = []
    while True:
        token = basic_lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    keyword_tokens = [t for t in tokens if t.type in (TokenType.ROLE, TokenType.CONTEXT, TokenType.ACTION)]
    assert len(keyword_tokens) == 4  # 1 Role, 2 Context (one nested), 1 Action
    assert keyword_tokens[0].type == TokenType.ROLE
    assert keyword_tokens[1].type == TokenType.CONTEXT
    assert keyword_tokens[2].type == TokenType.CONTEXT  # Nested context
    assert keyword_tokens[3].type == TokenType.ACTION


def test_indentation_handling():
    """Test handling of indentation"""
    # All at same indentation level
    input_text = \
        "Role: Test\n" \
        "    First block\n" \
        "    Still first block\n" \
        "    Back at first\n"

    lexer = MetaphorLexer(input_text, "test.txt")
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    indent_tokens = [t for t in tokens if t.type == TokenType.INDENT]
    outdent_tokens = [t for t in tokens if t.type == TokenType.OUTDENT]

    # We expect one indentation level with multiple lines at that level
    assert len(indent_tokens) == 1
    assert indent_tokens[0].line == 2  # First indent
    assert len(outdent_tokens) == 1    # One outdent at the end

    # Check that all text tokens maintain the same indentation
    text_tokens = [t for t in tokens if t.type == TokenType.TEXT]
    assert all(t.column == text_tokens[0].column for t in text_tokens)

    # Test nested Context blocks which should show multiple indent levels
    nested_input = \
        "Context: Outer\n" \
        "    First level\n" \
        "Context: Inner\n" \
        "    Second level\n"

    lexer = MetaphorLexer(nested_input, "test.txt")
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    # For Context blocks, each new Context: creates its own indent level
    indent_tokens = [t for t in tokens if t.type == TokenType.INDENT]
    assert len(indent_tokens) == 2  # One for each Context block


def test_bad_indentation():
    """Test handling of incorrect indentation"""
    # 3 spaces instead of 4
    input_text = \
        "Role: Test\n" \
        "   Bad indent\n"

    lexer = MetaphorLexer(input_text, "test.txt")
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    bad_indent_tokens = [t for t in tokens if t.type == TokenType.BAD_INDENT]
    assert len(bad_indent_tokens) == 1
    assert bad_indent_tokens[0].column == 4


def test_bad_outdentation():
    """Test handling of incorrect outdentation"""
    # 5 spaces instead of 4 or 8
    input_text = \
        "Role: Test\n" \
        "        Double indented\n" \
        "     Bad outdent\n"

    lexer = MetaphorLexer(input_text, "test.txt")
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    bad_outdent_tokens = [t for t in tokens if t.type == TokenType.BAD_OUTDENT]
    assert len(bad_outdent_tokens) == 1
    assert bad_outdent_tokens[0].column == 6


def test_keyword_text_handling():
    """Test handling of text after keywords"""
    input_text = "Role: Test Description"
    lexer = MetaphorLexer(input_text, "test.txt")
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    assert tokens[0].type == TokenType.ROLE
    assert tokens[1].type == TokenType.KEYWORD_TEXT
    assert tokens[1].value == "Test Description"


def test_text_block_continuation():
    """Test handling of continued text blocks"""
    input_text = \
        "Role: Test\n" \
        "    First line\n" \
        "    Second line\n" \
        "    Third line\n"

    lexer = MetaphorLexer(input_text, "test.txt")
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    text_tokens = [t for t in tokens if t.type == TokenType.TEXT]
    assert len(text_tokens) == 3
    assert all(t.column == text_tokens[0].column for t in text_tokens)


def test_empty_lines():
    """Test handling of empty lines"""
    input_text = \
        "Role: Test\n" \
        "\n" \
        "    Text after empty line\n"

    lexer = MetaphorLexer(input_text, "test.txt")
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    text_tokens = [t for t in tokens if t.type == TokenType.TEXT]
    assert len(text_tokens) == 1
    assert text_tokens[0].value == "Text after empty line"


def test_mixed_content():
    """Test handling of mixed content types"""
    input_text = \
        "Role: Test\n" \
        "    Description\n" \
        "Context: First\n" \
        "    Some text\n" \
        "    Context: Nested\n" \
        "        \t\n" \
        "        Nested text\n" \
        "    Back to first\n" \
        "Action: Do\n" \
        "    Steps to take\n"

    lexer = MetaphorLexer(input_text, "test.txt")
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    # Verify token sequence
    token_types = [t.type for t in tokens if t.type not in (TokenType.INDENT, TokenType.OUTDENT)]
    assert TokenType.ROLE in token_types
    assert TokenType.CONTEXT in token_types
    assert TokenType.ACTION in token_types
    assert token_types.count(TokenType.TEXT) >= 4  # At least 4 text blocks


def test_fenced_code():
    """Test handling of fenced code"""
    input_text = \
        "Role: Test\n" \
        "    Description\n" \
        "Context: First\n" \
        "    Some text\n" \
        "    ```metaphor\n" \
        "    Context: Nested\n" \
        "        Nested text\n" \
        "    ```\n" \
        "    Back to first\n" \
        "Action: Do\n" \
        "    Steps to take\n"

    lexer = MetaphorLexer(input_text, "test.txt")
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END_OF_FILE:
            break

    # Verify token sequence
    token_types = [t.type for t in tokens if t.type not in (TokenType.INDENT, TokenType.OUTDENT)]
    assert TokenType.ROLE in token_types
    assert TokenType.CONTEXT in token_types
    assert TokenType.ACTION in token_types
    assert token_types.count(TokenType.TEXT) == 8
