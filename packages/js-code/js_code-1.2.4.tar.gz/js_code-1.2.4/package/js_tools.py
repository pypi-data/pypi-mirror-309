import json
import subprocess
from functools import partial  # 锁定参数

# 防止乱码
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs


# 读取javascript 代码，执行js代码并返回 结果
def js_read(file: str = None, code: str = None, encoding="utf-8"):
    """
    读取并编译 JavaScript 代码。

    :param file: str, 可选参数。JavaScript 文件路径。
    :param code: str, 可选参数。需要添加在文件开头的 JavaScript 代码。
                 示例: code = "var a = 10;"
    :param encoding: str, 文件编码格式，默认为 "utf-8"。
    :return: execjs 编译后的 JavaScript 对象。
    """
    if not file and not code:
        raise ValueError("参数 `file` 和 `code` 至少需要提供一个。")

    try:
        # 如果提供了文件路径，读取文件内容
        if file:
            with open(file, mode="r", encoding=encoding) as f:
                file_content = f.read()
            js_code = code + '\n' + file_content if code else file_content
        else:
            # 仅使用提供的 `code`
            js_code = code
    except Exception as e:
        raise RuntimeError(f"无法读取文件或处理 JavaScript 代码: {e}") from e

    # 编译 JavaScript 代码
    return execjs.compile(js_code)


# 在控制台执行 js 代码 拿到控制台打印js结果 返回列表
def js_run(file: str, *args, split='\n', number=1):
    """
    使用 Python 调用 Node.js 执行 JavaScript 文件，并返回控制台输出的结果。

    :param file: str
        需要执行的 Node.js 文件的绝对路径。

    :param args: tuple
        传递给 Node.js 文件的参数，支持字符串、数字、字典、列表等。Python 中的列表和字典会被转换为 JavaScript 数组和对象。
        - 字符串和数字参数会直接传递给 Node.js。
        - 列表和字典会被转换为 JavaScript 中的数组和对象。

    :param split: str, optional
        用于分割输出的分隔符，默认为 `'\n'`。此参数指定如何分割 Node.js 的标准输出。若指定了其他分隔符，返回值将按该分隔符进行切割。

    :param number: int, optional
        控制返回值的段落。在分割输出后，使用该参数指定返回的段落索引。默认值 `1` 返回第二段。
        - `number` 为负数时，索引从输出的末尾开始计数。例如，`-1` 返回最后一段，`-2` 返回倒数第二段。
        - 如果 `number` 为正数，则返回按正序排序的对应段落。
        - 如果索引超出了分割后的段落范围，将返回完整的标准输出。

    :return: list or str
        - 如果使用默认的 `split='\n'`，返回控制台输出的每一行，作为一个列表。
        - 如果指定了自定义分隔符，返回按分隔符切割后的指定段落（由 `number` 决定）。

    :note:
        - 在 Node.js 中，通过 `process.argv.slice(2)` 获取传入的参数，Python 会将参数传递为 JSON 字符串。在 Node.js 中解析时，使用 `JSON.parse()` 将字符串转换为 JavaScript 数组或对象。
        - 例如，如果传入一个字符串 `args = 'hello'`，在 Node.js 中 `args[0]` 会是 `"hello"`。如果传入一个列表 `[1, 2, 3]`，则在 Node.js 中会解析为 `[1, 2, 3]`。
        - 在 Node.js 中，可以通过 `args = JSON.parse(args[0])` 来解析传递的 JSON 字符串。

    :example:
        Python 调用示例：
        ```python
        js_run('your_js_file.js', 'arg1', 'arg2', [1, 2, 3], {'key': 'value'})
        js_run('your_js_file.js', ['arg1', 'arg2', [1, 2, 3], {'key': 'value'}])
        ```
        在 JavaScript 中通过以下代码接收参数：
        ```javascript
        const args = JSON.parse(process.argv[2]);
        console.log(args[0]);  // 输出 'arg1'
        console.log(args[3].key);  // 输出 'value'
        ```

    """
    # 构造 Node.js 命令
    cmd = ['node', file]
    if args:
        # 将 Python 参数转换为 JSON 字符串并传递给 Node.js
        cmd.append(json.dumps(list(args), separators=(",", ":")))

    # 执行 Node.js 命令并捕获输出
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

    # 获取 Node.js 执行的标准输出
    stdout = result.stdout

    # 如果分隔符是换行符，返回按行分割的输出
    if split == '\n':
        return stdout.splitlines()

    # 使用自定义分隔符分割输出，并根据 `number` 返回指定的段落
    segments = stdout.split(split)
    return segments[number] if len(segments) > abs(number) else stdout
