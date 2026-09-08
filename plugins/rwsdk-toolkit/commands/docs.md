---
description: Look up RedwoodSDK documentation for a specific topic
allowed-tools: Read, Glob, Grep
argument-hint: <topic>
---

Use the rwsdk-docs skill to answer this question.

Topic: $ARGUMENTS

Read the relevant reference file(s) from the rwsdk-docs skill based on the topic. Use the Documentation Index and Topic Quick-Lookup in the rwsdk-docs SKILL.md to find the right file, then read it and provide a clear, actionable answer with code examples.

Before answering, check `DOC-ACCURACY.md` in the rwsdk-docs skill. The references mirror the
official docs site, which lags the published `rwsdk` package: if that file covers the topic,
prefer it over the `.mdx` and tell the user which release changed things. Index rows marked ⚠
are the ones it contradicts or supplements.
