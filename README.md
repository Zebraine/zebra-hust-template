# typst-template-hust

华中科技大学课程实验报告的 Typst 模板，是对 TeX 报告模板的简单重写，提供封面、目录、页眉页脚、图片题注、代码块和参考文献排版。

默认使用 `course-report` 配置集。`main.typ` 顶部保留已注释的基础配置覆盖示例，下方编写正文；模板的高级设置放在 `config.typ`，文献数据使用独立的 `.bib` 文件。

## 项目结构

```text
.
├── main.typ                  # 唯一编译入口：顶部基础配置，下方正文
├── config.typ                # 模板高级配置与 report 组装函数
├── presets/
│   ├── course-report.typ     # 默认课程报告配置集
│   └── cs-thesis.typ         # 计算机学院本科毕业设计配置集
├── examples/                # 各配置集的示例源码与 PDF
│   ├── course-report.typ
│   ├── course-report.pdf
│   ├── cs-thesis.typ
│   └── cs-thesis.pdf
├── references.bib            # BibLaTeX 文献数据库
├── fonts/                    # 内置开源字体、许可及使用说明
├── Makefile                  # 自动传入字体目录的编译入口
├── output.pdf                # 示例 PDF / 编译输出
├── images/                   # 校徽和示例图片
└── modules/
    ├── page_settings.typ     # 页面设置
    ├── header.typ            # 页眉内容
    ├── cover.typ             # 课程报告 / 论文封面与共用字段标签
    ├── outline.typ           # 目录
    ├── figure_setup.typ      # 图片排版与辅助函数
    ├── code_setup.typ        # 代码块排版
    ├── references.typ        # 原生 bibliography 的排版封装
    ├── appendix.typ          # 自动编号的附录页
    └── thesis.typ            # 论文专用布局与前置页
```

## 快速开始

可先预览 [课程报告示例](examples/course-report.pdf) 和 [本科毕业设计示例](examples/cs-thesis.pdf)。对应 `.typ` 源码位于同一目录，在项目根目录执行 `make examples` 可重新生成两份 PDF。

1. 默认直接使用 `course-report` 配置集；需要自定义时，取消 `main.typ` 顶部配置和 `report.with` 中对应参数的注释，再修改字段。
2. 在同一文件的 `#show: report.with(...)` 下方编写正文。
3. 在 `references.bib` 中维护文献，正文中用 `@文献键` 引用。
4. 在项目根目录编译：

```bash
typst compile --font-path fonts main.typ output.pdf
```

默认 `course-report` 按“封面 → 目录 → 正文 → 参考文献 → 附录”组装文档；`cs-thesis` 还提供声明、中英文摘要和致谢。

## main.typ：基础配置与正文

### 配置集

当前默认配置集 `course-report` 保留原有封面占位信息、三级目录、完整文献列表及示例附录，定义在 `presets/course-report.typ`。

```typst
#show: report.with(preset: "course-report")
```

省略 `preset` 时也使用 `course-report`。`main.typ` 中原有四组配置及对应传参默认以 `/* ... */` 注释，不影响编译。自定义时取消两处注释，或直接在现有 `report.with` 中只写需要覆盖的字段：

```typst
#show: report.with(
  preset: "course-report",
  cover: (name: [张三], course: [数据结构实验]),
  references: (full: false,),
  appendices: (),
)
```

封面、目录、文献配置按字段覆盖配置集，未提供的字段保留默认值；附录数组整体替换，`auto` 表示沿用配置集，`()` 表示关闭附录。目录深度与字号数组仍需匹配。示例中的 `#show` 用于替换原有调用，不要重复应用模板。

新增配置集时，在 `presets/` 新建 `.typ` 文件并导出包含 `cover`、`outline`、`references`、`appendices` 的字典，然后在 `config.typ` 导入并注册到 `presets` 字典。通过 `preset: "配置集名称"` 选择；未知名称会报错。

### cs-thesis：本科毕业设计

