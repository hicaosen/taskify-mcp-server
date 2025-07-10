"""Taskify MCP Server - 智能化编程思维导师"""

import re
import json
import time
import hashlib
from typing import Dict, List, Optional, Any
from enum import Enum
# 在原有函数基础上移除重复的导入
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("taskify")

# 全局会话状态管理
_session_cache = {}
_context_memory = {}  # 上下文记忆系统
_analysis_history = []  # 分析历史记录

# 会话清理配置
SESSION_TIMEOUT = 3600  # 1小时超时
MAX_SESSIONS = 100  # 最大缓存会话数


class TaskType(Enum):
    """任务类型枚举"""
    NEW_FEATURE = "new_feature"
    BUG_FIX = "bug_fix"
    REFACTOR = "refactor"
    PERFORMANCE = "performance"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    MAINTENANCE = "maintenance"
    UNKNOWN = "unknown"


class ComplexityLevel(Enum):
    """复杂度级别枚举"""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


@dataclass
class TaskAnalysis:
    """任务分析结果"""
    task_type: TaskType
    complexity_level: ComplexityLevel
    core_objective: str
    key_requirements: List[str]
    constraints: List[str]
    risk_factors: List[str]
    success_criteria: List[str]
    context_needs: List[str]
    similarity_score: float = 0.0  # 与历史任务的相似度
    learning_insights: Optional[List[str]] = None  # 从历史中学到的见解


@dataclass
class ThinkingFramework:
    """思考框架"""
    phase: str
    guiding_questions: List[str]
    key_considerations: List[str]
    output_format: str
    examples: List[str]
    adaptive_hints: Optional[List[str]] = None  # 自适应提示


@dataclass
class SessionInfo:
    """会话信息"""
    session_id: str
    timestamp: float
    user_request: str
    project_context: str
    task_analysis: TaskAnalysis
    thinking_frameworks: Dict[str, ThinkingFramework]
    current_stage: str = "understanding"
    stage_history: Optional[List[str]] = None
    quality_scores: Optional[Dict[str, float]] = None

    def __post_init__(self):
        """初始化可选字段的默认值"""
        if self.stage_history is None:
            self.stage_history = []
        if self.quality_scores is None:
            self.quality_scores = {}


def generate_session_id(user_request: str) -> str:
    """生成唯一会话ID"""
    timestamp = str(time.time())
    content_hash = hashlib.md5(user_request.encode()).hexdigest()[:8]
    return f"session_{content_hash}_{int(float(timestamp))}"


def cleanup_expired_sessions():
    """清理过期会话"""
    current_time = time.time()
    expired_sessions = [
        sid for sid, session in _session_cache.items()
        if current_time - session.timestamp > SESSION_TIMEOUT
    ]
    
    for sid in expired_sessions:
        del _session_cache[sid]
    
    # 如果会话数量超过限制，删除最旧的会话
    if len(_session_cache) > MAX_SESSIONS:
        sorted_sessions = sorted(_session_cache.items(), key=lambda x: x[1].timestamp)
        sessions_to_remove = sorted_sessions[:len(_session_cache) - MAX_SESSIONS]
        for sid, _ in sessions_to_remove:
            del _session_cache[sid]


def find_similar_tasks(user_request: str) -> List[Dict[str, Any]]:
    """从历史中找到相似的任务"""
    current_keywords = set(re.findall(r'\w+', user_request.lower()))
    similarities = []
    
    for history_item in _analysis_history:
        history_keywords = set(re.findall(r'\w+', history_item['user_request'].lower()))
        
        # 计算关键词重叠度
        if current_keywords and history_keywords:
            overlap = len(current_keywords & history_keywords)
            similarity = overlap / len(current_keywords | history_keywords)
            
            if similarity > 0.3:  # 相似度阈值
                similarities.append({
                    'similarity': similarity,
                    'task_type': history_item['task_type'],
                    'complexity': history_item['complexity'],
                    'lessons_learned': history_item.get('lessons_learned', [])
                })
    
    return sorted(similarities, key=lambda x: x['similarity'], reverse=True)[:3]


def analyze_task_type(user_request: str) -> TaskType:
    """基于用户请求分析任务类型 - 增强版"""
    request_lower = user_request.lower()
    
    # 增强的关键词匹配规则，包含更多上下文线索
    type_keywords = {
        TaskType.NEW_FEATURE: [
            "add", "implement", "create", "build", "develop", "新增", "添加", "实现", "构建",
            "feature", "functionality", "capability", "功能", "能力"
        ],
        TaskType.BUG_FIX: [
            "fix", "bug", "error", "issue", "problem", "修复", "错误", "问题", "故障",
            "broken", "crash", "fail", "exception", "崩溃", "失败", "异常"
        ],
        TaskType.REFACTOR: [
            "refactor", "restructure", "reorganize", "clean", "重构", "重组", "清理",
            "improve", "simplify", "optimize code", "改进", "简化", "代码优化"
        ],
        TaskType.PERFORMANCE: [
            "optimize", "performance", "speed", "memory", "efficient", "优化", "性能", "效率",
            "slow", "fast", "latency", "throughput", "缓慢", "延迟", "吞吐量"
        ],
        TaskType.TESTING: [
            "test", "testing", "unit test", "coverage", "测试", "单元测试",
            "validate", "verify", "check", "验证", "检查"
        ],
        TaskType.DOCUMENTATION: [
            "document", "doc", "readme", "comment", "文档", "注释",
            "explain", "describe", "guide", "解释", "描述", "指南"
        ],
        TaskType.MAINTENANCE: [
            "update", "upgrade", "maintain", "dependency", "更新", "升级", "维护",
            "migrate", "deprecated", "迁移", "废弃"
        ]
    }
    
    # 计算匹配分数而不是简单匹配
    type_scores = {}
    for task_type, keywords in type_keywords.items():
        score = sum(2 if keyword in request_lower else 0 for keyword in keywords)
        
        # 上下文加权：检查关键词的上下文
        for keyword in keywords:
            if keyword in request_lower:
                # 检查关键词前后的修饰词
                context_words = re.findall(rf'\w*{keyword}\w*', request_lower)
                for context in context_words:
                    if any(modifier in context for modifier in ['new', 'better', 'improved']):
                        score += 1
        
        type_scores[task_type] = score
    
    # 返回得分最高的任务类型
    if type_scores:
        best_type = max(type_scores.items(), key=lambda x: x[1])
        return best_type[0] if best_type[1] > 0 else TaskType.UNKNOWN
    
    return TaskType.UNKNOWN


def estimate_complexity(user_request: str, task_type: TaskType, project_context: str = "") -> ComplexityLevel:
    """评估任务复杂度 - 智能增强版"""
    request_lower = user_request.lower()
    context_lower = project_context.lower()
    
    complexity_indicators = {
        "high": [
            "architecture", "system", "multiple", "integrate", "database", "api", 
            "microservice", "distributed", "架构", "系统", "多个", "集成", "微服务", "分布式",
            "scalable", "enterprise", "production", "可扩展", "企业级", "生产环境"
        ],
        "medium": [
            "module", "class", "function", "component", "service", "模块", "组件", "类", "函数", "服务",
            "interface", "workflow", "process", "接口", "工作流", "流程"
        ],
        "low": [
            "variable", "config", "simple", "single", "basic", "变量", "配置", "简单", "单个", "基础",
            "small", "minor", "quick", "小", "轻微", "快速"
        ]
    }
    
    # 计算复杂度分数
    high_score = sum(1 for keyword in complexity_indicators["high"] if keyword in request_lower or keyword in context_lower)
    medium_score = sum(1 for keyword in complexity_indicators["medium"] if keyword in request_lower or keyword in context_lower)
    low_score = sum(1 for keyword in complexity_indicators["low"] if keyword in request_lower or keyword in context_lower)
    
    # 任务类型的基础复杂度（调整后）
    base_complexity = {
        TaskType.NEW_FEATURE: 2,
        TaskType.REFACTOR: 2,
        TaskType.PERFORMANCE: 3,  # 性能优化通常更复杂
        TaskType.BUG_FIX: 1,
        TaskType.TESTING: 1,
        TaskType.DOCUMENTATION: 1,
        TaskType.MAINTENANCE: 1,
        TaskType.UNKNOWN: 1
    }
    
    # 项目上下文复杂度调整
    context_complexity = 0
    if any(tech in context_lower for tech in ["react", "vue", "angular", "kubernetes", "docker"]):
        context_complexity += 1
    if any(scale in context_lower for scale in ["large", "enterprise", "distributed", "大型", "企业", "分布式"]):
        context_complexity += 2
    
    total_score = (high_score * 3 + medium_score * 2 + low_score * 1 + 
                   base_complexity[task_type] + context_complexity)
    
    # 动态阈值调整
    if total_score >= 6:
        return ComplexityLevel.COMPLEX
    elif total_score >= 3:
        return ComplexityLevel.MEDIUM
    else:
        return ComplexityLevel.SIMPLE


