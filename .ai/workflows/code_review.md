# Code Review Workflow

This workflow ensures systematic, thorough code reviews that maintain code quality, catch issues early, and facilitate knowledge sharing across the AI agent team.

## Overview

**Purpose**: Systematic code quality assurance and knowledge sharing
**Scope**: All code changes before merge to main branch
**Duration**: 30 minutes - 2 hours per review
**Quality Gates**: 3 mandatory checkpoints

## Review Types

### 1. Feature Review 🚀
**Scope**: New feature implementations
**Focus**: Architecture, design patterns, integration quality
**Reviewer**: Code Quality Architect + Domain Specialist

### 2. Bug Fix Review 🐛
**Scope**: Bug fixes and hotfixes
**Focus**: Root cause addressing, testing, regression prevention
**Reviewer**: Code Quality Architect + Original implementer (if different)

### 3. Refactoring Review 🔄
**Scope**: Code structure improvements
**Focus**: Maintainability, performance, architectural compliance
**Reviewer**: Code Quality Architect + affected component specialists

### 4. Documentation Review 📚
**Scope**: Documentation and comment changes
**Focus**: Accuracy, completeness, clarity
**Reviewer**: Web Research Specialist + Domain Specialist

## Pre-Review Checklist

### Author Responsibilities

#### Before Submitting for Review
- [ ] **Self-review completed**: Author has reviewed their own code
- [ ] **Tests written and passing**: All tests pass locally
- [ ] **Documentation updated**: Relevant docs reflect changes
- [ ] **Commit messages clear**: Descriptive, following conventions
- [ ] **Branch up to date**: Rebased on latest main branch

#### Code Preparation Standards
- [ ] **Atomic commits**: Each commit represents a logical change
- [ ] **Clean history**: No merge commits, clear progression
- [ ] **Consistent formatting**: Code follows project standards
- [ ] **No debugging code**: Remove console.log, debug prints, etc.
- [ ] **Error handling**: Appropriate error handling implemented

#### Protected Systems Check ⚠️
- [ ] **Variant metafield system**: Not modified without approval
- [ ] **SIM carrier variants**: Functionality preserved
- [ ] **Working API integrations**: No breaking changes
- [ ] **Configuration integrity**: No unintended config changes

## Review Process

### Phase 1: Initial Assessment 📋

#### 1.1 Change Overview
**Reviewer**: Primary assigned reviewer
**Duration**: 5-10 minutes

**Assessment Tasks**:
- [ ] Review pull request description
- [ ] Understand the change purpose
- [ ] Identify scope and complexity
- [ ] Check for related issues/tickets
- [ ] Verify all files are relevant

**Change Analysis**:
```markdown
## Change Summary
- **Type**: [Feature/Bug Fix/Refactoring/Documentation]
- **Scope**: [Component/Module affected]
- **Complexity**: [Low/Medium/High]
- **Risk Level**: [Low/Medium/High]
- **Review Priority**: [Low/Medium/High]
```

#### 1.2 Automated Checks Verification
**Duration**: 2-5 minutes

**Verification Tasks**:
- [ ] All CI/CD checks passing
- [ ] Test coverage maintained or improved
- [ ] No linting errors
- [ ] No security vulnerabilities detected
- [ ] Performance benchmarks acceptable

**Quality Gate**: ✅ Automated checks pass

### Phase 2: Technical Review 🔍

#### 2.1 Architecture & Design Review
**Reviewer**: Code Quality Architect
**Duration**: 15-30 minutes

**Architecture Checklist**:
- [ ] **Clean Architecture Compliance**: Proper layer separation
- [ ] **SOLID Principles**: Single responsibility, open/closed, etc.
- [ ] **Design Patterns**: Appropriate pattern usage
- [ ] **Dependency Management**: Proper dependency injection
- [ ] **Abstraction Levels**: Appropriate abstraction usage

**Domain Model Review**:
- [ ] **Entity Integrity**: Domain entities properly modeled
- [ ] **Business Rules**: Correctly implemented in domain layer
- [ ] **Value Objects**: Immutable and validated
- [ ] **Repository Pattern**: Proper data access abstraction
- [ ] **Service Layer**: Business logic properly organized

#### 2.2 Implementation Quality Review
**Reviewer**: Domain Specialist
**Duration**: 20-45 minutes

**Code Quality Checklist**:
- [ ] **Readability**: Code is clear and self-documenting
- [ ] **Maintainability**: Easy to understand and modify
- [ ] **Performance**: No obvious performance issues
- [ ] **Error Handling**: Comprehensive and appropriate
- [ ] **Security**: No security vulnerabilities

