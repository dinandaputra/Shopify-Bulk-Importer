# Complete Guide to Utilizing the Collaborative AI Agent System

## Table of Contents
1. [System Overview](#system-overview)
2. [Agent Specializations](#agent-specializations)
3. [Workflow Implementation](#workflow-implementation)
4. [Context Preservation](#context-preservation)
5. [Pattern Application](#pattern-application)
6. [Quality Assurance](#quality-assurance)
7. [Practical Scenarios](#practical-scenarios)
8. [Advanced Collaboration](#advanced-collaboration)
9. [Troubleshooting](#troubleshooting)

---

## System Overview

### What is the AI Agent System?
The AI Agent System is a structured framework of 4 specialized AI agents working collaboratively on the Shopify Bulk Importer project. Each agent has specific expertise, decision authority, and responsibilities.

### Key Benefits
- **Specialized Expertise**: Each agent focuses on their domain of strength
- **Quality Consistency**: Standardized workflows and quality gates
- **Context Preservation**: Seamless handoffs between sessions
- **Risk Mitigation**: Protected systems and quality checkpoints
- **Knowledge Sharing**: Centralized patterns and best practices

### Framework Structure
```
.ai/
├── agents/           # 4 specialized agent roles + general rules
├── workflows/        # 3 standardized process templates
├── patterns/         # 3 code pattern libraries  
├── checklists/       # 3 quality assurance gates
├── context/          # 5 state preservation files
└── templates/        # Future expansion space
```

---

## Agent Specializations

### 🏗️ Code Quality Architect
**Primary Expertise**: Architecture, Testing, Performance, Quality

#### When to Engage
- Implementing new features requiring architectural decisions
- Refactoring code for better structure
- Performance optimization needs
- Test strategy and implementation
- Code review and quality assurance

#### Decision Authority
- ✅ **Can Decide**: Code refactoring approaches, test strategies, performance optimizations
- ⚠️ **Requires Consultation**: Major architectural changes, breaking API changes

#### Best Practices for Collaboration
```
# Example Request
"As Code Quality Architect, please review the proposed smartphone template 
enhancement for architectural compliance and suggest testing approach."

# What They'll Provide
- Clean architecture assessment
- Performance impact analysis
- Comprehensive test strategy
- Code quality recommendations
```

#### Key Strengths
- Clean Architecture expertise
- SOLID principles enforcement
- Testing pattern mastery
- Performance profiling
- Security review capabilities

---

### 🛒 Shopify API Developer  
**Primary Expertise**: Shopify Integration, API Management, Metaobjects

#### When to Engage
- Any Shopify API integration work
- Metafield and metaobject management
- Rate limiting and error handling
- API performance optimization
- GraphQL/REST API decisions

#### Decision Authority
- ✅ **Can Decide**: API endpoint selection, query optimization, rate limit strategies
- ⚠️ **Requires Consultation**: API scope changes, authentication method changes

#### Critical Protected Systems ⚠️
This agent is the **ONLY** one authorized to modify:
- Variant metafield linking system (`assign_metafields_to_variants()`)
- SIM carrier variant creation logic
- Working GraphQL mutations

#### Best Practices for Collaboration
```
# Example Request
"As Shopify API Developer, please implement metafield creation for the new 
laptop GPU specifications while ensuring rate limiting compliance."

# What They'll Provide
- Optimal API approach (REST vs GraphQL)
- Rate limiting strategy
- Error handling implementation
- Data format validation
```

#### Key Strengths
- Shopify platform expertise
- API optimization techniques
- Metaobject system mastery
- Rate limiting management
- Integration robustness

---

### 🔍 Web Research Specialist
**Primary Expertise**: Research, Documentation, Best Practices, Product Specification Research

#### When to Engage
- Researching new technologies or approaches
- Updating documentation and guides
- Investigating best practices
- External API research
- Competitive analysis
- **Product specification research** (smartphones, laptops available in Japan)
- **Market analysis** and pricing research
- **Product template creation** and validation
- **Technical specification verification** and cross-referencing

#### Decision Authority
- ✅ **Can Decide**: Research methodologies, documentation updates, source prioritization, product specification validation, template creation
- ⚠️ **Requires Consultation**: Major technology recommendations, changes to existing product data structures, integration of research findings into workflows

#### Best Practices for Collaboration
```
# Technology Research Example
"As Web Research Specialist, please research the latest Shopify API 
updates and document any changes affecting our metafield implementation."

# Product Research Example
"As Web Research Specialist, please research all iPhone 16 models 
available in Japan, including carrier-specific variants and pricing, 
then create templates for the product entry system."

# What They'll Provide
- Comprehensive research findings with verified specifications
- Updated documentation and product templates
- Market analysis and competitive positioning
- Cross-referenced sources and validation
- Best practice recommendations
- Risk assessments for changes
```

#### Key Strengths
- Information synthesis and cross-referencing
- Documentation excellence and template creation
- Best practices knowledge across technologies and markets
- Technology trend awareness and product lifecycle tracking
- Validation and fact-checking with multiple source verification
- **Japan market expertise** for electronics and consumer devices
- **Product specification analysis** and technical validation
- **Competitive intelligence** and market positioning research

---

### 📋 Product Strategy Advisor
**Primary Expertise**: Features, UX, Business Logic, Roadmap

#### When to Engage
- Planning new features
- User experience optimization  
- Business logic design
- Workflow improvement
- Requirements analysis

#### Decision Authority
- ✅ **Can Decide**: Feature prioritization, UX designs, business rule definitions
- ⚠️ **Requires Consultation**: Major system changes, budget implications

#### Best Practices for Collaboration
```
# Example Request
"As Product Strategy Advisor, please analyze the user workflow for bulk 
laptop imports and suggest UX improvements to reduce entry time."

# What They'll Provide
- User workflow analysis
- UX improvement recommendations
- Business impact assessment
- Implementation priorities
```

#### Key Strengths
- User-centric thinking
- Business logic design
- Workflow optimization
- Requirements gathering
- Stakeholder communication

---

## Workflow Implementation

### 🚀 Feature Implementation Workflow
**Use Case**: Adding new functionality or capabilities

#### Phase 1: Planning & Analysis (Multi-Agent)
1. **Product Strategy Advisor** (0.5-1 day)
   - Requirements analysis
   - User story creation
   - Business impact assessment

2. **Code Quality Architect** (0.5-1 day)  
   - Technical analysis
   - Architecture impact assessment
   - Testing strategy planning

3. **Web Research Specialist + Shopify API Developer** (0.5-1 day)
   - API research and feasibility
   - Integration pattern design

#### Phase 2: Implementation (Specialized Agent)
4. **Code Quality Architect** (0.1-0.2 day)
   - Environment setup
   - Branch creation

5. **Domain Specialist** (1-5 days)
   - Core implementation based on feature type
   - Domain layer, infrastructure, presentation

6. **Shopify API Developer** (0.5-2 days)
   - API integration implementation

#### Phase 3: Quality Assurance (Code Quality Architect)
7. **Testing** (0.5-1 day)
   - Unit, integration, E2E testing

8. **Documentation** (Web Research Specialist, 0.2-0.5 day)
   - Documentation updates

#### Phase 4: Review & Deployment
9. **Code Review** (Code Quality Architect, 0.2-0.5 day)
10. **Deployment** (Multi-Agent, 0.1-0.5 day)

### 🐛 Bug Fixing Workflow
**Use Case**: Resolving issues and problems

#### Quick Reference by Severity
- **P0 (Critical)**: 4-hour resolution, immediate multi-agent response
- **P1 (High)**: 24-hour resolution, single agent with architect support
- **P2 (Medium)**: 1-week resolution, standard workflow
- **P3 (Low)**: Next release cycle, background work

#### Standard Bug Fix Process
1. **Triage** (Appropriate Specialist) - Reproduce and classify
2. **Root Cause Analysis** (Domain Expert) - Investigate thoroughly  
3. **Solution Design** (Code Quality Architect + Specialist) - Plan fix approach
4. **Implementation** (Domain Expert) - Implement and test
5. **Verification** (Product Strategy Advisor) - End-to-end validation

### 📝 Code Review Workflow
**Use Case**: Quality assurance for all changes

#### Review Assignment Matrix
| Change Type | Primary Reviewer | Secondary Reviewer |
|-------------|------------------|-------------------|
| API Integration | Shopify API Developer | Code Quality Architect |
| UI/UX Changes | Product Strategy Advisor | Code Quality Architect |
| Architecture | Code Quality Architect | Shopify API Developer |
| Documentation | Web Research Specialist | Product Strategy Advisor |

#### Review Process
1. **Pre-Review** - Automated checks verification
2. **Technical Review** - Architecture, implementation, integration
3. **Testing Review** - Test coverage and quality
4. **Documentation Review** - Documentation completeness
5. **Decision** - Approve, conditional approval, or request changes

---

## Context Preservation

### State Tracking Files
The system maintains 5 key context files for seamless collaboration:

#### 📊 CODEBASE_STATE.md
**Purpose**: Current system status and architecture overview
**Update Frequency**: After major changes
**Key Sections**:
- Project status summary
- Architecture overview
- Protected systems status
- Current working features

```markdown
# When to Update
- After completing major features
- When architecture changes
- After resolving critical issues
- Weekly during active development
```

#### 📝 WORK_LOG.md  
**Purpose**: Chronological record of all development work
**Update Frequency**: Daily during active development
**Key Sections**:
- Daily work summaries
- Technical achievements
- Decisions made
- Next priorities

```markdown
# Example Entry
## 2025-08-02 (Today)
### Phase 5: AI Agent System Implementation
**Agent**: Code Quality Architect
**Status**: ✅ Complete

#### ✅ Completed Today
- Created comprehensive AI agent framework
- Implemented 4 specialized agent roles
- Established context preservation system
```

#### 🏗️ ARCHITECTURE_DECISIONS.md
**Purpose**: Record of significant architectural decisions (ADRs)
**Update Frequency**: When architectural decisions are made
**Key Sections**:
- Decision context and rationale
- Alternatives considered
- Implementation approach
- Consequences and trade-offs

#### ⚠️ KNOWN_ISSUES.md
**Purpose**: Track current issues and technical debt
**Update Frequency**: As issues are discovered/resolved
**Key Sections**:
- Critical issues (immediate attention)
- Minor issues (planned resolution)
- Technical debt tracking

#### 💳 TECHNICAL_DEBT.md
**Purpose**: Comprehensive technical debt management
**Update Frequency**: Monthly reviews
**Key Sections**:
- Debt categorization and prioritization
- Remediation timelines
- Impact assessments

### Session Handoff Protocol

#### Starting a New Session
```markdown
# Session Startup Checklist
1. Read CODEBASE_STATE.md for current status
2. Review WORK_LOG.md for recent changes  
3. Check KNOWN_ISSUES.md for blockers
4. Review relevant agent role definition
5. Check for any protected system constraints
```

#### Ending a Session
```markdown
# Session Completion Checklist
1. Update WORK_LOG.md with work completed
2. Update CODEBASE_STATE.md if major changes
3. Log any new issues in KNOWN_ISSUES.md
4. Document decisions in ARCHITECTURE_DECISIONS.md
5. Prepare handoff notes for next session
```

#### Multi-Agent Coordination
```markdown
# Agent Handoff Template
## From: [Current Agent]
## To: [Next Agent]  
## Context: [Brief description]

### Work Completed
- [Task 1] - Status and notes
- [Task 2] - Status and notes

### Next Steps
1. [High priority task]
2. [Medium priority task]

### Important Notes
- [Any constraints or considerations]
- [Files modified]
- [Dependencies]
```

---

## Pattern Application

### 🛒 API Patterns (Shopify Integration)
**File**: `.ai/patterns/api_patterns.md`

#### Core Principles
1. **Always use centralized API client** - Never direct HTTP calls
2. **Respect rate limiting** - Implement backoff strategies  
3. **Comprehensive error handling** - Handle all API error types
4. **Data validation** - Validate inputs and outputs

#### Common Patterns

**Product Creation with Metafields**
```python
# ✅ Correct Pattern
def create_product_with_metafields(self, product_data: Dict, metafields: List[Dict]) -> Dict:
    # 1. Validate input data
    validated_data = self._validate_product_data(product_data)
    
    # 2. Create product via API
    product = self.api_client.create_product(validated_data)
    
    # 3. Attach metafields post-creation
    metafield_results = []
    for metafield in metafields:
        result = self.api_client.create_metafield(
            product["id"], "product", metafield
        )
        metafield_results.append(result)
    
    return {"product": product, "metafields": metafield_results}
```

**Rate Limiting with Retry**
```python
# ✅ Correct Pattern
@retry_with_backoff(max_retries=3)
async def api_call_with_retry(self, *args, **kwargs):
    try:
        return await self.api_client.call(*args, **kwargs)
    except RateLimitError as e:
        # Backoff handled by decorator
        raise
    except ShopifyAPIError as e:
        logger.error(f"API error: {e}")
        raise ProductCreationError(f"Could not complete operation: {e}") from e
```

### 🎨 UI Patterns (Streamlit)
**File**: `.ai/patterns/ui_patterns.md`

#### Core Principles
1. **User-centric design** - Prioritize workflow efficiency
2. **Consistency** - Maintain patterns across pages
3. **Progressive disclosure** - Show essential info first
4. **Error prevention** - Design to prevent mistakes

#### Common Patterns

**Standard Form Structure**
```python
# ✅ Correct Pattern
def create_product_form(product_type: str) -> Optional[Dict]:
    with st.form(key=f"{product_type}_form", clear_on_submit=True):
        st.subheader(f"📱 {product_type} Details")
        
        # Required fields section
        st.markdown("**Required Information**")
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Product Title*", help="Store display name")
        with col2:
            price = st.number_input("Price (JPY)*", min_value=0, step=100)
        
        # Form submission with validation
        submitted = st.form_submit_button("➕ Add Product", type="primary")
        
        if submitted:
            if not title or not price:
                st.error("Please fill in all required fields marked with *")
                return None
            return {"title": title, "price": price}
    return None
```

**Template Selection with Preview**
```python
# ✅ Correct Pattern  
def create_template_selector(templates: Dict[str, Dict]) -> Optional[str]:
    selected_template = st.selectbox(
        "Choose a template to auto-fill form",
        ["None (Manual Entry)"] + list(templates.keys())
    )
    
    if selected_template != "None (Manual Entry)":
        template_data = templates[selected_template]
        
        # Template preview
        with st.expander("👀 Template Preview", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"• Brand: {template_data.get('brand', 'N/A')}")
                st.write(f"• Model: {template_data.get('model', 'N/A')}")
        
        if st.button("✨ Apply Template"):
            # Apply template to form fields
            for key, value in template_data.items():
                st.session_state[f"form_{key}"] = value
            st.success("Template applied!")
            st.rerun()
```

### 🧪 Testing Patterns
**File**: `.ai/patterns/testing_patterns.md`

#### Core Principles
1. **Test pyramid structure** - More unit tests, fewer E2E tests
2. **AAA pattern** - Arrange, Act, Assert
3. **Independence** - Tests don't depend on each other
4. **Meaningful assertions** - Test behavior, not implementation

#### Common Patterns

**Unit Testing with Mocks**
```python
# ✅ Correct Pattern
class TestProductService:
    @pytest.fixture
    def mock_api_client(self):
        return Mock(spec=ShopifyAPIClient)
    
    @pytest.fixture  
    def service(self, mock_api_client):
        return ProductService(api_client=mock_api_client)
    
    def test_create_product_success(self, service, mock_api_client):
        # Arrange
        product_data = {"title": "Test Product", "price": 100000}
        mock_api_client.create_product.return_value = {"id": 123, "title": "Test Product"}
        
        # Act
        result = service.create_smartphone_product(product_data)
        
        # Assert
        assert result["id"] == 123
        mock_api_client.create_product.assert_called_once()
```

**Parameterized Testing**
```python
# ✅ Correct Pattern
@pytest.mark.parametrize("price,expected_valid", [
    (0, False),        # Zero price invalid
    (-100, False),     # Negative price invalid  
    (100, True),       # Positive price valid
    (999999, True),    # Large price valid
])
def test_price_validation(price, expected_valid):
    product_data = {"title": "Test", "price": price}
    
    if expected_valid:
        product = SmartphoneProduct(**product_data)
        assert product.price == price
    else:
        with pytest.raises(ValidationError):
            SmartphoneProduct(**product_data)
```

---

## Quality Assurance

### Quality Gates System
The AI Agent System includes 3 mandatory quality gates:

#### 1. 📋 PRE_CODING Checklist
**When**: Before starting any coding work
**Purpose**: Ensure proper preparation

**Key Sections**:
- Context understanding and technical analysis
- Protected systems verification  
- Environment setup and risk assessment
- Agent-specific preparation requirements

```markdown
# Example Usage
Before starting smartphone template enhancement:

✅ Read current requirements and business context
✅ Review CODEBASE_STATE.md for system status  
✅ Verify no impact on variant metafield system
✅ Check existing smartphone template patterns
✅ Plan testing approach for template changes
```

#### 2. ✅ PRE_COMMIT Checklist  
**When**: Before committing code changes
**Purpose**: Ensure code quality and system integrity

**Key Sections**:
- Functionality testing and protected systems verification
- Code standards compliance and architecture review
- API integration validation and performance checks
- Documentation updates and version control standards

```markdown
# Example Usage
Before committing new laptop metafield feature:

✅ All unit and integration tests passing
✅ Variant metafield system unmodified and working
✅ Clean architecture compliance verified
✅ Rate limiting and error handling implemented
✅ Documentation updated with new feature details
```

#### 3. 🔍 CODE_REVIEW Checklist
**When**: During code review process  
**Purpose**: Systematic quality assurance

**Key Sections**:
- Architecture and design review
- Code quality assessment  
- Testing and security verification
- Documentation and knowledge sharing

```markdown
# Example Usage
Reviewing smartphone bulk import feature:

✅ Clean architecture layers properly separated
✅ Shopify API integration follows established patterns
✅ Comprehensive test coverage including edge cases
✅ User-friendly error messages and validation
✅ Documentation updated and examples provided
```

### Quality Decision Matrix

#### Code Review Decisions
| Criteria | Approve ✅ | Conditional ⚠️ | Request Changes ❌ |
|----------|------------|----------------|---------------------|
| Functionality | Works correctly | Minor issues | Major bugs |
| Code Quality | High quality | Acceptable with notes | Quality issues |
| Testing | Comprehensive | Adequate | Insufficient |
| Documentation | Complete | Minor gaps | Major gaps |  
| Security | Secure | Minor concerns | Security issues |

#### Emergency Bypass Conditions
Sometimes quality gates may be bypassed for critical issues:
- **System completely down** - Total system failure
- **Data loss in progress** - Active data loss situation  
- **Security breach active** - Active security compromise

**Emergency Protocol**:
1. Document bypass reason clearly
2. Implement minimal scope fix only
3. Plan comprehensive follow-up review
4. Complete full quality gates post-emergency

---

## Practical Scenarios

### Scenario 1: Adding New Product Type (Tablets)
**Goal**: Extend system to support tablet product entry

#### Step-by-Step Agent Coordination

**Phase 1: Planning (Multi-Agent)**
```markdown
1. Product Strategy Advisor (Day 1):
   - "Analyze user workflow for tablet entry"
   - "Define tablet-specific fields and validation rules"
   - "Create user stories for tablet product entry"

2. Code Quality Architect (Day 1):  
   - "Review architectural impact of adding tablet support"
   - "Plan testing strategy for new product type"
   - "Assess performance implications"

3. Web Research Specialist (Day 1):
   - "Research tablet specifications and industry standards"
   - "Document tablet metafield requirements"
   - "Update API documentation for tablet support"
```

**Phase 2: Implementation (Specialized)**
```markdown
4. Code Quality Architect (Day 2):
   - "Create feature branch: feature/product-strategy/tablet-support"
   - "Set up tablet entity in domain layer"
   - "Create tablet Pydantic model with validation"

5. Shopify API Developer (Day 2-3):
   - "Implement tablet metafield mapping"
   - "Add tablet-specific API integration"
   - "Test metafield creation for tablet specs"

6. Product Strategy Advisor (Day 3):
   - "Create tablet entry Streamlit page"
   - "Implement tablet templates and auto-fill"
   - "Add tablet navigation and user workflow"
```

**Phase 3: Quality Assurance (Code Quality Architect)**
```markdown
7. Testing (Day 4):
   - "Create comprehensive tablet test suite"
   - "Test tablet product creation end-to-end"
   - "Verify no regressions in existing functionality"

8. Review & Deploy (Day 4):
   - "Conduct code review using CODE_REVIEW checklist"
   - "Update documentation and user guides"  
   - "Deploy to staging and production"
```

### Scenario 2: Optimizing API Performance
**Goal**: Reduce product creation time by 50%

#### Agent Coordination Strategy

**Phase 1: Analysis**
```markdown
1. Code Quality Architect:
   - "Profile current product creation performance" 
   - "Identify bottlenecks in API call patterns"
   - "Benchmark current performance metrics"

2. Shopify API Developer:
   - "Analyze API call frequency and efficiency"
   - "Research GraphQL bulk operations"
   - "Identify rate limiting optimization opportunities"
```

**Phase 2: Research & Planning**  
```markdown
3. Web Research Specialist:
   - "Research Shopify API performance best practices"
   - "Document bulk operation patterns"
   - "Find optimization case studies"

4. Product Strategy Advisor:
   - "Analyze user workflow impact of optimizations"
   - "Define acceptable performance targets"
   - "Plan rollout strategy for performance improvements"
```

**Phase 3: Implementation**
```markdown
5. Shopify API Developer:
   - "Implement GraphQL bulk product creation"
   - "Add intelligent batching for metafields"
   - "Optimize API call sequencing"

6. Code Quality Architect:
   - "Add performance monitoring and logging"
   - "Create performance regression tests"
   - "Validate optimization effectiveness"
```

### Scenario 3: Critical Bug Response (P0)
**Goal**: System down - product creation failing

#### Emergency Response Protocol

**Immediate Response (0-15 minutes)**
```markdown
1. Any Available Agent:
   - "Acknowledge critical issue immediately"
   - "Check system status and error logs"
   - "Determine scope of impact"
   - "Activate incident response"
```

**Assessment (15-60 minutes)**
```markdown
2. Shopify API Developer (if API-related):
   - "Investigate API integration failures"
   - "Check rate limiting and authentication"
   - "Assess need for immediate rollback"

3. Code Quality Architect:
   - "Analyze recent code changes"
   - "Check for obvious regressions"
   - "Prepare rollback plan if needed"
```

**Resolution (1-4 hours)**
```markdown
4. Domain Expert:
   - "Implement immediate fix or rollback"
   - "Test fix in staging environment"
   - "Deploy emergency resolution"

5. Product Strategy Advisor:
   - "Communicate with stakeholders"  
   - "Document business impact"
   - "Plan follow-up user communication"
```

**Post-Resolution**
```markdown
6. Code Quality Architect:
   - "Conduct post-mortem analysis"
   - "Document lessons learned"
   - "Plan prevention measures"
   - "Update monitoring and alerting"
```

### Scenario 4: Product Research & Template Creation
**Goal**: Research and create templates for new smartphone models available in Japan

#### Comprehensive Product Research Workflow

**Phase 1: Market Research (Web Research Specialist)**
```markdown
1. Web Research Specialist (Day 1-2):
   - "Research all iPhone 16 series models available in Japan"
   - "Investigate carrier-specific variants and pricing"
   - "Document technical specifications from official sources"
   - "Create comprehensive product specification reports"
   - "Analyze market positioning and competitive landscape"
```

**Phase 2: Template Development (Web Research Specialist + Product Strategy Advisor)**
```markdown
2. Web Research Specialist (Day 2-3):
   - "Create product templates based on research findings"
   - "Map technical specifications to existing metaobjects"
   - "Validate template data against multiple sources"
   - "Document template creation methodology"

3. Product Strategy Advisor (Day 3):
   - "Review templates for user workflow optimization"
   - "Validate business logic and categorization"
   - "Optimize template structure for data entry efficiency"
   - "Plan template integration into user interface"
```

**Phase 3: Technical Integration (Shopify API Developer + Code Quality Architect)**
```markdown
4. Shopify API Developer (Day 3-4):
   - "Review metafield mappings for new specifications"
   - "Identify any missing metaobjects required"
   - "Validate API compatibility with new data structures"
   - "Test template data with existing systems"

5. Code Quality Architect (Day 4):
   - "Integrate templates into master_data.py"
   - "Add validation rules for new product types"
   - "Create tests for template functionality"
   - "Update documentation with new templates"
```

**Example Research Output:**
```markdown
# iPhone 16 Pro Max Research Report
## Official Specifications (Apple Japan)
- **Display**: 6.7-inch Super Retina XDR, 2796x1290, ProMotion 120Hz
- **Processor**: A18 Pro chip with 6-core CPU
- **Storage Options**: 256GB, 512GB, 1TB
- **Colors**: Natural Titanium, Blue Titanium, White Titanium, Black Titanium
- **Camera**: 48MP Main, 48MP Ultra Wide, 12MP 5x Telephoto
- **5G Bands**: All Japan carrier bands supported

## Japan Market Analysis
- **Docomo**: Available in all colors, 24-month payment plans
- **Softbank**: Exclusive early access program
- **AU**: Trade-in programs available
- **SIM-Free**: Apple Store Japan, major electronics retailers
- **Pricing**: ¥189,800 (256GB), ¥219,800 (512GB), ¥249,800 (1TB)

## Template Creation
```json
{
  "iPhone 16 Pro Max 256GB [Natural Titanium]": {
    "title": "iPhone 16 Pro Max 256GB Natural Titanium",
    "brand": "Apple",
    "model": "iPhone 16 Pro Max",
    "storage": "256GB",
    "color": "Natural Titanium",
    "ram": "8GB",
    "display": "6.7-inch Super Retina XDR",
    "processor": "A18 Pro",
    "camera": "48MP Triple Camera System",
    "connectivity": "5G (all Japan bands)"
  }
}
```

**Phase 4: Quality Assurance & Deployment**
```markdown
6. Code Quality Architect (Day 5):
   - "Test template integration end-to-end"
   - "Verify metafield creation with new templates"
   - "Validate no regressions in existing functionality"
   - "Deploy templates to production"

7. Web Research Specialist (Ongoing):
   - "Monitor for new model announcements"
   - "Update templates with specification changes"
   - "Maintain market analysis and pricing data"
   - "Validate template accuracy quarterly"
```

---

## Advanced Collaboration

### Multi-Agent Project Coordination

#### Project Planning Template
```markdown
# Project: [Name]
## Duration: [Timeline]
## Agents Involved: [List]

### Phase 1: Research & Planning
- **Web Research Specialist**: [Specific tasks]
- **Product Strategy Advisor**: [Specific tasks] 
- **Duration**: [Timeline]

### Phase 2: Architecture & Design  
- **Code Quality Architect**: [Specific tasks]
- **Shopify API Developer**: [Specific tasks]
- **Duration**: [Timeline]

### Phase 3: Implementation
- **Primary Agent**: [Lead implementer]
- **Supporting Agents**: [Support roles]
- **Duration**: [Timeline]

### Phase 4: Quality & Deployment
- **Code Quality Architect**: [QA tasks]
- **All Agents**: [Review and validation]
- **Duration**: [Timeline]

### Coordination Points
- Daily standup: [Time/method]
- Weekly review: [Schedule]
- Milestone gates: [Checkpoints]
```

#### Knowledge Sharing Sessions
```markdown
# Weekly Knowledge Sharing
## Format: 30-minute collaborative session

### Agenda Template
1. **Recent Learnings** (5 minutes each agent)
   - New patterns discovered
   - Technical insights gained
   - Best practices refined

2. **Pattern Updates** (10 minutes)
   - API pattern improvements
   - UI pattern enhancements  
   - Testing pattern additions

3. **Process Improvements** (10 minutes)
   - Workflow optimizations
   - Quality gate refinements
   - Tool and automation ideas

4. **Next Week Planning** (5 minutes)
   - Upcoming challenges
   - Collaboration needs
   - Priority alignment
```

### Continuous Improvement Process

#### Monthly Retrospective Template
```markdown
# Monthly Retrospective - [Month Year]

## What Went Well ✅
- [Agent collaboration successes]
- [Quality improvements achieved]  
- [Process optimizations implemented]

## What Could Be Better ⚠️
- [Communication gaps identified]
- [Process bottlenecks found]
- [Quality issues encountered]

## Action Items 🎯
- [Specific improvements to implement]
- [Process changes to trial]
- [Documentation updates needed]

## Metrics Review 📊
- [Code quality metrics]
- [Performance indicators]
- [User satisfaction scores]
```

#### Agent Skill Development
```markdown
# Skill Enhancement Framework

## Code Quality Architect
- Advanced architecture patterns
- Performance optimization techniques
- Security best practices
- Testing methodologies

## Shopify API Developer  
- New Shopify API features
- GraphQL optimization
- Integration patterns
- Rate limiting strategies

## Web Research Specialist
- Information validation techniques and source verification
- Documentation standards and template creation
- Research methodologies for technology and product analysis
- Knowledge synthesis and competitive intelligence
- **Japan market research expertise** and consumer electronics analysis
- **Product specification validation** and technical accuracy verification
- **Market trend analysis** and pricing intelligence

## Product Strategy Advisor
- User experience research
- Business analysis methods
- Workflow optimization
- Stakeholder communication
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Agent Role Confusion
**Symptoms**: Agents working outside their expertise areas
**Solution**:
```markdown
1. Review agent role definitions in .ai/agents/
2. Use decision authority matrix to clarify responsibilities
3. Refer to workflow phase assignments
4. Escalate to Code Quality Architect for coordination
```

#### Issue: Context Loss Between Sessions
**Symptoms**: Repeated work, missing important decisions
**Solution**:
```markdown
1. Always start sessions by reading CODEBASE_STATE.md
2. Update WORK_LOG.md at end of each session
3. Use session handoff template for agent transitions
4. Keep context files current and detailed
```

#### Issue: Quality Gate Conflicts
**Symptoms**: Disagreement on quality standards or decisions  
**Solution**:
```markdown
1. Refer to specific quality checklist criteria
2. Use decision matrix for objective assessment
3. Escalate to Code Quality Architect for final decision
4. Document resolution in ARCHITECTURE_DECISIONS.md
```

#### Issue: Protected System Violations
**Symptoms**: Breaking changes to working systems
**Solution**:
```markdown
1. Immediately stop and assess impact
2. Check GENERAL_RULES.md for protected systems
3. Revert changes if any protected systems modified
4. Only Shopify API Developer can modify protected systems
5. Document any approved exceptions
```

### Escalation Procedures

#### Technical Escalation Path
```markdown
Level 1: Domain Specialist (individual agent expertise)
Level 2: Code Quality Architect (coordination and standards)
Level 3: Multi-Agent Collaboration (complex issues)
Level 4: External Consultation (outside expertise needed)
```

#### Business Escalation Path
```markdown
Level 1: Product Strategy Advisor (business impact assessment)
Level 2: Stakeholder Communication (business decision needed)
Level 3: Executive Escalation (high-level business decision)
```

#### Emergency Escalation
```markdown
Critical Issues (P0):
- Immediate acknowledgment required
- Multi-agent response activated
- Bypass normal quality gates if necessary
- Document all emergency decisions
- Plan comprehensive post-emergency review
```

---

## Quick Reference Cards

### Agent Selection Guide
```markdown
Task Type → Recommended Agent

Architecture Changes → Code Quality Architect
API Integration → Shopify API Developer  
Technology Research → Web Research Specialist
**Product Specification Research** → Web Research Specialist
**Market Analysis** → Web Research Specialist + Product Strategy Advisor
UX/Workflow → Product Strategy Advisor
Bug Investigation → Domain Specialist + Code Quality Architect
Performance Issues → Code Quality Architect + Shopify API Developer
Documentation → Web Research Specialist + Domain Expert
**Template Creation** → Web Research Specialist + Product Strategy Advisor
**Competitive Analysis** → Web Research Specialist
```

### Workflow Selection Guide
```markdown
Work Type → Recommended Workflow

New Feature → Feature Implementation Workflow
Bug/Issue → Bug Fixing Workflow  
Code Changes → Code Review Workflow
Research Task → Custom coordination (no specific workflow)
Emergency → Emergency Response Protocol
```

### Quality Gate Quick Check
```markdown
Before Starting Work:
✅ Read PRE_CODING checklist
✅ Understand requirements and context
✅ Check protected systems
✅ Plan approach and testing

Before Committing:  
✅ Complete PRE_COMMIT checklist
✅ All tests passing
✅ Documentation updated
✅ No protected system modifications

During Review:
✅ Use CODE_REVIEW checklist  
✅ Check all quality criteria
✅ Provide constructive feedback
✅ Document decisions
```

---

**Guide Version**: 1.1.0  
**Created**: 2025-08-02  
**Last Updated**: 2025-08-02  
**Maintainer**: All AI Agents (Collaborative)

## Recent Updates (v1.1.0)
- **Enhanced Web Research Specialist role** with product specification research capabilities
- **Added Japan market research expertise** for smartphones and laptops
- **New product research methodologies** and validation processes  
- **Comprehensive template creation workflows** and market analysis procedures
- **Added Scenario 4**: Product Research & Template Creation example
- **Updated agent selection guide** with product research task types

## Getting Started

1. **Read this guide thoroughly** - Understand the system before using it
2. **Choose your task** - Identify what you want to accomplish  
3. **Select appropriate agent(s)** - Use the agent selection guide
4. **Follow the workflow** - Use standardized processes
5. **Maintain context** - Update context files as you work
6. **Use quality gates** - Don't skip the checklists
7. **Share knowledge** - Document learnings and improvements

The AI Agent System is designed to make development more efficient, consistent, and high-quality. Take time to learn the system and it will significantly improve your development experience and outcomes.