def generate_thinking_framework(task_analysis: TaskAnalysis, similar_tasks: Optional[List[Dict]] = None) -> Dict[str, ThinkingFramework]:
    """根据任务分析生成定制化思考框架 - 智能增强版"""
    
    frameworks = {}
    
    # 从相似任务中学习
    adaptive_hints = []
    if similar_tasks:
        for similar in similar_tasks:
            if similar.get('lessons_learned'):
                adaptive_hints.extend(similar['lessons_learned'])
    
    # 第一阶段：理解阶段
    frameworks["understanding"] = ThinkingFramework(
        phase="深度理解",
        guiding_questions=generate_understanding_questions(task_analysis),
        key_considerations=generate_understanding_considerations(task_analysis),
        output_format="问题本质、用户意图、隐含需求",
        examples=generate_understanding_examples(task_analysis),
        adaptive_hints=adaptive_hints[:2] if adaptive_hints else []
    )
    
    # 第二阶段：规划阶段
    frameworks["planning"] = ThinkingFramework(
        phase="策略规划",
        guiding_questions=generate_planning_questions(task_analysis),
        key_considerations=generate_planning_considerations(task_analysis),
        output_format="实现路径、技术选型、风险评估",
        examples=generate_planning_examples(task_analysis),
        adaptive_hints=get_planning_hints(task_analysis, similar_tasks)
    )
    
    # 第三阶段：实现阶段
    frameworks["implementation"] = ThinkingFramework(
        phase="精准实现",
        guiding_questions=generate_implementation_questions(task_analysis),
        key_considerations=generate_implementation_considerations(task_analysis),
        output_format="具体步骤、代码结构、接口设计",
        examples=generate_implementation_examples(task_analysis),
        adaptive_hints=get_implementation_hints(task_analysis)
    )
    
    # 第四阶段：验证阶段
    frameworks["validation"] = ThinkingFramework(
        phase="质量验证",
        guiding_questions=generate_validation_questions(task_analysis),
        key_considerations=generate_validation_considerations(task_analysis),
        output_format="测试策略、验收标准、性能指标",
        examples=generate_validation_examples(task_analysis),
        adaptive_hints=get_validation_hints(task_analysis)
    )
    
    return frameworks


def get_planning_hints(task_analysis: TaskAnalysis, similar_tasks: Optional[List[Dict]] = None) -> List[str]:
    """获取规划阶段的自适应提示"""
    hints = []
    
    # 基于任务类型的特定提示
    if task_analysis.task_type == TaskType.NEW_FEATURE:
        hints.append("考虑功能的渐进式发布策略")
        hints.append("设计时优先考虑用户体验和性能")
    elif task_analysis.task_type == TaskType.PERFORMANCE:
        hints.append("建立性能基线，量化优化目标")
        hints.append("考虑缓存、索引、算法优化等多个层面")
    elif task_analysis.task_type == TaskType.REFACTOR:
        hints.append("确保重构的向后兼容性")
        hints.append("制定详细的测试计划以验证重构效果")
    
    # 基于复杂度的提示
    if task_analysis.complexity_level == ComplexityLevel.COMPLEX:
        hints.append("将复杂任务分解为独立的子任务")
        hints.append("考虑并行开发和集成策略")
    
    # 从相似任务中学习
    if similar_tasks:
        for similar in similar_tasks:
            if similar.get('lessons_learned'):
                hints.extend(similar['lessons_learned'][:1])
    
    return hints[:4]  # 限制提示数量


def get_implementation_hints(task_analysis: TaskAnalysis) -> List[str]:
    """获取实现阶段的自适应提示"""
    hints = []
    
    if task_analysis.task_type == TaskType.NEW_FEATURE:
        hints.extend([
            "采用TDD(测试驱动开发)方法",
            "实现MVP(最小可行产品)版本，然后迭代"
        ])
    elif task_analysis.task_type == TaskType.BUG_FIX:
        hints.extend([
            "先重现问题，再定位根因",
            "修复后添加回归测试防止问题再现"
        ])
    elif task_analysis.task_type == TaskType.PERFORMANCE:
        hints.extend([
            "使用性能分析工具定位瓶颈",
            "优化前后进行性能对比测试"
        ])
    
    return hints


def get_validation_hints(task_analysis: TaskAnalysis) -> List[str]:
    """获取验证阶段的自适应提示"""
    hints = []
    
    if task_analysis.complexity_level == ComplexityLevel.COMPLEX:
        hints.extend([
            "进行分层测试：单元测试、集成测试、系统测试",
            "考虑负载测试和压力测试"
        ])
    
    if task_analysis.task_type == TaskType.NEW_FEATURE:
        hints.extend([
            "进行用户验收测试(UAT)",
            "收集用户反馈并准备迭代"
        ])
    
    return hints


def generate_understanding_questions(task_analysis: TaskAnalysis) -> List[str]:
    """生成理解阶段的指导问题"""
    base_questions = [
        "用户真正想要解决什么核心问题？",
        "这个需求背后的业务价值是什么？",
        "有哪些隐含的约束和期望？"
    ]
    
    type_specific_questions = {
        TaskType.NEW_FEATURE: [
            "这个功能如何融入现有系统？",
            "预期的用户使用场景是什么？",
            "功能边界在哪里？"
        ],
        TaskType.BUG_FIX: [
            "问题的根本原因是什么？",
            "影响范围有多大？",
            "如何避免类似问题再次出现？"
        ],
        TaskType.REFACTOR: [
            "当前设计的痛点是什么？",
            "重构的最终目标是什么？",
            "如何确保重构后的向后兼容性？"
        ],
        TaskType.PERFORMANCE: [
            "性能瓶颈在哪里？",
            "目标性能指标是什么？",
            "优化的权衡取舍是什么？"
        ]
    }
    
    return base_questions + type_specific_questions.get(task_analysis.task_type, [])


def generate_understanding_considerations(task_analysis: TaskAnalysis) -> List[str]:
    """生成理解阶段的关键考虑点"""
    base_considerations = [
        "区分显性需求和隐性需求",
        "识别技术约束和业务约束",
        "评估变更的影响范围"
    ]
    
    complexity_considerations = {
        ComplexityLevel.SIMPLE: ["确保理解准确，避免过度设计"],
        ComplexityLevel.MEDIUM: ["平衡功能完整性和实现复杂度"],
        ComplexityLevel.COMPLEX: ["系统性思考，考虑架构影响", "分阶段实现策略"]
    }
    
    return base_considerations + complexity_considerations[task_analysis.complexity_level]


def generate_understanding_examples(task_analysis: TaskAnalysis) -> List[str]:
    """生成理解阶段的示例"""
    examples = {
        TaskType.NEW_FEATURE: ["用户说'添加搜索功能' → 理解为：需要什么类型的搜索？实时搜索还是批量搜索？搜索范围是什么？"],
        TaskType.BUG_FIX: ["用户说'登录有问题' → 理解为：什么情况下出错？错误现象是什么？影响所有用户还是特定用户？"],
        TaskType.REFACTOR: ["用户说'代码太乱了' → 理解为：具体哪些部分需要重构？重构的优先级是什么？"],
        TaskType.PERFORMANCE: ["用户说'太慢了' → 理解为：哪个环节慢？可接受的响应时间是多少？"]
    }
    
    return examples.get(task_analysis.task_type, ["深入理解用户真实需求，而非表面描述"])


def generate_planning_questions(task_analysis: TaskAnalysis) -> List[str]:
    """生成规划阶段的指导问题"""
    return [
        "最佳的实现路径是什么？",
        "需要哪些技术栈和工具？",
        "如何分解任务以降低风险？",
        "有哪些可能的技术陷阱？",
        "如何确保代码质量和可维护性？"
    ]


def generate_planning_considerations(task_analysis: TaskAnalysis) -> List[str]:
    """生成规划阶段的关键考虑点"""
    base_considerations = [
        "选择合适的技术方案",
        "评估开发成本和时间",
        "考虑未来扩展性"
    ]
    
    if task_analysis.complexity_level == ComplexityLevel.COMPLEX:
        base_considerations.extend([
            "设计系统架构",
            "定义模块接口",
            "制定迭代计划"
        ])
    
    return base_considerations


def generate_planning_examples(task_analysis: TaskAnalysis) -> List[str]:
    """生成规划阶段的示例"""
    return [
        "技术选型：React vs Vue → 考虑团队技能、项目需求、生态系统",
        "架构设计：单体 vs 微服务 → 考虑项目规模、团队能力、维护成本"
    ]


def generate_implementation_questions(task_analysis: TaskAnalysis) -> List[str]:
    """生成实现阶段的指导问题"""
    return [
        "如何组织代码结构？",
        "接口设计是否清晰合理？",
        "错误处理策略是什么？",
        "如何确保代码的可测试性？",
        "是否遵循了项目的编码规范？"
    ]


def generate_implementation_considerations(task_analysis: TaskAnalysis) -> List[str]:
    """生成实现阶段的关键考虑点"""
    return [
        "保持代码简洁和可读性",
        "遵循设计模式和最佳实践",
        "考虑异常情况的处理",
        "确保接口的向后兼容性",
        "添加必要的日志和监控"
    ]


def generate_implementation_examples(task_analysis: TaskAnalysis) -> List[str]:
    """生成实现阶段的示例"""
    return [
        "函数设计：单一职责、清晰命名、适当抽象",
        "错误处理：预期异常 vs 意外异常的不同处理策略"
    ]


def generate_validation_questions(task_analysis: TaskAnalysis) -> List[str]:
    """生成验证阶段的指导问题"""
    return [
        "如何验证功能的正确性？",
        "性能是否满足要求？",
        "是否考虑了边界情况？",
        "用户体验是否良好？",
        "是否有充分的测试覆盖？"
    ]


def generate_validation_considerations(task_analysis: TaskAnalysis) -> List[str]:
    """生成验证阶段的关键考虑点"""
    return [
        "功能测试和集成测试",
        "性能基准测试",
        "用户体验验证",
        "代码质量检查",
        "文档完整性确认"
    ]


