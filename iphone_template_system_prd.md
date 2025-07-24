# iPhone Template System - Product Requirements Document

**Project**: Shopify Bulk Importer - iPhone Template Enhancement  
**Team**: MyByte International  
**Date**: July 22, 2025  
**Status**: Phase 1 & 2 Complete - Ready for Phase 3  
**Last Updated**: July 23, 2025  

## Project Overview

### Current Problem
MyByte International staff currently spend excessive time on manual product entry, requiring:
- Manual typing of product titles, models, and storage
- Separate selection of brand, model, storage fields 
- Manual inclusion selection without smart groupings
- No standardized color/storage validation for iPhone models
- Inconsistent collection assignment
- Time-consuming workflow with repetitive data entry

### Solution Goals
Implement a smart template system that:
- **Reduces product entry time by 70%**
- **Eliminates specification errors** with validated iPhone database
- **Automates collection assignment** with manual override capability
- **Streamlines inclusion selection** with smart mapping
- **Integrates professional image upload** with Shopify CDN
- **Maintains data accuracy** while improving speed

### Target Users
MyByte International staff entering used electronics (primarily iPhones) into Shopify inventory system.

## Detailed Requirements

### 1. iPhone Template System

#### 1.1 Template Format
- **User Selection**: `"iPhone 15 Pro Max 256GB [Desert Titanium]"`
- **Generated Title**: `"iPhone 15 Pro Max 5G 256GB (SIM Free)"` (iPhone 12+)
- **Generated Title**: `"iPhone 11 Pro Max 256GB (SIM Free)"` (iPhone 11 and older - NO 5G)
- **Editable Output**: Staff can modify title for rare cases like `(Dual SIM)` or `(Silent Camera)`

#### 1.2 5G Logic Implementation
- **iPhone 12 and above**: Include "5G" in generated title
- **iPhone 11 and older**: NO "5G" in title (4G LTE only)
- **Auto-detection**: Based on iPhone model from comprehensive database

#### 1.3 Auto-Extraction from Template
When template is selected, automatically populate:
- **Product Title**: Generated with correct 5G designation
- **Brand**: "iPhone" 
- **Color**: Extracted from template `[Color]` and mapped to color metafield
- **Collections**: "All Products" + "iPhone" (auto-selected, editable)

### 2. Comprehensive iPhone Specifications Database

#### 2.1 iPhone Models with 5G Support (2020+)
**iPhone 16 Series (2024)**:
- iPhone 16: 128GB/256GB/512GB | Black, White, Pink, Teal, Ultramarine  
- iPhone 16 Plus: 128GB/256GB/512GB | Black, White, Pink, Teal, Ultramarine
- iPhone 16 Pro: 128GB/256GB/512GB/1TB | Black Titanium, White Titanium, Natural Titanium, Desert Titanium
- iPhone 16 Pro Max: 256GB/512GB/1TB | Black Titanium, White Titanium, Natural Titanium, Desert Titanium

**iPhone 15 Series (2023)**:
- iPhone 15: 128GB/256GB/512GB | Black, Blue, Green, Yellow, Pink
- iPhone 15 Plus: 128GB/256GB/512GB | Black, Blue, Green, Yellow, Pink  
- iPhone 15 Pro: 128GB/256GB/512GB/1TB | Black Titanium, White Titanium, Blue Titanium, Natural Titanium
- iPhone 15 Pro Max: 256GB/512GB/1TB | Black Titanium, White Titanium, Blue Titanium, Natural Titanium

**iPhone 14 Series (2022)**:
- iPhone 14: 128GB/256GB/512GB | Blue, Purple, Midnight, Starlight, (PRODUCT)RED
- iPhone 14 Plus: 128GB/256GB/512GB | Blue, Purple, Midnight, Starlight, (PRODUCT)RED
- iPhone 14 Pro: 128GB/256GB/512GB/1TB | Deep Purple, Gold, Silver, Space Black
- iPhone 14 Pro Max: 128GB/256GB/512GB/1TB | Deep Purple, Gold, Silver, Space Black