**Implementation Standards**:
- [ ] **Naming Conventions**: Consistent and descriptive names
- [ ] **Function Size**: Functions are appropriately sized
- [ ] **Complexity**: Cyclomatic complexity under control
- [ ] **Duplication**: No unnecessary code duplication
- [ ] **Comments**: Complex logic appropriately commented

#### 2.3 Integration Review
**Reviewer**: Shopify API Developer (if applicable)
**Duration**: 10-30 minutes

**API Integration Checklist**:
- [ ] **API Usage**: Proper Shopify API usage patterns
- [ ] **Rate Limiting**: Appropriate rate limit handling
- [ ] **Error Handling**: Proper API error processing
- [ ] **Data Validation**: Input/output validation
- [ ] **Authentication**: Proper auth token usage

**Data Flow Review**:
- [ ] **Data Consistency**: Proper data validation and transformation
- [ ] **State Management**: Session and state properly managed
- [ ] **Concurrency**: Thread safety where applicable
- [ ] **Transaction Handling**: Proper data transaction management
- [ ] **Rollback Scenarios**: Error recovery mechanisms

**Quality Gate**: ✅ Technical implementation approved

### Phase 3: Testing & Quality Assurance 🧪

#### 3.1 Test Coverage Review
**Reviewer**: Code Quality Architect
**Duration**: 10-20 minutes

**Test Quality Checklist**:
- [ ] **Unit Tests**: Adequate unit test coverage (>80%)
- [ ] **Integration Tests**: Component integration tested
- [ ] **Edge Cases**: Boundary conditions tested
- [ ] **Error Scenarios**: Error paths tested
- [ ] **Mock Usage**: Proper mocking of dependencies

**Test Implementation Review**:
- [ ] **Test Clarity**: Tests are readable and maintainable
- [ ] **Test Independence**: Tests don't depend on each other
- [ ] **Test Data**: Appropriate test fixtures and data
- [ ] **Assertion Quality**: Clear and specific assertions
- [ ] **Performance Tests**: Performance critical paths tested

#### 3.2 Business Logic Validation
**Reviewer**: Product Strategy Advisor
**Duration**: 10-20 minutes

**Business Requirements Checklist**:
- [ ] **Requirements Met**: All acceptance criteria satisfied
- [ ] **User Experience**: Changes improve or maintain UX
- [ ] **Business Rules**: Domain rules correctly implemented
- [ ] **Workflow Impact**: User workflows properly considered
- [ ] **Data Integrity**: Business data properly validated

**Quality Gate**: ✅ Testing and business requirements validated

### Phase 4: Documentation & Knowledge Transfer 📚

#### 4.1 Documentation Review
**Reviewer**: Web Research Specialist
**Duration**: 5-15 minutes

**Documentation Checklist**:
- [ ] **API Documentation**: Public APIs documented
- [ ] **Code Comments**: Complex logic explained
- [ ] **Configuration**: Config changes documented
- [ ] **User Guides**: User-facing changes documented
- [ ] **Troubleshooting**: New issues and solutions documented

#### 4.2 Knowledge Sharing
**Reviewer**: All involved agents
**Duration**: 5-10 minutes

**Knowledge Transfer Tasks**:
- [ ] **Context Sharing**: Implementation decisions explained
- [ ] **Pattern Documentation**: New patterns documented
- [ ] **Lessons Learned**: Insights shared with team
- [ ] **Future Considerations**: Technical debt or improvements noted

## Review Guidelines by Change Type

### Feature Implementation Reviews

#### Focus Areas
1. **Architecture Alignment**: Does the feature fit the clean architecture?
2. **API Integration**: Proper Shopify API usage and error handling
3. **User Experience**: Does it improve the user workflow?
4. **Performance Impact**: No significant performance degradation
5. **Testing Completeness**: Comprehensive test coverage

#### Common Issues to Watch For
- Tight coupling between layers
- Missing error handling for API calls
- Inadequate input validation
- Performance bottlenecks
- Missing or poor test coverage

### Bug Fix Reviews

#### Focus Areas
1. **Root Cause**: Does the fix address the actual root cause?
2. **Scope**: Is the fix appropriately scoped?
3. **Regression Risk**: Could this fix break other functionality?
4. **Testing**: Are there tests to prevent regression?
5. **Documentation**: Is the fix properly documented?

#### Common Issues to Watch For
- Fixing symptoms instead of root cause
- Over-broad fixes that could introduce new bugs
- Missing regression tests
- Insufficient error handling
- Poor change documentation

