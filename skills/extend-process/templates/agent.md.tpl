---
name: <unique-name>
description: '<When the main session should hand work to this agent. One or two sentences.>'
tools: Read, Grep, Glob
model: sonnet
---

You are <role>. <One line on the job.>

## Context
Current state: <what exists today>
Target: <what it should become, or what to check against>

## Do
1.
2.

## Do not
- Edit files (unless the tools above include Edit or Write)
- Call other agents

## Return
<The exact shape of the answer: for example a short report with findings by severity.>
