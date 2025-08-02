# Code Review Checklist

This checklist ensures thorough, consistent code reviews that maintain quality, catch issues early, and facilitate knowledge sharing across the AI agent team.

## Overview

**Purpose**: Systematic code review quality assurance
**Scope**: All code changes requiring review
**Responsibility**: Assigned reviewer agents
**Duration**: 30 minutes - 2 hours per review

## Pre-Review Setup ⚙️

### 1. Reviewer Preparation
- [ ] **Understand the context** - Read PR description and related issues
- [ ] **Check automated tests** - Verify all CI/CD checks are passing
- [ ] **Review change scope** - Understand the size and complexity
- [ ] **Identify review focus** - Determine key areas to emphasize
- [ ] **Set aside adequate time** - Allocate sufficient time for thorough review

### 2. Access and Tools
- [ ] **Development environment ready** - Can run code locally if needed
- [ ] **Testing credentials available** - Can test changes if required
- [ ] **Documentation accessible** - Have access to relevant docs
- [ ] **Previous context available** - Can reference related changes
- [ ] **Communication channels open** - Can discuss with author

## Architecture & Design Review 🏗️

### 1. Clean Architecture Compliance
- [ ] **Layer separation maintained** - Domain, infrastructure, application layers distinct
- [ ] **Dependency direction correct** - Dependencies point toward domain core
- [ ] **Single responsibility principle** - Classes/functions have clear single purpose
- [ ] **Open/closed principle** - Code open for extension, closed for modification
- [ ] **Interface segregation** - Interfaces are focused and cohesive
- [ ] **Dependency inversion** - Depends on abstractions, not concretions

### 2. Design Patterns and Structure
- [ ] **Appropriate patterns used** - Design patterns applied correctly
- [ ] **Repository pattern correct** - Data access properly abstracted
- [ ] **Service layer organized** - Business logic properly structured
- [ ] **Entity integrity maintained** - Domain entities properly modeled
- [ ] **Value objects immutable** - Value objects follow immutability principle

### 3. Component Integration
- [ ] **Component boundaries clear** - Clear separation between components
- [ ] **Integration points well-defined** - Clear interfaces between components
- [ ] **Dependency injection proper** - DI used appropriately
- [ ] **Error boundaries established** - Error handling at appropriate boundaries
- [ ] **Configuration management sound** - Config handled consistently

## Code Quality Assessment 📋

### 1. Readability and Maintainability
- [ ] **Code is self-documenting** - Code intent is clear without comments
- [ ] **Naming conventions consistent** - Variables, functions, classes named well
- [ ] **Function size appropriate** - Functions are focused and not too large
- [ ] **Class cohesion high** - Classes have related responsibilities
- [ ] **Coupling appropriately low** - Dependencies are minimized

### 2. Code Standards Compliance
- [ ] **Consistent formatting** - Code follows project formatting standards
- [ ] **Import organization correct** - Imports organized properly
- [ ] **Type hints present** - New code has appropriate type annotations
- [ ] **Docstrings provided** - Public APIs have documentation
- [ ] **Comments meaningful** - Comments explain why, not what

### 3. Complexity Management
- [ ] **Cyclomatic complexity acceptable** - Functions not overly complex
- [ ] **Nesting levels reasonable** - Code not excessively nested
- [ ] **Logic flow clear** - Code execution path is understandable
- [ ] **Edge cases handled** - Boundary conditions properly addressed
- [ ] **Error scenarios covered** - Error paths properly implemented

## Shopify API Integration Review 🛒

### 1. Protected Systems Verification ⚠️
- [ ] **Variant metafield system untouched** - Working implementation preserved
- [ ] **SIM carrier variants preserved** - 1-5 variant system functionality maintained
- [ ] **GraphQL mutations intact** - Working metafieldsSet mutations unchanged
- [ ] **API integration patterns followed** - Established patterns maintained
- [ ] **Configuration integrity maintained** - No unintended config changes

### 2. API Usage Best Practices
- [ ] **Rate limiting handled** - Proper rate limit management implemented
- [ ] **Error handling comprehensive** - All API error types handled appropriately
- [ ] **Authentication secure** - No credentials exposed in code
- [ ] **Request validation present** - Input data validated before API calls
- [ ] **Response validation implemented** - API responses properly validated

### 3. Data Format and Consistency
- [ ] **Metafield format correct** - JSON array format for list.metaobject_reference
- [ ] **GID format proper** - Shopify GID format used correctly
- [ ] **Currency handling consistent** - JPY format with no decimals maintained
- [ ] **Date format standardized** - Consistent date format usage
- [ ] **Handle generation working** - Product handle generation functional

## Testing and Quality Assurance 🧪

