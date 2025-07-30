# MyByte Shopify Product Manager - PRD

## 📖 Executive Summary

Build a **Streamlit web application** that helps MyByte staff efficiently input used electronics data and generate Shopify-compatible CSV files for product import. The app will replace manual Google Sheets workflow and reduce data entry time by 50%.

**Key Goal**: Create individual product listings for used electronics with proper metafields, auto-generated handles, and validation.

---

## 🎯 Product Overview

### What We're Building
A Streamlit-based product data entry system that:
- Captures electronics product information through forms
- Validates data according to business rules
- Auto-generates Shopify handles with daily counters
- Exports properly formatted CSV files for Shopify import
- Supports both smartphone and laptop categories

### Success Metrics
- **Data entry time**: Reduce from 5 minutes to 2 minutes per product
- **Error rate**: Zero formatting errors on Shopify import
- **Daily capacity**: Handle 45+ products per day efficiently
- **User adoption**: 100% staff usage within 2 weeks

---

## 👥 Users & Use Cases

### Primary Users
**MyByte Staff** (2-3 people, non-technical)
- Input 45+ used products daily
- Work primarily on desktop, occasionally mobile
- Speak Indonesian/English, some Japanese
- Need fast, error-proof data entry

### User Stories

**As a MyByte staff member, I want to:**
1. **Quick Entry**: Input product details in under 2 minutes
2. **Auto-Handle**: Get handles generated automatically with proper format
3. **Validation**: See errors immediately before saving
4. **CSV Export**: Download ready-to-import Shopify CSV files
5. **Mobile Access**: Use the app on mobile when needed
6. **Batch Processing**: Enter multiple products efficiently

**As a store manager, I want to:**
1. **Data Consistency**: Ensure all products follow standardized format
2. **Error Prevention**: Prevent invalid data from reaching Shopify
3. **Audit Trail**: Track daily product entry counts
4. **Quick Training**: Onboard new staff easily

---

## ⚡ Core Features

### 🔥 Must-Have Features (Phase 1 - Smartphone MVP)

#### 1. Product Title System
```
GIVEN I want to enter a product
WHEN I start typing product name
THEN I see template suggestions OR can enter free text
AND title auto-updates brand/model fields if using template
AND I can override with completely custom title
```

#### 2. Smartphone Data Entry Form
```
GIVEN I'm entering smartphone data
WHEN I fill the form
THEN I can input:
- Title: Template suggestions or free text
- Basic info: brand, model, storage, price
- Metafields: SIM carriers, rank, RAM, inclusions (multi), minus (multi), color
AND I see real-time validation
AND handle is auto-generated
```

#### 3. Auto Handle Generation
```
GIVEN I enter product title "iPhone 15 Pro 128GB"
WHEN system generates handle
THEN format is "iphone-15-pro-128gb-250715-001"
AND counter increments daily (001, 002, 003...)
AND resets every day at midnight
```

#### 4. Multi-Select Fields
```
GIVEN I select metafields
WHEN I choose inclusions or minus
THEN I can select multiple options
AND they display as tags/chips in UI
AND export as comma-separated in CSV
```

#### 5. Data Validation
```
GIVEN I submit product data
WHEN validation runs
THEN I see errors for:
- Missing required fields (title, price)
- Invalid price (≤0)
AND I get warnings for recommendations (SIM carrier)
AND cannot export until errors fixed
```

#### 6. CSV Export
```
GIVEN I have valid products
WHEN I click export
THEN I get Shopify-compatible CSV with:
- Proper column headers
- Multi-select fields joined with ", "
- Ready for direct import
```

### 🚀 Nice-to-Have Features (Phase 2 - Laptop Category)

#### 7. Laptop Category Support
- Complete laptop form with all metafields
- Processor, RAM, graphics, display, storage fields
- Category-specific validation rules

#### 8. Enhanced Features
- Batch entry capability
- Session management
- Performance optimization

### 🔮 Future Features (Phase 3)
- Shopify API integration (direct upload)
- Photo upload and management
- GSTPad barcode integration
- Multi-language interface

---

## 🏗️ Technical Specifications

### Technology Stack
```python
# Core Framework
streamlit >= 1.28.0

# Data Processing
pandas >= 2.0.0
pydantic >= 2.0.0

# Utilities
python-dateutil >= 2.8.0
```

