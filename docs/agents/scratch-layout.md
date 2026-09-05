# `.scratch/<story-id>/` 布局

story-level scratch 目录的固定结构，所有 `<story-id>` 子目录都遵循同一形状。

```
.scratch/<story-id>/
  issues/        # ticket 文件
  story          # 软链到 docs/features/<id>-feature-<slug>/story/<id>-story-<slug>.md
  spec.md        # 当前 story 的 spec
  pr/            # write-pr skill 的 PR body 草稿
  review/        # review-finding / review-what 产出
    from-<reviewer>.md
    from-<reviewer>-comment.md
  show-me/       # show-me skill 产出
```

`AGENTS.md` 不复述这套结构，仅保留指针。