### 1. Test Coverage and Quality
- [ ] **New functionality tested** - All new code has corresponding tests
- [ ] **Test coverage maintained** - Overall test coverage not decreased
- [ ] **Test types appropriate** - Right mix of unit, integration, E2E tests
- [ ] **Test independence verified** - Tests don't depend on each other
- [ ] **Test readability good** - Tests are clear and maintainable

### 2. Test Implementation Quality
- [ ] **Meaningful assertions** - Tests check for correct behavior
- [ ] **Edge cases tested** - Boundary conditions covered
- [ ] **Error scenarios tested** - Failure paths tested
- [ ] **Mock usage appropriate** - Mocks used correctly and meaningfully
- [ ] **Test data realistic** - Test data represents real scenarios

### 3. Testing Patterns Followed
- [ ] **AAA pattern used** - Arrange, Act, Assert structure
- [ ] **Fixtures used properly** - Test fixtures organized and reusable
- [ ] **Parameterized tests utilized** - Multiple scenarios tested efficiently
- [ ] **Performance tests included** - Performance-critical paths tested
- [ ] **Integration tests present** - Component interactions tested

## Security and Performance Review 🔒

### 1. Security Considerations
- [ ] **No credentials exposed** - All secrets properly externalized
- [ ] **Input validation present** - User input validated and sanitized
- [ ] **Authentication proper** - Access controls correctly implemented
- [ ] **SQL injection prevented** - Parameterized queries used
- [ ] **XSS prevention implemented** - User content properly escaped

### 2. Performance Assessment
- [ ] **No obvious performance regressions** - Code doesn't degrade performance
- [ ] **Memory usage reasonable** - No memory leaks or excessive usage
- [ ] **Database queries efficient** - Data access patterns optimized
- [ ] **Caching appropriate** - Expensive operations cached when beneficial
- [ ] **Bulk operations optimized** - Large datasets handled efficiently

### 3. Scalability Considerations
- [ ] **Resource usage bounded** - Resource consumption predictable
- [ ] **Concurrency handled** - Thread safety considerations addressed
- [ ] **Rate limiting respected** - External service limits respected
- [ ] **Graceful degradation** - System continues working during partial failures
- [ ] **Monitoring hooks present** - Performance monitoring enabled

## Documentation Review 📚

### 1. Code Documentation
- [ ] **Public API documented** - All public methods have docstrings
- [ ] **Complex logic explained** - Non-obvious code has explanatory comments
- [ ] **Configuration documented** - New config options documented
- [ ] **Usage examples provided** - Complex functionality has usage examples
- [ ] **Deprecation warnings added** - Deprecated features properly marked

### 2. Project Documentation Updates
- [ ] **README.md current** - Main documentation reflects changes
- [ ] **API documentation updated** - API changes properly documented
- [ ] **Architecture docs current** - Architectural changes reflected
- [ ] **User guides updated** - User-facing changes documented
- [ ] **Troubleshooting updated** - New issues and solutions documented

### 3. Context File Updates
- [ ] **WORK_LOG.md updated** - Changes logged with appropriate detail
- [ ] **CODEBASE_STATE.md current** - Current state accurately reflected
- [ ] **KNOWN_ISSUES.md updated** - Issues added/resolved as appropriate
- [ ] **TECHNICAL_DEBT.md maintained** - Technical debt properly tracked
- [ ] **ARCHITECTURE_DECISIONS.md current** - New ADRs added if needed

## Agent-Specific Review Focus

### For Code Quality Architect Changes 🏗️
- [ ] **Architecture patterns correct** - Clean architecture principles followed
- [ ] **Design decisions sound** - Architectural decisions well-reasoned
- [ ] **Performance implications assessed** - Performance impact considered
- [ ] **Testing strategy comprehensive** - Testing approach thorough
- [ ] **Quality metrics maintained** - Code quality standards upheld

### For Shopify API Developer Changes 🛒
- [ ] **API integration robust** - Shopify API usage correct and resilient
- [ ] **Metafield operations verified** - Metafield creation/update working
- [ ] **Error handling comprehensive** - All API error scenarios covered
- [ ] **Data synchronization correct** - Shopify data consistency maintained
- [ ] **Rate limiting appropriate** - API usage respects limits

### For Web Research Specialist Changes 🔍
- [ ] **Documentation accuracy verified** - All documentation accurate and current
- [ ] **Research findings valid** - Research conclusions properly supported
- [ ] **Best practices current** - Recommendations reflect current best practices
- [ ] **External references updated** - Links and references current
- [ ] **Examples tested** - Code examples verified to work

### For Product Strategy Advisor Changes 📋
- [ ] **Business requirements met** - All acceptance criteria satisfied
- [ ] **User experience improved** - Changes enhance user workflow
- [ ] **Business logic correct** - Domain rules properly implemented
- [ ] **Error handling user-friendly** - Error messages clear to users
- [ ] **Accessibility considered** - User accessibility implications addressed

## Review Comments Guidelines 💬