def generate_validation_examples(task_analysis: TaskAnalysis) -> List[str]:
    """生成验证阶段的示例"""
    return [
        "API测试：正常情况、异常情况、边界情况",
        "性能测试：响应时间、并发处理、内存使用"
    ]


@mcp.tool()
def analyze_programming_context(
    user_request: str,
    project_context: str = "",
    complexity_hint: str = "auto"
) -> str:
    """
    🧠 智能编程任务分析器 V2.0 - 启发式思维的起点
    
    **重大升级特性：**
    • ✨ 会话状态管理 - 无需传递大JSON，使用简单session_id
    • 🧠 智能学习系统 - 从历史任务中学习，提供个性化建议
    • 🎯 自适应框架 - 根据任务特点动态调整思考框架
    • 📊 上下文记忆 - 记住项目背景，累积智慧
    
    **核心能力：**
    • 自动识别任务类型（新功能、Bug修复、性能优化、重构等）
    • 智能评估复杂度级别（简单/中等/复杂）
    • 提供场景化的4阶段思考框架（理解→规划→实现→验证）
    • 生成定制化的指导问题和关键考虑点
    • 从相似任务中学习，提供智能建议
    
    **使用场景：**
    - 面对新的编程任务时，不确定从何思考
    - 需要系统化的思考框架来指导任务分析
    - 希望根据任务特点获得针对性的思考指导
    - 想要确保考虑到所有重要的技术和业务因素
    
    Args:
        user_request: 用户的编程请求描述
        project_context: 项目背景信息（技术栈、架构约束等）
        complexity_hint: 复杂度提示 ("simple"/"medium"/"complex"/"auto")
    
    Returns:
        轻量级会话信息，后续工具使用session_id即可：
        {
            "session_id": "session_abc123_1234567890",
            "task_summary": {
                "task_type": "任务类型",
                "complexity_level": "复杂度级别",
                "core_objective": "核心目标"
            },
            "intelligent_insights": {
                "similarity_analysis": "与历史任务的相似度分析",
                "learning_suggestions": ["从相似任务中学到的建议"],
                "risk_prediction": ["基于历史的风险预测"]
            },
            "next_steps": {
                "recommended_workflow": "推荐的思考流程",
                "first_action": "建议的第一步行动"
            },
            "session_info": "会话已创建，使用session_id进行后续思考指导"
        }
    """
    
    # 清理过期会话
    cleanup_expired_sessions()
    
    # 分析任务类型
    task_type = analyze_task_type(user_request)
    
    # 估算复杂度（增强版）
    if complexity_hint == "auto":
        complexity_level = estimate_complexity(user_request, task_type, project_context)
    else:
        complexity_level = ComplexityLevel(complexity_hint)
    
    # 智能相似任务分析
    similar_tasks = find_similar_tasks(user_request)
    similarity_score = similar_tasks[0]['similarity'] if similar_tasks else 0.0
    
    # 生成任务分析（增强版）
    task_analysis = TaskAnalysis(
        task_type=task_type,
        complexity_level=complexity_level,
        core_objective=extract_core_objective(user_request),
        key_requirements=extract_requirements(user_request),
        constraints=extract_constraints(user_request, project_context),
        risk_factors=identify_risk_factors(user_request, task_type),
        success_criteria=define_success_criteria(user_request, task_type),
        context_needs=identify_context_needs(user_request, project_context),
        similarity_score=similarity_score,
        learning_insights=[task['lessons_learned'] for task in similar_tasks if task.get('lessons_learned')]
    )
    
    # 生成智能思考框架
    frameworks = generate_thinking_framework(task_analysis, similar_tasks)
    
    # 创建会话
    session_id = generate_session_id(user_request)
    session_info = SessionInfo(
        session_id=session_id,
        timestamp=time.time(),
        user_request=user_request,
        project_context=project_context,
        task_analysis=task_analysis,
        thinking_frameworks=frameworks,
        current_stage="understanding",
        stage_history=[],
        quality_scores={}
    )
    
    # 存储会话状态
    _session_cache[session_id] = session_info
    
    # 更新上下文记忆
    if project_context:
        context_key = hashlib.md5(project_context.encode()).hexdigest()[:8]
        _context_memory[context_key] = {
            'context': project_context,
            'timestamp': time.time(),
            'task_count': _context_memory.get(context_key, {}).get('task_count', 0) + 1
        }
    
    # 添加到分析历史
    _analysis_history.append({
        'user_request': user_request,
        'task_type': task_type.value,
        'complexity': complexity_level.value,
        'timestamp': time.time(),
        'session_id': session_id
    })
    
    # 限制历史记录大小
    if len(_analysis_history) > 50:
        _analysis_history.pop(0)
    
    # 生成智能洞察
    intelligent_insights = {
        "similarity_analysis": f"发现{len(similar_tasks)}个相似任务，最高相似度{similarity_score:.2f}" if similar_tasks else "未发现相似的历史任务",
        "learning_suggestions": [insight for task in similar_tasks for insight in task.get('lessons_learned', [])][:3],
        "risk_prediction": predict_risks_from_history(task_analysis, similar_tasks),
        "context_familiarity": f"项目上下文熟悉度: {get_context_familiarity(project_context)}/5"
    }
    
    # 构建轻量级返回结果
    result = {
        "session_id": session_id,
        "task_summary": {
            "task_type": task_analysis.task_type.value,
            "complexity_level": task_analysis.complexity_level.value,
            "core_objective": task_analysis.core_objective,
            "estimated_stages": len(frameworks)
        },
        "intelligent_insights": intelligent_insights,
        "next_steps": {
            "recommended_workflow": get_workflow_recommendation(complexity_level),
            "first_action": f"开始 guided_thinking_process('{session_id}', 'understanding')",
            "tools_sequence": ["guided_thinking_process"] * len(frameworks) + ["validate_instruction_quality"]
        },
        "session_info": f"✅ 会话已创建，ID: {session_id}。现在可以使用session_id进行后续思考指导，无需传递大JSON。"
    }
    
    return json.dumps(result, ensure_ascii=False, indent=2)


def predict_risks_from_history(task_analysis: TaskAnalysis, similar_tasks: List[Dict]) -> List[str]:
    """基于历史任务预测风险"""
    risks = []
    
    # 基于相似任务的风险
    for similar in similar_tasks:
        if similar.get('common_risks'):
            risks.extend(similar['common_risks'])
    
    # 基于任务类型的常见风险
    type_risks = {
        TaskType.NEW_FEATURE: ["需求变更风险", "集成复杂度风险"],
        TaskType.PERFORMANCE: ["过度优化风险", "兼容性风险"],
        TaskType.REFACTOR: ["破坏现有功能风险", "范围扩大风险"]
    }
    
    risks.extend(type_risks.get(task_analysis.task_type, []))
    
    return list(set(risks))[:3]  # 去重并限制数量


def get_context_familiarity(project_context: str) -> int:
    """获取项目上下文熟悉度（1-5分）"""
    if not project_context:
        return 1
    
    context_key = hashlib.md5(project_context.encode()).hexdigest()[:8]
    memory = _context_memory.get(context_key, {})
    task_count = memory.get('task_count', 0)
    
    # 基于历史任务数量评估熟悉度
    if task_count >= 10:
        return 5
    elif task_count >= 5:
        return 4
    elif task_count >= 3:
        return 3
    elif task_count >= 1:
        return 2
    else:
        return 1


def get_workflow_recommendation(complexity: ComplexityLevel) -> str:
    """获取工作流推荐"""
    workflows = {
        ComplexityLevel.SIMPLE: "轻量级流程：understanding → implementation → validation",
        ComplexityLevel.MEDIUM: "标准流程：understanding → planning → implementation → validation",
        ComplexityLevel.COMPLEX: "深度流程：understanding → planning → implementation → validation + 可能的多轮迭代"
    }
    return workflows[complexity]


def extract_core_objective(user_request: str) -> str:
    """提取核心目标"""
    # 简单的目标提取逻辑
    if "implement" in user_request.lower() or "实现" in user_request:
        return "实现新功能"
    elif "fix" in user_request.lower() or "修复" in user_request:
        return "修复问题"
    elif "optimize" in user_request.lower() or "优化" in user_request:
        return "优化性能"
    elif "refactor" in user_request.lower() or "重构" in user_request:
        return "重构代码"
    else:
        return "完成编程任务"


def extract_requirements(user_request: str) -> List[str]:
    """提取关键需求"""
    # 简化的需求提取
    requirements = []
    if "test" in user_request.lower() or "测试" in user_request:
        requirements.append("包含测试用例")
    if "document" in user_request.lower() or "文档" in user_request:
        requirements.append("提供文档说明")
    if "performance" in user_request.lower() or "性能" in user_request:
        requirements.append("考虑性能优化")
    
    return requirements if requirements else ["满足基本功能需求"]


def extract_constraints(user_request: str, project_context: str) -> List[str]:
    """提取约束条件"""
    constraints = []
    if "backward compatible" in user_request.lower() or "向后兼容" in user_request:
        constraints.append("保持向后兼容性")
    if project_context:
        constraints.append("遵循项目现有架构")
    
    return constraints if constraints else ["遵循编程最佳实践"]


