# zebra-hust-template

华中科技大学课程报告与本科毕业设计的非官方 Typst 模板，提供封面、目录、页眉页脚、图表、代码块、参考文献和附录排版。

包含 `course-report` 和 `cs-thesis` 两种配置集，默认使用课程报告。

## 如何使用

需要 Typst 0.15.0 或更新版本，首次编译需要联网下载第三方依赖。

```bash
git clone https://github.com/Zebraine/zebra-hust-template.git
cd zebra-hust-template
make
```

输出为 `output.pdf`。修改时自动更新用 `make watch`，编译两种配置集的示例用 `make examples`。

没有 Make 也可以直接编译：

```bash
typst compile --font-path fonts main.typ output.pdf
typst compile --root . --font-path fonts examples/cs-thesis.typ examples/cs-thesis.pdf
```

## 如何编写

`main.typ` 顶部放基础配置，下方编写正文。默认配置无需展开，需要时修改 `report` 的参数：

```typ
#import "config.typ": report, references, appendix
#import "modules/figure_setup.typ": img

#show: report.with(
  preset: "course-report",
  cover: (
    title: [课程实验报告],
    name: [张三],
  ),
)
```

切换配置集可将 `preset` 改为 `"cs-thesis"`，摘要等配置参考 `examples/cs-thesis.typ`。课程报告标题手动编号，毕业设计标题自动编号。高级样式直接修改 `config.typ`，示例数据和文献请替换为自己的内容。

### 图片、参考文献与附录

图片和文献路径使用 `path(...)`，相对于编写这段代码的文件：

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

仓库在 `fonts/` 中内置 Fandol 宋体、黑体、楷体和 TeX Gyre Termes 开源字体，无需另外下载即可用于编译。

`make` 会自动加载内置字体；直接编译时传入 `--font-path fonts`，编辑器预览也需设置相同的字体路径。字体选择与优先级在 `config.typ` 的 `font_config` 中修改，如需固定使用内置字体，将对应字体名称设为 FandolSong、FandolHei、FandolKai 和 TeX Gyre Termes。

字体来源与许可见 [fonts/README.md](fonts/README.md)。

### 许可

项目代码与示例统一采用 [MIT 许可证](LICENSE)。第三方字体遵循各自附带的许可证，见 [fonts/README.md](fonts/README.md)。

第三方素材不包含在项目的 MIT 授权中：`images/go.png` 的 Go gopher 作者为 Renee French，使用遵循 [CC BY 4.0](https://go.dev/blog/gopher)；`images/HUSTGreen.svg` 的标识权利属于相应权利人，使用时遵守学校的[视觉标识规范](https://www.hust.edu.cn/xmxhxg.htm)，本项目不授予额外的标识使用权。

### 其他问题

有问题请提 issue，当然 PR 更好，毕竟我懒。
