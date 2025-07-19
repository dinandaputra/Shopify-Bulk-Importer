# Shopify GraphQL Metaobject API Documentation

## Overview
- **Access Scope Required**: `read_metaobjects` (read), `write_metaobjects` (write)
- **Represents**: Flexible custom data objects with predefined structure
- **Instance of**: MetaobjectDefinition

## Key Metaobject Fields

### Core Fields
- `id`: Globally unique identifier
- `handle`: Unique object identifier
- `type`: Metaobject type
- `displayName`: Preferred display name
- `fields`: Collection of defined fields
- `definition`: The MetaobjectDefinition modeling the object type

## Primary Operations

### 1. Create Metaobject
- **Mutation**: `metaobjectCreate`
- **Access Scope**: `write_metaobjects`
- **Requirement**: Must have pre-existing MetaobjectDefinition

### 2. Update Metaobject
- **Mutation**: `metaobjectUpdate`
- **Purpose**: Update existing metaobject by ID

### 3. Upsert Metaobject
- **Mutation**: `metaobjectUpsert`
- **Purpose**: Creates or updates based on handle
- **Use Case**: Ensuring a specific metaobject exists

## Example Create Mutation

```graphql
mutation CreateMetaobject($metaobject: MetaobjectCreateInput!) {
  metaobjectCreate(metaobject: $metaobject) {
    metaobject {
      handle
      fields {
        key
        value
      }
    }
    userErrors {
      field
      message
      code
    }
  }
}
```

## Key Capabilities
- Supports custom field definitions
- Can be referenced by other resources (products, variants, etc.)
- Configurable access and publishing rules
- Flexible data structure based on MetaobjectDefinition

## Usage Notes for Product Integration
- Metaobjects can be referenced in product metafields
- Use metaobject IDs or handles for references
- Common use cases: Colors, specifications, categories, conditions