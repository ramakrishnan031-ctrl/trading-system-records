---
name: ""
metadata: 
  node_type: memory
  originSessionId: eb1e5157-79f2-4b1e-85be-8679efbceb60
---

When copying a script/file to the VM, do NOT pipe a heredoc into `ssh trading-vm 'cat > file'`. Even with a quoted `<<'EOF'` delimiter, one layer of backslash-escape processing halves `\\`→`\` in transit (observed 06-Jul: a Python regex `[^"\\]` arrived as `[^"\]` and crashed at import; single `\s` survived — only doubled backslashes collapsed), so any content with `\\`, regex, or escapes arrives corrupted and silently wrong.

**Why:** the failure is silent-until-runtime — the file looks fine, then a regex/parse crashes; worse, a crash mid-pipeline can leave a follow-on step operating on unmodified data.

**How to apply:** author the file locally (Write tool), then transfer byte-exact with base64:
`base64 -w0 "<local>" | ssh trading-vm 'base64 -d > <remote>'`
Then verify on the VM: `python3 -c "import ast; ast.parse(open('<remote>').read()); print('ok')"` + a self-test on FAKE data before running for real. Sibling escaping gotcha: [[feedback_vm_curl_tests]].