### Architecture
```
streamlit_app.py (main entry point)
├── config/
│   ├── settings.py
│   └── master_data.py
├── database/
│   ├── handle_counter.py (persistent daily counter)
│   └── session_manager.py
├── pages/
│   ├── smartphone_entry.py
│   └── laptop_entry.py (Phase 2)
├── components/
│   ├── product_form.py
│   ├── validation_panel.py
│   └── export_panel.py
├── models/
│   ├── smartphone.py
│   └── laptop.py
├── services/
│   ├── title_templates.py
│   ├── validation_service.py
│   └── export_service.py
├── utils/
│   ├── handle_generator.py
│   ├── csv_exporter.py
│   └── validators.py
└── tests/
    ├── test_validation.py
    └── test_export.py
```

### Data Models

#### Smartphone Product
```python
class SmartphoneProduct(BaseModel):
    # Core fields
    title: str
    brand: str  
    model: str
    storage: Optional[str]
    price: float
    quantity: int = 1
    
    # Metafields (exact Shopify metaobject names)
    color: Optional[str] = None
    sim_carriers: Optional[str] = None  # "SIM Free", "Docomo (-)", etc.
    minus: Optional[List[str]] = None  # Multi-select: ["Battery service", "White spot"]
    product_inclusions: Optional[List[str]] = None
    product_rank: Optional[str] = None  # "A", "A+", "S", "S+", "BNIB", etc.
    ram_size: Optional[str] = None  # "3GB", "4GB", "6GB", etc.
    
    # Auto-generated
    handle: Optional[str] = None
    vendor: str = "myByte International"
    tags: str = "smartphone"
    published: str = "TRUE"
```

### CSV Output Format
```csv
Handle,Title,Body HTML,Vendor,Type,Tags,Published,Variant SKU,Variant Inventory Qty,Variant Price,Variant Barcode,Metafield: custom.color,Metafield: custom.sim_carriers,Metafield: custom.minus,Metafield: custom.product_inclusions,Metafield: custom.product_rank,Metafield: custom.ram_size
iphone-15-pro-128gb-250715-001,iPhone 15 Pro 128GB,,myByte International,,smartphone,TRUE,,1,89800,,,SIM Free,,With box,A+,8GB
```

---

## 📊 Data Requirements

### Master Data (Dropdown Options)

#### SIM Carriers (5 options)
```python
SIM_CARRIERS = [
    "SIM Free",
    "Docomo (-)", 
    "AU (-)",
    "Softbank (-)",
    "Rakuten Mobile (-)"
]
```

#### Product Rank (7 options)
```python
PRODUCT_RANKS = [
    "A",      # Fair condition, visible screen marks
    "A+",     # Good condition, minor screen marks  
    "S",      # Excellent condition, no screen scratches
    "S+",     # Like new condition, very light usage
    "BNWB",   # Brand New Without Box
    "BNOB",   # Brand New Open Box
    "BNIB"    # Brand New In Box
]
```

#### Product Inclusions (9 options, multi-select)
```python
PRODUCT_INCLUSIONS = [
    "Bonus charger",
    "Bonus anti gores",
    "Bonus softcase", 
    "Bukan box bawaan",
    "With box",
    "No box",
    "Full set cable",
    "Full set (charger)",
    "Bonus adapter"
]
```

#### Minus Options (5 options, multi-select)
```python
MINUS_OPTIONS = [
    "Battery service",      # Need battery service
    "Speaker pecah",        # Speaker damaged/cracked
    "White spot",          # White spot on screen
    "Shadow",              # Screen burn-in present
    "Dead Pixel"           # Dead pixel on screen
]
```

#### RAM Options (6 options)
```python
RAM_OPTIONS = ["3GB", "4GB", "6GB", "8GB", "12GB", "16GB"]
```

### Handle Generation Logic
```
Format: {brand}-{model}-{specs}-{YYMMDD}-{counter}
Example: iphone-15-pro-128gb-250715-001

Rules:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters
- Daily counter reset (001, 002, 003...)
- Date format: YYMMDD
```

---

## 🎨 User Interface Requirements

