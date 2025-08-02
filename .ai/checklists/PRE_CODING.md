# Pre-Coding Checklist

This checklist ensures that all necessary preparation is completed before beginning any coding work, preventing common issues and setting up for success.

## Overview

**Purpose**: Ensure proper preparation before coding
**Scope**: All coding tasks (features, bug fixes, refactoring)
**Responsibility**: All AI agents before implementation work

## General Preparation ✅

### 1. Context Understanding
- [ ] **Read current task requirements** - Understand what needs to be implemented
- [ ] **Review CODEBASE_STATE.md** - Understand current system state
- [ ] **Check WORK_LOG.md** - Review recent changes and decisions
- [ ] **Review KNOWN_ISSUES.md** - Check for related known issues
- [ ] **Understand business context** - Know why this change is needed

### 2. Technical Analysis
- [ ] **Read relevant documentation** - Review API docs, architecture docs
- [ ] **Understand affected components** - Identify what will be modified
- [ ] **Review existing patterns** - Check established patterns for similar work
- [ ] **Assess architectural impact** - Consider clean architecture compliance
- [ ] **Check dependency implications** - Understand dependency chain effects

### 3. Protected Systems Review ⚠️
- [ ] **Variant metafield system** - Verify no impact on working implementation
- [ ] **SIM carrier variants** - Ensure functionality preservation
- [ ] **Working API integrations** - Confirm no breaking changes planned
- [ ] **Configuration integrity** - Check impact on existing configs

## Agent-Specific Preparation

### Code Quality Architect 🏗️

#### Architecture Assessment
- [ ] **Review clean architecture compliance** - Ensure proper layer separation
- [ ] **Check SOLID principles adherence** - Validate design principles
- [ ] **Assess performance implications** - Consider performance impact
- [ ] **Review security considerations** - Check for security implications
- [ ] **Plan testing strategy** - Define comprehensive testing approach

#### Quality Standards
- [ ] **Review coding standards** - Ensure consistency with project standards
- [ ] **Check type hinting requirements** - Plan for proper type annotations
- [ ] **Assess complexity implications** - Consider cyclomatic complexity
- [ ] **Plan error handling approach** - Design comprehensive error handling
- [ ] **Review documentation needs** - Plan documentation updates

### Shopify API Developer 🛒

#### API Integration Review
- [ ] **Check Shopify API documentation** - Review relevant API endpoints
- [ ] **Verify API rate limits** - Understand rate limiting implications
- [ ] **Review authentication requirements** - Confirm auth token validity
- [ ] **Check metaobject definitions** - Verify required metaobjects exist
- [ ] **Plan error handling for API calls** - Design robust error handling

#### Protected System Verification
- [ ] **Variant metafield system status** - Confirm system is protected
- [ ] **GraphQL mutation integrity** - Verify working implementations safe
- [ ] **Metaobject reference format** - Confirm JSON array format usage
- [ ] **Rate limiting respect** - Plan for proper rate limit handling
- [ ] **Backward compatibility** - Ensure no breaking changes

### Web Research Specialist 🔍

#### Research Requirements
- [ ] **Identify research needs** - Understand what research is required
- [ ] **Check existing documentation** - Review current documentation state
- [ ] **Verify external references** - Confirm external links and references
- [ ] **Plan documentation updates** - Identify docs needing updates
- [ ] **Research best practices** - Find relevant best practices

#### Knowledge Verification
- [ ] **Check API version compatibility** - Verify using current API versions
- [ ] **Review third-party libraries** - Confirm library versions and security
- [ ] **Validate patterns and examples** - Ensure examples are current
- [ ] **Research performance implications** - Find performance best practices
- [ ] **Check security best practices** - Review security recommendations

### Product Strategy Advisor 📋

#### Business Requirements
- [ ] **Understand user requirements** - Clear understanding of user needs
- [ ] **Review acceptance criteria** - Detailed acceptance criteria defined
- [ ] **Check workflow impact** - Understand user workflow implications
- [ ] **Assess business value** - Confirm business value and priority
- [ ] **Plan user testing approach** - Define user validation strategy

#### UX Considerations
- [ ] **Review UI patterns** - Check established UI patterns
- [ ] **Plan user feedback mechanisms** - Design user feedback approach
- [ ] **Consider mobile responsiveness** - Plan for mobile compatibility
- [ ] **Check accessibility requirements** - Consider accessibility needs
- [ ] **Plan error message strategy** - Design user-friendly error messages

## Development Environment Setup ⚙️

### Local Environment
- [ ] **Development environment current** - Latest code from main branch
- [ ] **Dependencies installed** - All required packages installed
- [ ] **Environment variables set** - Proper .env configuration
- [ ] **Testing framework ready** - Test environment operational
- [ ] **Debug tools available** - Debugging tools configured