该配置集参考 [HUST-CS-Thesis 的类文件](https://github.com/zeyuanyin/HUST-CS-Thesis/blob/main/HustGraduPaper.cls)及其 [sample.tex](https://github.com/zeyuanyin/HUST-CS-Thesis/blob/main/sample.tex)，采用独立论文布局，默认配置集仍为 `course-report`。

| 项目 | `cs-thesis` 行为 |
| --- | --- |
| 结构 | 封面 → 可选声明 → 中文摘要 → 英文摘要 → 目录 → 正文 → 可选致谢 → 参考文献 → 附录。 |
| 封面 | “本科生毕业设计”、论文题目、院系、专业班级、姓名、学号、指导教师和日期；不显示课程名称。 |
| 页面 | A4；左、右 1.25in，上 1.28in，下 1.06in。 |
| 页眉页脚 | 红色楷体“华中科技大学毕业设计”、蓝色双线，页码两侧有横线；封面和声明不显示页眉页码。 |
| 页码 | 摘要和目录使用 I、II、III；正文重新从 1 开始，目录链接和页码随之更新。 |
| 正文 | 小四（12pt）、两字首行缩进、两端对齐；Typst 行间距设为 `0.8em`。 |
| 标题 | 自动编号 1、1.1、1.1.1；一级居中、小二（18pt）、另起一页，二级四号（14pt）、三级小四（12pt）。 |
| 图表 | 按章重置，编号如“图 1-1”“表 2-1”，表题在上、图题在下。表格需包在 `figure(table(...), caption: ...)` 中。 |
| 目录 | 默认收录两级，与参考项目的示例一致；摘要、致谢、参考文献和附录也进入目录。 |
| 文献 | 默认使用内置 `gb-7714-2005-numeric`（上标引用），对应参考项目示例；可覆盖为 `gb-7714-2015-numeric`。 |
| 字体 | 使用本项目内置 Fandol / TeX Gyre Termes，无文字描边。 |

在 `main.typ` 中替换现有的 `#show: report.with(...)`：

```typst
#show: report.with(
  preset: "cs-thesis",
  cover: (
    title: [毕业设计题目],
    name: [张三],
    college: [计算机科学与技术学院],
  ),
  front-matter: (
    abstract-zh: [中文摘要正文。],
    keywords-zh: ("关键词一", "关键词二"),
    abstract-en: [English abstract.],
    keywords-en: ("keyword one", "keyword two"),
  ),
  acknowledgments: [致谢正文。],
  appendices: ((title: [实验数据], body: [补充材料。]),),
)

= 绪论

== 研究背景

正文内容。
```

切换时请删除原正文标题中手写的“1.”、“1.1”等编号，直接写 `= 绪论`、`== 研究背景`，避免重复编号。封面、目录、文献和 `front-matter` 均按字段覆盖。将 `abstract-zh` 或 `abstract-en` 设为 `none` 可隐藏对应摘要；关键词为字符串数组。`statement`、`acknowledgments` 默认为 `none`，传入内容即可启用，`auto` 沿用配置集。

声明内容由使用者提供，例如 `statement: [#include "/statement.typ"]`；这里不预填原创性或授权声明，也不自动填写签名。附录默认为空；如需“大学期间发表或提交的论文”，可作为一篇带标题的附录传入。

完整示例在 `examples/cs-thesis.typ`，从项目根目录编译：

```bash
typst compile --root . --font-path fonts examples/cs-thesis.typ examples/cs-thesis.pdf
```

`config.typ` 中的 `thesis_config` 控制论文页边距、行间距和标题字号；其中 `cover` 控制封面各区域距纸张顶部的目标位置、信息栏行距和区域最小间隔 `min-gap`。封面按 [参考项目 PDF 首页](https://www.overleaf.com/latex/templates/hust-cs-thesis/bsmgrypbwyxs.pdf) 调整校名、标题、信息栏和日期布局，字段标签两端对齐、下划线等长。长标题与长字段自动换行，后续区域按实际高度顺延；内容超过一页容量时会提示缩短内容或调整间距。`page_config` 继续用于课程报告。

实现上参考 [werifu/HUST-typst-template 的封面模块](https://github.com/werifu/HUST-typst-template/blob/main/pages/paper-cover.typ) 的顺序布局与信息栏组织方式，使用本项目 `modules/cover.typ` 中的 `thesis-cover` 和共用 `cover-label` 实现，保留已有字体、字号、目录、代码块、文献和附录工具，不引入该项目的伪粗体或其他依赖。其公开示例默认选择网安配置，本项目仍保持 `cs-thesis` 的计院封面比例。

这里移植的是参考项目的主要结构与排版约定；Typst 的行距模型、开源字体和 CSL 文献排版与 LaTeX 不完全相同，不保证逐像素复现，参考项目的专用算法、定理等 LaTeX 环境也未移植。

### 封面

取消注释后修改文件顶部的 `cover_config`，通过 `cover: cover_config` 覆盖配置集：

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

封面使用 `images/HUSTGreen.svg`。覆盖配置中省略的字段沿用配置集的值，请在提交报告前完整填写个人信息。

### 目录

```typst
#let outline_config = (
  depth: 3,
  font_sizes: (12pt, 12pt, 12pt),
)
```

`depth` 是收录的标题深度，`font_sizes` 是各层目录的字号，两者长度必须匹配。一级目录项加粗。单层目录的字号数组写作 `(12pt,)`。

### 参考文献

```typst
#let references_config = (
  source: "/references.bib",
  title: [参考文献],
  full: true,
)
```

| 参数 | 说明 |
| --- | --- |
| `source` | 文献数据库路径。推荐以 `/` 开头，表示相对于项目根目录，避免模块内部解析相对路径产生偏差。 |
| `title` | 文献页标题。 |
| `full` | `true` 列出数据库中的所有条目，保留原模板的完整列表行为；改为 `false` 则只列出正文引用的条目。 |

`references.bib` 使用 Typst 支持的 BibLaTeX 格式，例如：

```bibtex
@article{zhang2020,
  author = {{张三} and {李四} and {王五}},
  title = {深度学习在图像识别中的应用研究},
  journaltitle = {计算机学报},
  date = {2020},
  volume = {43},
  number = {6},
  pages = {1001--1015},
  langid = {chinese},
}
```

`zhang2020` 是唯一文献键。作者之间用 `and` 分隔，中文姓名用花括号保护；期刊可用 `@article`，专著用 `@book`，网页用 `@online`。网页条目可填写 `url` 和 `urldate`。

在正文中引用：

```typst
相关研究见 @zhang2020。
也可以显式调用 #cite(<zhang2020>)。
```

编号和参考文献列表由 Typst 联动生成，默认使用内置的 `gb-7714-2015-numeric` 样式，无需运行 BibTeX 或 Biber。更多字段和引用机制见 [Typst bibliography 文档](https://typst.app/docs/reference/model/bibliography/)。仓库内文献为演示数据，正式报告请替换为实际来源。

### 附录

在 `main.typ` 顶部的 `appendices_config` 中填写附录，按数组顺序自动生成“附录 A”“附录 B”…“附录 Z”标题。每篇附录另起一页，标题居中、黑体、小二（18pt），使用原生粗体，不添加描边，并自动收录进目录。

```typst
#let appendices_config = (
  (body: [第一篇附录内容。],),
  (
    title: [实验数据],
    body: [
      第二篇附录内容。

      == 数据说明

      这里可以插入表格、图片或代码。
    ],
  ),
)
```

每个字典的 `body` 是附录正文，`title` 可选：省略时仅显示“附录 A”，填写时显示“附录 B 实验数据”。单篇附录也要保留数组末尾的逗号；不需要附录时设为 `()`，不会产生空白附录页。超过 26 篇时按 Typst 字母编号继续为 AA、AB 等。附录内部小节从 `==` 开始，避免额外生成一级标题。

这一组织方式参照 [HUST-CS-Thesis 的附录设置](https://github.com/zeyuanyin/HUST-CS-Thesis/blob/main/HustGraduPaper.cls)。附录内容仍集中在 `main.typ`，通过 `report.with(appendices: appendices_config, ...)` 传入；附录标题字体和字号在 `config.typ` 的 `appendix_style` 中调整。

### 正文与插图

基础配置后通过以下规则应用模板，后续内容就是正文：

```typst
#show: report.with(
  cover: cover_config,
  outline: outline_config,
  references: references_config,
  appendices: appendices_config,
)

= 1. 实验结果

#img("/images/go.png", width: 40%, caption: [示例图片])

== 1.1 分析

正文内容。
```

`main.typ` 已导入 `img`。其签名为 `img(dir, width: 80%, caption: "这是 Go, 一个很好的编程语言。")`，第一个参数为图片路径。也可使用 `"../images/go.png"`，此时路径相对于函数所在的 `modules/figure_setup.typ`。

图片居中并显示“章节号.图片序号”。每个一级标题使章节号加一，图片序号全文连续、不按章节重置；一级标题之前的图片章节号为 `0`。标题未开启自动编号，需要时请手动填写。

代码块直接写语言名称即可：

````typst
```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```
````

## config.typ：高级模板配置

日常写报告无需修改此文件。需要调整模板时，可修改以下配置：

| 配置 | 默认值 | 用途 |
| --- | --- | --- |
| `page_config.paper` | `"a4"` | 纸张类型。 |
| `page_config.margin` | `(top: 9.5em)` | 页边距，可增加 `bottom`、`left`、`right` 等字段。 |
| `font_config` | 内置 Fandol 与 TeX Gyre Termes | 集中设置西文、宋体、黑体、楷体及封面字体。 |
| `page_config.header-font` / `footer-font` | 当前方案的楷体 / 封面字体 | 页眉与页码字体。 |
| `bibliography_config.style` | `"gb-7714-2015-numeric"` | 引用与文献列表样式。 |
| `bibliography_config.font` | 当前方案的西文 + 宋体 | 文献正文字体。 |
| `bibliography_config.title-font` | 当前方案的西文 + 黑体 | 文献标题字体。 |

`report(preset: "course-report", cover: (:), outline: (:), references: (:), appendices: auto, front-matter: (:), statement: auto, acknowledgments: auto, body)` 是模板入口。后三组前置页 / 致谢参数用于 `cs-thesis`；`body` 由 `#show: report.with(...)` 自动传入。配置集注册和全局排版规则均在此文件维护。

底层模块也可以单独导入使用；使用 `report` 时不需要重复应用它们：

| 函数 / 内容 | 用法与作用 |
| --- | --- |
| `page-setup(paper: "a4", margin: (top: 9.5em), header-font: "FandolKai", footer-font: "FandolSong", body)` | `#show: page-setup`，设置页面、页眉页脚。第一页不显示页眉页脚，第二个物理页起显示页码 `1`，目录计入页码。 |
| `figure_setup(font: "FandolHei", body)` | `#show: figure_setup`，设置图片编号与题注字体。 |
| `code_setup(body)` | `#show: code_setup`，初始化 `codly` 与语言配置。 |
| `appendix-pages(entries: (), font: ("TeX Gyre Termes", "FandolHei"), size: 18pt)` | `#appendix-pages(entries: appendices_config)`，按顺序生成独立附录页；空数组不输出内容。 |
| `cover-page(...)` | `#cover-page(..cover_config)`，生成封面并分页，参数对应封面字段，另接受 `font`、`title-font`，默认均为 `"FandolSong"`。 |
| `outline_with_sizes(depth: 3, font_sizes: (), font: "FandolSong", title-font: "FandolHei")` | `#outline_with_sizes(..outline_config)`，生成目录并分页；不可直接无参调用，字号数组长度必须等于深度。 |
| `references-page(...)` | `#references-page(..references_config)`，分页并输出文献；除基础参数外，支持 `style`、`font` 和 `title-font`，默认值同上表。 |
| `header_colorful` | `modules/header.typ` 中的内容值，不是函数；默认页眉为红色报告标题和蓝色双横线。 |

例如，独立输出文献页：

```typst
#import "modules/references.typ": references-page

#references-page(source: "/references.bib", full: false)
```

旧版的 `apply_cover()`、`apply_outline()`、`apply_references()` 和 `reference-item()` 已由 `report` 和原生文献系统替代；旧文献字典数组迁移至 `references.bib`。旧的 `output.typ` 与 `content.typ` 已合并为 `main.typ`。

## 编译环境

安装 Typst CLI 后，用 `typst --version` 检查。项目依赖 `@preview/pointless-size:0.1.2`、`@preview/zh-format:0.1.0`、`@preview/codly:1.3.0` 和 `@preview/codly-languages:0.1.10`，首次编译且本地未缓存时需要联网下载。

字体用途参照 [HUST-CS-Thesis](https://github.com/zeyuanyin/HUST-CS-Thesis/blob/main/HustGraduPaper.cls)，采用宋体正文、黑体标题与题注、楷体页眉。正文设为小四（12pt），目录条目使用宋体。

默认使用内置的 Fandol 宋体、黑体、楷体，以及 TeX Gyre Termes 西文字体，封面与页码使用 FandolSong。字体来源和使用说明见 [fonts/README.md](fonts/README.md)。高级字体配置统一位于 `config.typ` 的 `font_config`，无需修改 `main.typ`。

Typst 需要显式加载字体目录；运行 `typst fonts --font-path fonts` 检查。也可直接执行 `make` 编译、`make watch` 持续编译，Makefile 会自动传入 `--font-path fonts`。编辑器预览需配置相同的字体搜索目录。

在项目根目录执行：

```bash
typst compile --font-path fonts main.typ output.pdf
```

持续监听并编译：

```bash
typst watch --font-path fonts main.typ output.pdf
```

检查内置字体不依赖系统字体：

```bash
typst compile --font-path fonts --ignore-system-fonts main.typ output.pdf
```

## 许可证

模板代码使用 [MIT License](LICENSE)，`fonts/` 中的第三方字体分别遵循随附许可证。
