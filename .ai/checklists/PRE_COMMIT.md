# Pre-Commit Checklist

This checklist ensures that all code changes meet quality standards before being committed to the repository, preventing regressions and maintaining codebase integrity.

## Overview

**Purpose**: Ensure code quality before committing changes
**Scope**: All code commits (features, bug fixes, documentation)
**Responsibility**: All AI agents before making commits

## Code Quality Verification ✅

### 1. Functionality Testing
- [ ] **All new features working** - New functionality operates as expected
- [ ] **Bug fixes verified** - Bugs are actually fixed
- [ ] **No regressions introduced** - Existing functionality still works
- [ ] **Edge cases tested** - Boundary conditions handled properly
- [ ] **Error scenarios handled** - Error paths tested and working

### 2. Protected Systems Verification ⚠️
- [ ] **Variant metafield system** - Working implementation not modified
- [ ] **SIM carrier variants** - 1-5 variant system still functional
- [ ] **GraphQL metafieldsSet mutation** - Core mutation not changed
- [ ] **Working API integrations** - Existing integrations preserved
- [ ] **Configuration integrity** - No unintended config changes

### 3. Test Suite Execution
- [ ] **All unit tests passing** - Complete unit test suite passes
- [ ] **Integration tests passing** - All integration tests pass
- [ ] **New tests added** - Tests for new functionality included
- [ ] **Test coverage maintained** - Coverage not decreased
- [ ] **Test quality verified** - Tests are meaningful and maintainable

## Code Standards Compliance 📋

### 1. Clean Architecture Compliance
- [ ] **Layer separation maintained** - Domain, infrastructure, application layers distinct
- [ ] **Dependency direction correct** - Dependencies point inward to domain
- [ ] **Repository pattern followed** - Data access properly abstracted
- [ ] **Domain logic in domain layer** - Business rules in correct location
- [ ] **Infrastructure concerns isolated** - External services properly abstracted

### 2. Code Quality Standards
- [ ] **Consistent naming conventions** - Variables, functions, classes named consistently
- [ ] **Appropriate function size** - Functions are focused and not too large
- [ ] **Proper error handling** - Errors handled appropriately with custom exceptions
- [ ] **No code duplication** - DRY principle followed
- [ ] **SOLID principles followed** - Design principles applied appropriately

### 3. Type Safety & Documentation
- [ ] **Type hints added** - All new functions have proper type annotations
- [ ] **Complex logic documented** - Non-obvious code has explanatory comments
- [ ] **Public APIs documented** - Public methods have docstrings
- [ ] **Configuration documented** - New config options documented
- [ ] **Examples provided** - Usage examples for complex functionality

## API Integration Standards 🛒

### 1. Shopify API Best Practices
- [ ] **Rate limiting respected** - Proper rate limit handling implemented
- [ ] **Error handling comprehensive** - All API error types handled
- [ ] **Authentication secure** - No credentials exposed in code
- [ ] **Request validation** - Input data validated before API calls
- [ ] **Response validation** - API responses properly validated

### 2. Data Format Consistency
- [ ] **Metafield format correct** - JSON array format for list.metaobject_reference
- [ ] **GID format proper** - Shopify GID format used correctly
- [ ] **Currency handling correct** - JPY format with no decimals
- [ ] **Date format consistent** - ISO format used for dates
- [ ] **Handle generation working** - Product handles generated correctly

### 3. Integration Robustness
- [ ] **Retry logic implemented** - Transient failures handled with retry
- [ ] **Logging comprehensive** - API calls logged appropriately
- [ ] **Monitoring enabled** - Performance and error monitoring in place
- [ ] **Graceful degradation** - System continues working if non-critical APIs fail
- [ ] **Rollback capability** - Changes can be reverted if needed

## Performance & Security 🔒

