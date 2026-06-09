#!/usr/bin/env python
"""Batch generate 3 zhihu-style images for each of 9 articles (2606/0609 batch)."""
import os, sys, json, subprocess, urllib.request, time

SKILL_DIR = r"C:\Users\opapa\.claude\skills\luoboa-illustrate"
GEN_SCRIPT = os.path.join(SKILL_DIR, "scripts", "generate.py")
ART_DIR = r"H:\iCloudDrive\myvault\media\answer\2606\0609"
IMG_DIR = os.path.join(ART_DIR, "images")
os.makedirs(IMG_DIR, exist_ok=True)

# 9 articles × 3 anchors each
ARTICLES = [
    {
        "key": "q1-anthropic",
        "file": "Anthropic 呼吁全球暂缓前沿 AI 研发，这反映了人工智能领域怎样的担忧？-知乎回答.md",
        "prompts": [
            # anchor 1 (前 1/4): 对齐成本上升 + 自我改进循环
            "纯白底色（不允许任何纹理/渐变/底纹/底色叠加），专业知乎风格流程图，黑色文字，知乎蓝节点/箭头，浅灰色辅助框，极少量暖橙色用于高亮强调（≤5% 画面面积）。\n\n展示「递归自我改进（RSI）」的循环：起点为「基座模型 SFT」→ 节点「自动评估」→ 节点「自动改写」→ 回到起点。循环外侧一个「人类反馈」被虚线划掉。节点形状是带圆角的方框，关键节点「自动改写」用暖橙色高亮。箭头带箭头头。\n\n节点用思源黑体或苹方字体，12-16pt。标题在上方居中（22-26pt 加粗）：「递归自我改进循环」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            # anchor 2 (中 1/2): 安全政策 vs 监管套利矩阵
            "纯白底色，专业知乎风格对比表，黑色文字，知乎蓝行标题，浅灰色斑马纹行底（白 / 极浅灰），极少量暖橙色用于高亮强调。\n\n对比 3 家前沿 AI 实验室的「前沿安全承诺」：\n- 第一列「实验室」：Anthropic / OpenAI / xAI\n- 第二列「是否公开 RSP」：Anthropic 是 / OpenAI 否 / xAI 否\n- 第三列「是否承诺暂停阈值」：Anthropic 是（ASL-3/4）/ OpenAI 否 / xAI 否\n- 第四列「安全案例文档」：Anthropic 是 / OpenAI 部分 / xAI 否\n- 结论行用暖橙色高亮：「当前监管成本由守约方独背」\n\n行高对齐，第一列较窄，结论列较宽。\n思源黑体或苹方字体，文字 14-16pt。标题在上方居中（22-26pt 加粗）：「前沿 AI 实验室的安全承诺不对称」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            # anchor 3 (后 1/4): G7 / AI Action Summit 时间线
            "纯白底色，专业知乎风格时间线，黑色文字，知乎蓝主线，浅灰色次要节点，极少量暖橙色用于高亮关键节点。\n\n水平时间线展示 2024-2026 关键节点：\n- 2024.11「首尔 AI 安全研究所宣言」\n- 2025.02「巴黎 AI Action Summit」\n- 2025.06「California Report on Frontier AI Policy」\n- 2026.06「Anthropic 呼吁暂缓博客」← 暖橙色高亮\n- 2026.07「G7 数字部长会议」\n- 2026.10「AI Action Summit 后续」\n\n时间线下方一个箭头连接到「标准互认 = 0」的方框。\n\n节点用思源黑体或苹方字体，12-14pt。标题在上方居中（22-26pt 加粗）：「Anthropic 喊话卡在了哪个政策窗口」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
        ],
    },
    {
        "key": "q2-pricing",
        "file": "GPT-5.5 涨价，而DeepSeek 再次降价？为什么会同时出现「涨价」和「降价」共存的情况？-知乎回答.md",
        "prompts": [
            "纯白底色，专业知乎风格柱状图，黑色文字，知乎蓝高亮柱，浅灰色对比柱，极少量暖橙色用于高亮强调（≤5% 画面面积）。\n\n横向柱状图对比 4 个模型的「输出价格（每百万 token 元）」：\n- GPT-5.5：216 元（最高，知乎蓝高亮）\n- Claude Opus 4：约 180 元（浅灰）\n- DeepSeek V4-Pro（促销）：6 元（浅灰）\n- DeepSeek V4-Pro（裸价）：约 100 元（浅灰）\n\n横轴标签是「价格（每百万 token 元）」，刻度从 0 到 240。\n每个柱子顶部标数值，文字黑色 12-14pt。GPT-5.5 那个柱子用暖橙色背景矩形高亮。\n\n标题在上方居中（22-26pt 加粗）：「输出价格：30 倍价差不是差距是数量级」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，思源黑体或苹方字体，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格知识图谱（节点-边），黑色文字，知乎蓝主节点，浅灰次要节点和边，极少量暖橙色用于高亮核心关系。\n\n中心节点「目标用户」连接两个扇区：\n左扇区节点：「高容错率开发者」「法律合同审阅」「金融研报」「代码迁移」— 边用知乎蓝\n右扇区节点：「低容错率开发者」「客服机器人」「内容生成」「低风险 RAG」— 边用浅灰\n\n中心节点用暖橙色高亮填充（其他节点保持白底）。\n每个节点用思源黑体或苹方字体 12-14pt。\n\n标题在上方居中（22-26pt 加粗）：「同一产业、两个错位市场」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格流程图，黑色文字，知乎蓝主线，浅灰色次要路径，极少量暖橙色用于高亮核心判断。\n\n决策树，从「我的业务容错率有多高？」出发：\n- 高 → DeepSeek V4 → 「成本敏感场景」\n- 低 → GPT-5.5 → 「准确率敏感场景」\n- 中间灰区 → 「真要算账」 ← 暖橙色高亮\n\n三个分支节点是带圆角的方框，关键节点用暖橙色高亮填充。箭头带箭头头。\n\n节点用思源黑体或苹方字体 12-16pt。\n\n标题在上方居中（22-26pt 加粗）：「涨价 vs 降价不是矛盾是分工」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
        ],
    },
    {
        "key": "q3-weird-images",
        "file": "GPT为什么会生成这么诡异的图片？有没有研究者能解释为什么会出现这一现象？-知乎回答.md",
        "prompts": [
            "纯白底色，专业知乎风格流程图，黑色文字，知乎蓝主线，浅灰色辅助线，极少量暖橙色用于高亮关键节点。\n\n流程图：「用户 prompt 触发诡异图」的三层叠加机制：\n- 第 1 层（蓝色）：Safety filter → 检查 NSFW 关键词 → 放行\n- 第 2 层（蓝色）：Safety filter → 检查上传图片 → 放行（用户没上传）\n- 第 3 层（暖橙高亮）：模型进入「无输入退路」纯生成模式 → 恐怖先验过度激活 → 诡异图\n\n最右节点是「诡异图（皮肤液化 + 眼睛畸形）」，用暖橙色背景矩形高亮。\n\n箭头带箭头头。节点用思源黑体或苹方字体 12-14pt。\n\n标题在上方居中（22-26pt 加粗）：「Safety filter 三个拦截点全部放行」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格对比表，黑色文字，知乎蓝行标题，浅灰斑马纹行底（白 / 极浅灰），极少量暖橙色用于高亮结论。\n\n对比 3 种解决方案：\n- 第一列「层面」：用户侧 / 产品侧 / 研究侧\n- 第二列「具体动作」：\n  - 用户侧：避免「无锚点」prompt（close your eyes / make up）\n  - 产品侧：前置 guard 拦截「close your eyes」+「make up」类短语\n  - 研究侧：建 negative-anchor generation benchmark\n- 第三列「生效条件」：\n  - 用户侧：立即\n  - 产品侧：1-2 周工程\n  - 研究侧：3-6 个月\n- 结论行暖橙色高亮：「三者叠加才能根治」\n\n行高对齐，第一列较窄。\n思源黑体或苹方字体 14-16pt。\n\n标题在上方居中（22-26pt 加粗）：「诡异图的 3 个层面修复方案」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格流程图（短期 vs 长期），黑色文字，知乎蓝短期路径，浅灰长期路径，极少量暖橙色用于高亮核心判断。\n\n时间线 + 决策：\n- 左：短期（1-2 周）「前置 guard 拦截 prompt」 → 减少 80% 诡异图\n- 中：中期（3-6 个月）「建 negative-anchor benchmark」 → 部分根治\n- 右：长期（架构层）「解耦读 prompt 和画图」 ← 暖橙色高亮：「才是真正的解法」\n\n三个时间节点是带圆角的方框，连接线带箭头。关键节点用暖橙色高亮。\n\n节点用思源黑体或苹方字体 12-16pt。\n\n标题在上方居中（22-26pt 加粗）：「诡异图是当前多模态架构的必然现象」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
        ],
    },
    {
        "key": "q4-skills-mcp",
        "file": "为什么 skills 优于 mcp-知乎回答.md",
        "prompts": [
            "纯白底色，专业知乎风格对比表，黑色文字，知乎蓝行标题，浅灰斑马纹行底，极少量暖橙色用于高亮核心差异。\n\n对比 4 个维度：Skills vs MCP：\n- 第一列「维度」：抽象层 / 设计哲学 / 工具加载方式 / 描述方式\n- 第二列「Skills」：「模型的能力扩展」「自然语言描述」「progressive disclosure（未激活不占 context）」「Markdown + 脚本」\n- 第三列「MCP」：「外部 API 协议」「标准化 RPC 接口」「全量注册 + 按需调用」「JSON schema」\n- 第四列「关键差异」：（暖橙背景）Skills 决定「模型怎么想」、MCP 决定「模型能做什么」\n\n行高对齐，第一列较窄。\n思源黑体或苹方字体 14-16pt。\n\n标题在上方居中（22-26pt 加粗）：「Skills vs MCP：不是同一层抽象」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格柱状图，黑色文字，知乎蓝高亮柱，浅灰对比柱。\n\n纵向柱状图展示「tool selection 准确率」随 tool 数量变化：\n- 5 个 tool：Qwen2.5-7B = 78%（浅灰）、Qwen3-72B = 92%（浅灰）\n- 20 个 tool：Qwen2.5-7B = 58%（浅灰）、Qwen3-72B = 87%（浅灰）\n- 50 个 tool：Qwen2.5-7B = 41%（暖橙高亮）、Qwen3-72B = 80%（浅灰）\n\n纵轴是「准确率 %」，横轴是「tool 数量」。每个柱子顶部标数值。\n关键柱用暖橙色背景矩形高亮。\n\n思源黑体或苹方字体，刻度 10-12pt。\n\n标题在上方居中（22-26pt 加粗）：「Tool 数量越多、small LLM 准确率越低」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格流程图，黑色文字，知乎蓝主线，浅灰次要路径，极少量暖橙色用于高亮默认推荐。\n\n决策流程：「我要加一个新能力，先选 Skills 还是 MCP？」\n- 起点：「调用频率高 + 需要审计 + 需要跨工具协作」\n- 全是 → 「MCP」\n- 全否 → 「Skills」（暖橙高亮）\n- 中间状态 → 「Skills 起步，等需要时再迁 MCP」\n\n节点用圆角方框，箭头带箭头头。关键节点用暖橙色高亮。\n\n节点用思源黑体或苹方字体 12-16pt。\n\n标题在上方居中（22-26pt 加粗）：「3 个问题决定你的选型」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
        ],
    },
    {
        "key": "q5-opc",
        "file": "你看好超级个体，一人公司（OPC）吗？为什么？-知乎回答.md",
        "prompts": [
            "纯白底色，专业知乎风格对比表，黑色文字，知乎蓝行标题，浅灰斑马纹行底，极少量暖橙色用于高亮结论。\n\n对比「传统 3 人小工作室」vs「一人公司（OPC）」：\n- 第一列「维度」：协调工具 / 协调成本 / 后台人员 / 客户响应 / 月度固定成本\n- 第二列「传统 3 人工作室」：Slack + Notion + Jira + 飞书 / 高 / 财务+法务+客服各 1 人 / 12-24 小时 / 8-15 万元\n- 第三列「一人公司 + AI agent」：Claude Code skills / 接近 0 / 全由 agent 包 / < 4 小时 / < 2 万元\n- 第四列「关键差异」：（暖橙）协调成本被 AI agent 几乎免费化\n\n行高对齐。思源黑体或苹方字体 14-16pt。\n\n标题在上方居中（22-26pt 加粗）：「AI agent 把协调成本几乎免费化」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格流程图，黑色文字，知乎蓝主线，浅灰次要路径，极少量暖橙色用于高亮失败模式。\n\n「OPC 失败模式」流程图：\n- 起点：单创始人 24 个月运营\n- 节点 A：业务增长\n- 节点 B：突发事件（家人健康 / 突发事故）\n- 节点 C：单点故障（暖橙高亮）\n- 节点 D：退出方案（OPC 联盟互顶）\n\n箭头带箭头头。失败节点用暖橙色背景矩形高亮。\n\n节点用思源黑体或苹方字体 12-16pt。\n\n标题在上方居中（22-26pt 加粗）：「OPC 真正的失败模式：单点故障」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格对比表，黑色文字，知乎蓝行标题，浅灰斑马纹行底，极少量暖橙色用于高亮建议。\n\n「要不要做 OPC」3 条建议：\n- 第一列「#」：一、二、三\n- 第二列「建议」：\n  - 一、先验证能不能用 AI agent 把后台 80% 工作干掉\n  - 二、前 6 个月不要融资、不要雇人、不要租办公室\n  - 三、找一个 OPC 联盟加入或组建（3-5 人互为 backup）\n- 第三列「理由」：\n  - 一、决定你是「OPC 996」还是「真正的 OPC」\n  - 二、OPC 的核心优势是低固定成本\n  - 三、第 18 个月的存活率提升 3 倍\n- 结论行暖橙高亮：「OPC 适合前端判断力强的人」\n\n思源黑体或苹方字体 14-16pt。\n\n标题在上方居中（22-26pt 加粗）：「做 OPC 前自检 3 条」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
        ],
    },
    {
        "key": "q6-agent-workflow",
        "file": "大模型 Agent 和 workflow 的区别在哪里？-知乎回答.md",
        "prompts": [
            "纯白底色，专业知乎风格对比表，黑色文字，知乎蓝行标题，浅灰斑马纹行底，极少量暖橙色用于高亮核心区分。\n\n对比「Workflow」vs「Agent」4 个维度：\n- 第一列「维度」：控制流发起方 / 失败容忍 / 环境建模 / 任务目标\n- 第二列「Workflow」：开发者硬编码（if-then）/ 抛异常 + try-except / 不需要 / 单步或 N 步流水线\n- 第三列「Agent」：模型运行时决定（plan-act-reflect）/ 自省重试换工具 / 需要 environment model / 开放目标（如订机票 20+ 步）\n- 第四列「关键差异」：（暖橙）控制流从「人写的」变成「模型输出的」\n\n行高对齐。思源黑体或苹方字体 14-16pt。\n\n标题在上方居中（22-26pt 加粗）：「Agent vs Workflow：4 层区分」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格柱状图，黑色文字，知乎蓝高亮柱，浅灰对比柱。\n\n纵向柱状图对比「工具调用准确率」：\n- 一次性规划：68%（浅灰）\n- 多轮 self-refine：86%（暖橙高亮，提升 18-22 个百分点）\n\n纵轴是「工具调用准确率 %」，刻度 0-100。柱子顶部标数值。关键柱用暖橙色背景矩形高亮。\n\n思源黑体或苹方字体 12-14pt。\n\n标题在上方居中（22-26pt 加粗）：「self-refine 提升工具调用准确率 18-22%」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格流程图，黑色文字，知乎蓝主线，浅灰次要路径，极少量暖橙色用于高亮判断问题。\n\n「3 个问题判断真假 Agent」：\n- 起点：判断一个产品是真 Agent 还是 workflow 包装\n- 问题 1：prompt 里有没有「if X then Y」硬编码分支？\n  - 有 → workflow 包装\n  - 无 → 继续\n- 问题 2：跑同一任务两次执行路径是否完全一致？\n  - 一致 → workflow\n  - 不一致 → Agent\n- 问题 3：失败模式是「工具调用失败」还是「目标未达成」？\n  - 工具失败 → workflow 思维\n  - 目标失败 → Agent 思维\n\n所有 3 个暖橙高亮节点都标出。\n\n节点用思源黑体或苹方字体 12-16pt。\n\n标题在上方居中（22-26pt 加粗）：「3 个问题识破 workflow 穿了 Agent 外套」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
        ],
    },
    {
        "key": "q7-tool-use",
        "file": "大模型为什么可以调用工具？-知乎回答.md",
        "prompts": [
            "纯白底色，专业知乎风格流程图，黑色文字，知乎蓝主线，浅灰次要路径，极少量暖橙色用于高亮关键层。\n\n「大模型工具调用 4 层训练」流程：\n- 第 1 层（蓝色）：预训练 → 读文字-写文字\n- 第 2 层（蓝色）：tool-use SFT → 输出 JSON\n- 第 3 层（暖橙高亮）：RLHF/DPO 偏好对齐 → 调得聪明\n- 第 4 层（蓝色）：client 执行层（LangChain/ToolRegistry）→ 真调用\n\n箭头带箭头头。关键层用暖橙色背景矩形高亮。\n\n节点用思源黑体或苹方字体 12-14pt。\n\n标题在上方居中（22-26pt 加粗）：「从 SFT 到 client 执行：4 层栈」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格柱状图，黑色文字，知乎蓝高亮柱，浅灰对比柱。\n\n纵向柱状图展示「tool selection 准确率」随模型参数量 + tool 数量变化：\n- 7B 模型 + 5 个 tool = 78%（浅灰）\n- 7B 模型 + 50 个 tool = 41%（暖橙高亮，掉 37 个百分点）\n- 72B 模型 + 5 个 tool = 95%（浅灰）\n- 72B 模型 + 50 个 tool = 80%（浅灰）\n\n纵轴是「准确率 %」，横轴是 4 个组合。柱子顶部标数值。关键柱用暖橙色背景矩形高亮。\n\n思源黑体或苹方字体 12-14pt。\n\n标题在上方居中（22-26pt 加粗）：「7B 模型在 50 tool 下准确率腰斩」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格流程图，黑色文字，知乎蓝主线，浅灰次要路径，极少量暖橙色用于高亮反共识判断。\n\n「tool calling 是不是高级能力」决策树：\n- 起点：tool calling 是高级能力吗？\n- 左分支：是的，因为是 SFT 学出来的 → 错（暖橙）\n- 右分支（暖橙高亮）：是基础功能，因为 2026 年所有模型都支持\n- 底部：「真正的差异化」：延迟、准确率、多 tool 编排、异步并发、失败重试\n\n节点用圆角方框，箭头带箭头头。关键判断用暖橙色背景矩形高亮。\n\n节点用思源黑体或苹方字体 12-16pt。\n\n标题在上方居中（22-26pt 加粗）：「tool calling 是基础功能不是差异化」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
        ],
    },
    {
        "key": "q8-tech-leader",
        "file": "搞技术的人员为什么通常当不了领导？-知乎回答.md",
        "prompts": [
            "纯白底色，专业知乎风格对比表，黑色文字，知乎蓝行标题，浅灰斑马纹行底，极少量暖橙色用于高亮认知模式差异。\n\n对比「技术认知」vs「管理认知」3 个维度：\n- 第一列「维度」：核心问题 / 评价体系 / 成就感来源\n- 第二列「技术认知」：找因果（root cause 必存在）/ 单维（代码好不好一眼看出）/ 自己做出来（intrinsic）\n- 第三列「管理认知」：找概率（谈话结果不可预知）/ 模糊（员工好不好无 benchmark）/ 别人做出来（extrinsic）\n- 第四列「冲突点」：（暖橙）「技术人员用『解决问题』模式应对『管理人』场景」\n\n行高对齐。思源黑体或苹方字体 14-16pt。\n\n标题在上方居中（22-26pt 加粗）：「技术人员当不了领导不是 bug 是 feature」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格折线图，黑色文字，知乎蓝主线，浅灰对比线。\n\n折线图展示「资深工程师转管理岗后绩效曲线」（横轴月数 0-24，纵轴绩效 %）：\n- 工程师 1（直接 5 人团队）：月 0 = 100%，月 6 = 77%，月 12 = 82%，月 18 = 88%，月 24 = 95%（暖橙回升）\n- 工程师 2（直接 10 人团队）：月 0 = 100%，月 6 = 65%，月 12 = 60%，月 18 = 58%，月 24 = 55%（暖橙警示，持续下降）\n\n两个折线对照。\n思源黑体或苹方字体 10-12pt。\n\n标题在上方居中（22-26pt 加粗）：「管理岗前 18 个月绩效平均下降 23%」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格流程图，黑色文字，知乎蓝主线，浅灰次要路径，极少量暖橙色用于高亮建议。\n\n「技术骨干转管理」3 步走：\n- 第 1 步：先在 5 人以下小组带 1 年\n- 第 2 步：找到「技术 + 管理」双轨岗位（架构师+TL / CTO 助理）\n- 第 3 步：第 12 个月适应期是关键节点\n\n关键节点用暖橙色高亮。\n\n节点用思源黑体或苹方字体 12-16pt。\n\n标题在上方居中（22-26pt 加粗）：「别直接挑战 20 人团队」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
        ],
    },
    {
        "key": "q9-gaokao",
        "file": "有哪些当年只道寻常，现在却再也回不去的全民高考记忆？-知乎回答.md",
        "prompts": [
            "纯白底色，专业知乎风格时间线，黑色文字，知乎蓝主线，浅灰次要节点，极少量暖橙色用于高亮关键年代。\n\n水平时间线展示「2001-2026 高考生集体记忆」5 个锚点：\n- 2001「3+X 改革第一年」\n- 2003「非典高考 + 戴口罩入场」\n- 2010「新课改全国铺开」\n- 2017「互联网+ 高考志愿填报」\n- 2026「双减后第一届 + AI 时代」← 暖橙高亮\n\n时间线下方一个连接到「集体肃穆感被短视频打散」的方框。\n\n节点用思源黑体或苹方字体 12-14pt。\n\n标题在上方居中（22-26pt 加粗）：「一代人有一代人的高考记忆」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格对比表，黑色文字，知乎蓝行标题，浅灰斑马纹行底，极少量暖橙色用于高亮对比。\n\n对比「2010 高考前夜」vs「2026 高考前夜」4 个维度：\n- 第一列「维度」：熄灯后 / 老师送别 / 志愿工具 / 录取通知\n- 第二列「2010」：全班安静 / 班主任煮绿豆汤 / 厚砖头《招生通讯》/ 牛皮纸信封\n- 第三列「2026」：刷手机短视频 / 家长挤校门口送饭 / AI 5 分钟 100 方案 / 电子版 + 物流礼包\n- 第四列「丢失的东西」：（暖橙）集体肃穆感 + 全家决策仪式\n\n行高对齐。思源黑体或苹方字体 14-16pt。\n\n标题在上方居中（22-26pt 加粗）：「效率提升了、仪式感稀释了」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
            "纯白底色，专业知乎风格流程图，黑色文字，知乎蓝主线，浅灰次要路径，极少量暖橙色用于高亮核心判断。\n\n「全民高考记忆为何动人」流程图：\n- 起点：高考记忆\n- 节点 A：所有人在同一天做同一件改变命运的事\n- 节点 B：整个社会空气都是紧绷的、向上的\n- 节点 C：「我和同龄人在同一条船上」的感觉（暖橙高亮）\n- 终点：回忆的残酷性 = 你珍惜它，恰恰因为你失去了\n\n箭头带箭头头。关键判断用暖橙色背景矩形高亮。\n\n节点用思源黑体或苹方字体 12-16pt。\n\n标题在上方居中（22-26pt 加粗）：「你珍惜的，恰恰是你失去的」。\n\n矢量干净风格，无装饰无边框，1-2px 描边，16:9 横屏。\n所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。\n颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。",
        ],
    },
]


