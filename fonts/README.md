# 项目字体

本目录内置兜底使用的开源字体，可在未安装中文系统字体的环境中编译。默认优先使用系统中的目标字体，其次使用开源替代字体；页眉缺少 KaiTi 时优先使用内置 FandolKai，保持楷体字形。字体配置统一位于 `config.typ` 的 `font_config`。

| 用途 | 内置字体 |
| --- | --- |
| 正文、目录条目、参考文献正文 | FandolSong |
| 标题、目录标题、图题 | FandolHei |
| 页眉 | FandolKai |
| 封面、页码 | FandolSong |
| 西文正文 | TeX Gyre Termes |

## 字体来源与许可

- `fandol/`：Fandol 0.3，作者 Clerk Ma、Jie Su；来自 [CTAN Fandol](https://ctan.org/pkg/fandol)。包含宋体、黑体的常规和粗体，以及楷体常规，共五个未修改的 OTF 文件。上游声明为 GPL + font exception，完整许可与声明保留在 `COPYING` 和 `README`。
- `tex-gyre-termes/`：TeX Gyre Termes 2.004，作者 Bogusław Jackowski、Janusz M. Nowacki；来自 [CTAN TeX Gyre](https://ctan.org/pkg/tex-gyre) 2.501 字体合集。包含常规、粗体、斜体、粗斜体四个未修改的 OTF 文件。保留 GUST Font License、上游说明和文件清单；本目录只收录该字体的 OpenType 子集。

字体分别遵循各自许可证，不适用项目代码的 MIT 许可证。数学和代码仍使用 Typst 自带的数学与等宽字体。

## 使用

在项目根目录执行 `make`，或：

```bash
typst compile --font-path fonts main.typ output.pdf
typst watch --font-path fonts main.typ output.pdf
```

Typst 不会因为存在 `fonts/` 就自动加载字体，必须传入 `--font-path fonts`（或设置 `TYPST_FONT_PATHS`）。编辑器预览也需要配置相同的字体搜索目录。

可运行 `typst fonts --font-path fonts` 检查已识别的字体。