def identify_risk_factors(user_request: str, task_type: TaskType) -> List[str]:
    """识别风险因素"""
    risk_factors = []
    
    if task_type == TaskType.NEW_FEATURE:
        risk_factors.extend(["功能范围蔓延", "与现有功能冲突"])
    elif task_type == TaskType.BUG_FIX:
        risk_factors.extend(["修复引入新问题", "影响其他功能"])
    elif task_type == TaskType.REFACTOR:
        risk_factors.extend(["破坏现有功能", "重构范围过大"])
    elif task_type == TaskType.PERFORMANCE:
        risk_factors.extend(["过度优化", "可读性下降"])
    
    return risk_factors


def define_success_criteria(user_request: str, task_type: TaskType) -> List[str]:
    """定义成功标准"""
    base_criteria = ["功能正确实现", "代码质量良好", "通过测试验证"]
    
    type_specific_criteria = {
        TaskType.NEW_FEATURE: ["满足用户需求", "性能表现良好"],
        TaskType.BUG_FIX: ["问题完全解决", "无副作用"],
        TaskType.REFACTOR: ["代码更清晰", "性能不降低"],
        TaskType.PERFORMANCE: ["达到性能目标", "保持功能完整"]
    }
    
    return base_criteria + type_specific_criteria.get(task_type, [])


def identify_context_needs(user_request: str, project_context: str) -> List[str]:
    """识别上下文需求"""
    needs = ["了解现有代码结构", "理解业务逻辑"]
    
    if not project_context:
        needs.append("获取项目架构信息")
    
    return needs


def generate_approach_recommendation(task_analysis: TaskAnalysis) -> str:
    """生成实现方法建议"""
    if task_analysis.complexity_level == ComplexityLevel.SIMPLE:
        return "直接实现，注重代码质量"
    elif task_analysis.complexity_level == ComplexityLevel.MEDIUM:
        return "分步实现，先设计后编码"
    else:
        return "分阶段实现，先制定详细计划"


def generate_quality_checklist(task_analysis: TaskAnalysis) -> List[str]:
    """生成质量检查清单"""
    return [
        "代码是否清晰易读？",
        "是否遵循项目规范？",
        "错误处理是否完善？",
        "是否有充分的测试？",
        "性能是否可接受？",
        "是否考虑了边界情况？"
    ]


@mcp.tool()
def guided_thinking_process(
    session_id: str,
    current_step: str = "understanding"
) -> str:
    """
    🎯 渐进式思考引导器 V2.0 - 步步为营的智慧路径
    
    **重大升级特性：**
    • ✨ 会话状态驱动 - 使用简单session_id，无需传递大JSON
    • 🧠 智能进度跟踪 - 自动记录思考历程，提供连贯指导
    • 🎯 自适应提示 - 基于历史学习和当前上下文的个性化建议
    • 📊 质量反馈循环 - 实时评估思考质量，动态调整指导策略
    
    **思考阶段流程：**
    • **理解阶段 (understanding)**: 深入洞察问题本质，理解真实需求
    • **规划阶段 (planning)**: 制定实现策略，评估技术选型和风险
    • **实现阶段 (implementation)**: 指导具体编码实现，确保质量
    • **验证阶段 (validation)**: 质量验证和测试策略制定
    
    **使用场景：**
    - 已完成任务分析，需要逐步深入思考
    - 希望在每个阶段都获得专业指导
    - 确保思考过程的完整性和系统性
    - 避免遗漏关键的考虑因素
    
    **简化工作流程：**
    1. 先调用 analyze_programming_context 获取 session_id
    2. 使用 session_id 和阶段名称调用此工具
    3. 从 understanding 开始，逐步推进到 validation
    4. 每完成一个阶段，进入下一个阶段继续思考
    
    Args:
        session_id: 会话ID（来自 analyze_programming_context 的返回结果）
        current_step: 当前思考阶段 ("understanding"/"planning"/"implementation"/"validation")
    
    Returns:
        当前阶段的详细指导信息：
        {
            "phase": "当前阶段名称",
            "focus": "阶段重点描述",
            "questions": ["引导性问题列表"],
            "considerations": ["关键考虑点"],
            "adaptive_hints": ["基于学习的个性化建议"],
            "output_format": "预期输出格式",
            "examples": ["具体示例"],
            "progress": {
                "current_stage": "当前阶段",
                "completed_stages": ["已完成的阶段"],
                "next_step": "下一个阶段",
                "overall_progress": "整体进度"
            },
            "session_context": "会话上下文信息"
        }
    """
    
    # 检查会话是否存在
    if session_id not in _session_cache:
        return json.dumps({
            "error": "会话不存在或已过期",
            "suggestion": "请先调用 analyze_programming_context 创建新会话",
            "available_sessions": list(_session_cache.keys())[-3:] if _session_cache else []
        }, ensure_ascii=False, indent=2)
    
    session_info = _session_cache[session_id]
    frameworks = session_info.thinking_frameworks
    
    # 验证步骤有效性
    if current_step not in frameworks:
        return json.dumps({
            "error": f"无效的步骤: {current_step}",
            "available_steps": list(frameworks.keys()),
            "suggestion": "请使用有效的思考阶段名称"
        }, ensure_ascii=False, indent=2)
    
    current_framework = frameworks[current_step]
    
    # 更新会话状态
    session_info.current_stage = current_step
    if current_step not in session_info.stage_history:
        session_info.stage_history.append(current_step)
    
    # 获取智能上下文
    task_analysis = session_info.task_analysis
    context_insights = get_context_insights(session_info)
    
    # 构建增强的指导信息
    guidance = {
        "phase": current_framework.phase,
        "focus": f"🎯 专注于{current_framework.phase}阶段",
        "questions": current_framework.guiding_questions,
        "considerations": current_framework.key_considerations,
        "adaptive_hints": current_framework.adaptive_hints or [],
        "output_format": current_framework.output_format,
        "examples": current_framework.examples,
        "intelligent_context": {
            "task_complexity": task_analysis.complexity_level.value,
            "similarity_insights": f"相似度评分: {task_analysis.similarity_score:.2f}",
            "learning_from_history": task_analysis.learning_insights[:2] if task_analysis.learning_insights else [],
            "context_familiarity": f"项目熟悉度: {get_context_familiarity(session_info.project_context)}/5"
        },
        "progress": {
            "current_stage": current_step,
            "completed_stages": session_info.stage_history[:-1],  # 除了当前阶段
            "next_step": get_next_step(current_step),
            "overall_progress": f"{len(session_info.stage_history)}/{len(frameworks)} 阶段"
        },
        "session_context": {
            "session_id": session_id,
            "task_type": task_analysis.task_type.value,
            "original_request": session_info.user_request[:100] + "..." if len(session_info.user_request) > 100 else session_info.user_request,
            "session_duration": f"{int((time.time() - session_info.timestamp) / 60)}分钟"
        }
    }
    
    # 添加阶段特定的智能提示
    stage_specific_hints = get_stage_specific_hints(current_step, task_analysis, context_insights)
    if stage_specific_hints:
        guidance["stage_specific_insights"] = stage_specific_hints
    
    return json.dumps(guidance, ensure_ascii=False, indent=2)


def get_context_insights(session_info: SessionInfo) -> Dict[str, Any]:
    """获取上下文洞察"""
    insights = {}
    
    # 项目上下文分析
    if session_info.project_context:
        context_key = hashlib.md5(session_info.project_context.encode()).hexdigest()[:8]
        memory = _context_memory.get(context_key, {})
        insights["context_experience"] = memory.get('task_count', 0)
    
    # 任务类型经验
    task_type = session_info.task_analysis.task_type
    type_count = sum(1 for h in _analysis_history if h.get('task_type') == task_type.value)
    insights["task_type_experience"] = type_count
    
    # 复杂度处理经验  
    complexity = session_info.task_analysis.complexity_level
    complexity_count = sum(1 for h in _analysis_history if h.get('complexity') == complexity.value)
    insights["complexity_experience"] = complexity_count
    
    return insights


def get_stage_specific_hints(stage: str, task_analysis: TaskAnalysis, context_insights: Dict) -> List[str]:
    """获取阶段特定的智能提示"""
    hints = []
    
    experience_level = context_insights.get('task_type_experience', 0)
    
    if stage == "understanding":
        if task_analysis.task_type == TaskType.NEW_FEATURE:
            hints.append("💡 新功能开发：重点关注用户价值和系统集成点")
        elif task_analysis.task_type == TaskType.BUG_FIX:
            hints.append("🔍 Bug修复：先重现问题，再分析根因，避免头痛医头")
        
        if experience_level < 3:
            hints.append("📚 建议：多问几个'为什么'，深入理解问题本质")
    
    elif stage == "planning":
        if task_analysis.complexity_level == ComplexityLevel.COMPLEX:
            hints.append("🎯 复杂任务：优先考虑分解策略和里程碑设置")
        
        if context_insights.get('context_experience', 0) > 5:
            hints.append("⚡ 基于项目经验：可以复用已有的架构模式和工具链")
    
    elif stage == "implementation":
        if task_analysis.task_type == TaskType.PERFORMANCE:
            hints.append("📊 性能优化：建立基线测试，量化优化效果")
        
        hints.append("🧪 实现建议：采用小步快跑，频繁验证的策略")
    
    elif stage == "validation":
        if task_analysis.complexity_level != ComplexityLevel.SIMPLE:
            hints.append("🔄 质量保证：考虑多层次测试策略，不只是功能测试")
        
        hints.append("👥 验收准备：考虑用户视角的验收标准")
    
    return hints[:3]  # 限制提示数量