**iPhone 13 Series (2021)**:
- iPhone 13 mini: 128GB/256GB/512GB | Pink, Blue, Midnight, Starlight, (PRODUCT)RED
- iPhone 13: 128GB/256GB/512GB | Pink, Blue, Midnight, Starlight, (PRODUCT)RED
- iPhone 13 Pro: 128GB/256GB/512GB/1TB | Sierra Blue, Gold, Silver, Graphite
- iPhone 13 Pro Max: 128GB/256GB/512GB/1TB | Sierra Blue, Gold, Silver, Graphite

**iPhone 12 Series (2020)**:
- iPhone 12 mini: 64GB/128GB/256GB | Black, White, Red, Green, Blue, Purple
- iPhone 12: 64GB/128GB/256GB | Black, White, Red, Green, Blue, Purple
- iPhone 12 Pro: 128GB/256GB/512GB | Graphite, Silver, Gold, Pacific Blue
- iPhone 12 Pro Max: 128GB/256GB/512GB | Graphite, Silver, Gold, Pacific Blue

#### 2.2 iPhone Models WITHOUT 5G Support (2019 and older)
**iPhone 11 Series (2019)**:
- iPhone 11: 64GB/128GB/256GB | Black, Green, Yellow, Purple, White, (PRODUCT)RED
- iPhone 11 Pro: 64GB/256GB/512GB | Midnight Green, Space Gray, Silver, Gold
- iPhone 11 Pro Max: 64GB/256GB/512GB | Midnight Green, Space Gray, Silver, Gold

**Legacy Models**:
- iPhone XS: 64GB/256GB/512GB | Space Gray, Silver, Gold
- iPhone XS Max: 64GB/256GB/512GB | Space Gray, Silver, Gold
- iPhone XR: 64GB/128GB/256GB | Black, White, Red, Yellow, Blue, Coral

### 3. Smart Inclusion Mapping System

#### 3.1 Separate Inclusion Mapping Field
After template selection, show dropdown with inclusion presets:

#### 3.2 Exact Inclusion Mappings
- **"Full set cable"** → [Full set cable, Bonus adapter, Bonus softcase, Bonus anti gores]
- **"Full set (charger)"** → [Full set (charger), Bonus softcase, Bonus anti gores]
- **"With box"** → [With box, Bonus charger, Bonus softcase, Bonus anti gores]
- **"No box"** → [No box, Bonus charger, Bonus softcase, Bonus anti gores]

