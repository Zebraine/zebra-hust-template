# typst-template-hust

华中科技大学课程实验报告的 Typst 模板，是对 TeX 报告模板的简单重写，提供封面、目录、页眉页脚、图片题注、代码块和参考文献排版。

基础配置和正文集中在 `main.typ`，模板的高级设置放在 `config.typ`，文献数据使用独立的 `.bib` 文件。

## 项目结构

```text
.
├── main.typ                  # 唯一编译入口：顶部基础配置，下方正文
├── config.typ                # 模板高级配置与 report 组装函数
├── references.bib            # BibLaTeX 文献数据库
├── fonts/                    # 内置开源字体、许可及使用说明
├── Makefile                  # 自动传入字体目录的编译入口
├── output.pdf                # 示例 PDF / 编译输出
├── images/                   # 校徽和示例图片
└── modules/
    ├── page_settings.typ     # 页面设置
    ├── header.typ            # 页眉内容
    ├── cover.typ             # 封面
    ├── outline.typ           # 目录
    ├── figure_setup.typ      # 图片排版与辅助函数
    ├── code_setup.typ        # 代码块排版
    └── references.typ        # 原生 bibliography 的排版封装
```

## 快速开始

1. 修改 `main.typ` 顶部的封面、目录和参考文献配置。
2. 在同一文件的 `#show: report.with(...)` 下方编写正文。
3. 在 `references.bib` 中维护文献，正文中用 `@文献键` 引用。
4. 在项目根目录编译：

```bash
typst compile --font-path fonts main.typ output.pdf
```

`report` 自动按“封面 → 目录 → 正文 → 参考文献”组装文档，无需在正文末尾另加参考文献函数。

## main.typ：基础配置与正文

### 封面

修改文件顶部的 `cover_config`，所有字段都会传给 `cover-page`：

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

封面使用 `images/HUSTGreen.svg`。所有字段均可省略，但省略时会使用模块中的示例值，请在提交报告前完整填写。

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

### 正文与插图

基础配置后通过以下规则应用模板，后续内容就是正文：

```typst
#show: report.with(
  cover: cover_config,
  outline: outline_config,
  references: references_config,
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

`report(cover: (:), outline: (depth: 3, font_sizes: (12pt, 12pt, 12pt)), references: (:), body)` 是模板入口，接收三组基础配置和正文。通过 `#show: report.with(...)` 使用，`body` 由 Typst 自动传入。后续全局排版规则和模块组装可在此函数中扩展。

底层模块也可以单独导入使用；使用 `report` 时不需要重复应用它们：

| 函数 / 内容 | 用法与作用 |
| --- | --- |
| `page-setup(paper: "a4", margin: (top: 9.5em), header-font: "FandolKai", footer-font: "FandolSong", body)` | `#show: page-setup`，设置页面、页眉页脚。第一页不显示页眉页脚，第二个物理页起显示页码 `1`，目录计入页码。 |
| `figure_setup(font: "FandolHei", body)` | `#show: figure_setup`，设置图片编号与题注字体。 |
| `code_setup(body)` | `#show: code_setup`，初始化 `codly` 与语言配置。 |
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