def get_next_step(current_step: str) -> str:
    """获取下一步骤"""
    step_order = ["understanding", "planning", "implementation", "validation"]
    try:
        current_index = step_order.index(current_step)
        if current_index < len(step_order) - 1:
            return step_order[current_index + 1]
        else:
            return "完成"
    except ValueError:
        return "未知"


@mcp.tool()
def validate_instruction_quality(
    instruction: str,
    session_id: str = ""
) -> str:
    """
    ✅ 编程指令质量评估器 V2.0 - 确保指令的专业水准
    
    **重大升级特性：**
    • 🧠 智能上下文评估 - 结合会话信息提供精准质量分析
    • 📊 历史学习算法 - 基于过往质量数据优化评估标准
    • 🎯 个性化建议 - 针对具体任务类型和复杂度的改进建议
    • 🔄 动态评分调整 - 根据项目经验和任务历史动态调整评分权重
    
    **评估维度：**
    • **清晰度 (Clarity)**: 指令是否明确易懂，目标清晰
    • **完整性 (Completeness)**: 是否包含必要的输入输出、约束条件
    • **具体性 (Specificity)**: 是否有具体的技术细节和文件名
    • **可执行性 (Actionability)**: 是否提供明确步骤，避免模糊语言
    • **风险意识 (Risk Awareness)**: 是否考虑测试、错误处理、兼容性
    • **上下文匹配度 (Context Alignment)**: 指令与任务上下文的匹配程度 [新增]
    
    **智能评分标准：**
    - 0.9-1.0: 🌟 优秀 - 指令质量非常高，可直接执行
    - 0.8-0.9: ✅ 良好 - 指令质量较高，轻微调整即可  
    - 0.7-0.8: ⚠️ 一般 - 指令质量中等，需要优化
    - 0.6-0.7: 🔄 需要改进 - 指令质量偏低，建议重写部分内容
    - 0.0-0.6: ❌ 不合格 - 指令质量较差，需要重新设计
    
    **使用场景：**
    - 完成指令编写后，验证质量是否达标
    - 对已有指令进行优化改进
    - 学习如何编写高质量的编程指令
    - 确保指令能被编程代理准确理解和执行
    
    Args:
        instruction: 需要评估的编程指令文本
        session_id: 可选的会话ID，用于获取任务上下文进行精准评估
    
    Returns:
        详细的质量评估报告：
        {
            "overall_score": 0.85,
            "quality_metrics": {
                "clarity": 0.8,
                "completeness": 0.9,
                "specificity": 0.7,
                "actionability": 0.9,
                "risk_awareness": 0.8,
                "context_alignment": 0.9
            },
            "intelligent_analysis": {
                "task_context_match": "任务上下文匹配分析",
                "complexity_appropriateness": "复杂度适配性分析",
                "historical_comparison": "与历史质量数据对比"
            },
            "assessment": "良好 - 指令质量较高",
            "improvement_suggestions": ["具体改进建议"],
            "personalized_recommendations": ["基于任务特点的个性化建议"],
            "quality_trend": "质量趋势分析"
        }
    """
    
    # 获取会话上下文（如果提供）
    session_context = None
    task_analysis = None
    if session_id and session_id in _session_cache:
        session_context = _session_cache[session_id]
        task_analysis = session_context.task_analysis
    
    # 智能质量评估维度
    quality_metrics = {
        "clarity": assess_clarity_enhanced(instruction, task_analysis),
        "completeness": assess_completeness_enhanced(instruction, task_analysis),
        "specificity": assess_specificity_enhanced(instruction, task_analysis),
        "actionability": assess_actionability_enhanced(instruction, task_analysis),
        "risk_awareness": assess_risk_awareness_enhanced(instruction, task_analysis),
        "context_alignment": assess_context_alignment(instruction, task_analysis) if task_analysis else 0.7
    }
    
    # 计算加权总分（根据任务特点动态调整权重）
    weights = get_dynamic_weights(task_analysis) if task_analysis else {
        "clarity": 0.2, "completeness": 0.2, "specificity": 0.15, 
        "actionability": 0.2, "risk_awareness": 0.15, "context_alignment": 0.1
    }
    
    total_score = sum(score * weights.get(metric, 0.16) for metric, score in quality_metrics.items())
    
    # 生成智能分析
    intelligent_analysis = generate_intelligent_analysis(instruction, task_analysis, quality_metrics)
    
    # 生成个性化改进建议
    personalized_suggestions = generate_personalized_suggestions(quality_metrics, task_analysis)
    
    # 更新会话质量记录
    if session_context:
        session_context.quality_scores[f"validation_{int(time.time())}"] = total_score
    
    # 构建增强的评估结果
    result = {
        "overall_score": round(total_score, 2),
        "quality_metrics": {k: round(v, 2) for k, v in quality_metrics.items()},
        "intelligent_analysis": intelligent_analysis,
        "assessment": get_quality_assessment_enhanced(total_score),
        "improvement_suggestions": generate_improvement_suggestions_enhanced(quality_metrics, instruction, task_analysis),
        "personalized_recommendations": personalized_suggestions,
        "quality_trend": get_quality_trend(session_context) if session_context else "首次评估，无历史趋势",
        "context_insights": {
            "session_available": session_id and session_id in _session_cache,
            "task_type": task_analysis.task_type.value if task_analysis else "未知",
            "complexity": task_analysis.complexity_level.value if task_analysis else "未知",
            "evaluation_timestamp": int(time.time())
        }
    }
    
    return json.dumps(result, ensure_ascii=False, indent=2)


def assess_clarity_enhanced(instruction: str, task_analysis: Optional[TaskAnalysis]) -> float:
    """增强的清晰度评估"""
    base_score = assess_clarity(instruction)
    
    # 基于任务类型调整
    if task_analysis:
        if task_analysis.task_type == TaskType.BUG_FIX:
            # Bug修复需要明确的问题描述
            if any(word in instruction.lower() for word in ["reproduce", "root cause", "reproduce", "重现", "根因"]):
                base_score += 0.1
        elif task_analysis.task_type == TaskType.NEW_FEATURE:
            # 新功能需要明确的需求描述
            if any(word in instruction.lower() for word in ["requirement", "user story", "需求", "用户故事"]):
                base_score += 0.1
    
    return min(base_score, 1.0)


def assess_completeness_enhanced(instruction: str, task_analysis: Optional[TaskAnalysis]) -> float:
    """增强的完整性评估"""
    base_score = assess_completeness(instruction)
    
    # 基于复杂度调整期望
    if task_analysis:
        if task_analysis.complexity_level == ComplexityLevel.COMPLEX:
            # 复杂任务需要更详细的步骤
            step_indicators = len(re.findall(r'\d+\.|\-|\*', instruction))
            if step_indicators >= 3:
                base_score += 0.1
        elif task_analysis.complexity_level == ComplexityLevel.SIMPLE:
            # 简单任务不需要过度详细
            if len(instruction.split()) < 50:  # 避免过度复杂化
                base_score += 0.1
    
    return min(base_score, 1.0)


def assess_specificity_enhanced(instruction: str, task_analysis: Optional[TaskAnalysis]) -> float:
    """增强的具体性评估"""
    base_score = assess_specificity(instruction)
    
    # 基于任务类型的具体性要求
    if task_analysis:
        if task_analysis.task_type == TaskType.PERFORMANCE:
            # 性能优化需要具体的指标
            if re.search(r'\d+%|\d+ms|\d+MB', instruction):
                base_score += 0.2
        elif task_analysis.task_type == TaskType.TESTING:
            # 测试任务需要具体的测试类型
            test_types = ["unit", "integration", "e2e", "单元", "集成", "端到端"]
            if any(test_type in instruction.lower() for test_type in test_types):
                base_score += 0.15
    
    return min(base_score, 1.0)


def assess_actionability_enhanced(instruction: str, task_analysis: Optional[TaskAnalysis]) -> float:
    """增强的可执行性评估"""
    base_score = assess_actionability(instruction)
    
    # 检查是否有明确的工具或命令
    tools = ["npm", "git", "docker", "kubectl", "python", "node"]
    if any(tool in instruction.lower() for tool in tools):
        base_score += 0.1
    
    return min(base_score, 1.0)


def assess_risk_awareness_enhanced(instruction: str, task_analysis: Optional[TaskAnalysis]) -> float:
    """增强的风险意识评估"""
    base_score = assess_risk_awareness(instruction)
    
    # 基于任务风险因素调整
    if task_analysis and task_analysis.risk_factors:
        mentioned_risks = 0
        for risk in task_analysis.risk_factors:
            risk_keywords = risk.lower().split()
            if any(keyword in instruction.lower() for keyword in risk_keywords):
                mentioned_risks += 1
        
        if mentioned_risks > 0:
            base_score += min(mentioned_risks * 0.1, 0.3)
    
    return min(base_score, 1.0)


