#!/usr/bin/env python3
"""
Missing Metaobjects Admin Report

This Streamlit page provides comprehensive admin tools for managing missing 
metaobject entries, analyzing trends, and generating batch creation scripts.

Features:
- Detailed missing entries analysis by category
- Frequency and trend reporting
- Script generation for batch updates
- Data export capabilities
- Maintenance and cleanup tools

Author: myByte International
Generated: July 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List
import json
import io

from repositories.metaobject_repository import MetaobjectRepository
# Legacy import for compatibility
try:
    from config.laptop_metafield_mapping_enhanced import (
        missing_logger,
        get_missing_entries_report,
        generate_batch_update_scripts
    )
except ImportError:
    # Fallback functions using new architecture
    class MockMissingLogger:
        def _load_existing_log(self):
            pass
        def generate_creation_script(self, field_name: str, limit: int = 20) -> str:
            return f"# Creation script for {field_name} (limit: {limit})\n# Updated to use MetaobjectRepository"
    
    missing_logger = MockMissingLogger()
    
    def get_missing_entries_report() -> Dict:
        return {
            'statistics': {
                'total_fields': 0,
                'total_unique_values': 0,
                'total_frequency': 0,
                'most_frequent_overall': [],
                'log_file_path': 'New architecture - no log file',
                'last_updated': datetime.now().isoformat()
            },
            'summary': {},
            'session_missing': []
        }
    
    def generate_batch_update_scripts() -> List[str]:
        return []

def generate_new_architecture_script(field_name: str, missing_entries: List[Dict]) -> str:
    """
    Generate creation script for new architecture using JSON files
    
    Args:
        field_name: Field name (e.g., 'processor', 'vga')
        missing_entries: List of missing entry dictionaries
        
    Returns:
        Python script content for adding missing entries to JSON files
    """
    if not missing_entries:
        return ""
    
    # Map field names to JSON files
    field_to_file = {
        'processor': 'processors.json',
        'vga': 'vga.json', 
        'graphics': 'graphics.json',
        'display': 'displays.json',
        'storage': 'storage.json',
        'color': 'colors.json',
        'os': 'os.json',
        'keyboard_layout': 'keyboard_layouts.json',
        'keyboard_backlight': 'keyboard_backlights.json'
    }
    
    json_file = field_to_file.get(field_name, f'{field_name}.json')
    
    script_content = f'''#!/usr/bin/env python3
"""
Generated script to add missing {field_name} entries to {json_file}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This script adds missing {field_name} entries to the metaobject mapping file.
You will need to:
1. Create the actual metaobjects in Shopify Admin
2. Get their GIDs
3. Update this script with the correct GIDs
4. Run the script to update the JSON file
"""

import json
import os
from typing import Dict

def add_missing_{field_name}_entries():
    """Add missing {field_name} entries to {json_file}"""
    
    # Path to the JSON file
    json_path = os.path.join('data', 'metaobjects', '{json_file}')
    
    # Load existing mappings
    try:
        with open(json_path, 'r') as f:
            existing_mappings = json.load(f)
    except FileNotFoundError:
        existing_mappings = {{}}
        print(f"Creating new file: {{json_path}}")
    
    # Missing entries to add (YOU NEED TO UPDATE THE GIDs!)
    missing_entries = {{
'''
    
    # Add each missing entry
    for entry in missing_entries:
        value = entry.get('value', '')
        frequency = entry.get('frequency', 1)
        
        # Escape quotes in value
        escaped_value = value.replace('"', '\\"')
        
        script_content += f'''        "{escaped_value}": "gid://shopify/Metaobject/YOUR_GID_HERE",  # Frequency: {frequency}
'''
    
    script_content += f'''    }}
    
    # Add missing entries to existing mappings
    updates_made = 0
    for key, gid in missing_entries.items():
        if key not in existing_mappings:
            if gid != "gid://shopify/Metaobject/YOUR_GID_HERE":
                existing_mappings[key] = gid
                updates_made += 1
                print(f"Added: {{key}} -> {{gid}}")
            else:
                print(f"SKIPPED (needs GID): {{key}}")
        else:
            print(f"Already exists: {{key}}")
    
    if updates_made > 0:
        # Create backup
        backup_path = json_path + f".backup.{{datetime.now().strftime('%Y%m%d_%H%M%S')}}"
        if os.path.exists(json_path):
            import shutil
            shutil.copy2(json_path, backup_path)
            print(f"Backup created: {{backup_path}}")
        
        # Write updated mappings
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w') as f:
            json.dump(existing_mappings, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Updated {{json_path}} with {{updates_made}} new entries")
    else:
        print("❌ No updates made - please update GIDs in the script")
    
    return updates_made

if __name__ == "__main__":
    print(f"Adding missing {field_name} entries...")
    print("⚠️  WARNING: You must update the GIDs in this script before running!")
    print("   1. Create the metaobjects in Shopify Admin")
    print("   2. Get their GIDs from the Admin API")
    print("   3. Replace 'YOUR_GID_HERE' with actual GIDs")
    print("   4. Run this script again")
    print()
    
    updates = add_missing_{field_name}_entries()
    
    if updates > 0:
        print(f"\\n🎉 Successfully added {{updates}} {field_name} entries!")
        print("   The MetaobjectRepository will now find these mappings.")
    else:
        print("\\n❌ No entries were added. Please update the GIDs and try again.")
'''
    
    return script_content

def show_missing_metaobjects_admin():
    """Admin interface for missing metaobject management - Updated for new architecture"""
    
    st.title("🔍 Missing Metaobjects Admin Report")
    st.markdown("*Comprehensive analysis and management of missing laptop metaobject entries*")
    
    # Show architecture info
    st.info("📢 **New Architecture**: This system now uses the MetaobjectRepository and TemplateCacheService. Missing metaobjects are managed through the new data structure.")
    
    # Initialize repository
    metaobject_repo = MetaobjectRepository()
    
    # Show repository status
    with st.expander("🔍 Repository Status"):
        st.markdown("**Available Metaobject Mappings:**")
        try:
            processor_count = len(metaobject_repo.get_processor_mapping())
            vga_count = len(metaobject_repo.get_vga_mapping())
            graphics_count = len(metaobject_repo.get_graphics_mapping())
            display_count = len(metaobject_repo.get_display_mapping())
            storage_count = len(metaobject_repo.get_storage_mapping())
            color_count = len(metaobject_repo.get_color_mapping())
            os_count = len(metaobject_repo.get_os_mapping())
            keyboard_layout_count = len(metaobject_repo.get_keyboard_layout_mapping())
            keyboard_backlight_count = len(metaobject_repo.get_keyboard_backlight_mapping())
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Processors", processor_count)
                st.metric("VGA Cards", vga_count)
                st.metric("Graphics", graphics_count)
            with col2:
                st.metric("Displays", display_count)
                st.metric("Storage", storage_count)
                st.metric("Colors", color_count)
            with col3:
                st.metric("OS Options", os_count)
                st.metric("Keyboard Layouts", keyboard_layout_count)
                st.metric("Keyboard Backlights", keyboard_backlight_count)
                
        except Exception as e:
            st.error(f"Error loading repository data: {e}")
    
    # Refresh data
    if st.button("🔄 Refresh Data", help="Reload missing entries data"):
        try:
            missing_logger._load_existing_log()
            st.success("✅ Data refreshed!")
        except:
            st.info("Using new architecture - no legacy log file to refresh")
        st.rerun()
    
    # Get comprehensive report
    report = get_missing_entries_report()
    stats = report.get('statistics', {})
    summary = report.get('summary', {})
    session_missing = report.get('session_missing', [])
    
    # Overview metrics
    st.subheader("📊 Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Missing Fields", 
            stats.get('total_fields', 0),
            help="Number of different metafield types with missing entries"
        )
    
    with col2:
        st.metric(
            "Unique Missing Values", 
            stats.get('total_unique_values', 0),
            help="Total number of unique missing specification values"
        )
    
    with col3:
        st.metric(
            "Total Frequency", 
            stats.get('total_frequency', 0),
            help="Total number of times missing entries were requested"
        )
    
    with col4:
        st.metric(
            "Session Entries", 
            len(session_missing),
            help="Missing entries detected in current session"
        )
    
    # Priority Analysis
    st.subheader("🎯 Priority Analysis")
    
    if stats.get('most_frequent_overall'):
        st.markdown("**Top 10 Most Requested Missing Entries:**")
        
        top_missing = stats['most_frequent_overall'][:10]
        
        # Create priority DataFrame
        priority_data = []
        for entry in top_missing:
            priority_data.append({
                'Field': entry['field'].replace('_', ' ').title(),
                'Value': entry['value'],
                'Frequency': entry['frequency'],
                'Priority': 'High' if entry['frequency'] >= 5 else 'Medium' if entry['frequency'] >= 3 else 'Low'
            })
        
        df_priority = pd.DataFrame(priority_data)
        
        # Display as colored table
        def color_priority(val):
            if val == 'High':
                return 'background-color: #ffebee; color: #c62828'
            elif val == 'Medium':
                return 'background-color: #fff3e0; color: #ef6c00'
            else:
                return 'background-color: #e8f5e8; color: #2e7d32'
        
        styled_df = df_priority.style.applymap(color_priority, subset=['Priority'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Frequency chart
        fig_freq = px.bar(
            df_priority, 
            x='Value', 
            y='Frequency',
            color='Priority',
            title="Missing Entry Frequency Analysis",
            color_discrete_map={
                'High': '#f44336',
                'Medium': '#ff9800', 
                'Low': '#4caf50'
            }
        )
        fig_freq.update_xaxes(tickangle=45)
        st.plotly_chart(fig_freq, use_container_width=True)
    
    # Detailed breakdown by field
    st.subheader("📋 Detailed Breakdown by Field")
    
    if summary:
        # Field selector
        field_options = list(summary.keys())
        selected_field = st.selectbox(
            "Select field to analyze:",
            field_options,
            help="Choose a metafield category to view detailed missing entries"
        )
        
        if selected_field and summary[selected_field]:
            field_data = summary[selected_field]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**{selected_field.replace('_', ' ').title()} Missing Entries**")
                
                # Convert to DataFrame for better display
                df_data = []
                for entry in field_data:
                    df_data.append({
                        'Value': entry['value'],
                        'Frequency': entry['frequency'],
                        'First Seen': entry['first_seen'][:10],
                        'Last Seen': entry['last_seen'][:10],
                        'Days Since First': (datetime.now() - datetime.fromisoformat(entry['first_seen'].replace('Z', '+00:00'))).days
                    })
                
                df_field = pd.DataFrame(df_data)
                df_field = df_field.sort_values('Frequency', ascending=False)
                
                st.dataframe(df_field, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("**Field Statistics**")
                
                total_entries = len(field_data)
                total_frequency = sum(entry['frequency'] for entry in field_data)
                avg_frequency = total_frequency / total_entries if total_entries > 0 else 0
                
                st.metric("Total Entries", total_entries)
                st.metric("Total Requests", total_frequency)
                st.metric("Avg Frequency", f"{avg_frequency:.1f}")
                
                # Most frequent entry
                if field_data:
                    most_frequent = max(field_data, key=lambda x: x['frequency'])
                    st.write(f"**Most Frequent:**")
                    st.write(f"{most_frequent['value']} ({most_frequent['frequency']}x)")
            
            # Quick actions for selected field
            st.markdown("**Quick Actions**")
            
            col_action1, col_action2, col_action3 = st.columns(3)
            
            with col_action1:
                if st.button(f"📝 Generate Script", key=f"script_{selected_field}"):
                    script_content = generate_new_architecture_script(selected_field, field_data[:20])
                    if script_content:
                        st.download_button(
                            label="📥 Download Creation Script",
                            data=script_content,
                            file_name=f"create_{selected_field}_metaobjects.py",
                            mime="text/x-python",
                            help="Download Python script to create missing metaobjects"
                        )
                    else:
                        st.warning("No missing entries found for this field")
            
            with col_action2:
                if st.button(f"📊 Export CSV", key=f"csv_{selected_field}"):
                    if df_field is not None and not df_field.empty:
                        csv_buffer = io.StringIO()
                        df_field.to_csv(csv_buffer, index=False)
                        
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv_buffer.getvalue(),
                            file_name=f"missing_{selected_field}_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            help="Export missing entries as CSV file"
                        )
                    else:
                        st.warning("No data to export")
            
            with col_action3:
                if st.button(f"🔍 View Context", key=f"context_{selected_field}"):
                    # Show context information for entries
                    with st.expander("Context Information"):
                        for entry in field_data[:5]:  # Show first 5
                            if entry.get('context'):
                                st.write(f"**{entry['value']}:**")
                                context = entry['context']
                                if isinstance(context, dict):
                                    for key, value in context.items():
                                        st.write(f"  • {key}: {value}")
                                else:
                                    st.write(f"  • {context}")
                                st.divider()
    
    # Trends and Analytics
    st.subheader("📈 Trends & Analytics")
    
    # Time-based analysis would require more detailed timestamp tracking
    # For now, show frequency distribution
    if summary:
        all_frequencies = []
        all_fields = []
        
        for field_name, entries in summary.items():
            for entry in entries:
                all_frequencies.append(entry['frequency'])
                all_fields.append(field_name.replace('_', ' ').title())
        
        if all_frequencies:
            df_trends = pd.DataFrame({
                'Field': all_fields,
                'Frequency': all_frequencies
            })
            
            # Frequency distribution by field
            fig_dist = px.box(
                df_trends,
                x='Field',
                y='Frequency',
                title="Frequency Distribution by Field Type"
            )
            fig_dist.update_xaxes(tickangle=45)
            st.plotly_chart(fig_dist, use_container_width=True)
            
            # Summary statistics
            field_stats = df_trends.groupby('Field')['Frequency'].agg(['count', 'sum', 'mean', 'max']).round(1)
            field_stats.columns = ['Unique Entries', 'Total Requests', 'Avg Frequency', 'Max Frequency']
            
            st.markdown("**Field Summary Statistics:**")
            st.dataframe(field_stats, use_container_width=True)
    
    # Batch Operations
    st.subheader("⚡ Batch Operations")
    
    col_batch1, col_batch2 = st.columns(2)
    
    with col_batch1:
        st.markdown("**Generate Creation Scripts**")
        
        if st.button("📝 Generate All Scripts", use_container_width=True):
            try:
                scripts = generate_batch_update_scripts()
                if scripts:
                    st.success(f"✅ Generated {len(scripts)} creation scripts!")
                    
                    for script_path in scripts:
                        st.write(f"• {script_path}")
                else:
                    st.info("📢 New Architecture: Missing entries are now managed through JSON files. Check data/metaobjects/ for current mappings.")
                    
            except Exception as e:
                st.info("📢 New Architecture: Scripts are generated through the new repository system. Missing entries should be added to JSON files in data/metaobjects/.")
    
    with col_batch2:
        st.markdown("**Export & Backup**")
        
        if st.button("💾 Export Full Report", use_container_width=True):
            # Create comprehensive export
            export_data = {
                'generated_at': datetime.now().isoformat(),
                'statistics': stats,
                'summary': summary,
                'session_missing': session_missing,
                'metadata': {
                    'total_fields': stats.get('total_fields', 0),
                    'total_unique_values': stats.get('total_unique_values', 0),
                    'total_frequency': stats.get('total_frequency', 0)
                }
            }
            
            export_json = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="📥 Download Full Report (JSON)",
                data=export_json,
                file_name=f"missing_metaobjects_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    # System Information
    with st.expander("🔧 System Information"):
        st.markdown("**Configuration:**")
        st.write(f"• Log file: {stats.get('log_file_path', 'Unknown')}")
        st.write(f"• Last updated: {stats.get('last_updated', 'Unknown')}")
        
        # Show raw statistics for debugging
        st.markdown("**Raw Statistics:**")
        st.json(stats)
    
    # Footer
    st.divider()
    st.markdown("""
    **🔍 How to use this report (New Architecture):**
    1. **Review Repository Status** - Check available metaobject mappings in JSON files
    2. **Add Missing Entries** - Update JSON files in `data/metaobjects/` with new mappings
    3. **Generate Scripts** - Use generated scripts to help add missing entries systematically
    4. **Export Data** - Download reports for offline analysis or documentation
    
    **💡 New Architecture Tips:**
    - Missing entries are now managed through JSON files instead of log files
    - Add new metaobjects by updating files in `data/metaobjects/`
    - The MetaobjectRepository automatically loads mappings from JSON files
    - Use the TemplateCacheService for laptop template management
    - Generated scripts help you add missing entries to the correct JSON files
    
    **📁 Key Files:**
    - `data/metaobjects/processors.json` - CPU/Processor mappings
    - `data/metaobjects/vga.json` - Dedicated graphics card mappings  
    - `data/metaobjects/graphics.json` - Integrated graphics mappings
    - `data/metaobjects/displays.json` - Display specification mappings
    - `data/metaobjects/storage.json` - Storage option mappings
    - `data/metaobjects/colors.json` - Color option mappings
    - `data/metaobjects/os.json` - Operating system mappings
    - `data/metaobjects/keyboard_layouts.json` - Keyboard layout mappings
    - `data/metaobjects/keyboard_backlights.json` - Keyboard backlight mappings
    """)

def main():
    """Main function for standalone execution"""
    st.set_page_config(
        page_title="Missing Metaobjects Report",
        page_icon="🔍",
        layout="wide"
    )
    
    show_missing_metaobjects_admin()

if __name__ == "__main__":
    main()