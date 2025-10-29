# Sub-agent Mode

子代理模式（Sub-agent Mode）是 MCP 框架中用于让各个工具（Tool）独立运行的小型智能代理机制。

它的核心思想是：
1. 每个工具对应一个独立子代理；
2. 主模型只发出 `instruction` 指令；
3. 子代理自动完成配置、依赖解析、执行，并返回结果。

这种机制可让 LLM 高效协调多个工具（如 Slack、Google Sheets、Linear）协作。