### Version Control
- [ ] **Git status clean** - No uncommitted changes
- [ ] **Main branch updated** - Latest changes pulled
- [ ] **Feature branch created** - New branch for the work
- [ ] **Branch naming follows convention** - Proper naming pattern used
- [ ] **Remote tracking set up** - Branch configured for push

### Tools and Resources
- [ ] **API documentation accessible** - Can access Shopify docs
- [ ] **Testing credentials available** - Test environment credentials ready
- [ ] **Monitoring tools ready** - Performance and error monitoring available
- [ ] **Communication channels open** - Can coordinate with other agents
- [ ] **Issue tracking accessible** - Can log and track issues

## Risk Assessment & Planning 🎯

### Risk Identification
- [ ] **Technical risks identified** - Known technical challenges documented
- [ ] **Integration risks assessed** - API integration risks considered
- [ ] **Performance risks evaluated** - Performance impact assessed
- [ ] **Security risks reviewed** - Security implications considered
- [ ] **Business risks understood** - Business impact risks identified

### Mitigation Planning
- [ ] **Rollback plan prepared** - Strategy for reverting changes if needed
- [ ] **Testing strategy comprehensive** - Thorough testing approach planned
- [ ] **Monitoring plan ready** - Post-deployment monitoring planned
- [ ] **Communication plan set** - Stakeholder communication planned
- [ ] **Timeline realistic** - Realistic implementation timeline set

### Dependencies & Coordination
- [ ] **Dependencies identified** - All technical dependencies mapped
- [ ] **Agent coordination planned** - Multi-agent work coordinated
- [ ] **External dependencies checked** - Third-party service status verified
- [ ] **Resource availability confirmed** - Required resources available
- [ ] **Blocking issues resolved** - No blockers preventing work

## Quality Gates Before Coding 🚪

### Documentation Review
- [ ] **Requirements documented** - Clear requirements documentation exists
- [ ] **Technical specifications ready** - Technical approach documented
- [ ] **Test plan outlined** - Testing approach documented
- [ ] **Acceptance criteria defined** - Clear success criteria established
- [ ] **Risk mitigation planned** - Risk response strategies documented

### Team Coordination
- [ ] **Work assignment clear** - Roles and responsibilities defined
- [ ] **Communication plan active** - Regular check-in schedule set
- [ ] **Progress tracking enabled** - Progress monitoring in place
- [ ] **Quality standards agreed** - Quality expectations aligned
- [ ] **Timeline coordinated** - Schedule coordinated with other work

### Technical Readiness
- [ ] **Architecture approach approved** - Technical approach validated
- [ ] **Patterns identified** - Relevant patterns selected for use
- [ ] **Tools and libraries selected** - Technology choices made
- [ ] **Performance benchmarks set** - Performance targets defined
- [ ] **Security requirements understood** - Security standards clear

## Final Pre-Coding Verification 🔍

### Checklist Completion
- [ ] **All relevant sections completed** - Appropriate checklist items done
- [ ] **Quality gates passed** - All quality checks satisfied
- [ ] **Risks mitigated** - Risk mitigation strategies in place
- [ ] **Resources ready** - All required resources available
- [ ] **Team aligned** - All team members aligned on approach

### Documentation Update
- [ ] **WORK_LOG.md updated** - Current work logged
- [ ] **Context files current** - Relevant context files updated
- [ ] **Agent handoff notes prepared** - Clear handoff documentation ready
- [ ] **Progress tracking initialized** - Progress monitoring set up
- [ ] **Success criteria documented** - Clear completion criteria defined

## Emergency Bypass Conditions 🚨

These conditions may warrant bypassing some checklist items for critical issues:

### Critical Production Issues
- [ ] **System down or data corruption** - Critical system failure
- [ ] **Security vulnerability** - Active security threat
- [ ] **Data loss risk** - Immediate data loss prevention needed

**If bypassing checklist:**
- [ ] **Document bypass reason** - Clear justification documented
- [ ] **Plan follow-up review** - Schedule post-emergency review
- [ ] **Communicate to team** - Inform team of bypass decision
- [ ] **Complete checklist post-emergency** - Finish checklist after resolution

---

**Checklist Version**: 1.0.0
**Last Updated**: 2025-08-02
**Review Frequency**: Monthly
**Next Review**: 2025-09-02

## Notes for Agents

- **Complete all applicable sections** - Not every item applies to every task
- **Document any skipped items** - Provide justification for skipped items
- **Update context files** - Keep project context current
- **Communicate progress** - Keep team informed of progress
- **Focus on quality** - Better to prepare thoroughly than rush into coding