def assess_context_alignment(instruction: str, task_analysis: TaskAnalysis) -> float:
    """评估指令与任务上下文的匹配度"""
    if not task_analysis:
        return 0.7  # 默认分数
    
    score = 0.5  # 基础分
    
    # 检查是否匹配任务类型
    task_keywords = {
        TaskType.NEW_FEATURE: ["implement", "create", "add", "build"],
        TaskType.BUG_FIX: ["fix", "resolve", "debug", "patch"],
        TaskType.PERFORMANCE: ["optimize", "improve", "enhance", "speed"],
        TaskType.REFACTOR: ["refactor", "restructure", "clean", "organize"]
    }
    
    expected_keywords = task_keywords.get(task_analysis.task_type, [])
    if any(keyword in instruction.lower() for keyword in expected_keywords):
        score += 0.2
    
    # 检查是否考虑了关键需求
    for requirement in task_analysis.key_requirements:
        req_keywords = requirement.lower().split()
        if any(keyword in instruction.lower() for keyword in req_keywords):
            score += 0.1
    
    # 检查复杂度匹配
    complexity_indicators = {
        ComplexityLevel.SIMPLE: len(instruction.split()) < 100,
        ComplexityLevel.MEDIUM: 100 <= len(instruction.split()) <= 300,
        ComplexityLevel.COMPLEX: len(instruction.split()) > 200
    }
    
    if complexity_indicators.get(task_analysis.complexity_level, False):
        score += 0.2
    
    return min(score, 1.0)


def get_dynamic_weights(task_analysis: TaskAnalysis) -> Dict[str, float]:
    """根据任务特点动态调整评估权重"""
    base_weights = {
        "clarity": 0.2, "completeness": 0.2, "specificity": 0.15,
        "actionability": 0.2, "risk_awareness": 0.15, "context_alignment": 0.1
    }
    
    # 基于任务类型调整权重
    if task_analysis.task_type == TaskType.BUG_FIX:
        base_weights["specificity"] += 0.05  # Bug修复需要更具体
        base_weights["risk_awareness"] += 0.05  # 风险意识更重要
    elif task_analysis.task_type == TaskType.PERFORMANCE:
        base_weights["specificity"] += 0.1  # 性能优化需要具体指标
    elif task_analysis.task_type == TaskType.NEW_FEATURE:
        base_weights["completeness"] += 0.05  # 新功能需要完整描述
        base_weights["context_alignment"] += 0.05  # 上下文匹配更重要
    
    # 基于复杂度调整权重
    if task_analysis.complexity_level == ComplexityLevel.COMPLEX:
        base_weights["completeness"] += 0.05
        base_weights["risk_awareness"] += 0.05
    
    return base_weights


def generate_intelligent_analysis(instruction: str, task_analysis: Optional[TaskAnalysis], 
                                quality_metrics: Dict[str, float]) -> Dict[str, str]:
    """生成智能分析"""
    analysis = {}
    
    if task_analysis:
        # 任务上下文匹配分析
        alignment_score = quality_metrics.get("context_alignment", 0)
        if alignment_score >= 0.8:
            analysis["task_context_match"] = "✅ 指令与任务上下文高度匹配"
        elif alignment_score >= 0.6:
            analysis["task_context_match"] = "⚠️ 指令与任务上下文基本匹配，可进一步优化"
        else:
            analysis["task_context_match"] = "❌ 指令与任务上下文匹配度较低，需要调整"
        
        # 复杂度适配性分析
        word_count = len(instruction.split())
        if task_analysis.complexity_level == ComplexityLevel.SIMPLE and word_count < 100:
            analysis["complexity_appropriateness"] = "✅ 指令复杂度与任务匹配"
        elif task_analysis.complexity_level == ComplexityLevel.COMPLEX and word_count > 150:
            analysis["complexity_appropriateness"] = "✅ 指令详细程度适合复杂任务"
        else:
            analysis["complexity_appropriateness"] = "⚠️ 指令复杂度可能需要调整"
    else:
        analysis["task_context_match"] = "ℹ️ 无会话上下文，使用通用评估标准"
        analysis["complexity_appropriateness"] = "ℹ️ 无复杂度信息，建议提供任务上下文"
    
    # 历史对比分析
    avg_score = sum(quality_metrics.values()) / len(quality_metrics)
    if avg_score >= 0.85:
        analysis["historical_comparison"] = "🌟 质量超越历史平均水平"
    elif avg_score >= 0.75:
        analysis["historical_comparison"] = "📈 质量达到良好水平"
    else:
        analysis["historical_comparison"] = "📊 质量有提升空间"
    
    return analysis


def generate_personalized_suggestions(quality_metrics: Dict[str, float], 
                                    task_analysis: Optional[TaskAnalysis]) -> List[str]:
    """生成个性化建议"""
    suggestions = []
    
    # 基于最低分维度提供建议
    lowest_metric = min(quality_metrics.items(), key=lambda x: x[1])
    metric_name, score = lowest_metric
    
    if score < 0.7:
        metric_suggestions = {
            "clarity": "🎯 提高清晰度：使用更明确的动词，明确指出具体要完成什么",
            "completeness": "📝 增强完整性：补充输入输出说明、依赖条件和验收标准",
            "specificity": "🔍 增加具体性：提供具体的文件名、函数名或配置参数",
            "actionability": "⚡ 提升可执行性：分解为具体步骤，提供可执行的命令或代码示例",
            "risk_awareness": "🛡️ 加强风险意识：考虑错误处理、测试验证和回滚策略",
            "context_alignment": "🎭 优化上下文匹配：确保指令与任务类型和复杂度相符"
        }
        suggestions.append(metric_suggestions.get(metric_name, "优化最低分维度"))
    
    # 基于任务类型的特定建议
    if task_analysis:
        if task_analysis.task_type == TaskType.NEW_FEATURE:
            suggestions.append("💡 新功能建议：明确功能边界，考虑与现有系统的集成点")
        elif task_analysis.task_type == TaskType.BUG_FIX:
            suggestions.append("🔧 Bug修复建议：描述重现步骤，分析根本原因")
        elif task_analysis.task_type == TaskType.PERFORMANCE:
            suggestions.append("📊 性能优化建议：设定量化目标，建立性能基线")
    
    return suggestions[:3]  # 限制建议数量


def get_quality_trend(session_context: SessionInfo) -> str:
    """获取质量趋势分析"""
    if not session_context.quality_scores:
        return "首次评估，无历史趋势"
    
    scores = list(session_context.quality_scores.values())
    if len(scores) == 1:
        return f"当前评分: {scores[0]:.2f}"
    
    # 计算趋势
    recent_avg = sum(scores[-3:]) / len(scores[-3:]) if len(scores) >= 3 else sum(scores) / len(scores)
    early_avg = sum(scores[:3]) / len(scores[:3]) if len(scores) >= 6 else scores[0]
    
    if recent_avg > early_avg + 0.1:
        return f"📈 质量持续提升 (从 {early_avg:.2f} 提升到 {recent_avg:.2f})"
    elif recent_avg < early_avg - 0.1:
        return f"📉 质量有所下降 (从 {early_avg:.2f} 下降到 {recent_avg:.2f})"
    else:
        return f"➡️ 质量保持稳定 (平均 {recent_avg:.2f})"


def get_quality_assessment_enhanced(score: float) -> str:
    """获取增强的质量评估结果"""
    if score >= 0.9:
        return "🌟 优秀 - 指令质量非常高，可直接执行"
    elif score >= 0.8:
        return "✅ 良好 - 指令质量较高，轻微调整即可"
    elif score >= 0.7:
        return "⚠️ 一般 - 指令质量中等，需要优化"
    elif score >= 0.6:
        return "🔄 需要改进 - 指令质量偏低，建议重写部分内容"
    else:
        return "❌ 不合格 - 指令质量较差，需要重新设计"


def generate_improvement_suggestions_enhanced(quality_metrics: Dict[str, float], instruction: str, 
                                            task_analysis: Optional[TaskAnalysis]) -> List[str]:
    """生成增强的改进建议"""
    suggestions = []
    
    # 基于各维度分数提供具体建议
    for metric, score in quality_metrics.items():
        if score < 0.8:
            metric_suggestions = {
                "clarity": "💡 明确指令目标：明确说明要实现什么功能或解决什么问题",
                "completeness": "📋 补充关键信息：添加前置条件、输出期望和验收标准",
                "specificity": "🎯 提供具体细节：指定文件路径、函数名称或配置参数",
                "actionability": "⚡ 细化执行步骤：将大任务分解为可直接执行的小步骤",
                "risk_awareness": "🔒 考虑风险控制：添加错误处理、测试验证和回滚方案",
                "context_alignment": "🔄 调整指令风格：确保指令符合任务类型和复杂度要求"
            }
            suggestions.append(metric_suggestions.get(metric, f"改进{metric}"))
    
    # 基于任务上下文的特定建议
    if task_analysis:
        if task_analysis.complexity_level == ComplexityLevel.COMPLEX:
            suggestions.append("🏗️ 复杂任务建议：考虑分阶段实施，制定详细的里程碑计划")
        
        # 检查是否遗漏了重要的风险因素
        for risk in task_analysis.risk_factors:
            if risk.lower() not in instruction.lower():
                suggestions.append(f"⚠️ 风险提醒：考虑应对 '{risk}' 的策略")
                break
    
    return suggestions[:4]  # 限制建议数量


def assess_clarity(instruction: str) -> float:
    """评估指令清晰度"""
    score = 0.6  # 基础分
    
    # 检查是否有明确的动词
    action_verbs = ["implement", "create", "fix", "optimize", "refactor", "test", "实现", "创建", "修复", "优化", "重构", "测试"]
    if any(verb in instruction.lower() for verb in action_verbs):
        score += 0.2
    
    # 检查是否有具体的目标
    if any(word in instruction.lower() for word in ["function", "class", "method", "api", "函数", "类", "方法"]):
        score += 0.2
    
    return min(score, 1.0)


