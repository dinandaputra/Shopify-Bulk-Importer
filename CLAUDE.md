# CLAUDE.md

This file provides **MANDATORY** guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🤖 MANDATORY: Claude Code Sub-Agent System Framework

**CRITICAL**: Every new session MUST use the Claude Code Sub-Agent System. This is not optional.

### 📋 SESSION STARTUP PROTOCOL (MANDATORY)

#### 1. REQUIRED READING - Session Start Checklist
**Before any work begins, agents MUST read these files in order:**

1. **`.ai/context/CODEBASE_STATE.md`** - Current system status and architecture overview
2. **`.ai/context/WORK_LOG.md`** - Recent development work and progress  
3. **`.ai/context/KNOWN_ISSUES.md`** - Active issues and blockers
4. **`.ai/agents/GENERAL_RULES.md`** - Core principles and protected systems (if exists)
5. **Claude Code Sub-Agents** available in `.claude/agents/`:
   - `code-quality-architect` - Architecture, testing, performance
   - `shopify-api-developer` - API integration, metaobjects  
   - `shopify-research-specialist` - Research, documentation, product specs
   - `product-strategy-advisor` - Features, UX, business logic
   - `test-coverage-specialist` - Comprehensive testing support
   - `ux-design-specialist` - UI/UX design and optimization

#### 2. MANDATORY QUALITY GATES
**Every task MUST follow these quality checkpoints:**

1. **PRE-CODING**: Read `.ai/checklists/PRE_CODING.md` before starting work
2. **PRE-COMMIT**: Read `.ai/checklists/PRE_COMMIT.md` before committing
3. **CODE REVIEW**: Use `.ai/checklists/CODE_REVIEW.md` for all reviews

#### 3. REQUIRED PROGRESS LOGGING
**Agents MUST update these files during work:**

- **`.ai/context/WORK_LOG.md`** - Log all significant work completed (MANDATORY - update at end of session)
- **`.ai/context/CODEBASE_STATE.md`** - Update when major changes made
- **`.ai/context/KNOWN_ISSUES.md`** - Log new issues discovered
- **`.ai/context/ARCHITECTURE_DECISIONS.md`** - Document architectural decisions

#### 4. WORKFLOW SELECTION (MANDATORY)
**Choose appropriate workflow based on task type:**

- **New Features**: Follow `.ai/workflows/feature_implementation.md`
- **Bug Fixes**: Follow `.ai/workflows/bug_fixing.md`  
- **Code Changes**: Follow `.ai/workflows/code_review.md`

#### 5. PATTERN APPLICATION (MANDATORY)
**Use established patterns from:**

- **`.ai/patterns/api_patterns.md`** - For Shopify API work
- **`.ai/patterns/ui_patterns.md`** - For Streamlit UI development
- **`.ai/patterns/testing_patterns.md`** - For all testing work

### 🎯 CLAUDE CODE SUB-AGENT SELECTION GUIDE (MANDATORY)

**Task Type → Required Sub-Agent(s):**

| Task Type | Primary Sub-Agent | Secondary Sub-Agent |
|-----------|-------------------|---------------------|
| Architecture Changes | code-quality-architect | - |
| API Integration | shopify-api-developer | - |
| Technology Research | shopify-research-specialist | - |
| Product Research | shopify-research-specialist | - |
| Market Analysis | shopify-research-specialist | product-strategy-advisor |
| UX/Workflow Design | ux-design-specialist | product-strategy-advisor |
| Feature Planning | product-strategy-advisor | - |
| Bug Investigation | code-quality-architect | - |
| Performance Issues | code-quality-architect | shopify-api-developer |
| Testing Implementation | test-coverage-specialist | code-quality-architect |
| UI/UX Improvements | ux-design-specialist | - |

### ⚠️ CRITICAL PROTECTED SYSTEMS (DO NOT MODIFY)

**ONLY shopify-api-developer sub-agent can modify these systems:**

1. **Variant Metafield System** - `services/shopify_api.py:assign_metafields_to_variants()`
2. **SIM Carrier Variants** - Working 1-5 variant creation logic
3. **GraphQL Mutations** - All working GraphQL metafield operations

### 📚 COMPLETE UTILIZATION GUIDE

**For comprehensive guidance, always reference:**
- **`.ai/AGENT_UTILIZATION_GUIDE.md`** - Complete 1,200+ line guide with examples, scenarios, and best practices

### 🔄 SESSION HANDOFF TEMPLATE (MANDATORY)

**When ending a session, MUST provide:**

```markdown
## Session Handoff Summary
### Agent: [Current Agent Role]
### Work Completed:
- [Task 1] - Status and outcome
- [Task 2] - Status and outcome

### Files Modified:
- [List all changed files]

### Next Steps:
1. [High priority task]
2. [Medium priority task]

### Important Notes:
- [Any constraints or considerations]
- [Dependencies identified]
- [Issues encountered]
```

---

## 📖 Project Documentation

### Quick Project Context
Shopify Bulk Importer - Streamlit web app for MyByte International staff to efficiently input used electronics data and create products directly in Shopify via API integration.

### Documentation Structure
- **CODEBASE_OVERVIEW.md** - Project context, architecture, commands, and current status
- **TECHNICAL_REFERENCE.md** - Implementation details, API documentation, and development guides
- **CLAUDE.md** (this file) - AI Agent System Framework and behavior instructions

### Essential Quick Reference
- **Running**: `streamlit run streamlit_app.py`
- **Store**: jufbtk-ut.myshopify.com (JPY currency, Japan timezone)
- **Products**: Smartphones (with SIM variants) and Laptops (with templates)
- **Status**: Phase 5 complete - AI Agent System operational

---

## 🚨 FINAL REMINDER: MANDATORY CLAUDE CODE SUB-AGENT SYSTEM

**Every new session MUST:**

1. **START** by reading the 5 required context files
2. **IDENTIFY** appropriate Claude Code sub-agent(s) for the task
3. **USE** Claude Code sub-agents via Task tool: `Use the [sub-agent-name] to [task description]`
4. **FOLLOW** established workflows and patterns
5. **USE** mandatory quality gates (PRE-CODING, PRE-COMMIT, CODE_REVIEW)
6. **LOG** progress in WORK_LOG.md at session end
7. **PROTECT** critical systems (variant metafields, SIM carrier variants)

**Available Claude Code Sub-Agents:**
- `code-quality-architect` - Architecture, testing, performance optimization
- `shopify-api-developer` - Shopify API integration, metaobjects, webhooks
- `shopify-research-specialist` - Research, documentation, product specifications
- `product-strategy-advisor` - Feature planning, workflow optimization, business logic
- `test-coverage-specialist` - Comprehensive testing and coverage analysis
- `ux-design-specialist` - UI/UX design, accessibility, user experience optimization

**No exceptions. This framework ensures:**
- ✅ Consistent quality and standards
- ✅ Context preservation across sessions  
- ✅ Protection of working systems
- ✅ Efficient collaboration with specialized expertise
- ✅ Knowledge sharing and documentation

**The Claude Code Sub-Agent System is now the ONLY approved way to work on this project.**

