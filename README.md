# typst-template-hust

华中科技大学课程实验报告的 Typst 模板，对陈加忠老师的 TeX 报告模板的简单重写。提供了封面、目录、页眉页脚、图片题注、代码块和参考文献排版。

## 项目结构

```text
.
├── output.typ                # 编译入口，组装各部分
├── content.typ               # 报告正文
├── config.typ                # 封面、目录、参考文献配置
├── output.pdf                # 仓库中的示例 PDF
├── images/                   # 校徽和示例图片
└── modules/
    ├── page_settings.typ     # 页面设置
    ├── header.typ            # 页眉内容
    ├── cover.typ             # 封面
    ├── outline.typ           # 目录
    ├── figure_setup.typ      # 图片排版与辅助函数
    ├── code_setup.typ        # 代码块排版
    └── references.typ        # 参考文献
```

## 开始

1. 修改 `config.typ` 中的 `cover_config`，填写标题、课程、班级、学号、姓名等信息。
2. 在 `content.typ` 中编写正文，将图片放入 `images/`。
3. 修改 `config.typ` 中的 `outline_config` 和 `references_config`，设置目录及参考文献。
4. 在项目根目录执行：

```bash
typst compile output.typ output.pdf
```

文档按“封面 → 目录 → 正文 → 参考文献”的顺序生成。通常只需编辑配置和正文，无需改动入口文件。

## 函数与配置

以下导入示例假设代码写在项目根目录的 `.typ` 文件中。`#show: ...` 用于应用排版规则，应放在需要排版的内容之前。

### 页面与代码排版

入口 `output.typ` 已应用以下三个函数：

```typst
#import "modules/page_settings.typ": page-setup
#import "modules/figure_setup.typ": figure_setup
#import "modules/code_setup.typ": code_setup

#show: page-setup
#show: figure_setup
#show: code_setup
```

| 函数 | 用途 |
| --- | --- |
| `page-setup(body)` | 设置 A4 纸张、顶部边距、页眉和页脚。第一页不显示页眉页脚，从第二个物理页起显示页码 `1`，因此目录也计入页码。 |
| `figure_setup(body)` | 为图片居中排版，并生成加粗的中文题注和“章节号.图片序号”编号。 |
| `code_setup(body)` | 初始化 `codly`，加载 `codly-languages` 的语言配置，为代码块提供排版。 |

这些函数接收后续文档内容 `body`，使用时通过 `#show` 传入即可。应用 `code_setup` 后，正文中可直接写带语言名称的代码块：

````typst
```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```
````

`modules/header.typ` 还提供 `header_colorful`，它是可复用的内容值，不是函数。默认页面设置已使用它，内容为红色报告标题和蓝色双横线；需要修改页眉时可编辑该模块。

### 封面：`cover-page`

推荐直接修改 `config.typ` 中的配置：

```typst
#let cover_config = (
  title: [课程实验报告],
  course: [数据结构实验],
  class: [计算机科学与技术 2401 班],
  student-id: [U2024xxxxx],
  name: [张三],
  teacher: [李四],
  report-date: [2026年10月18日],
  college: [计算机科学与技术学院],
)
```

`apply_cover()` 会将配置传给 `cover-page`。也可以绕过配置文件，直接调用：

```typst
#import "modules/cover.typ": cover-page

#cover-page(
  title: [课程实验报告],
  course: [数据结构实验],
  name: [张三],
)
```

全部参数均为可选的命名参数，名称与 `cover_config` 的字段一致。省略的参数使用 `modules/cover.typ` 中的示例值；提交报告前请检查并替换个人信息。封面使用 `images/HUSTGreen.svg`，末尾自动分页。

### 目录：`outline_with_sizes`

```typst
#import "modules/outline.typ": outline_with_sizes

#outline_with_sizes(
  depth: 3,
  font_sizes: (14pt, 12pt, 10pt),
)
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `depth` | `3` | 收录的标题层级深度。 |
| `font_sizes` | `()` | 各层级目录项的字号，长度必须等于 `depth`。 |

目录从正文标题自动生成，一级目录项加粗，末尾自动分页。由于默认字号数组为空，直接无参调用会触发断言；应同时提供匹配的深度和字号数组。仅设置一级目录时，使用 `(12pt,)` 表示单元素数组。

使用现有入口时，修改 `config.typ` 中的 `outline_config` 即可，`apply_outline()` 会读取它。

### 插图：`img`

```typst
#import "modules/figure_setup.typ": img

= 实验结果

#img("../images/go.png", width: 40%, caption: [示例图片])
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `dir` | 必填 | 图片路径，作为第一个位置参数传入。 |
| `width` | `80%` | 图片宽度。 |
| `caption` | `"这是 Go, 一个很好的编程语言。"` | 图片题注。 |

