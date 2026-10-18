# zebra-hust

华中科技大学课程报告与本科毕业设计的非官方 Typst 模板，提供封面、目录、页眉页脚、图表、代码块、参考文献和附录排版。

包含 `course-report` 和 `cs-thesis` 两种配置集，默认使用课程报告。

## 如何使用

需要 Typst 0.15.0 或更新版本。

发布到 Typst Universe 后，或已在本地安装此包时，可以初始化项目：

```bash
typst init @preview/zebra-hust:0.1.0 my-report
cd my-report
typst compile main.typ
```

修改时自动更新：

```bash
typst watch main.typ
```

本科毕业设计示例使用 `typst compile cs-thesis.typ` 编译。初始化后的文件都可以直接修改，示例数据和文献请替换为自己的内容。

如果直接使用 GitHub 仓库源码，在仓库根目录执行 `make`、`make watch` 或 `make examples` 即可编译默认文档、监听修改或生成两种配置集的示例 PDF。

## 如何编写

`main.typ` 顶部放基础配置，下方编写正文。默认配置无需展开，需要时修改 `report` 的参数：

```typ
#import "@preview/zebra-hust:0.1.0": report, references, appendix, img

#show: report.with(
  preset: "course-report",
  cover: (
    title: [课程实验报告],
    name: [张三],
  ),
)
```

切换配置集可将 `preset` 改为 `"cs-thesis"`，摘要等配置参考随附的 `cs-thesis.typ`。课程报告标题手动编号，毕业设计标题自动编号。

### 图片、参考文献与附录

图片和文献路径使用 `path(...)`，确保读取当前项目中的文件：

```typ
#img(path("images/go.png"), width: 20%, caption: [示例图片])

相关研究见 @zhang2020。

#references(source: path("references.bib"))

#appendix(title: [补充材料])[
  这里填写附录正文。
]
```

文献使用 BibLaTeX 格式，按引用出现顺序编号。参考文献和附录放在哪里，就排在哪里；附录自动以 A、B、C……编号。表格写法参考默认示例。

### 字体问题

默认优先使用 Times New Roman、宋体（SimSun）、黑体（SimHei）、楷体（KaiTi）和华文中宋（STZhongsong），分别用于英文、正文、标题、页眉及封面与页码。不使用额外描粗。

缺少目标字体时，英文回退到 `Libertinus Serif`，中文回退到 `Noto Serif CJK SC` 或 `Noto Sans CJK SC`；替代字体的版式可能略有不同。

发布包不附带字体。请自行合法安装所需字体并遵守其使用与 PDF 嵌入许可，也可通过 `typst compile --font-path 字体目录 main.typ` 指定字体目录；网页端缺少字体时需自行上传有相应授权的字体。

仓库中的 `fonts/` 保留了其他开源字体，不是当前默认字体。需要进一步修改样式时，可在仓库源码的 `config.typ` 中调整 `font_config` 等配置；初始化的项目只包含正文示例，样式由包提供。

### 许可

模板库采用 MIT；`template/` 下的 Typst 正文与文献示例采用 MIT-0，正常修改后生成的文档无需保留软件署名。第三方素材不包含在这两项授权中：`template/images/go.png` 的 Go gopher 作者为 Renee French，使用遵循 [CC BY 4.0](https://go.dev/blog/gopher)；`images/HUSTGreen.svg` 的标识权利属于相应权利人，使用时遵守学校的[视觉标识规范](https://www.hust.edu.cn/xmxhxg.htm)，本项目不授予额外的标识使用权。

### 提交到 Universe

需要 Python 3.11+、Typst、jj 和已通过 `gh auth login` 登录的 GitHub CLI。

`make check-release` 打包、编译，并联网核对依赖版本和获取官方 PR 清单，不修改远端。确认源代码已用 jj 提交后，执行 `make submit-pr`，按提示审核清单、许可及文件差异，再分别确认推送和创建 PR。未经确认不会自动提交。

脚本读取 `typst.toml`，生成发布副本及 `pr-body.md`，不改动源文件。提交必须先由本地 jj 创建提交并推送 Fork，再验证远端提交与差异。网络失败即停止，不改用 API 创建提交。

运行目录保留在 `build/submit-*/`；已有版本或分支不会被覆盖。关闭过旧 PR 后重提，可通过 `python3 scripts/submit-pr.py --branch 新分支名` 指定新分支。SSH 连接可用 `--upstream-url git@github.com:typst/packages.git` 和 `GIT_SSH_COMMAND` 配置；首次克隆官方仓库可能较大。

### 其他问题

有问题请提 issue，当然 PR 更好，毕竟我懒。
