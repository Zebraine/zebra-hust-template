# typst-template-hust

华中科技大学课程实验报告的 Typst 模板，提供封面、目录、页眉页脚、图片题注、代码块和参考文献排版。

包含课程报告(course-report)和本科毕业设计(cs-thesis)两种配置集，默认使用课程报告。

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

## 如何使用

首先确保已安装 Typst，推荐使用 [Typst Desktop](https://typst.app/download) 或 [Typst CLI](https://typst.app/docs/cli)。

使用默认配置编译：
```bash
make # 或 make build
```

默认输出 PDF 文件为 [output.pdf](output.pdf)。

修改时自动更新:
```bash
make watch
```

## 如何编写

入口是 [main.typ](main.typ)，顶部是基础配置，正文部分可以直接编写 Typst 语法。

如果使用默认配置，直接编写正文部分即可。
如果使用其他配置集，请在顶部取消注释并修改字段。

进一步的自定义可以在 [config.typ](config.typ) 中修改模板的高级配置。

### 参考文献与附录

参考文献写在 [references.bib](references.bib)，可使用 BibLaTeX 格式。

附录正文可以直接在 `#appendix[...]` 中编写，支持图片、表格和代码块。

### 字体问题

所有字体均为开源字体，已包含在 [fonts](fonts) 目录中。请勿删除或修改字体文件。

对于cs-thesis配置集，默认使用思源宋体作为正文字体，思源黑体作为标题字体。
若需要修改字体为Times New Roman或华文中宋，请在 [config.typ](config.typ) 中修改 `font-family` 配置。

### 其他问题

好像没有，如果有请提issue。
不过当然PR更好，毕竟我懒。