`img` 内部在 `modules/figure_setup.typ` 中调用 `image`，因此相对路径按该模块的位置解析。引用项目的 `images/go.png` 时使用 `"../images/go.png"`；也可使用相对于项目根目录的路径 `"/images/go.png"`。

配合 `figure_setup` 使用时，每遇到一个一级标题，章节计数加一。图片序号在全文中连续累加，不会在新章节重置，例如第一章有两张图片，第二章第一张图的编号为 `2.3`。一级标题之前插入的图片，其章节号为 `0`。

模板未开启标题自动编号。需要显示“1.”、“1.1”等编号时，可像现有 `content.typ` 一样手动写入标题。

### 参考文献：`references-page` 与 `reference-item`

`references-page(refs: (), title: "参考文献")` 会先分页，再输出标题和从 `1` 开始编号的文献列表：

```typst
#import "modules/references.typ": references-page

#references-page(
  title: "参考文献",
  refs: (
    (
      authors: ("张三", "李四"),
      title: "实验方法研究",
      doctype: "J",
      source: "某期刊",
      year: "2026",
      volume: "12",
      issue: "3",
      pages: "10-20",
    ),
    (
      authors: ("王五",),
      title: "在线实验指南",
      doctype: "EB/OL",
      source: "示例网站",
      year: "2026",
      url: "https://example.com/guide",
      date: "2026-10-18",
    ),
  ),
)
```

`refs` 为字典数组，每个字典支持以下字段：

| 字段 | 默认值 | 说明 |
| --- | --- | --- |
| `authors` | `()` | 作者数组，也接受字符串。超过三位作者时只显示前三位并加“等”。单作者数组写作 `("张三",)`。 |
| `title` | `""` | 文献标题。 |
| `doctype` | `"J"` | 类型标识，如 `J`（期刊）、`M`（专著）、`C`（会议论文）、`D`（学位论文）、`EB/OL`（网络资源）。 |
| `source` | `""` | 期刊、出版社或其他来源。 |
| `year` | `""` | 年份。 |
| `volume`、`issue`、`pages` | `none` | 可选的卷、期、页码。 |
| `url`、`date` | `none` | 可选的网址与访问日期；访问日期仅在提供网址时显示。 |

若只需输出单条文献，可调用 `reference-item`。它接受上述字段，但标题参数名为 `doc_title`，另有 `number` 参数（默认 `1`）：

```typst
#import "modules/references.typ": reference-item

#reference-item(
  number: 1,
  authors: ("张三",),
  doc_title: "实验方法研究",
  doctype: "J",
  source: "某期刊",
  year: "2026",
)
```

使用现有入口时，在 `config.typ` 的 `references_config` 中维护 `refs` 和 `title`，由 `apply_references()` 输出。此模块以 GB/T 7714 风格手工拼接条目，不提供文献数据库管理或正文引用联动。

### 配置包装函数

`config.typ` 导出三个无参函数，入口已按顺序调用：

```typst
#import "config.typ": apply_cover, apply_outline, apply_references

#apply_cover()
#apply_outline()
#include "content.typ"
#apply_references()
```

它们分别读取 `cover_config`、`outline_config`、`references_config`，调用对应模块。修改入口时，可按需调整这些部分的顺序或移除不需要的部分。

## 编译

### 环境与依赖

需要安装 Typst CLI，可通过 `typst --version` 检查是否可用。项目通过 `@preview` 引入以下固定版本的包，首次编译且本地未缓存时需要联网下载：

| 包 | 版本 |
| --- | --- |
| `pointless-size` | `0.1.2` |
| `zh-format` | `0.1.0` |
| `codly` | `1.3.0` |
| `codly-languages` | `0.1.10` |

模板显式使用 `HYFangSongJ`、`SimHei`、`SimSun` 字体，仓库不附带字体文件。请安装这些字体，或在模块中将字体名替换为本机可用字体。缺失字体时可能出现 `unknown font family` 警告和字体回退，影响最终排版。可用以下命令查看 Typst 识别到的字体：

```bash
typst fonts
```

### 一次编译与持续编译

在项目根目录执行一次编译：

```bash
typst compile output.typ output.pdf
```

写作时监听文件变化并自动重新生成 PDF：

```bash
typst watch output.typ output.pdf
```

如果字体未安装到系统，可指定字体目录：

```bash
typst compile --font-path /path/to/fonts output.typ output.pdf
```

请以 `output.typ` 为入口编译；单独编译 `content.typ` 不会应用入口中的页面、图片、代码样式，也不会包含封面、目录和参考文献。

## 许可证

本项目使用 [MIT License](LICENSE)。
