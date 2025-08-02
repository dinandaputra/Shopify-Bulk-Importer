# General Rules for All AI Agents

This document establishes the fundamental rules and guidelines that ALL AI agents must follow when working on the Shopify Bulk Importer codebase.

## Core Principles

### 1. Preserve Working Functionality
- **NEVER** break existing functionality
- **ALWAYS** test changes before committing
- **MAINTAIN** backward compatibility
- **PRESERVE** all working integrations

### 2. Communication & Documentation
- **UPDATE** context files after every significant change
- **DOCUMENT** all decisions in ADR format when appropriate
- **LOG** all changes in WORK_LOG.md with timestamps
- **COMMENT** complex logic only when explicitly requested
- **MAINTAIN** clear commit messages following conventional commits

### 3. Code Quality Standards
- **FOLLOW** existing code conventions and patterns
- **USE** type hints for all new functions
- **MAINTAIN** clean architecture principles
- **ENSURE** proper error handling and logging
- **RESPECT** the DRY principle

### 4. Shopify API Best Practices
- **CHECK** rate limits before bulk operations
- **USE** GraphQL for complex queries
- **VALIDATE** all API responses
- **HANDLE** errors gracefully
- **LOG** API failures for debugging

### 5. Critical Protected Systems
These systems are WORKING and must NOT be modified without explicit approval:

#### Variant Metafield System ⚠️ DO NOT MODIFY
- `services/shopify_api.py:assign_metafields_to_variants()`
- GraphQL metafieldsSet mutation implementation
- Variant-to-metafield linking logic

#### SIM Carrier Variants ⚠️ DO NOT MODIFY
- Current implementation supports 1-5 variants
- Inventory distribution logic
- Product option creation system

## Agent Collaboration Protocol

### 1. Before Starting Work
- **READ** relevant agent role definition
- **CHECK** CODEBASE_STATE.md for current status
- **REVIEW** WORK_LOG.md for recent changes
- **VERIFY** no conflicting work in progress
- **UNDERSTAND** the current architecture

### 2. During Task Execution
- **USE** appropriate agent for specialized tasks
- **FOLLOW** established patterns and conventions
- **UPDATE** context files incrementally
- **TEST** changes continuously
- **MAINTAIN** clean git history

### 3. After Task Completion
- **UPDATE** all relevant documentation
- **RUN** appropriate test suites
- **LOG** changes in WORK_LOG.md
- **PREPARE** handoff notes for next session
- **TAG** stable versions when appropriate

## File Organization Rules

### 1. Directory Structure
- **MAINTAIN** clean architecture separation
- **PLACE** files in appropriate directories
- **AVOID** creating files in root directory
- **FOLLOW** naming conventions

### 2. Import Management
- **USE** absolute imports from project root
- **AVOID** circular dependencies
- **ORGANIZE** imports: standard library, third-party, local
- **REMOVE** unused imports

## Testing Requirements

### 1. Before Any Major Change
- **RUN** existing test suite
- **ENSURE** all tests pass
- **CREATE** tests for new functionality
- **UPDATE** tests for modified functionality

### 2. Test Categories
- **UNIT**: Test individual functions/methods
- **INTEGRATION**: Test component interactions
- **E2E**: Test complete workflows
- **API**: Test Shopify API integrations

## Error Handling Protocol

### 1. Exception Management
- **USE** custom exceptions from `infrastructure/exceptions.py`
- **CATCH** specific exceptions, not generic
- **LOG** errors with appropriate detail
- **PROVIDE** user-friendly error messages

### 2. API Error Handling
- **CHECK** response status codes
- **HANDLE** rate limiting gracefully
- **RETRY** transient failures with backoff
- **LOG** persistent failures

## Security Guidelines

### 1. Credentials & Secrets
- **NEVER** commit credentials
- **USE** environment variables
- **FOLLOW** .env.example template
- **VALIDATE** all user inputs

### 2. API Security
- **VALIDATE** webhook signatures
- **USE** proper authentication
- **LIMIT** API scope appropriately
- **MONITOR** for suspicious activity

## Performance Considerations

### 1. Optimization Rules
- **PROFILE** before optimizing
- **BATCH** API operations when possible
- **CACHE** expensive operations
- **PAGINATE** large result sets

### 2. Resource Management
- **CLOSE** file handles properly
- **LIMIT** memory usage in sessions
- **CLEAN** temporary files
- **MONITOR** API rate limits

## Version Control Guidelines

### 1. Commit Standards
- **USE** conventional commit format
- **KEEP** commits atomic and focused
- **WRITE** clear, descriptive messages
- **REFERENCE** issue numbers when applicable

### 2. Branch Management
- **CREATE** feature branches for new work
- **REBASE** on main before merging
- **DELETE** merged branches
- **TAG** stable releases

## Handoff Protocol

### 1. Session Completion
- **SUMMARIZE** work completed
- **LIST** any blockers or issues
- **IDENTIFY** next priorities
- **UPDATE** all documentation

### 2. Context Preservation
- **SAVE** work state in context files
- **DOCUMENT** any partial implementations
- **NOTE** any assumptions made
- **HIGHLIGHT** areas needing attention

## Emergency Procedures

### 1. If Breaking Change Detected
1. **STOP** immediately
2. **REVERT** to last stable state
3. **DOCUMENT** what went wrong
4. **PLAN** proper fix approach

### 2. If API Limits Hit
1. **PAUSE** all API operations
2. **LOG** the rate limit event
3. **IMPLEMENT** backoff strategy
4. **NOTIFY** in WORK_LOG.md

## Quality Checklist

Before considering any task complete:

- [ ] All tests pass
- [ ] Documentation updated
- [ ] No new linting errors
- [ ] Performance maintained
- [ ] Security validated
- [ ] Backward compatibility verified
- [ ] Error handling implemented
- [ ] Logging added where appropriate
- [ ] Context files updated
- [ ] Handoff notes prepared

---

**Remember**: These rules exist to maintain code quality, ensure smooth collaboration between agents, and protect the stability of the production system. When in doubt, err on the side of caution and document your decisions.

**Last Updated**: 2025-08-02
**Version**: 1.0.0