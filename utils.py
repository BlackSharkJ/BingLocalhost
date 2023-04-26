import html
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
# from typing import List, Tuple

from markdown import markdown
import mdtex2html


ALREADY_CONVERTED_MARK = "<!-- 已转换. -->"

# def postprocess(
#     self, y: List[Tuple[str | None, str | None]]
# ) -> List[Tuple[str | None, str | None]]:
def postprocess(self, y):
    if y is None or y == []:
        return []
    user, bot = y[-1]
    if user:
        if not detect_converted_mark(user):
            user = convert_asis(user)
    if bot:
        if not detect_converted_mark(bot):
            bot = convert_mdtext(bot)
    y[-1] = (user, bot)
    return y

def detect_converted_mark(userinput):
    if userinput.endswith(ALREADY_CONVERTED_MARK):
        return True
    else:
        return False

def convert_asis(userinput):
    return (
        f'<p style="white-space:pre-wrap;">{html.escape(userinput)}</p>'
        + ALREADY_CONVERTED_MARK
    )


def convert_mdtext(md_text):
    code_block_pattern = re.compile(r"```(.*?)(?:```|$)", re.DOTALL)
    inline_code_pattern = re.compile(r"`(.*?)`", re.DOTALL)
    code_blocks = code_block_pattern.findall(md_text)
    non_code_parts = code_block_pattern.split(md_text)[::2]

    result = []
    for non_code, code in zip(non_code_parts, code_blocks + [""]):
        if non_code.strip():
            non_code = normalize_markdown(non_code)
            if inline_code_pattern.search(non_code):
                result.append(markdown(non_code, extensions=["tables"]))
            else:
                result.append(mdtex2html.convert(non_code, extensions=["tables"]))
        if code.strip():
            # _, code = detect_language(code)  # 暂时去除代码高亮功能，因为在大段代码的情况下会出现问题
            # code = code.replace("\n\n", "\n") # 暂时去除代码中的空行，因为在大段代码的情况下会出现问题
            code = f"\n```{code}\n\n```"
            code = markdown_to_html_with_syntax_highlight(code)
            result.append(code)
    result = "".join(result)
    result += ALREADY_CONVERTED_MARK
    return result

def normalize_markdown(md_text: str) -> str:
    lines = md_text.split("\n")
    normalized_lines = []
    inside_list = False

    for i, line in enumerate(lines):
        if re.match(r"^(\d+\.|-|\*|\+)\s", line.strip()):
            if not inside_list and i > 0 and lines[i - 1].strip() != "":
                normalized_lines.append("")
            inside_list = True
            normalized_lines.append(line)
        elif inside_list and line.strip() == "":
            if i < len(lines) - 1 and not re.match(
                r"^(\d+\.|-|\*|\+)\s", lines[i + 1].strip()
            ):
                normalized_lines.append(line)
            continue
        else:
            inside_list = False
            normalized_lines.append(line)

    return "\n".join(normalized_lines)


def markdown_to_html_with_syntax_highlight(md_str):
    def replacer(match):
        lang = match.group(1) or "text"
        code = match.group(2)

        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ValueError:
            lexer = get_lexer_by_name("text", stripall=True)

        formatter = HtmlFormatter()
        highlighted_code = highlight(code, lexer, formatter)

        return f'<pre><code class="{lang}">{highlighted_code}</code></pre>'

    code_block_pattern = r"```(\w+)?\n([\s\S]+?)\n```"
    md_str = re.sub(code_block_pattern, replacer, md_str, flags=re.MULTILINE)

    html_str = markdown(md_str)
    return html_str
