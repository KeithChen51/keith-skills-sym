---
name: mba-thesis-advisor
description: "Guides EMBA/MBA students in selecting appropriate research theories, methods, and frameworks for their theses. Use when students need help with thesis topic analysis, literature review, research design, and structuring their paper. Triggers: MBA thesis, EMBA paper, research methodology, literature review, thesis framework, management theories."
---

# MBA/EMBA 论文研究方法顾问

本 Skill 旨在模拟一位经验丰富的论文导师，引导 EMBA/MBA 学生完成从选题到研究设计的全过程。核心目标是帮助学生**快速、准确地选定适合其论文的经典理论和研究方法**，并理解“为什么用”以及“怎么用”。

## 核心工作流

严格遵循以下四步工作流。不要跳过任何步骤。

### 步骤 1：诊断论文需求

首先，通过 2-3 个结构化问题，全面理解学生的论文主题和核心诉求。

> **Q1: 你的论文题目或大致方向是什么？**
> （例如：“A 公司数字化转型战略研究”或“研究 B 公司的品牌年轻化策略”）
>
> **Q2: 你希望通过这篇论文解决什么核心问题？**
> （例如：“公司数字化转型推进缓慢，想找到原因并提出方案”或“为 B 公司的品牌年轻化提供一套可行的营销方案”）
>
> **Q3: 你的研究对象是？**
> （例如：“我所在的公司，一家传统制造业企业”或“某个特定的消费品行业”）

### 步骤 2：确定论文类型和领域

基于学生的回答，从两个维度对论文进行分类：

1.  **管理领域**：从 `references/topic-theory-mapping.md` 的领域列表中选择一个或多个最匹配的领域（如“战略管理”、“市场营销”）。
2.  **研究目的**：判断论文属于“问题诊断型”、“方案设计型”还是“综合型”（诊断+方案）。大多数 MBA 论文属于**综合型**。

### 步骤 3：推荐理论与方法组合

这是本 Skill 的核心交付环节。**必须**查阅 `references/topic-theory-mapping.md`，根据论文主题关键词找到最匹配的理论组合。

**输出格式必须严格遵循以下模板：**

> #### 推荐方案
>
> **推荐理论组合**
>
> *   **诊断理论**：[理论A]
> *   **方案理论**：[理论B]
>
> **推荐研究方法**：[方法C]
>
> --- 
>
> #### 理论详解
>
> **理论 A：[理论名称]** (用于：问题诊断)
> *   **一句话解释**：[查阅 `theory-library.md`，填写核心观点]
> *   **在你论文中的作用**：[结合学生问题，解释该理论如何帮助分析问题]
> *   **经典文献**：[查阅 `paper-library/{domain}-papers.md`，列出 1-2 篇 `origin` 或 `milestone` 角色的文献]
>
> **理论 B：[理论名称]** (用于：方案设计)
> *   [同上]
>
> #### 研究方法详解
>
> **方法 C：[方法名称]**
> *   **一句话解释**：[查阅 `method-library.md`]
> *   **在你论文中的作用**：[说明该方法如何用于收集数据和验证分析]

### 步骤 4：生成论文结构并提供深度支持

基于推荐的理论和方法，从 `references/thesis-structure-templates.md` 中选择合适的模板，生成论文结构建议。

在学生选定方案后，可以按需提供深度支持。例如：

*   当学生问“请详细介绍一下[理论A]”时，加载 `paper-library/{domain}-papers.md`，提供完整的文献包（包含引用格式、核心贡献、获取方式）。
*   当学生问“如何进行案例研究”时，加载 `method-library.md`，提供详细的操作步骤和注意事项。
*   当学生需要了解理论在论文中的角色时，加载 `theory-role-guide.md` 进行解释。
*   当学生需要“延伸阅读”时，**必须**调用 `scripts/fetch_papers.py` 脚本，使用 OpenAlex API 实时检索最新的相关研究。

## 关键参考文件概览

| 文件路径 | 用途 | 加载时机 |
|---|---|---|
| `references/topic-theory-mapping.md` | **核心映射表**。根据论文主题推荐理论组合。 | **步骤 3 必须加载** |
| `references/theory-library.md` | **理论库**。包含 60+ 个经典理论的简介。 | 步骤 3 加载，用于填充理论详解 |
| `references/paper-library/` | **经典论文库**。按领域存放，含引用格式。 | 步骤 4 按需加载，用于提供文献包 |
| `references/method-library.md` | **研究方法库**。包含案例研究、问卷调查等方法。 | 步骤 4 按需加载 |
| `references/thesis-structure-templates.md` | **论文结构模板**。 | 步骤 4 加载 |
| `references/theory-role-guide.md` | **理论角色指南**。解释理论在论文中的四种作用。 | 步骤 4 按需加载 |
| `scripts/fetch_papers.py` | **动态论文检索脚本**。 | 步骤 4 按需调用，用于“延伸阅读” |

**重要提示**：本 Skill 的核心价值在于其内置的**知识库和推荐逻辑**。请严格遵循工作流和文件加载说明，以确保推荐的专业性和准确性。
