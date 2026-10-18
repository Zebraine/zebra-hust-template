#import "config.typ": report
#import "modules/figure_setup.typ": img

#let cover_config = (
  title: [文档标题],
  course: [课程名称],
  class: [班级名称],
  student-id: [学号],
  name: [作者姓名],
  teacher: [指导老师],
  report-date: [报告完成日期],
  college: [学院名称],
)

#let outline_config = (
  depth: 3,
  font_sizes: (12pt, 12pt, 12pt),
)

#let references_config = (
  source: "/references.bib",
  title: [参考文献],
  full: true,
)

#let appendices_config = (
  (
    body: [
      这里填写补充材料、实验数据或完整代码。
    ],
  ),
)

#show: report.with(
  cover: cover_config,
  outline: outline_config,
  references: references_config,
  appendices: appendices_config,
)

#align(center)[
  = 1. 图片示例
]

#img("../images/go.png", width: 20%, caption: "这是 Golang, 一个编程语言。")

== 1.1 子标题
123

图像识别相关研究见 @zhang2020，人工智能基础可参考 @zhao2019。

$limits(1) > 2$

= 2. 代码示例

```go
package main
import "fmt"
func main() {
    fmt.Println("Hello, World!")
}
```