### 1. Performance Considerations
- [ ] **No obvious performance regressions** - Code doesn't slow down system
- [ ] **Memory usage reasonable** - No memory leaks or excessive usage
- [ ] **Database queries optimized** - Efficient data access patterns
- [ ] **Caching used appropriately** - Expensive operations cached when beneficial
- [ ] **Bulk operations efficient** - Large datasets handled efficiently

### 2. Security Standards
- [ ] **No credentials in code** - All secrets in environment variables
- [ ] **Input validation present** - User input validated and sanitized
- [ ] **SQL injection prevention** - Parameterized queries used
- [ ] **XSS prevention** - User content properly escaped
- [ ] **Authentication/authorization correct** - Proper access controls

### 3. Data Protection
- [ ] **Personal data handled properly** - Privacy considerations addressed
- [ ] **Sensitive data encrypted** - Sensitive information protected
- [ ] **Audit trails maintained** - Important operations logged
- [ ] **Data integrity preserved** - Data consistency maintained
- [ ] **Backup considerations** - Data backup implications considered

## Documentation Updates 📚

### 1. Code Documentation
- [ ] **README.md updated** - Main documentation reflects changes
- [ ] **API documentation current** - API changes documented
- [ ] **Configuration docs updated** - New config options documented
- [ ] **Troubleshooting guides current** - Common issues documented
- [ ] **Architecture docs updated** - Architectural changes reflected

### 2. Context Files Updated
- [ ] **WORK_LOG.md updated** - Changes logged with timestamp
- [ ] **CODEBASE_STATE.md current** - Current state accurately reflected
- [ ] **KNOWN_ISSUES.md updated** - New issues added, resolved issues updated
- [ ] **TECHNICAL_DEBT.md current** - New debt documented, resolved debt removed
- [ ] **ARCHITECTURE_DECISIONS.md updated** - New ADRs added if applicable

### 3. User-Facing Documentation
- [ ] **User guides updated** - User workflow changes documented
- [ ] **Help text current** - In-app help reflects changes
- [ ] **Error messages clear** - User-friendly error messages provided
- [ ] **Installation docs current** - Setup instructions accurate
- [ ] **Migration guides provided** - Breaking changes documented

## Version Control Best Practices 🔄

### 1. Commit Quality
- [ ] **Atomic commits** - Each commit represents one logical change
- [ ] **Clear commit messages** - Messages follow conventional commit format
- [ ] **Relevant files only** - Only necessary files included in commit
- [ ] **No binary files** - No unnecessary binary files committed
- [ ] **Secrets excluded** - No credentials or secrets in commit

### 2. Branch Management
- [ ] **Feature branch current** - Branch rebased on latest main
- [ ] **Conflict resolution complete** - All merge conflicts resolved
- [ ] **Branch naming correct** - Branch name follows convention
- [ ] **Remote tracking set** - Branch properly configured for push
- [ ] **Clean git history** - History is logical and clean

### 3. File Organization
- [ ] **Files in correct directories** - New files placed appropriately
- [ ] **Naming conventions followed** - File names follow project standards
- [ ] **Import paths correct** - All imports resolve properly
- [ ] **Dependencies up to date** - Required dependencies added to requirements
- [ ] **Unused files removed** - Obsolete files cleaned up

## Agent-Specific Checks

### Code Quality Architect 🏗️
- [ ] **Architecture patterns followed** - Clean architecture maintained
- [ ] **Design patterns appropriate** - Correct patterns used
- [ ] **Code complexity acceptable** - Cyclomatic complexity under control
- [ ] **Test coverage adequate** - New code has sufficient test coverage
- [ ] **Performance benchmarks met** - Performance requirements satisfied

### Shopify API Developer 🛒
- [ ] **API integration tested** - Shopify API calls work correctly
- [ ] **Metafield operations verified** - Metafield creation/update working
- [ ] **Rate limiting tested** - Rate limit handling verified
- [ ] **Error scenarios covered** - API error handling tested
- [ ] **Data synchronization working** - Shopify data stays consistent