#### 3.3 Inclusion Behavior
- **Auto-select**: When inclusion mapping is chosen, automatically select corresponding items
- **Additive**: Add to existing selections (don't replace)
- **Editable**: Staff can still manually adjust individual inclusions after auto-selection

### 4. Simplified Form Interface

#### 4.1 Fields to Remove
- **Model field**: Auto-extracted from template
- **Storage field**: Auto-extracted from template

#### 4.2 Enhanced Template Selection
- **Organized by series**: iPhone 16, iPhone 15, iPhone 14, etc.
- **Real-time search**: Filter as user types
- **Smart suggestions**: Most popular models first

#### 4.3 Streamlined Workflow
1. **Template Selection**: Choose from comprehensive iPhone database
2. **Auto-fill**: Title, brand, color, default collections populated
3. **Inclusion Mapping**: Select preset inclusion group (optional)
4. **Required Fields**: Only Price and Product Rank remain required
5. **Optional Fields**: SIM carriers, RAM, minus/issues, image upload
6. **Collections Review**: Auto-selected collections (editable)
7. **Create**: One-click product creation

#### 4.4 Collections Management
- **Field rename**: "Brand" → "Brand (Collections)"
- **Auto-selection logic**:
  - Always: "All Products"
  - iPhone products: + "iPhone" collection
  - Android products: + "Android" + brand collection (Samsung, Google, etc.)
- **Manual override**: Allow editing selected collections
- **API integration**: Fetch existing Shopify collections dynamically

### 5. Product Images Integration

#### 5.1 Image Upload Features
- **Drag & drop upload** in form interface
- **Multiple images**: Bulk upload for single product
- **Image preview**: Show thumbnails before product creation
- **Optional**: Images not required but recommended

#### 5.2 Shopify CDN Integration
- **Direct upload**: Images stored on Shopify CDN
- **Naming convention**: 
  - Single image: `{product_handle}`
  - Multiple images: `{product_handle}_1`, `{product_handle}_2`, `{product_handle}_3`
- **Auto-association**: Link images to created product via API

#### 5.3 Error Handling
- **Graceful fallback**: Product creation proceeds even if image upload fails
- **Retry mechanism**: Allow re-upload of failed images
- **Format validation**: Support common image formats (JPG, PNG, WebP)

### 6. Sales Channels Configuration

#### 6.1 Default Settings
- **All channels enabled by default**: Online Store, Point of Sale, Shop
- **User configurable**: Allow per-product channel selection
- **Bulk setting**: Apply to all products in session

#### 6.2 API Integration
- **Channel assignment**: Set product availability during creation
- **Error handling**: Continue if channel assignment fails
- **Validation**: Ensure valid channel configurations

### 7. Session Management & Inline Editing

#### 7.1 Enhanced Session Display
- **Inline editing**: Click any field to edit directly in session list
- **Position control**: Drag & drop reordering of products in session
- **Bulk operations**: Multi-select products for batch editing
- **Quick duplicate**: Copy product with one-click modification

#### 7.2 Session Persistence
- **Browser restart**: Maintain session across page reloads
- **10 product limit**: Current limit maintained for memory management
- **Clear session**: Enhanced bulk operations

## Implementation Plan

### Phase 1: Foundation (High Priority)
1. **iPhone Specifications Database** (`config/iphone_specs.py`)
   - Complete iPhone model/color/storage database
   - 5G capability flags
   - Validation functions

2. **Enhanced Template System** (`config/master_data.py`)
   - Template generation with 5G logic
   - Auto-extraction functions
   - Inclusion mapping definitions

### Phase 2: Core Interface (High Priority)  
3. **Simplified Form Interface** (`pages/smartphone_entry.py`)
   - Remove Model/Storage fields
   - Enhanced template selection
   - Separate inclusion mapping field
   - Auto-fill logic implementation

4. **Collections Management** (New service)
   - Fetch existing Shopify collections
   - Auto-assignment logic
   - Manual override capability

### Phase 3: Advanced Features (Medium Priority)
5. **Image Upload System** (`services/image_service.py`)
   - Drag & drop interface
   - Shopify CDN integration
   - Naming convention implementation

6. **Inline Session Editing**
   - Click-to-edit functionality
   - Position control
   - Bulk operations

### Phase 4: Polish (Low Priority)
7. **Performance Optimizations**
   - Form speed improvements
   - Smart defaults
   - Enhanced validation

8. **Sales Channel Integration**
   - API configuration
   - Default settings
   - User overrides

## Success Metrics

### Performance Targets
- **70% reduction** in product entry time
- **Zero specification errors** for iPhone models
- **50% fewer clicks** required per product
- **90% user satisfaction** with new workflow

### Quality Targets
- **100% accurate** iPhone specifications database
- **Consistent collection assignment** across all products
- **Professional image quality** with CDN integration
- **Error-free** product creation with validation

## Technical Architecture

### New Files Required
- `config/iphone_specs.py`: Complete iPhone database
- `services/collection_service.py`: Shopify collection management
- `services/image_service.py`: Image upload and CDN integration

### Modified Files
- `config/master_data.py`: Enhanced templates with 5G logic
- `pages/smartphone_entry.py`: Simplified form interface  
- `models/smartphone.py`: Add collections and sales channels fields
- `services/product_service.py`: Integration with new services

### API Integrations
- **Shopify Collections API**: Fetch and assign collections
- **Shopify Image API**: Upload images to CDN
- **Shopify Sales Channels API**: Configure product availability

## Risk Mitigation

### Technical Risks
- **API rate limits**: Implement proper throttling and error handling
- **Image upload failures**: Graceful degradation if CDN unavailable
- **Collection assignment errors**: Continue product creation if collections fail

### User Experience Risks
- **Learning curve**: Provide clear onboarding and documentation
- **Data loss**: Maintain session persistence and backup
- **Performance degradation**: Monitor form response times

## Future Enhancements (Out of Scope)

### Potential Future Features
- **Template system for other device categories** (Samsung, Google, etc.)
- **AI-powered price suggestions** based on condition and market data
- **Integration with inventory management systems**
- **Advanced reporting and analytics**
- **Multi-user collaborative sessions**

### Integration Opportunities
- **Barcode scanning** for faster product identification
- **Camera integration** for automatic photo capture
- **Marketplace sync** for cross-platform listing
- **Customer messaging** integration for inquiries

---

## Development Status

**Current Status**: Phase 1 & 2 Complete - Ready for Phase 3  
**Last Updated**: July 23, 2025

### ✅ **Completed Features (Ready for Production)**
- **Complete iPhone specifications database** (378 templates, all models iPhone XR+ to iPhone 16)
- **Smart 5G detection logic** (iPhone 12+ vs older models)  
- **Enhanced template system** with parsing and title generation
- **Smart inclusion mapping** (4 preset combinations with auto-add)
- **Auto collection assignment** (iPhone, Android + brand collections)
- **Collection service integration** with Shopify API
- **Enhanced product model** with collections and sales channels support
- **Complete test coverage** (all core functions validated)

### ✅ **Resolved Issue: Template Auto-Fill UI**
**Problem**: Template auto-fill only triggered on Enter key in search field, not immediate dropdown selection
**Solution**: Fixed session state management and form refresh behavior
**Status**: ✅ RESOLVED (July 23, 2025) - Templates now apply immediately on dropdown selection

### 📋 **Implementation Progress**

#### Phase 1: Foundation ✅ **COMPLETE**
- ✅ iPhone specifications database (`config/iphone_specs.py`) - 378 valid templates
- ✅ Enhanced template system (`config/master_data.py`) - 5G logic + inclusion mapping
- ✅ Product model updates (`models/smartphone.py`) - collections & sales channels
- ✅ Collection service (`services/collection_service.py`) - Shopify API integration

#### Phase 2: Core Interface ✅ **COMPLETE** 
- ✅ Enhanced form interface (`pages/smartphone_entry.py`) - simplified workflow
- ✅ Template selection with search and series organization
- ✅ Separate inclusion mapping field as requested
- ✅ Auto-collection assignment with brand detection
- ✅ **Template auto-fill UI behavior** - working properly

#### Phase 3: Advanced Features 🚧 **READY TO START**
- 🚧 Image upload system (`services/image_service.py`) - ready to implement
- 🚧 Inline session editing - ready to implement  
- 🚧 Drag & drop functionality - ready to implement

#### Phase 4: Polish ⏳ **PENDING**
- ⏳ Performance optimizations - not started
- ⏳ Sales channel integration - basic implementation done
- ⏳ Enhanced validation - basic implementation done

### 🎯 **Next Steps**
1. ✅ **Template auto-fill UI issue** - RESOLVED
2. ✅ **Phase 2 completion** - COMPLETE
3. 🚧 **Begin Phase 3** image upload system (READY TO START)
4. **User testing** with MyByte International staff

**Estimated Timeline**: 
- Phase 2 completion: ✅ COMPLETE (July 23, 2025)
- Phase 3-4: 1-2 weeks
- Total: 1-2 weeks remaining for full implementation  

**Dependencies**: Existing variant metafield system must remain stable ✅  

## Notes for Future Developers

### Critical Preservation
- **DO NOT MODIFY** existing variant metafield linking system (`services/shopify_api.py:assign_metafields_to_variants()`)
- **Maintain compatibility** with current SIM carrier variant system
- **Preserve** session management and CSV export functionality

### Implementation Guidelines
- **Test thoroughly** with actual iPhone models and colors
- **Validate** against real Shopify store collections
- **Maintain** existing error handling patterns
- **Document** any new API rate limit considerations

This PRD serves as the complete specification for the iPhone Template System enhancement project.