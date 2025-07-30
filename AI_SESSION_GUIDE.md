# AI Session Management Guide for Shopify Bulk Importer

> **Purpose**: This guide helps you (the human developer) effectively manage AI-assisted coding sessions for the Shopify Bulk Importer restructuring project.

## Table of Contents
1. [Quick Start Templates](#quick-start-templates)
2. [Session Types](#session-types)
3. [Effective Communication Patterns](#effective-communication-patterns)
4. [Phase-Specific Instructions](#phase-specific-instructions)
5. [Power Commands](#power-commands)
6. [Efficiency Tips](#efficiency-tips)
7. [Troubleshooting](#troubleshooting)
8. [Session Closing](#session-closing)

---

## Quick Start Templates

### 🚀 Generic Session Starter
```
I need to work on [SPECIFIC TASK] from the CODEBASE_RESTRUCTURING_PLAN.md.

1. First, read the restructuring plan and check current progress
2. Create a todo list for this session
3. Implement [SPECIFIC PHASE/TASK]
4. Work autonomously on read operations
5. Update progress as you go

Begin.
```

### 📚 Phase 1: Documentation & Cleanup
```
Let's implement Phase 1 of the restructuring plan. 

1. Read CODEBASE_RESTRUCTURING_PLAN.md
2. Create session todos for Phase 1 tasks
3. Start with creating README.md (Task 1.1)
4. Then organize test files (Task 1.2)
5. Clean root directory (Task 1.3)
6. Test everything still works after moves

Work autonomously and use any agents needed.
```

### 🔧 Configuration Consolidation
```
Time to consolidate configuration files (Phase 2).

1. Analyze all duplicate config files
2. Show me comparison of laptop metafield files
3. Recommend which to keep
4. Consolidate into single files
5. Update all imports
6. Test the application

Use the shopify-api-developer agent for Shopify-specific decisions.
```

### 🏗️ Architecture Implementation
```
Implement [SPECIFIC ARCHITECTURE PATTERN] from Phase 4.

1. Review current architecture in services/
2. Create implementation plan
3. Implement without breaking existing code
4. Add tests for new components
5. Update documentation

Use code-quality-architect agent for design decisions.
```

---

## Session Types

### 1. Analysis Session
**When**: Before making any changes
**Template**:
```
I need to understand [ASPECT OF CODEBASE] before we make changes.

Analyze:
- Current structure
- Dependencies
- What uses this code
- Potential impacts

Don't make changes, just report findings.
```

### 2. Implementation Session
**When**: Ready to make changes
**Template**:
```
Implement [SPECIFIC FEATURE/CHANGE] as defined in [DOCUMENT].

Requirements:
- Maintain backward compatibility
- Add tests for new code
- Update documentation
- Follow existing patterns

Work autonomously and update todos.
```

### 3. Cleanup Session
**When**: Organizing/moving files
**Template**:
```
Let's clean up [SPECIFIC AREA].

1. List all files to be moved/deleted
2. Create new directory structure
3. Move files in batches
4. Update imports
5. Run tests after each batch

Create backups before starting.
```

### 4. Bug Fix Session
**When**: Something is broken
**Template**:
```
There's an issue with [DESCRIBE PROBLEM].

1. Reproduce the issue
2. Identify root cause
3. Propose fix
4. Implement fix
5. Add test to prevent regression

Show me your analysis before fixing.
```

---

## Effective Communication Patterns

### ✅ DO Use These Patterns

#### Be Specific
```
❌ "Fix the configuration"
✅ "Consolidate the 4 laptop_metafield_mapping*.py files into one"

❌ "Clean up"
✅ "Move all test_*.py files from root to tests/unit/"

❌ "Make it better"
✅ "Implement repository pattern as defined in Phase 4.1"
```

#### Provide Context
```
Good: "I'm working on Phase 2 of the restructuring plan. Today I want to consolidate all configuration files."

Better: "I'm working on Phase 2.1 - consolidating laptop metafield mappings. Yesterday we completed Phase 1. No blockers."
```

#### Set Boundaries
```
"Work on Phase 1 only. Don't touch:
- Any files in services/
- The working variant metafield system
- Any production configuration"
```

### ⚡ Power Phrases

1. **"Work autonomously"** - Reduces confirmation requests
2. **"Use all necessary agents"** - Enables specialized agent use
3. **"Don't ask for confirmation on read operations"** - Speeds up analysis
4. **"Create a comprehensive plan before implementing"** - Gets better thought-out solutions
5. **"Show me a summary first"** - Gets overview before details
6. **"Update the todo list as you progress"** - Maintains progress visibility

---

## Phase-Specific Instructions

### Phase 1: Documentation & Cleanup (Days 1-4)

#### Day 1: Documentation
```
Create project documentation structure:
1. Read CODEBASE_RESTRUCTURING_PLAN.md Phase 1
2. Create README.md with template from plan
3. Create docs/ directory structure
4. Write INSTALLATION.md
5. Write ARCHITECTURE.md overview

Focus only on documentation today.
```

#### Day 2-3: Test Organization
```
Organize test files:
1. List all test_*.py in root
2. Create tests/ directory structure
3. Move tests to appropriate subdirectories
4. Update any import statements
5. Run all tests to ensure they work
6. Update .gitignore if needed
```

#### Day 4: Root Cleanup
```
Clean root directory:
1. List all .py files in root (except streamlit_app.py)
2. Create scripts/ directory structure  
3. Move utility scripts
4. Move one-time scripts to scripts/one_time/
5. Verify application still runs
```

### Phase 2: Configuration Management (Days 5-8)

#### Laptop Configs
```
Consolidate laptop metafield mappings:
1. Compare all 4 files
2. Identify differences
3. Create merged version
4. Test with sample products
5. Archive old versions
6. Update all imports
```

#### Color Management
```
Organize color configuration:
1. Create config/color/ directory
2. Identify all color-related files
3. Design unified color system
4. Move files maintaining compatibility
5. Document color workflow
```

### Phase 3: Scripts Organization (Days 9-10)
```
Organize utility scripts:
1. Read Phase 3 requirements
2. Create directory structure
3. Categorize each script
4. Move to appropriate location
5. Create README for each category
6. Test critical scripts still work
```

### Phase 4: Architecture (Days 11-15)
```
[Implement one pattern at a time]
Repository Pattern:
1. Create repositories/ directory
2. Implement base repository
3. Create product repository
4. Gradually migrate service code
5. Maintain backward compatibility
```

### Phase 5: AI Agent System (Days 16-19)
```
Set up AI agent framework:
1. Create .ai/ directory structure
2. Write agent-specific guides
3. Create workflow templates
4. Set up context preservation
5. Test with simple tasks
```

### Phase 6: Testing & QA (Days 20-28)
```
Implement comprehensive testing:
1. Set up pytest configuration
2. Write unit tests for services
3. Create integration tests
4. Set up CI/CD pipeline
5. Add pre-commit hooks
```

---

## Power Commands

### 🔍 Analysis Commands
```bash
# See what needs organizing
find . -maxdepth 1 -name "*.py" | grep -E "(test_|create_|verify_)" 

# Check for duplicate functionality
grep -r "class.*Mapping" config/

# Find all hardcoded values
grep -r "jufbtk-ut.myshopify.com" .
```

### 📁 Safe File Operations
```bash
# Create backup before moving
cp -r config/ config_backup_$(date +%Y%m%d)/

# Move with confirmation
mv -i test_*.py tests/unit/

# Check what would be deleted
rm -i duplicate_*.py
```

### 🧪 Testing Commands
```bash
# Test after moving files
python -m pytest tests/

# Test specific module still imports
python -c "from services.product_service import ProductService"

# Run the app to check it works
streamlit run streamlit_app.py
```

---

## Efficiency Tips

### 1. Batch Similar Operations
Instead of:
```
"Move test_color_mapping.py to tests/"
"Now move test_laptop_color_fix.py to tests/"
```

Do:
```
"Move all test_*.py files from root to tests/unit/ in one operation"
```

### 2. Use Todo Lists Effectively
Start every session with:
```
"Create a todo list for today's tasks from Phase X of the restructuring plan"
```

### 3. Minimize Context Switching
Complete one phase before moving to the next. Don't jump between phases.

### 4. Leverage Git for Safety
```
# Before risky operations
git add -A && git commit -m "WIP: Before restructuring Phase X"

# Create restore point
git tag backup-before-phase-1
```

### 5. Use Agents Strategically
- **Code Quality Architect**: Architecture decisions, patterns
- **Shopify API Developer**: Anything touching Shopify APIs
- **Web Research Specialist**: Best practices, documentation
- **Product Strategy Advisor**: Feature planning, workflows

### 6. Provide Examples
When asking for something new, provide an example:
```
"Create a repository pattern like this:
class BaseRepository:
    def find(self, id): pass
    def save(self, entity): pass
"
```

---

## Troubleshooting

### Issue: AI Asks Too Many Questions
**Solution**: Add "work autonomously" and "don't ask for confirmation on read operations"

### Issue: Changes Break Something
**Solution**: 
```
"The last change broke [X]. Please:
1. Revert the last change
2. Analyze why it broke
3. Implement a fixed version
4. Test thoroughly before committing"
```

### Issue: AI Is Doing Too Much
**Solution**: Be more specific about boundaries
```
"ONLY work on Phase 1, Task 1.2. Do not touch any other files or tasks."
```

### Issue: Lost Track of Progress
**Solution**:
```
"Show me:
1. Current todo list status
2. What files have been modified (git status)
3. What phase/task we're on
4. Any blockers encountered"
```

### Issue: Import Errors After Moving Files
**Solution**:
```
"We have import errors after moving files. Please:
1. Find all broken imports
2. Update them to new paths
3. Test each fix
4. Document any sys.path changes needed"
```

---

## Session Closing

### Standard Closing
```
"Let's wrap up this session:
1. Complete any in-progress tasks
2. Run all tests
3. Commit changes with descriptive message
4. Update todo list marking completed items
5. Create brief summary of what was accomplished
"
```

### Handoff for Next Session
```
"Prepare handoff notes including:
- What was completed today
- What's currently in progress (%)
- Any blockers or issues found
- Priority for next session
- Any decisions that were made
"
```

### Emergency Closing
```
"Quick close:
1. Stash any uncommitted changes
2. Note current task status
3. List any issues encountered
"
```

---

## Best Practices Checklist

Before starting a session:
- [ ] Know which phase you're working on
- [ ] Have the restructuring plan open
- [ ] Know what was done in last session
- [ ] Have specific tasks in mind

During the session:
- [ ] Start with todo list creation
- [ ] Be specific about tasks
- [ ] Set clear boundaries
- [ ] Test after changes
- [ ] Commit frequently

After the session:
- [ ] All tests passing
- [ ] Changes committed
- [ ] Todo list updated
- [ ] Handoff notes created

---

## Example: Perfect Session Flow

```
You: "I'm starting work on Phase 1 of the restructuring plan. Today is Day 2, focusing on test organization.

1. Read CODEBASE_RESTRUCTURING_PLAN.md Phase 1
2. Create todo list for test organization
3. List all test files in root
4. Create tests/ directory structure as specified
5. Move files in batches, testing after each
6. Update any broken imports
7. Ensure all tests pass
8. Commit with message 'Phase 1.2: Organize test files'

Work autonomously, don't ask for confirmation on reads. Begin."

[AI works through tasks]

You: "Great. Now close the session with summary and handoff notes."
```

---

## Quick Reference Card

### Session Starters by Goal

**"I want to understand X"** → Analysis session
**"I want to implement Y"** → Implementation session  
**"I want to fix Z"** → Bug fix session
**"I want to clean up"** → Cleanup session

### Magic Words
- "autonomously" - Less interruptions
- "comprehensive" - More thorough
- "use all agents" - Better analysis
- "show summary first" - Overview before details
- "update todos" - Progress tracking

### Always Include
1. Which phase/task from plan
2. Specific boundaries
3. Success criteria
4. How to handle issues

---

*Remember: The clearer and more specific your instructions, the better the results. When in doubt, refer to the CODEBASE_RESTRUCTURING_PLAN.md for exact task definitions.*