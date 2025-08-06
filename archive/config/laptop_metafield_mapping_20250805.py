# This file redirects to the enhanced version for backward compatibility
# The enhanced version is the authoritative laptop metafield mapping

from config.laptop_metafield_mapping_enhanced import *

# Re-export all functions for backward compatibility
from config.laptop_metafield_mapping_enhanced import (
    convert_laptop_data_to_metafields_enhanced as convert_laptop_data_to_metafields,
    get_metaobject_gid_enhanced as get_metaobject_gid,
    missing_logger,
    get_missing_entries_report,
    clear_session_data
)