### Web Research Specialist 🔍
- [ ] **Documentation accuracy verified** - All documentation accurate
- [ ] **External references current** - Links and references up to date
- [ ] **Best practices followed** - Current best practices applied
- [ ] **Examples tested** - Code examples work correctly
- [ ] **Research findings documented** - New insights documented

### Product Strategy Advisor 📋
- [ ] **User requirements met** - Business requirements satisfied
- [ ] **Acceptance criteria fulfilled** - All acceptance criteria met
- [ ] **User experience improved** - Changes improve user workflow
- [ ] **Error handling user-friendly** - Error messages clear to users
- [ ] **Business logic correct** - Domain rules implemented correctly

## Final Pre-Commit Verification 🎯

### 1. Comprehensive Testing
- [ ] **Local testing complete** - All functionality tested locally
- [ ] **Automated tests passing** - CI/CD pipeline would pass
- [ ] **Manual testing performed** - Key workflows manually verified
- [ ] **Regression testing done** - Existing features still work
- [ ] **Performance testing completed** - No performance regressions

### 2. Quality Assurance
- [ ] **Code review self-performed** - Author has reviewed own code
- [ ] **Standards compliance verified** - All coding standards met
- [ ] **Documentation completeness checked** - All required docs updated
- [ ] **Security review performed** - Security implications considered
- [ ] **Accessibility considered** - User accessibility implications addressed

### 3. Integration Readiness
- [ ] **Dependencies resolved** - All dependencies properly handled
- [ ] **Configuration correct** - Config changes properly implemented
- [ ] **Environment compatibility** - Works in all target environments
- [ ] **Rollback plan ready** - Can revert changes if needed
- [ ] **Monitoring prepared** - Post-deployment monitoring ready

## Emergency Commit Conditions 🚨

These conditions may warrant bypassing some checklist items for critical fixes:

### Critical Production Issues
- [ ] **System completely down** - Total system failure
- [ ] **Data loss in progress** - Active data loss situation
- [ ] **Security breach active** - Active security compromise
- [ ] **Customer impact severe** - Severe business impact

**Emergency Commit Protocol:**
- [ ] **Document bypass reason** - Clear justification for skipping checks
- [ ] **Minimal scope change** - Smallest possible fix
- [ ] **Plan follow-up review** - Schedule comprehensive review post-emergency
- [ ] **Communicate to team** - Notify team of emergency commit
- [ ] **Complete checklist post-fix** - Finish full checklist after resolution

## Commit Message Template 📝

```
type(scope): brief description

Detailed explanation of the changes and reasoning.

- Changed: what was modified
- Added: what was added
- Fixed: what was fixed
- Removed: what was removed

Breaking Changes:
- List any breaking changes

Closes: #issue-number
Co-authored-by: Agent Name <agent@example.com>

🤖 Generated with Claude Code
```

## Quality Gate Decision Matrix 🚪

| Criteria | Pass | Conditional Pass | Fail |
|----------|------|------------------|------|
| All tests passing | ✅ All pass | ⚠️ Minor test failures | ❌ Major test failures |
| Code standards | ✅ Full compliance | ⚠️ Minor violations | ❌ Major violations |
| Documentation | ✅ Complete | ⚠️ Minor gaps | ❌ Missing critical docs |
| Security review | ✅ No issues | ⚠️ Minor concerns | ❌ Security vulnerabilities |
| Performance | ✅ No regression | ⚠️ Acceptable impact | ❌ Significant regression |

**Decision Rules:**
- **All Pass**: Commit approved
- **Any Fail**: Must fix before commit
- **Conditional Pass only**: Acceptable with documented justification

---

**Checklist Version**: 1.0.0
**Last Updated**: 2025-08-02
**Review Frequency**: Monthly
**Next Review**: 2025-09-02

## Notes for Agents

- **Complete all applicable sections** - Tailor to the specific change type
- **Document any exceptions** - Provide clear justification for skipped items
- **Maintain quality standards** - Don't compromise on quality for speed
- **Communicate issues** - Escalate any blockers or concerns
- **Update tracking** - Log progress and completion status