### 1. Comment Categories and Usage
- [ ] **Must Fix**: Critical issues that block merge
- [ ] **Should Fix**: Important improvements that should be addressed
- [ ] **Consider**: Suggestions for improvement
- [ ] **Question**: Requests for clarification
- [ ] **Nitpick**: Minor style or convention issues

### 2. Effective Comment Writing
- [ ] **Specific and actionable** - Comments provide clear direction
- [ ] **Constructive tone** - Comments are helpful, not critical
- [ ] **Context provided** - Explanations include reasoning
- [ ] **Examples given** - Code examples provided when helpful
- [ ] **Positive feedback included** - Good practices acknowledged

### 3. Comment Quality Standards
- [ ] **Clear category indicated** - Comment type clearly marked
- [ ] **Reasoning explained** - Why the change is needed
- [ ] **Suggestions provided** - Specific improvement recommendations
- [ ] **Resources linked** - Relevant documentation linked when helpful
- [ ] **Follow-up planned** - Next steps clear

## Review Decision Matrix 🎯

### Approval Criteria
| Aspect | Approve | Approve with Minor Changes | Request Changes |
|--------|---------|---------------------------|-----------------|
| Functionality | ✅ Works correctly | ⚠️ Minor issues | ❌ Major bugs |
| Code Quality | ✅ High quality | ⚠️ Acceptable with notes | ❌ Quality issues |
| Testing | ✅ Comprehensive | ⚠️ Adequate | ❌ Insufficient |
| Documentation | ✅ Complete | ⚠️ Minor gaps | ❌ Major gaps |
| Security | ✅ Secure | ⚠️ Minor concerns | ❌ Security issues |

### Decision Guidelines
- [ ] **Approve**: All criteria met, ready to merge
- [ ] **Approve with Minor Changes**: Acceptable quality, minor improvements suggested
- [ ] **Request Changes**: Significant issues must be addressed before merge

## Post-Review Actions 📋

### 1. Review Completion
- [ ] **All code sections reviewed** - Complete review performed
- [ ] **Comments provided** - Appropriate feedback given
- [ ] **Decision made** - Clear approval status provided
- [ ] **Next steps clear** - Author understands required actions
- [ ] **Timeline communicated** - Re-review expectations set

### 2. Follow-up Planning
- [ ] **Re-review scheduled** - Plan for reviewing changes
- [ ] **Discussion topics noted** - Complex issues flagged for discussion
- [ ] **Learning opportunities identified** - Knowledge sharing opportunities noted
- [ ] **Process improvements suggested** - Feedback on review process
- [ ] **Documentation updates planned** - Updates to patterns/guidelines

### 3. Knowledge Sharing
- [ ] **Insights shared** - Valuable learnings communicated
- [ ] **Patterns documented** - New patterns added to documentation
- [ ] **Best practices updated** - Guidelines updated based on review
- [ ] **Team knowledge enhanced** - Knowledge spread across team
- [ ] **Lessons learned captured** - Experience documented for future reference

## Emergency Review Protocol 🚨

### Conditions for Expedited Review
- [ ] **Critical production issue** - System down or major functionality broken
- [ ] **Security vulnerability** - Active security threat
- [ ] **Data loss prevention** - Immediate action needed to prevent data loss
- [ ] **Time-sensitive business requirement** - Business-critical deadline

### Expedited Review Process
- [ ] **Focus on critical path** - Review essential functionality only
- [ ] **Security scan performed** - Quick security review completed
- [ ] **Basic testing verified** - Core functionality tested
- [ ] **Documentation minimal** - Basic documentation provided
- [ ] **Follow-up planned** - Full review scheduled post-emergency

## Review Quality Metrics 📊

### Effectiveness Measures
- [ ] **Defect detection rate** - Issues found in review vs production
- [ ] **Review coverage** - Percentage of code changes reviewed
- [ ] **Comment quality** - Helpfulness of review comments
- [ ] **Time to resolution** - Speed of addressing review feedback
- [ ] **Knowledge transfer** - Learning achieved through review

### Continuous Improvement
- [ ] **Review process feedback** - Feedback on review effectiveness
- [ ] **Tool effectiveness** - Assessment of review tools
- [ ] **Training needs identified** - Areas for reviewer improvement
- [ ] **Process refinements** - Improvements to review process
- [ ] **Quality trends tracked** - Monitoring of quality over time

---

**Checklist Version**: 1.0.0
**Last Updated**: 2025-08-02
**Review Frequency**: Monthly
**Next Review**: 2025-09-02

## Notes for Reviewers

- **Focus on high-impact areas** - Prioritize review effort on critical aspects
- **Provide constructive feedback** - Help improve code quality and team knowledge
- **Balance thoroughness with efficiency** - Be thorough but respect time constraints
- **Encourage good practices** - Acknowledge and reinforce positive patterns
- **Facilitate learning** - Use reviews as knowledge sharing opportunities