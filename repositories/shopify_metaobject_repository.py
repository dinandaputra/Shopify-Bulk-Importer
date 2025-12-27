"""
Shopify implementation of the metaobject repository interface.

This module provides concrete implementation of metaobject data access
operations using the Shopify GraphQL API.
"""

from typing import Dict, List, Optional, Any
import logging
import json
from services.shopify_api import ShopifyAPIClient

# Note: Interface and infrastructure imports removed - moved to archive/enhanced_architecture/
# This file now works as a standalone concrete implementation


class ShopifyMetaobjectRepository:
    """
    Shopify implementation of metaobject repository.
    
    This class provides concrete implementation of metaobject data access
    operations using the Shopify GraphQL API.
    """
    
    def __init__(self, api_client: ShopifyAPIClient):
        """
        Initialize the repository with a Shopify API client.
        
        Args:
            api_client: The Shopify API client instance
        """
        self._api_client = api_client
        self._logger = logging.getLogger(__name__)
        self._gid_cache: Dict[str, Dict[str, str]] = {}
    
    async def get_metaobject_gids(self, metaobject_type: str) -> Dict[str, str]:
        """
        Get metaobject GID mappings for a specific type.
        
        Args:
            metaobject_type: The type of metaobject
            
        Returns:
            Dictionary mapping values to GIDs
            
        Raises:
            Exception: If retrieval fails
        """
        try:
            # Check cache first
            if metaobject_type in self._gid_cache:
                return self._gid_cache[metaobject_type]
            
            # Map metaobject type to definition ID
            definition_mapping = {
                'cosmetic_condition': 'gid://shopify/MetaobjectDefinition/7936508053',
                'sim_carrier': 'gid://shopify/MetaobjectDefinition/7936540821',
                'operating_system': 'gid://shopify/MetaobjectDefinition/7936573589',
                'color': 'gid://shopify/MetaobjectDefinition/7936606357',
                'subscription_type': 'gid://shopify/MetaobjectDefinition/7936639125',
                'product_rank': 'gid://shopify/MetaobjectDefinition/7936671893',
                'product_inclusion': 'gid://shopify/MetaobjectDefinition/7936704661',
                'minus': 'gid://shopify/MetaobjectDefinition/7936737429',
                'processor': 'gid://shopify/MetaobjectDefinition/7936770197',
                'graphics': 'gid://shopify/MetaobjectDefinition/7936802965',
                'storage': 'gid://shopify/MetaobjectDefinition/7936835733',
                'memory': 'gid://shopify/MetaobjectDefinition/7936868501',
                'display': 'gid://shopify/MetaobjectDefinition/7936901269'
            }
            
            definition_id = definition_mapping.get(metaobject_type)
            if not definition_id:
                raise Exception(
                    f"Unknown metaobject type: {metaobject_type}"
                )
            
            # Query metaobjects for this definition
            query = f"""
            {{
                metaobjectDefinition(id: "{definition_id}") {{
                    metaobjects(first: 250) {{
                        edges {{
                            node {{
                                id
                                fields {{
                                    key
                                    value
                                }}
                            }}
                        }}
                    }}
                }}
            }}
            """
            
            result = self._api_client.graphql_query(query)
            
            if 'errors' in result:
                raise Exception(
                    f"GraphQL query failed: {result['errors']}"
                )
            
            # Extract GID mappings
            gid_mapping = {}
            edges = result.get('data', {}).get('metaobjectDefinition', {}).get('metaobjects', {}).get('edges', [])
            
            for edge in edges:
                node = edge['node']
                gid = node['id']
                
                # Find the display name or key field
                display_value = None
                for field in node['fields']:
                    if field['key'] in ['display_name', 'name', 'value']:
                        display_value = field['value']
                        break
                
                if display_value:
                    gid_mapping[display_value] = gid
            
            # Cache the result
            self._gid_cache[metaobject_type] = gid_mapping
            
            return gid_mapping
            
        except Exception as e:
            self._logger.error(f"Failed to get metaobject GIDs for {metaobject_type}: {str(e)}")
            raise Exception(
                f"Failed to retrieve metaobject GIDs: {str(e)}"
            )
    
    async def create_metaobject(self, metaobject_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new metaobject.
        
        Args:
            metaobject_data: Metaobject data including type and fields
            
        Returns:
            Created metaobject data
            
        Raises:
            Exception: If creation fails
        """
        try:
            # Extract required fields
            definition_id = metaobject_data.get('definition_id')
            fields = metaobject_data.get('fields', [])
            
            if not definition_id:
                raise Exception("definition_id is required")
            
            # Build GraphQL mutation
            mutation = """
            mutation CreateMetaobject($metaobject: MetaobjectCreateInput!) {
                metaobjectCreate(metaobject: $metaobject) {
                    metaobject {
                        id
                        type
                        fields {
                            key
                            value
                        }
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }
            """
            
            variables = {
                "metaobject": {
                    "type": definition_id,
                    "fields": fields
                }
            }
            
            result = self._api_client.graphql_query(mutation, variables)
            
            if 'errors' in result:
                raise Exception(
                    f"GraphQL mutation failed: {result['errors']}"
                )
            
            create_result = result.get('data', {}).get('metaobjectCreate', {})
            user_errors = create_result.get('userErrors', [])
            
            if user_errors:
                error_messages = [f"{err['field']}: {err['message']}" for err in user_errors]
                raise Exception(
                    f"Metaobject creation failed: {'; '.join(error_messages)}"
                )
            
            return create_result.get('metaobject', {})
            
        except Exception as e:
            self._logger.error(f"Failed to create metaobject: {str(e)}")
            raise Exception(
                f"Failed to create metaobject: {str(e)}"
            )
    
    async def query_metaobjects(self, query: str) -> List[Dict[str, Any]]:
        """
        Query metaobjects using GraphQL.
        
        Args:
            query: GraphQL query string
            
        Returns:
            List of metaobjects
            
        Raises:
            Exception: If query fails
        """
        try:
            result = self._api_client.graphql_query(query)
            
            if 'errors' in result:
                raise Exception(
                    f"GraphQL query failed: {result['errors']}"
                )
            
            # Extract metaobjects from result
            # This is a generic method, so we don't know the exact structure
            return result.get('data', {})
            
        except Exception as e:
            self._logger.error(f"GraphQL query failed: {str(e)}")
            raise Exception(f"Query execution failed: {str(e)}")
    
    async def get_metaobject_by_gid(self, gid: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific metaobject by GID.
        
        Args:
            gid: Global ID of the metaobject
            
        Returns:
            Metaobject data if found
            
        Raises:
            Exception: If retrieval fails
        """
        try:
            query = f"""
            {{
                metaobject(id: "{gid}") {{
                    id
                    type
                    fields {{
                        key
                        value
                    }}
                }}
            }}
            """
            
            result = self._api_client.graphql_query(query)
            
            if 'errors' in result:
                raise Exception(
                    f"GraphQL query failed: {result['errors']}"
                )
            
            return result.get('data', {}).get('metaobject')
            
        except Exception as e:
            self._logger.error(f"Failed to get metaobject by GID: {str(e)}")
            raise Exception(
                f"Failed to retrieve metaobject: {str(e)}"
            )
    
    async def update_metaobject(self, gid: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing metaobject.
        
        Args:
            gid: Global ID of the metaobject
            updates: Fields to update
            
        Returns:
            Updated metaobject data
            
        Raises:
            MetaobjectUpdateException: If update fails
        """
        try:
            # Check if metaobject exists
            existing = await self.get_metaobject_by_gid(gid)
            if not existing:
                raise MetaobjectNotFoundException(f"Metaobject {gid} not found")
            
            # Build update mutation
            mutation = """
            mutation UpdateMetaobject($id: ID!, $metaobject: MetaobjectUpdateInput!) {
                metaobjectUpdate(id: $id, metaobject: $metaobject) {
                    metaobject {
                        id
                        type
                        fields {
                            key
                            value
                        }
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }
            """
            
            variables = {
                "id": gid,
                "metaobject": {
                    "fields": updates.get('fields', [])
                }
            }
            
            result = self._api_client.graphql_query(mutation, variables)
            
            if 'errors' in result:
                raise Exception(
                    f"GraphQL mutation failed: {result['errors']}"
                )
            
            update_result = result.get('data', {}).get('metaobjectUpdate', {})
            user_errors = update_result.get('userErrors', [])
            
            if user_errors:
                error_messages = [f"{err['field']}: {err['message']}" for err in user_errors]
                raise MetaobjectUpdateException(
                    f"Metaobject update failed: {'; '.join(error_messages)}"
                )
            
            return update_result.get('metaobject', {})
            
        except MetaobjectNotFoundException:
            raise
        except Exception as e:
            self._logger.error(f"Failed to update metaobject: {str(e)}")
            raise MetaobjectUpdateException(
                f"Failed to update metaobject: {str(e)}"
            )
    
    async def get_metaobject_definitions(self) -> List[Dict[str, Any]]:
        """
        Get all metaobject definitions.
        
        Returns:
            List of metaobject definitions
            
        Raises:
            Exception: If retrieval fails
        """
        try:
            query = """
            {
                metaobjectDefinitions(first: 50) {
                    edges {
                        node {
                            id
                            type
                            name
                            description
                            fieldDefinitions {
                                key
                                name
                                type {
                                    name
                                }
                                required
                            }
                        }
                    }
                }
            }
            """
            
            result = self._api_client.graphql_query(query)
            
            if 'errors' in result:
                raise Exception(
                    f"GraphQL query failed: {result['errors']}"
                )
            
            edges = result.get('data', {}).get('metaobjectDefinitions', {}).get('edges', [])
            return [edge['node'] for edge in edges]
            
        except Exception as e:
            self._logger.error(f"Failed to get metaobject definitions: {str(e)}")
            raise Exception(
                f"Failed to retrieve metaobject definitions: {str(e)}"
            )
    
    async def get_metaobjects_by_definition(self, definition_id: str, 
                                          limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all metaobjects for a definition.
        
        Args:
            definition_id: Metaobject definition ID
            limit: Maximum results
            
        Returns:
            List of metaobjects
            
        Raises:
            Exception: If retrieval fails
        """
        try:
            first = limit or 250
            query = f"""
            {{
                metaobjectDefinition(id: "{definition_id}") {{
                    metaobjects(first: {first}) {{
                        edges {{
                            node {{
                                id
                                fields {{
                                    key
                                    value
                                }}
                            }}
                        }}
                    }}
                }}
            }}
            """
            
            result = self._api_client.graphql_query(query)
            
            if 'errors' in result:
                raise Exception(
                    f"GraphQL query failed: {result['errors']}"
                )
            
            edges = result.get('data', {}).get('metaobjectDefinition', {}).get('metaobjects', {}).get('edges', [])
            return [edge['node'] for edge in edges]
            
        except Exception as e:
            self._logger.error(f"Failed to get metaobjects by definition: {str(e)}")
            raise Exception(
                f"Failed to retrieve metaobjects: {str(e)}"
            )
    
    async def bulk_create_metaobjects(self, metaobjects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create multiple metaobjects.
        
        Args:
            metaobjects: List of metaobject data
            
        Returns:
            List of created metaobjects
            
        Raises:
            BulkOperationException: If bulk creation fails
        """
        created_metaobjects = []
        errors = []
        
        for i, metaobject_data in enumerate(metaobjects):
            try:
                created = await self.create_metaobject(metaobject_data)
                created_metaobjects.append(created)
            except Exception as e:
                errors.append(f"Metaobject {i}: {str(e)}")
        
        if errors:
            raise BulkOperationException(
                f"Bulk creation partially failed. Created {len(created_metaobjects)}/{len(metaobjects)}. "
                f"Errors: {'; '.join(errors)}"
            )
        
        return created_metaobjects
    
    async def find_metaobject_by_value(self, definition_type: str, field_key: str, 
                                     value: str) -> Optional[Dict[str, Any]]:
        """
        Find a metaobject by field value.
        
        Args:
            definition_type: Metaobject definition type
            field_key: Field to search by
            value: Value to search for
            
        Returns:
            Metaobject if found
            
        Raises:
            Exception: If search fails
        """
        try:
            # Get all metaobjects of this type
            gid_mapping = await self.get_metaobject_gids(definition_type)
            
            # Search for the value
            if value in gid_mapping:
                gid = gid_mapping[value]
                return await self.get_metaobject_by_gid(gid)
            
            return None
            
        except Exception as e:
            self._logger.error(f"Failed to find metaobject by value: {str(e)}")
            raise Exception(
                f"Failed to find metaobject: {str(e)}"
            )