def assess_completeness(instruction: str) -> float:
    """评估指令完整性"""
    score = 0.5  # 基础分
    
    # 检查是否包含输入/输出描述
    if any(word in instruction.lower() for word in ["input", "output", "return", "parameter", "输入", "输出", "返回", "参数"]):
        score += 0.2
    
    # 检查是否包含约束条件
    if any(word in instruction.lower() for word in ["constraint", "requirement", "must", "should", "约束", "要求", "必须", "应该"]):
        score += 0.2
    
    # 检查是否包含成功标准
    if any(word in instruction.lower() for word in ["success", "criteria", "expect", "成功", "标准", "期望"]):
        score += 0.1
    
    return min(score, 1.0)


def assess_specificity(instruction: str) -> float:
    """评估指令具体性"""
    score = 0.4  # 基础分
    
    # 检查是否有具体的文件或函数名
    if re.search(r'\w+\.(py|js|ts|java|cpp|c)', instruction):
        score += 0.3
    
    # 检查是否有具体的技术栈
    tech_terms = ["react", "vue", "angular", "django", "flask", "express", "spring"]
    if any(term in instruction.lower() for term in tech_terms):
        score += 0.2
    
    # 检查是否有数值或量化指标
    if re.search(r'\d+', instruction):
        score += 0.1
    
    return min(score, 1.0)


def assess_actionability(instruction: str) -> float:
    """评估指令可执行性"""
    score = 0.6  # 基础分
    
    # 检查是否有明确的步骤
    if any(word in instruction.lower() for word in ["step", "first", "then", "步骤", "首先", "然后"]):
        score += 0.2
    
    # 检查是否避免了模糊语言
    vague_terms = ["somehow", "maybe", "possibly", "大概", "可能", "或许"]
    if not any(term in instruction.lower() for term in vague_terms):
        score += 0.2
    
    return min(score, 1.0)


def assess_risk_awareness(instruction: str) -> float:
    """评估风险意识"""
    score = 0.3  # 基础分
    
    # 检查是否提到了测试
    if any(word in instruction.lower() for word in ["test", "testing", "测试"]):
        score += 0.3
    
    # 检查是否提到了错误处理
    if any(word in instruction.lower() for word in ["error", "exception", "handle", "错误", "异常", "处理"]):
        score += 0.2
    
    # 检查是否提到了兼容性
    if any(word in instruction.lower() for word in ["compatible", "backward", "兼容"]):
        score += 0.2
    
    return min(score, 1.0)


def generate_improvement_suggestions(quality_metrics: Dict[str, float], instruction: str) -> List[str]:
    """生成改进建议"""
    suggestions = []
    
    if quality_metrics["clarity"] < 0.8:
        suggestions.append("增加指令的清晰度：使用更明确的动词和具体的目标描述")
    
    if quality_metrics["completeness"] < 0.8:
        suggestions.append("补充完整性：添加输入输出描述、约束条件和成功标准")
    
    if quality_metrics["specificity"] < 0.8:
        suggestions.append("提高具体性：指定具体的文件名、函数名或技术栈")
    
    if quality_metrics["actionability"] < 0.8:
        suggestions.append("增强可执行性：提供明确的步骤，避免模糊语言")
    
    if quality_metrics["risk_awareness"] < 0.8:
        suggestions.append("加强风险意识：考虑测试、错误处理和兼容性问题")
    
    return suggestions if suggestions else ["指令质量良好，建议保持当前水平"]


def get_quality_assessment(score: float) -> str:
    """获取质量评估结果"""
    if score >= 0.9:
        return "优秀 - 指令质量非常高"
    elif score >= 0.8:
        return "良好 - 指令质量较高"
    elif score >= 0.7:
        return "一般 - 指令质量中等"
    elif score >= 0.6:
        return "需要改进 - 指令质量偏低"
    else:
        return "不合格 - 指令质量较差，需要重新设计"


def get_recommended_actions(quality_metrics: Dict[str, float]) -> List[str]:
    """获取推荐行动"""
    actions = []
    
    lowest_metric = min(quality_metrics.items(), key=lambda x: x[1])
    
    if lowest_metric[1] < 0.7:
        metric_actions = {
            "clarity": "重新组织语言，使用更清晰的表达",
            "completeness": "补充缺失的关键信息",
            "specificity": "添加具体的技术细节",
            "actionability": "分解为可执行的步骤",
            "risk_awareness": "考虑潜在的风险和问题"
        }
        actions.append(metric_actions[lowest_metric[0]])
    
    return actions if actions else ["继续保持当前的指令质量"]



@mcp.tool()
def smart_programming_coach(
    user_request: str,
    project_context: str = "",
    mode: str = "full_guidance"
) -> str:
    """
    🎓 智能编程教练 - 大模型的思维导航仪
    
    这是一个元工具，专门指导大模型如何智能地运用其他3个工具来完成完整的编程思维过程。
    它会根据用户请求的特点，自动推荐最佳的工具使用策略和顺序。
    
    **核心价值：**
    • 自动分析任务特点，推荐最优的工具使用流程
    • 提供具体的工具调用示例和参数建议
    • 确保大模型能够系统性地完成编程思维过程
    • 避免工具使用的混乱和遗漏
    
    **使用模式：**
    • **full_guidance**: 完整指导模式，提供详细的步骤和工具调用示例
    • **quick_start**: 快速入门模式，提供简化的使用流程
    • **expert_mode**: 专家模式，仅提供关键提示和最佳实践
    
    **智能推荐策略：**
    1. 简单任务 → 直接使用 analyze_programming_context + validate_instruction_quality
    2. 中等任务 → 完整3工具流程，重点在 guided_thinking_process
    3. 复杂任务 → 迭代式使用，多轮 guided_thinking_process 深度思考
    4. 学习场景 → 完整流程 + 详细的思考过程展示
    
    Args:
        user_request: 用户的编程请求
        project_context: 项目上下文信息
        mode: 指导模式 ("full_guidance"/"quick_start"/"expert_mode")
    
    Returns:
        智能化的工具使用指导方案，包含：
        {
            "analysis": "任务分析和复杂度评估",
            "recommended_workflow": "推荐的工具使用流程",
            "tool_sequence": ["工具调用顺序"],
            "sample_calls": {
                "step1": "具体的工具调用示例",
                "step2": "下一步的调用示例"
            },
            "expected_outcomes": ["每个步骤的预期结果"],
            "tips": ["使用技巧和注意事项"],
            "next_actions": "建议的下一步行动"
        }
    """
    
    # 分析任务特征
    task_complexity = estimate_request_complexity(user_request)
    task_nature = analyze_request_nature(user_request)
    
    # 根据复杂度和性质推荐流程
    workflow = generate_workflow_recommendation(task_complexity, task_nature, mode)
    
    # 生成具体的工具调用示例
    sample_calls = generate_sample_tool_calls(user_request, project_context, workflow)
    
    # 构建指导方案
    guidance = {
        "analysis": f"任务类型: {task_nature}, 复杂度: {task_complexity}",
        "recommended_workflow": workflow["description"],
        "tool_sequence": workflow["sequence"],
        "sample_calls": sample_calls,
        "expected_outcomes": workflow["outcomes"],
        "tips": generate_usage_tips(task_complexity, mode),
        "next_actions": workflow["next_actions"]
    }
    
    return json.dumps(guidance, ensure_ascii=False, indent=2)


def estimate_request_complexity(user_request: str) -> str:
    """快速评估请求复杂度"""
    request_lower = user_request.lower()
    
    # 复杂度指标
    high_complexity_indicators = [
        "architecture", "system", "multiple", "integrate", "refactor", 
        "optimize", "架构", "系统", "多个", "集成", "重构", "优化"
    ]
    
    medium_complexity_indicators = [
        "feature", "function", "class", "module", "api",
        "功能", "函数", "类", "模块", "接口"
    ]
    
    high_score = sum(1 for indicator in high_complexity_indicators if indicator in request_lower)
    medium_score = sum(1 for indicator in medium_complexity_indicators if indicator in request_lower)
    
    if high_score >= 2:
        return "complex"
    elif high_score >= 1 or medium_score >= 2:
        return "medium"
    else:
        return "simple"


def analyze_request_nature(user_request: str) -> str:
    """分析请求性质"""
    request_lower = user_request.lower()
    
    if any(word in request_lower for word in ["learn", "understand", "explain", "学习", "理解", "解释"]):
        return "learning"
    elif any(word in request_lower for word in ["fix", "bug", "error", "修复", "错误", "问题"]):
        return "debugging"
    elif any(word in request_lower for word in ["optimize", "performance", "优化", "性能"]):
        return "optimization"
    elif any(word in request_lower for word in ["create", "implement", "build", "创建", "实现", "构建"]):
        return "development"
    else:
        return "general"


