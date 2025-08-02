# Claude Code Sub-Agent System Migration

## Migration Completed: 2025-08-02

The project has successfully migrated from the custom `.ai/agents/` documentation system to the official Claude Code Sub-Agent System located in `.claude/agents/`.

## Agent Mapping

| Old Agent Name | New Sub-Agent Name | Description |
|----------------|-------------------|-------------|
| Web Research Specialist | `shopify-research-specialist` | Research and market analysis |
| Code Quality Architect | `code-quality-architect` | Architecture, testing, performance |
| Shopify API Developer | `shopify-api-developer` | API integration specialist |
| Product Strategy Advisor | `product-strategy-advisor` | Product planning and UX |
| N/A | `test-coverage-specialist` | Comprehensive testing support |
| N/A | `ux-design-specialist` | UI/UX design optimization |

## Available Claude Code Sub-Agents

All sub-agents are now properly configured in `.claude/agents/` with:
- ✅ YAML frontmatter with name, description, and tools
- ✅ Focused, specialized responsibilities
- ✅ Appropriate tool access restrictions
- ✅ Protected system awareness

## Usage

Use sub-agents via the Task tool:
```
Use the shopify-research-specialist to research smartphone trends
Use the code-quality-architect to review this code
Use the shopify-api-developer to optimize API calls
```

## Legacy References

Historical references to old agent names in documentation files (`.ai/`, `CODEBASE_RESTRUCTURING_PLAN.md`, `archive/`) have been preserved for historical context but should not be used for new work.

**All new work MUST use the Claude Code Sub-Agent System.**