### Layout Structure
```
┌─────────────────────────────────────────────────┐
│ 📱 MyByte Product Manager                      │
├─────────────────────────────────────────────────┤
│ Sidebar:                                        │
│ • Category Selection (Smartphone/Laptop)       │
│ • Export Panel                                  │
│ • Session Stats                                 │
├─────────────────────────────────────────────────┤
│ Main Area:                                      │
│ • Product Entry Form                            │
│ • Live Preview                                  │
│ • Validation Results                            │
└─────────────────────────────────────────────────┘
```

### Form Design

#### Smartphone Form Layout
```
┌─────────────────┬─────────────────┐
│ Title Templates [searchable] OR Title [free text] │
├─────────────────┼─────────────────┤
│ Brand* [dropdown] │ SIM Carriers [dropdown] │
│ Model* [text]     │ Rank [dropdown]         │
│ Storage [text]    │ RAM [dropdown]          │
│ Price* [number]   │ Color [text]            │
├─────────────────┴─────────────────┤
│ Inclusions [multiselect]          │
│ Minus [multiselect]               │
├───────────────────────────────────┤
│ Generated Handle: [preview]       │
│ ✅ Validation Status             │
└───────────────────────────────────┘
```

### Title Template System
```
User types: "iphone 15 pro"
System suggests:
• iPhone 15 Pro 128GB (SIM Free)
• iPhone 15 Pro 256GB (SIM Free) 
• iPhone 15 Pro 512GB (SIM Free)
• iPhone 15 Pro 1TB (SIM Free)

User types: "samsung galaxy s25"
System suggests:
• Samsung Galaxy S25 128GB (SIM Free)
• Samsung Galaxy S25 256GB (SIM Free)
• Samsung Galaxy S25 Ultra 256GB (SIM Free)

Or user can type completely custom title
```

### Desktop-Optimized Design (MVP Focus)
```css
Desktop (>1024px): Two-column form layout with sidebar
Desktop (768px-1024px): Single column with optimized form spacing
Tablet/Mobile: Basic functionality (Phase 3 enhancement)
```

---

## ✅ Acceptance Criteria

### Phase 1 Definition of Done

#### Feature: Smartphone Data Entry
```
✅ Form displays all required fields for smartphones only
✅ Title templates system working with search/suggestions
✅ Multi-select working for inclusions and minus fields
✅ Dropdowns populated with correct master data
✅ Real-time validation shows errors and warnings separately
✅ Handle auto-generates with correct format and daily counter
✅ Can save multiple products in session (10 max per session)
✅ Export generates valid Shopify CSV
✅ CSV imports successfully to Shopify test store
✅ Desktop layout is optimized for data entry speed
```

#### Feature: Data Validation  
```
✅ Required field validation (title, price)
✅ Price validation (must be >0)
✅ Handle format validation
✅ Warning system for recommendations (SIM carrier)
✅ Error messages are clear and actionable
✅ Cannot export with validation errors
✅ Warnings don't block export
```

#### Feature: CSV Export
```
✅ CSV has correct Shopify column headers for smartphones
✅ Multi-select metafields formatted as "option1, option2"
✅ Single metafield values formatted correctly
✅ Empty fields are blank (not "None")
✅ File downloads with timestamp in name
✅ Can import to Shopify without errors
```

### Performance Requirements
- **Form submission**: <500ms response time
- **CSV generation**: <1 second for 10 products per session (45+ daily total)
- **Page load**: <2 seconds on desktop
- **Memory usage**: <50MB for typical session (10 products max)

### Browser Support
- **Primary**: Chrome 120+, Safari 17+, Edge 120+
- **Minimum**: Modern browsers with ES6 support
- **Mobile**: Not required for MVP (future enhancement)

---

## 🚨 Business Rules & Constraints

### Data Validation Rules

#### Global Rules
1. **Required fields**: Title, price must not be empty
2. **Price validation**: Must be positive number
3. **Handle uniqueness**: System generates unique handles with daily counter (duplicate titles OK)
4. **Secondhand items**: Each product gets unique listing even with same title/model

#### Smartphone-Specific Rules
1. **SIM carrier recommendation**: Warning if not selected (not required)
2. **Multi-select handling**: Product inclusions and minus can have multiple values
3. **Title flexibility**: Allow free-form title input with optional templates

#### CSV Export Rules
1. **Metafield format**: Use exact display names from Shopify
2. **Multi-select handling**: Join with ", " (comma + space)
3. **Empty values**: Export as empty string, not "None"