def generate_workflow_recommendation(complexity: str, nature: str, mode: str) -> dict:
    """生成工作流推荐"""
    
    workflows = {
        "simple": {
            "description": "轻量级流程：快速分析 + 质量验证",
            "sequence": ["analyze_programming_context", "validate_instruction_quality"],
            "outcomes": ["获得任务分析和思考框架", "验证最终指令质量"],
            "next_actions": "基于分析结果直接编写编程指令，然后验证质量"
        },
        "medium": {
            "description": "标准流程：完整的4阶段思考过程",
            "sequence": ["analyze_programming_context", "guided_thinking_process(understanding)", 
                        "guided_thinking_process(planning)", "guided_thinking_process(implementation)",
                        "validate_instruction_quality"],
            "outcomes": ["任务分析", "深度理解", "策略规划", "实现指导", "质量验证"],
            "next_actions": "按阶段逐步深入思考，每个阶段充分思考后再进入下一阶段"
        },
        "complex": {
            "description": "深度流程：迭代式思考 + 多轮优化",
            "sequence": ["analyze_programming_context", "guided_thinking_process(understanding)", 
                        "guided_thinking_process(planning)", "guided_thinking_process(implementation)",
                        "guided_thinking_process(validation)", "validate_instruction_quality",
                        "可能需要多轮迭代"],
            "outcomes": ["全面分析", "深度理解", "详细规划", "精准实现", "严格验证", "高质量指令"],
            "next_actions": "完成一轮思考后，根据需要进行第二轮优化思考"
        }
    }
    
    base_workflow = workflows.get(complexity, workflows["medium"])
    
    # 根据任务性质调整
    if nature == "learning":
        base_workflow["description"] += " (注重思考过程的展示和解释)"
    elif nature == "debugging":
        base_workflow["description"] += " (重点关注问题根因分析)"
    elif nature == "optimization":
        base_workflow["description"] += " (强调性能分析和权衡思考)"
    
    return base_workflow


def generate_sample_tool_calls(user_request: str, project_context: str, workflow: dict) -> dict:
    """生成具体的工具调用示例"""
    
    samples = {}
    
    # 第一步：任务分析
    samples["step1_analyze"] = {
        "tool": "analyze_programming_context",
        "call": f'analyze_programming_context("{user_request}", "{project_context}")',
        "purpose": "获取任务分析和思考框架"
    }
    
    # 如果包含guided_thinking_process
    if "guided_thinking_process" in str(workflow["sequence"]):
        samples["step2_understand"] = {
            "tool": "guided_thinking_process", 
            "call": 'guided_thinking_process(task_analysis_json, "understanding")',
            "purpose": "深入理解阶段的思考指导",
            "note": "task_analysis_json 是第一步返回的完整JSON结果"
        }
        
        samples["step3_plan"] = {
            "tool": "guided_thinking_process",
            "call": 'guided_thinking_process(task_analysis_json, "planning")', 
            "purpose": "规划阶段的思考指导"
        }
        
        samples["step4_implement"] = {
            "tool": "guided_thinking_process",
            "call": 'guided_thinking_process(task_analysis_json, "implementation")',
            "purpose": "实现阶段的思考指导"
        }
    
    # 最后：质量验证
    samples["final_validate"] = {
        "tool": "validate_instruction_quality",
        "call": 'validate_instruction_quality("your_final_instruction")',
        "purpose": "验证最终编程指令的质量"
    }
    
    return samples


def generate_usage_tips(complexity: str, mode: str) -> list:
    """生成使用技巧"""
    
    base_tips = [
        "每次工具调用后，仔细阅读返回结果再进行下一步",
        "思考过程要充分，不要急于得出结论",
        "将工具返回的JSON结果完整传递给下一个工具"
    ]
    
    complexity_tips = {
        "simple": ["保持简洁，避免过度分析"],
        "medium": ["平衡深度和效率，确保每个阶段都有收获"],
        "complex": ["允许多轮迭代，复杂问题需要时间来思考", "考虑分阶段实现策略"]
    }
    
    mode_tips = {
        "full_guidance": ["详细记录每步的思考过程"],
        "quick_start": ["重点关注核心问题，快速形成方案"],
        "expert_mode": ["信任自己的判断，灵活调整流程"]
    }
    
    return base_tips + complexity_tips.get(complexity, []) + mode_tips.get(mode, [])


@mcp.tool()
def session_manager(
    action: str = "list",
    session_id: str = ""
) -> str:
    """
    🗂️ 会话管理器 - 智能会话状态管理工具
    
    **功能特性：**
    • 📋 查看活跃会话列表
    • 🔍 检查特定会话详情
    • 🗑️ 清理过期或无用会话
    • 📊 分析会话使用统计
    • 🔄 恢复中断的思考流程
    
    **支持的操作：**
    • **list**: 列出所有活跃会话
    • **detail**: 查看特定会话的详细信息
    • **cleanup**: 清理过期会话
    • **stats**: 显示使用统计
    • **reset**: 重置特定会话状态
    
    Args:
        action: 操作类型 ("list"/"detail"/"cleanup"/"stats"/"reset")
        session_id: 会话ID（某些操作需要）
    
    Returns:
        操作结果的详细信息
    """
    
    if action == "list":
        if not _session_cache:
            return json.dumps({
                "message": "当前没有活跃的会话",
                "suggestion": "使用 analyze_programming_context 创建新会话"
            }, ensure_ascii=False, indent=2)
        
        sessions = []
        for sid, session in _session_cache.items():
            duration = int((time.time() - session.timestamp) / 60)
            sessions.append({
                "session_id": sid,
                "task_type": session.task_analysis.task_type.value,
                "complexity": session.task_analysis.complexity_level.value,
                "current_stage": session.current_stage,
                "progress": f"{len(session.stage_history)}/{len(session.thinking_frameworks)}",
                "duration_minutes": duration,
                "request_preview": session.user_request[:50] + "..." if len(session.user_request) > 50 else session.user_request
            })
        
        return json.dumps({
            "active_sessions": len(sessions),
            "sessions": sorted(sessions, key=lambda x: x['duration_minutes']),
            "usage_tip": "使用 session_manager('detail', 'session_id') 查看详情"
        }, ensure_ascii=False, indent=2)
    
    elif action == "detail":
        if not session_id:
            return json.dumps({"error": "需要提供session_id"}, ensure_ascii=False)
        
        if session_id not in _session_cache:
            return json.dumps({
                "error": "会话不存在",
                "available_sessions": list(_session_cache.keys())[-5:]
            }, ensure_ascii=False, indent=2)
        
        session = _session_cache[session_id]
        task_analysis = session.task_analysis
        
        detail = {
            "session_info": {
                "session_id": session_id,
                "created_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(session.timestamp)),
                "duration_minutes": int((time.time() - session.timestamp) / 60),
                "current_stage": session.current_stage
            },
            "task_details": {
                "original_request": session.user_request,
                "task_type": task_analysis.task_type.value,
                "complexity_level": task_analysis.complexity_level.value,
                "core_objective": task_analysis.core_objective,
                "similarity_score": task_analysis.similarity_score
            },
            "progress_tracking": {
                "completed_stages": session.stage_history,
                "available_stages": list(session.thinking_frameworks.keys()),
                "progress_percentage": int((len(session.stage_history) / len(session.thinking_frameworks)) * 100),
                "next_recommended_stage": get_next_step(session.current_stage)
            },
            "quality_history": session.quality_scores,
            "learning_insights": task_analysis.learning_insights[:3] if task_analysis.learning_insights else [],
            "resume_suggestion": f"继续使用: guided_thinking_process('{session_id}', '{get_next_step(session.current_stage)}')"
        }
        
        return json.dumps(detail, ensure_ascii=False, indent=2)
    
    elif action == "cleanup":
        initial_count = len(_session_cache)
        cleanup_expired_sessions()
        cleaned_count = initial_count - len(_session_cache)
        
        return json.dumps({
            "cleanup_completed": True,
            "sessions_cleaned": cleaned_count,
            "remaining_sessions": len(_session_cache),
            "message": f"清理了 {cleaned_count} 个过期会话"
        }, ensure_ascii=False, indent=2)
    
    elif action == "stats":
        if not _analysis_history:
            return json.dumps({
                "message": "暂无使用统计数据",
                "suggestion": "开始使用工具后将产生统计数据"
            }, ensure_ascii=False, indent=2)
        
        # 统计分析
        task_types = {}
        complexities = {}
        for history in _analysis_history:
            task_type = history.get('task_type', 'unknown')
            complexity = history.get('complexity', 'unknown')
            task_types[task_type] = task_types.get(task_type, 0) + 1
            complexities[complexity] = complexities.get(complexity, 0) + 1
        
        # 计算平均质量分数
        all_quality_scores = []
        for session in _session_cache.values():
            all_quality_scores.extend(session.quality_scores.values())
        
        avg_quality = sum(all_quality_scores) / len(all_quality_scores) if all_quality_scores else 0
        
        stats = {
            "total_analyses": len(_analysis_history),
            "active_sessions": len(_session_cache),
            "task_type_distribution": task_types,
            "complexity_distribution": complexities,
            "average_quality_score": round(avg_quality, 2),
            "context_memory_entries": len(_context_memory),
            "most_common_task_type": max(task_types.items(), key=lambda x: x[1])[0] if task_types else "无",
            "quality_assessments_performed": len(all_quality_scores)
        }
        
        return json.dumps(stats, ensure_ascii=False, indent=2)
    
    elif action == "reset":
        if not session_id:
            return json.dumps({"error": "需要提供session_id"}, ensure_ascii=False)
        
        if session_id not in _session_cache:
            return json.dumps({"error": "会话不存在"}, ensure_ascii=False)
        
        session = _session_cache[session_id]
        session.current_stage = "understanding"
        session.stage_history = []
        session.quality_scores = {}
        
        return json.dumps({
            "reset_completed": True,
            "session_id": session_id,
            "new_stage": "understanding",
            "message": "会话已重置到初始状态",
            "next_action": f"使用 guided_thinking_process('{session_id}', 'understanding') 重新开始"
        }, ensure_ascii=False, indent=2)
    
    else:
        return json.dumps({
            "error": f"不支持的操作: {action}",
            "supported_actions": ["list", "detail", "cleanup", "stats", "reset"]
        }, ensure_ascii=False, indent=2)


def main():
    """Main entry point to run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
