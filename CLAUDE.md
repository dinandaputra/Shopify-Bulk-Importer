# CLAUDE.md

This file provides **MANDATORY** guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🤖 MANDATORY: AI Agent System Framework

**CRITICAL**: Every new session MUST use the comprehensive AI Agent System. This is not optional.

### 📋 SESSION STARTUP PROTOCOL (MANDATORY)

#### 1. REQUIRED READING - Session Start Checklist
**Before any work begins, agents MUST read these files in order:**

1. **`.ai/context/CODEBASE_STATE.md`** - Current system status and architecture overview
2. **`.ai/context/WORK_LOG.md`** - Recent development work and progress  
3. **`.ai/context/KNOWN_ISSUES.md`** - Active issues and blockers
4. **`.ai/agents/GENERAL_RULES.md`** - Core principles and protected systems
5. **Relevant agent role file** from `.ai/agents/` based on task type:
   - `code-quality-architect.md` - Architecture, testing, performance
   - `shopify-api-developer.md` - API integration, metaobjects  
   - `web-research-specialist.md` - Research, documentation, product specs
   - `product-strategy-advisor.md` - Features, UX, business logic

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

### 🎯 AGENT SELECTION GUIDE (MANDATORY)

**Task Type → Required Agent(s):**

| Task Type | Primary Agent | Secondary Agent |
|-----------|---------------|-----------------|
| Architecture Changes | Code Quality Architect | - |
| API Integration | Shopify API Developer | - |
| Technology Research | Web Research Specialist | - |
| Product Research | Web Research Specialist | - |
| Market Analysis | Web Research Specialist | Product Strategy Advisor |
| UX/Workflow | Product Strategy Advisor | - |
| Bug Investigation | Code Quality Architect | Domain Specialist |
| Performance Issues | Code Quality Architect | Shopify API Developer |
| Documentation | Web Research Specialist | Domain Expert |
| Template Creation | Web Research Specialist | Product Strategy Advisor |

### ⚠️ CRITICAL PROTECTED SYSTEMS (DO NOT MODIFY)

**ONLY Shopify API Developer can modify these systems:**

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

## 🚨 FINAL REMINDER: MANDATORY AI AGENT SYSTEM

**Every new session MUST:**

1. **START** by reading the 5 required context files
2. **IDENTIFY** appropriate agent role(s) for the task
3. **FOLLOW** established workflows and patterns
4. **USE** mandatory quality gates (PRE-CODING, PRE-COMMIT, CODE_REVIEW)
5. **LOG** progress in WORK_LOG.md at session end
6. **PROTECT** critical systems (variant metafields, SIM carrier variants)
7. **REFERENCE** `.ai/AGENT_UTILIZATION_GUIDE.md` for comprehensive guidance

**No exceptions. This framework ensures:**
- ✅ Consistent quality and standards
- ✅ Context preservation across sessions  
- ✅ Protection of working systems
- ✅ Efficient collaboration
- ✅ Knowledge sharing and documentation

**The AI Agent System is now the ONLY approved way to work on this project.**

