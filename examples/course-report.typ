#import "/config.typ": report, references, appendix
#import "/modules/figure_setup.typ": img

#show: report.with(
  preset: "course-report",
  cover: (
    title: [课程实验报告],
    course: [程序设计实验],
    class: [计算机科学与技术 2401 班],
    student-id: [U2024xxxxx],
    name: [张三],
    teacher: [李四],
    report-date: [2026年10月18日],
    college: [计算机科学与技术学院],
  ),
)

= 1. 实验目的

通过程序设计实验，熟悉基本语法与输出操作。相关背景可参考 @zhao2019。

== 1.1 实验环境

使用 Go 编程语言完成本次实验。

#img(path("../images/go.png"), width: 20%, caption: [Go 语言示例图片])

= 2. 实验过程

编写并运行以下程序：

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

== 2.1 实验结果

程序输出 `Hello, World!`，实验完成。

#figure(
  table(
    columns: 3,
    inset: 8pt,
    stroke: none,
    table.hline(stroke: 0.8pt),
    table.header([*测试项*], [*预期输出*], [*结果*]),
    table.hline(stroke: 0.5pt),
    [编译], [无错误], [通过],
    [运行], [`Hello, World!`], [通过],
    table.hline(stroke: 0.8pt),
  ),
  supplement: [表],
  caption: [程序测试结果],
) <test-results>

测试结果见 @test-results。

#references(source: path("../references.bib"))

#appendix(title: [实验记录])[
  + 将代码保存为 `hello.go`。
  + 执行 `go run hello.go`。
  + 终端输出 `Hello, World!`，与预期一致。
]