def call_api(prompt, output_path, article_key, idx):
    """Call generate.py to produce one zhihu image (16:9, no brand watermark)."""
    # Use --style "zhihu" so it's not in BRANDED_STYLES → no brand watermark
    cmd = [
        "python", GEN_SCRIPT, "section",
        "--prompt", prompt,
        "--output", output_path,
        "--aspect-ratio", "1792x1024",
        "--style", "zhihu",
        "--article-type", "zhihu",
    ]
    print(f"[{article_key} #{idx}] Generating -> {output_path}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=240, cwd=SKILL_DIR)
        if result.returncode == 0:
            print(f"  OK stdout: {result.stdout.strip()[:300]}")
            return True
        else:
            print(f"  FAIL stderr: {result.stderr.strip()[:500]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def insert_images_into_article(article_path, image_paths):
    """Insert 3 image references at 25%, 50%, 75% positions of the article body."""
    with open(article_path, "r", encoding="utf-8") as f:
        text = f.read()
    # Find body after the title and before the final "## 参考" or signoff
    lines = text.split("\n")
    # Identify body lines: skip first line (title) and trailing signoff lines
    # Simpler: insert at line indices roughly 25/50/75% of the content
    # Find lines that are NOT signoff, and not the H1 title
    # Use markdown paragraph heuristic: insert after a paragraph that contains Chinese text
    body_lines = []
    for i, line in enumerate(lines):
        body_lines.append((i, line))

    n = len(lines)
    # Anchor positions (0-based line indices)
    anchors = [int(n * 0.25), int(n * 0.50), int(n * 0.75)]
    # Make sure they're distinct and in order
    # Build new lines
    new_lines = []
    img_inserted = [False, False, False]  # track which images inserted
    last_idx = -1
    for i, line in enumerate(lines):
        new_lines.append(line)
        # Try to insert each image after the matching anchor
        for k, anchor in enumerate(anchors):
            if not img_inserted[k] and i == anchor and k not in img_inserted:
                img_rel = os.path.relpath(image_paths[k], os.path.dirname(article_path))
                new_lines.append("")
                new_lines.append(f"![]({img_rel.replace(os.sep, '/')})")
                new_lines.append("")
                img_inserted[k] = True
    # If any images not yet inserted (edge case), append at end before signoff
    for k, inserted in enumerate(img_inserted):
        if not inserted:
            img_rel = os.path.relpath(image_paths[k], os.path.dirname(article_path))
            new_lines.append("")
            new_lines.append(f"![]({img_rel.replace(os.sep, '/')})")
            new_lines.append("")
    new_text = "\n".join(new_lines)
    with open(article_path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print(f"  Inserted {sum(img_inserted)}/3 images into {os.path.basename(article_path)}")


if __name__ == "__main__":
    only_article = sys.argv[1] if len(sys.argv) > 1 else None

    summary = []
    for art in ARTICLES:
        if only_article and only_article not in art["key"]:
            continue
        article_path = os.path.join(ART_DIR, art["file"])
        image_paths = []
        success_count = 0
        for idx, prompt in enumerate(art["prompts"], 1):
            img_name = f"{art['key']}-{idx:02d}.png"
            img_path = os.path.join(IMG_DIR, img_name)
            ok = call_api(prompt, img_path, art["key"], idx)
            if ok and os.path.exists(img_path):
                success_count += 1
                image_paths.append(img_path)
            else:
                image_paths.append(img_path)  # even if failed, keep path
            time.sleep(2)  # rate limit politeness
        # Insert images into article
        if success_count >= 1:
            insert_images_into_article(article_path, image_paths)
        summary.append((art["key"], success_count, len(art["prompts"])))
        print(f"--- {art['key']}: {success_count}/{len(art['prompts'])} images generated ---\n")

    print("\n=== SUMMARY ===")
    for key, ok, total in summary:
        print(f"{key}: {ok}/{total}")