### Operational Constraints
1. **Daily volume**: Support 45+ products per day (10 products per session max)
2. **Session management**: Handle browser refresh gracefully
3. **File size**: CSV exports should be <1MB per session
4. **Concurrent users**: Support 2-3 simultaneous users

---

## 🚀 Implementation Plan

### Phase 1: Smartphone MVP (Week 1-2)
**Goal**: Complete smartphone entry system + CSV export

**Sprint 1** (Week 1):
- [ ] Project setup (Streamlit + dependencies)
- [ ] Basic UI layout with sidebar
- [ ] Smartphone data model (Pydantic)
- [ ] Master data integration (focus on smartphone only)
- [ ] Product title templates system
- [ ] Basic form rendering

**Sprint 2** (Week 2):
- [ ] Handle generation logic with persistent daily counter
- [ ] Data validation system (errors/warnings)
- [ ] CSV export functionality
- [ ] Testing with real Shopify import
- [ ] Desktop UI optimization and polish

### Phase 2: Laptop Category (Week 3-4)
**Goal**: Add laptop support + enhanced features

**Sprint 3** (Week 3):
- [ ] Laptop data model and form
- [ ] Category switching interface
- [ ] Laptop-specific validation
- [ ] Session state management

**Sprint 4** (Week 4):
- [ ] Batch entry interface
- [ ] Export multiple products
- [ ] Performance optimization
- [ ] User acceptance testing

### Phase 3: Future Enhancements
- [ ] Mobile responsive design and mobile UX optimization
- [ ] Shopify API integration (direct upload)
- [ ] Photo upload functionality
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] Advanced duplicate detection (if needed)

---

## 📝 Example User Journey

### Typical Daily Workflow
```
1. Staff opens app → Smartphone category (default)
2. Starts typing title → System suggests templates OR enters custom
3. Fills form:
   - Title: iPhone 15 Pro 128GB (from template or custom)
   - Brand: iPhone (auto-filled from template)
   - Model: 15 Pro (auto-filled from template) 
   - Storage: 128GB (auto-filled from template)
   - Price: ¥89,800
   - SIM Carriers: SIM Free
   - Rank: A+
   - Inclusions: [With box, Bonus charger] (multi-select)
   - Minus: [Battery service] (multi-select, if any)
4. System auto-generates handle: "iphone-15-pro-128gb-250715-001"
5. Validation passes ✅ (or shows warnings)
6. Clicks "Add to Export List"
7. Repeats for 5-10 more products (max 10 per session)
8. Clicks "Export CSV" 
9. Downloads: "mybyte-smartphones-2025-07-15-14-30.csv"
10. Imports to Shopify → All products created successfully
11. Starts new session for next batch (throughout the day to reach 45+ total)
```

### Error Handling Example
```
1. User enters price as "0"
2. Validation shows: ❌ "Price must be greater than 0"
3. User enters price as "89800"
4. Validation shows: ✅ "All fields valid"
5. Can proceed to add product
```

---

## 🎯 Success Metrics & KPIs

### Immediate Metrics (Week 1-4)
- **Data entry time**: Target <2 minutes per product
- **Error rate**: Target 0% validation errors
- **CSV import success**: Target 100% successful imports
- **User adoption**: Target 100% staff usage

### Long-term Metrics (Month 1-3)
- **Daily productivity**: Target 45+ products/day
- **Time savings**: Target 50% reduction vs manual process
- **Data quality**: Target 0% data correction needed
- **User satisfaction**: Target 4.5/5 rating from staff

---

## 📋 Testing Strategy

### Manual Testing
- [ ] Form validation with various inputs
- [ ] CSV export and Shopify import
- [ ] Mobile responsiveness
- [ ] Handle generation edge cases
- [ ] Session state persistence

### User Acceptance Testing
- [ ] Staff tests with real product data
- [ ] Performance testing with 50+ products
- [ ] Mobile usage scenarios
- [ ] Error recovery testing

### Test Data
```python
# Sample test products
test_products = [
    {
        "title": "iPhone 15 Pro 128GB",
        "brand": "iPhone",
        "model": "15 Pro", 
        "storage": "128GB",
        "price": 89800,
        "sim_carriers": "SIM Free",
        "product_rank": "A+",
        "expected_handle": "iphone-15-pro-128gb-YYMMDD-001"
    }
]
```

---

This PRD provides Claude Code with clear, actionable requirements to build the MyByte Shopify Product Manager application.