### Refactoring Reviews

#### Focus Areas
1. **Behavior Preservation**: Does refactoring maintain existing behavior?
2. **Improvement Clarity**: Is the refactoring clearly beneficial?
3. **Testing Coverage**: Are changes properly tested?
4. **Incremental Changes**: Are changes appropriately sized?
5. **Dependency Impact**: How do changes affect dependent code?

#### Common Issues to Watch For
- Behavioral changes disguised as refactoring
- Too large refactoring changes
- Missing tests for refactored code
- Breaking changes to public interfaces
- Unnecessary complexity introduction

## Review Comments Guidelines

### Effective Review Comments

#### Comment Categories
1. **Must Fix**: Issues that must be addressed before merge
2. **Should Fix**: Important improvements that should be made
3. **Consider**: Suggestions for improvement
4. **Nitpick**: Minor style or convention issues
5. **Question**: Requests for clarification

#### Comment Format
```markdown
**[Category]**: [Brief description]

[Detailed explanation of the issue or suggestion]

**Suggestion**: [Specific improvement recommendation]

**Example**: [Code example if helpful]
```

#### Positive Feedback
- Acknowledge good practices and clever solutions
- Highlight learning opportunities
- Recognize improvements in code quality
- Celebrate successful problem-solving

### Comment Examples

#### Good Comments
```markdown
**Must Fix**: Potential null pointer exception

This could throw a NullPointerException if `product.variants` is null. 
Consider adding a null check or using optional chaining.

**Suggestion**: 
```python
if product.variants:
    for variant in product.variants:
        # process variant
```
```

```markdown
**Consider**: Extract magic number to constant

The value `86400` appears multiple times. Consider extracting to a named constant like `SECONDS_PER_DAY`.

**Benefits**: Improved readability and maintainability
```

#### Avoid These Comment Types
- Vague complaints without specific suggestions
- Style nitpicks that aren't project standards
- Personal preference items
- Criticism without constructive feedback

## Review Resolution Process

### Author Response Requirements

#### Addressing Comments
- [ ] **Acknowledge**: Respond to all review comments
- [ ] **Fix or Explain**: Address issues or explain why not
- [ ] **Update Code**: Make requested changes
- [ ] **Re-request Review**: Ask for re-review after changes

#### Response Format
```markdown
**Comment**: [Original reviewer comment]
**Response**: [Author's response]
**Action**: [What was done to address the comment]
**Status**: [Fixed/Explained/Deferred]
```

### Re-review Process

#### When Re-review is Required
- Significant code changes made
- Architecture or design changes
- New functionality added
- Multiple "Must Fix" comments addressed

#### Expedited Re-review
- Only style/minor changes made
- Documentation updates only
- Test additions without logic changes
- Reviewer-suggested specific changes implemented

## Special Review Procedures

### Emergency/Hotfix Reviews

#### Expedited Process
1. **Immediate Review**: Within 30 minutes
2. **Focus Areas**: Root cause fix, regression risk, testing
3. **Reduced Scope**: Focus on critical path only
4. **Follow-up**: Full review after emergency resolved

#### Emergency Review Checklist
- [ ] Fixes the critical issue
- [ ] Minimal scope of change
- [ ] No breaking changes to other functionality
- [ ] Adequate testing for the fix
- [ ] Rollback plan available

### Large Feature Reviews

#### Multi-Phase Review
1. **Design Review**: Architecture and approach review first
2. **Implementation Review**: Code review in logical chunks
3. **Integration Review**: End-to-end review of complete feature
4. **Documentation Review**: Final documentation pass

#### Review Coordination
- Multiple reviewers for different aspects
- Staggered review timeline
- Regular check-ins during implementation
- Early feedback to prevent major rework

## Quality Metrics

### Review Effectiveness Metrics
- **Defect Detection Rate**: Issues caught in review vs production
- **Review Completion Time**: Time from submission to approval
- **Comment Resolution Rate**: Percentage of comments addressed
- **Re-review Frequency**: How often changes require re-review

### Code Quality Metrics
- **Test Coverage**: Maintained or improved coverage
- **Complexity**: Code complexity trends
- **Duplication**: Code duplication levels
- **Documentation**: Documentation coverage

### Process Improvement
- Regular review of review effectiveness
- Feedback collection from authors and reviewers
- Process refinement based on metrics
- Tool and automation improvements

---

**Workflow Version**: 1.0.0
**Last Updated**: 2025-08-02
**Next Review**: 2025-09-02
**Owner**: Code Quality Architect