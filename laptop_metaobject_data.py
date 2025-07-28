#!/usr/bin/env python3
"""
Comprehensive Laptop Metaobject Data for Batch Creation

This module contains comprehensive laptop specification data for creating 
metaobjects in Shopify via batch API operations. Data follows the simplified
label-only format matching current myByte store structure.

Coverage:
- Windows Laptops: 2018-2025 (7-year span)
- MacBooks: 2013-2025 (12-year span including Intel legacy)
- Only Windows & macOS operating systems (no Linux)
- Simplified structure: only 'label' field per entry

Generated for myByte International - July 2025
"""

# =============================================================================
# PROCESSOR DATA
# Extended coverage: Windows laptops (2018-2025) + MacBooks (2013-2025)
# Format: "Brand Model (Cores CPUs), ~Clock GHz"
# =============================================================================

PROCESSOR_DATA = [
    # Intel Core i9 Mobile Processors (2018-2025)
    {
        "display_name": "Intel Core i9-13980HX (32 CPUs), ~3.0GHz",
        "handle": "intel-core-i9-13980hx-32-cpus-3-0ghz",
        "fields": {"label": "Intel Core i9-13980HX (32 CPUs), ~3.0GHz"}
    },
    {
        "display_name": "Intel Core i9-13950HX (32 CPUs), ~3.0GHz",
        "handle": "intel-core-i9-13950hx-32-cpus-3-0ghz",
        "fields": {"label": "Intel Core i9-13950HX (32 CPUs), ~3.0GHz"}
    },
    {
        "display_name": "Intel Core i9-12950HX (24 CPUs), ~2.3GHz",
        "handle": "intel-core-i9-12950hx-24-cpus-2-3ghz",
        "fields": {"label": "Intel Core i9-12950HX (24 CPUs), ~2.3GHz"}
    },
    {
        "display_name": "Intel Core i9-12900HX (24 CPUs), ~2.3GHz",
        "handle": "intel-core-i9-12900hx-24-cpus-2-3ghz",
        "fields": {"label": "Intel Core i9-12900HX (24 CPUs), ~2.3GHz"}
    },
    {
        "display_name": "Intel Core i9-12900HK (20 CPUs), ~2.5GHz",
        "handle": "intel-core-i9-12900hk-20-cpus-2-5ghz",
        "fields": {"label": "Intel Core i9-12900HK (20 CPUs), ~2.5GHz"}
    },
    {
        "display_name": "Intel Core i9-12900H (20 CPUs), ~2.5GHz",
        "handle": "intel-core-i9-12900h-20-cpus-2-5ghz",
        "fields": {"label": "Intel Core i9-12900H (20 CPUs), ~2.5GHz"}
    },
    {
        "display_name": "Intel Core i9-11980HK (16 CPUs), ~2.6GHz",
        "handle": "intel-core-i9-11980hk-16-cpus-2-6ghz",
        "fields": {"label": "Intel Core i9-11980HK (16 CPUs), ~2.6GHz"}
    },
    {
        "display_name": "Intel Core i9-11950H (16 CPUs), ~2.6GHz",
        "handle": "intel-core-i9-11950h-16-cpus-2-6ghz",
        "fields": {"label": "Intel Core i9-11950H (16 CPUs), ~2.6GHz"}
    },
    {
        "display_name": "Intel Core i9-10980HK (16 CPUs), ~2.4GHz",
        "handle": "intel-core-i9-10980hk-16-cpus-2-4ghz",
        "fields": {"label": "Intel Core i9-10980HK (16 CPUs), ~2.4GHz"}
    },
    {
        "display_name": "Intel Core i9-10885H (16 CPUs), ~2.4GHz",
        "handle": "intel-core-i9-10885h-16-cpus-2-4ghz",
        "fields": {"label": "Intel Core i9-10885H (16 CPUs), ~2.4GHz"}
    },
    {
        "display_name": "Intel Core i9-9980HK (16 CPUs), ~2.4GHz",
        "handle": "intel-core-i9-9980hk-16-cpus-2-4ghz",
        "fields": {"label": "Intel Core i9-9980HK (16 CPUs), ~2.4GHz"}
    },
    {
        "display_name": "Intel Core i9-8950HK (12 CPUs), ~2.9GHz",
        "handle": "intel-core-i9-8950hk-12-cpus-2-9ghz",
        "fields": {"label": "Intel Core i9-8950HK (12 CPUs), ~2.9GHz"}
    },

    # Intel Core i7 Mobile Processors (2018-2025)
    {
        "display_name": "Intel Core i7-13700HX (24 CPUs), ~2.1GHz",
        "handle": "intel-core-i7-13700hx-24-cpus-2-1ghz",
        "fields": {"label": "Intel Core i7-13700HX (24 CPUs), ~2.1GHz"}
    },
    {
        "display_name": "Intel Core i7-13700H (20 CPUs), ~2.4GHz",
        "handle": "intel-core-i7-13700h-20-cpus-2-4ghz",
        "fields": {"label": "Intel Core i7-13700H (20 CPUs), ~2.4GHz"}
    },
    {
        "display_name": "Intel Core i7-12800HX (20 CPUs), ~2.0GHz",
        "handle": "intel-core-i7-12800hx-20-cpus-2-0ghz",
        "fields": {"label": "Intel Core i7-12800HX (20 CPUs), ~2.0GHz"}
    },
    {
        "display_name": "Intel Core i7-12700H (20 CPUs), ~2.3GHz",
        "handle": "intel-core-i7-12700h-20-cpus-2-3ghz",
        "fields": {"label": "Intel Core i7-12700H (20 CPUs), ~2.3GHz"}
    },
    {
        "display_name": "Intel Core i7-12650H (16 CPUs), ~2.3GHz",
        "handle": "intel-core-i7-12650h-16-cpus-2-3ghz",
        "fields": {"label": "Intel Core i7-12650H (16 CPUs), ~2.3GHz"}
    },
    {
        "display_name": "Intel Core i7-11800H (16 CPUs), ~2.3GHz",
        "handle": "intel-core-i7-11800h-16-cpus-2-3ghz",
        "fields": {"label": "Intel Core i7-11800H (16 CPUs), ~2.3GHz"}
    },
    {
        "display_name": "Intel Core i7-11700H (16 CPUs), ~2.3GHz",
        "handle": "intel-core-i7-11700h-16-cpus-2-3ghz",
        "fields": {"label": "Intel Core i7-11700H (16 CPUs), ~2.3GHz"}
    },
    {
        "display_name": "Intel Core i7-10750H (12 CPUs), ~2.6GHz",
        "handle": "intel-core-i7-10750h-12-cpus-2-6ghz",
        "fields": {"label": "Intel Core i7-10750H (12 CPUs), ~2.6GHz"}
    },
    {
        "display_name": "Intel Core i7-10700H (16 CPUs), ~2.6GHz",
        "handle": "intel-core-i7-10700h-16-cpus-2-6ghz",
        "fields": {"label": "Intel Core i7-10700H (16 CPUs), ~2.6GHz"}
    },
    {
        "display_name": "Intel Core i7-9750H (12 CPUs), ~2.6GHz",
        "handle": "intel-core-i7-9750h-12-cpus-2-6ghz",
        "fields": {"label": "Intel Core i7-9750H (12 CPUs), ~2.6GHz"}
    },
    {
        "display_name": "Intel Core i7-8750H (12 CPUs), ~2.2GHz",
        "handle": "intel-core-i7-8750h-12-cpus-2-2ghz",
        "fields": {"label": "Intel Core i7-8750H (12 CPUs), ~2.2GHz"}
    },

    # Intel Core i5 Mobile Processors (2018-2025)
    {
        "display_name": "Intel Core i5-13500H (18 CPUs), ~2.6GHz",
        "handle": "intel-core-i5-13500h-18-cpus-2-6ghz",
        "fields": {"label": "Intel Core i5-13500H (18 CPUs), ~2.6GHz"}
    },
    {
        "display_name": "Intel Core i5-12500H (16 CPUs), ~2.5GHz",
        "handle": "intel-core-i5-12500h-16-cpus-2-5ghz",
        "fields": {"label": "Intel Core i5-12500H (16 CPUs), ~2.5GHz"}
    },
    {
        "display_name": "Intel Core i5-12450H (12 CPUs), ~2.0GHz",
        "handle": "intel-core-i5-12450h-12-cpus-2-0ghz",
        "fields": {"label": "Intel Core i5-12450H (12 CPUs), ~2.0GHz"}
    },
    {
        "display_name": "Intel Core i5-11400H (12 CPUs), ~2.7GHz",
        "handle": "intel-core-i5-11400h-12-cpus-2-7ghz",
        "fields": {"label": "Intel Core i5-11400H (12 CPUs), ~2.7GHz"}
    },
    {
        "display_name": "Intel Core i5-10300H (8 CPUs), ~2.5GHz",
        "handle": "intel-core-i5-10300h-8-cpus-2-5ghz",
        "fields": {"label": "Intel Core i5-10300H (8 CPUs), ~2.5GHz"}
    },
    {
        "display_name": "Intel Core i5-10200H (8 CPUs), ~2.4GHz",
        "handle": "intel-core-i5-10200h-8-cpus-2-4ghz",
        "fields": {"label": "Intel Core i5-10200H (8 CPUs), ~2.4GHz"}
    },
    {
        "display_name": "Intel Core i5-9300H (8 CPUs), ~2.4GHz",
        "handle": "intel-core-i5-9300h-8-cpus-2-4ghz",
        "fields": {"label": "Intel Core i5-9300H (8 CPUs), ~2.4GHz"}
    },
    {
        "display_name": "Intel Core i5-8300H (8 CPUs), ~2.3GHz",
        "handle": "intel-core-i5-8300h-8-cpus-2-3ghz",
        "fields": {"label": "Intel Core i5-8300H (8 CPUs), ~2.3GHz"}
    },

    # AMD Ryzen 9000 Series (2024-2025)
    {
        "display_name": "AMD Ryzen 9 8945HS (16 CPUs), ~4.0GHz",
        "handle": "amd-ryzen-9-8945hs-16-cpus-4-0ghz",
        "fields": {"label": "AMD Ryzen 9 8945HS (16 CPUs), ~4.0GHz"}
    },
    {
        "display_name": "AMD Ryzen 9 7945HX (32 CPUs), ~2.5GHz",
        "handle": "amd-ryzen-9-7945hx-32-cpus-2-5ghz",
        "fields": {"label": "AMD Ryzen 9 7945HX (32 CPUs), ~2.5GHz"}
    },
    {
        "display_name": "AMD Ryzen 9 6900HX (16 CPUs), ~3.3GHz",
        "handle": "amd-ryzen-9-6900hx-16-cpus-3-3ghz",
        "fields": {"label": "AMD Ryzen 9 6900HX (16 CPUs), ~3.3GHz"}
    },
    {
        "display_name": "AMD Ryzen 9 5900HX (16 CPUs), ~3.3GHz",
        "handle": "amd-ryzen-9-5900hx-16-cpus-3-3ghz",
        "fields": {"label": "AMD Ryzen 9 5900HX (16 CPUs), ~3.3GHz"}
    },

    # AMD Ryzen 7000 Series (2022-2025)
    {
        "display_name": "AMD Ryzen 7 8845HS (16 CPUs), ~3.8GHz",
        "handle": "amd-ryzen-7-8845hs-16-cpus-3-8ghz",
        "fields": {"label": "AMD Ryzen 7 8845HS (16 CPUs), ~3.8GHz"}
    },
    {
        "display_name": "AMD Ryzen 7 7840HS (16 CPUs), ~3.8GHz",
        "handle": "amd-ryzen-7-7840hs-16-cpus-3-8ghz",
        "fields": {"label": "AMD Ryzen 7 7840HS (16 CPUs), ~3.8GHz"}
    },
    {
        "display_name": "AMD Ryzen 7 7735HS (16 CPUs), ~3.2GHz",
        "handle": "amd-ryzen-7-7735hs-16-cpus-3-2ghz",
        "fields": {"label": "AMD Ryzen 7 7735HS (16 CPUs), ~3.2GHz"}
    },
    {
        "display_name": "AMD Ryzen 7 6800H (16 CPUs), ~3.2GHz",
        "handle": "amd-ryzen-7-6800h-16-cpus-3-2ghz",
        "fields": {"label": "AMD Ryzen 7 6800H (16 CPUs), ~3.2GHz"}
    },
    {
        "display_name": "AMD Ryzen 7 5800H (16 CPUs), ~3.2GHz",
        "handle": "amd-ryzen-7-5800h-16-cpus-3-2ghz",
        "fields": {"label": "AMD Ryzen 7 5800H (16 CPUs), ~3.2GHz"}
    },
    {
        "display_name": "AMD Ryzen 7 4800H (16 CPUs), ~2.9GHz",
        "handle": "amd-ryzen-7-4800h-16-cpus-2-9ghz",
        "fields": {"label": "AMD Ryzen 7 4800H (16 CPUs), ~2.9GHz"}
    },

    # AMD Ryzen 5000 Series (2020-2023)
    {
        "display_name": "AMD Ryzen 5 7640HS (12 CPUs), ~4.3GHz",
        "handle": "amd-ryzen-5-7640hs-12-cpus-4-3ghz",
        "fields": {"label": "AMD Ryzen 5 7640HS (12 CPUs), ~4.3GHz"}
    },
    {
        "display_name": "AMD Ryzen 5 6600H (12 CPUs), ~3.3GHz",
        "handle": "amd-ryzen-5-6600h-12-cpus-3-3ghz",
        "fields": {"label": "AMD Ryzen 5 6600H (12 CPUs), ~3.3GHz"}
    },
    {
        "display_name": "AMD Ryzen 5 5600H (12 CPUs), ~3.3GHz",
        "handle": "amd-ryzen-5-5600h-12-cpus-3-3ghz",
        "fields": {"label": "AMD Ryzen 5 5600H (12 CPUs), ~3.3GHz"}
    },
    {
        "display_name": "AMD Ryzen 5 4600H (12 CPUs), ~3.0GHz",
        "handle": "amd-ryzen-5-4600h-12-cpus-3-0ghz",
        "fields": {"label": "AMD Ryzen 5 4600H (12 CPUs), ~3.0GHz"}
    },

    # Apple M-Series Processors (MacBooks 2020-2025)
    {
        "display_name": "Apple M3 Max Chip",
        "handle": "apple-m3-max-chip",
        "fields": {"label": "Apple M3 Max Chip"}
    },
    {
        "display_name": "Apple M3 Pro Chip",
        "handle": "apple-m3-pro-chip",
        "fields": {"label": "Apple M3 Pro Chip"}
    },
    {
        "display_name": "Apple M3 Chip",
        "handle": "apple-m3-chip",
        "fields": {"label": "Apple M3 Chip"}
    },
    {
        "display_name": "Apple M2 Ultra Chip",
        "handle": "apple-m2-ultra-chip",
        "fields": {"label": "Apple M2 Ultra Chip"}
    },
    {
        "display_name": "Apple M2 Max Chip",
        "handle": "apple-m2-max-chip",
        "fields": {"label": "Apple M2 Max Chip"}
    },
    {
        "display_name": "Apple M2 Pro Chip",
        "handle": "apple-m2-pro-chip",
        "fields": {"label": "Apple M2 Pro Chip"}
    },
    {
        "display_name": "Apple M2 Chip",
        "handle": "apple-m2-chip",
        "fields": {"label": "Apple M2 Chip"}
    },
    {
        "display_name": "Apple M1 Ultra Chip",
        "handle": "apple-m1-ultra-chip",
        "fields": {"label": "Apple M1 Ultra Chip"}
    },
    {
        "display_name": "Apple M1 Max Chip",
        "handle": "apple-m1-max-chip",
        "fields": {"label": "Apple M1 Max Chip"}
    },
    {
        "display_name": "Apple M1 Pro Chip",
        "handle": "apple-m1-pro-chip",
        "fields": {"label": "Apple M1 Pro Chip"}
    },
    {
        "display_name": "Apple M1 Chip",
        "handle": "apple-m1-chip",
        "fields": {"label": "Apple M1 Chip"}
    },

    # Intel Legacy MacBook Processors (2013-2020)
    {
        "display_name": "Intel Core i9 8-Core 2.3GHz",
        "handle": "intel-core-i9-8-core-2-3ghz",
        "fields": {"label": "Intel Core i9 8-Core 2.3GHz"}
    },
    {
        "display_name": "Intel Core i7 Quad-Core 2.8GHz",
        "handle": "intel-core-i7-quad-core-2-8ghz",
        "fields": {"label": "Intel Core i7 Quad-Core 2.8GHz"}
    },
    {
        "display_name": "Intel Core i7 Quad-Core 2.6GHz",
        "handle": "intel-core-i7-quad-core-2-6ghz",
        "fields": {"label": "Intel Core i7 Quad-Core 2.6GHz"}
    },
    {
        "display_name": "Intel Core i5 Quad-Core 2.4GHz",
        "handle": "intel-core-i5-quad-core-2-4ghz",
        "fields": {"label": "Intel Core i5 Quad-Core 2.4GHz"}
    },
    {
        "display_name": "Intel Core i5 Quad-Core 2.0GHz",
        "handle": "intel-core-i5-quad-core-2-0ghz",
        "fields": {"label": "Intel Core i5 Quad-Core 2.0GHz"}
    },
    {
        "display_name": "Intel Core i5 Dual-Core 2.7GHz",
        "handle": "intel-core-i5-dual-core-2-7ghz",
        "fields": {"label": "Intel Core i5 Dual-Core 2.7GHz"}
    },
    {
        "display_name": "Intel Core i5 Dual-Core 2.3GHz",
        "handle": "intel-core-i5-dual-core-2-3ghz",
        "fields": {"label": "Intel Core i5 Dual-Core 2.3GHz"}
    },
]

# =============================================================================
# GRAPHICS DATA (INTEGRATED)
# Integrated graphics from processors 2018-2025
# Format: "Brand Series Model"
# =============================================================================

GRAPHICS_DATA = [
    # Intel Integrated Graphics (2018-2025)
    {
        "display_name": "Intel Iris Xe Graphics",
        "handle": "intel-iris-xe-graphics",
        "fields": {"label": "Intel Iris Xe Graphics"}
    },
    {
        "display_name": "Intel UHD Graphics 770",
        "handle": "intel-uhd-graphics-770",
        "fields": {"label": "Intel UHD Graphics 770"}
    },
    {
        "display_name": "Intel UHD Graphics 630",
        "handle": "intel-uhd-graphics-630",
        "fields": {"label": "Intel UHD Graphics 630"}
    },
    {
        "display_name": "Intel UHD Graphics 620",
        "handle": "intel-uhd-graphics-620",
        "fields": {"label": "Intel UHD Graphics 620"}
    },
    {
        "display_name": "Intel Iris Plus Graphics",
        "handle": "intel-iris-plus-graphics",
        "fields": {"label": "Intel Iris Plus Graphics"}
    },
    {
        "display_name": "Intel HD Graphics 530",
        "handle": "intel-hd-graphics-530",
        "fields": {"label": "Intel HD Graphics 530"}
    },

    # AMD Integrated Graphics (2018-2025)
    {
        "display_name": "AMD Radeon Graphics",
        "handle": "amd-radeon-graphics",
        "fields": {"label": "AMD Radeon Graphics"}
    },
    {
        "display_name": "AMD Radeon 780M Graphics",
        "handle": "amd-radeon-780m-graphics",
        "fields": {"label": "AMD Radeon 780M Graphics"}
    },
    {
        "display_name": "AMD Radeon 680M Graphics",
        "handle": "amd-radeon-680m-graphics",
        "fields": {"label": "AMD Radeon 680M Graphics"}
    },
    {
        "display_name": "AMD Radeon Vega 8 Graphics",
        "handle": "amd-radeon-vega-8-graphics",
        "fields": {"label": "AMD Radeon Vega 8 Graphics"}
    },
    {
        "display_name": "AMD Radeon Vega 7 Graphics",
        "handle": "amd-radeon-vega-7-graphics",
        "fields": {"label": "AMD Radeon Vega 7 Graphics"}
    },
    {
        "display_name": "AMD Radeon Vega 6 Graphics",
        "handle": "amd-radeon-vega-6-graphics",
        "fields": {"label": "AMD Radeon Vega 6 Graphics"}
    },

    # Apple Integrated Graphics (MacBooks)
    {
        "display_name": "Apple GPU (M3 Max)",
        "handle": "apple-gpu-m3-max",
        "fields": {"label": "Apple GPU (M3 Max)"}
    },
    {
        "display_name": "Apple GPU (M3 Pro)",
        "handle": "apple-gpu-m3-pro",
        "fields": {"label": "Apple GPU (M3 Pro)"}
    },
    {
        "display_name": "Apple GPU (M3)",
        "handle": "apple-gpu-m3",
        "fields": {"label": "Apple GPU (M3)"}
    },
    {
        "display_name": "Apple GPU (M2 Ultra)",
        "handle": "apple-gpu-m2-ultra",
        "fields": {"label": "Apple GPU (M2 Ultra)"}
    },
    {
        "display_name": "Apple GPU (M2 Max)",
        "handle": "apple-gpu-m2-max",
        "fields": {"label": "Apple GPU (M2 Max)"}
    },
    {
        "display_name": "Apple GPU (M2 Pro)",
        "handle": "apple-gpu-m2-pro",
        "fields": {"label": "Apple GPU (M2 Pro)"}
    },
    {
        "display_name": "Apple GPU (M2)",
        "handle": "apple-gpu-m2",
        "fields": {"label": "Apple GPU (M2)"}
    },
    {
        "display_name": "Apple GPU (M1 Ultra)",
        "handle": "apple-gpu-m1-ultra",
        "fields": {"label": "Apple GPU (M1 Ultra)"}
    },
    {
        "display_name": "Apple GPU (M1 Max)",
        "handle": "apple-gpu-m1-max",
        "fields": {"label": "Apple GPU (M1 Max)"}
    },
    {
        "display_name": "Apple GPU (M1 Pro)",
        "handle": "apple-gpu-m1-pro",
        "fields": {"label": "Apple GPU (M1 Pro)"}
    },
    {
        "display_name": "Apple GPU (M1)",
        "handle": "apple-gpu-m1",
        "fields": {"label": "Apple GPU (M1)"}
    },
]

# =============================================================================
# VGA DATA (DEDICATED GRAPHICS)
# Dedicated GPUs from gaming/workstation laptops 2018-2025
# Format: "Brand Series Model VRAM"
# =============================================================================

VGA_DATA = [
    # NVIDIA RTX 40 Series (2023-2025)
    {
        "display_name": "NVIDIA GeForce RTX 4090 24GB",
        "handle": "nvidia-geforce-rtx-4090-24gb",
        "fields": {"label": "NVIDIA GeForce RTX 4090 24GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 4080 16GB",
        "handle": "nvidia-geforce-rtx-4080-16gb",
        "fields": {"label": "NVIDIA GeForce RTX 4080 16GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 4070 12GB",
        "handle": "nvidia-geforce-rtx-4070-12gb",
        "fields": {"label": "NVIDIA GeForce RTX 4070 12GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 4060 8GB",
        "handle": "nvidia-geforce-rtx-4060-8gb",
        "fields": {"label": "NVIDIA GeForce RTX 4060 8GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 4050 6GB",
        "handle": "nvidia-geforce-rtx-4050-6gb",
        "fields": {"label": "NVIDIA GeForce RTX 4050 6GB"}
    },

    # NVIDIA RTX 30 Series (2020-2023)
    {
        "display_name": "NVIDIA GeForce RTX 3080 Ti 16GB",
        "handle": "nvidia-geforce-rtx-3080-ti-16gb",
        "fields": {"label": "NVIDIA GeForce RTX 3080 Ti 16GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 3080 10GB",
        "handle": "nvidia-geforce-rtx-3080-10gb",
        "fields": {"label": "NVIDIA GeForce RTX 3080 10GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 3070 Ti 8GB",
        "handle": "nvidia-geforce-rtx-3070-ti-8gb",
        "fields": {"label": "NVIDIA GeForce RTX 3070 Ti 8GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 3070 8GB",
        "handle": "nvidia-geforce-rtx-3070-8gb",
        "fields": {"label": "NVIDIA GeForce RTX 3070 8GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 3060 6GB",
        "handle": "nvidia-geforce-rtx-3060-6gb",
        "fields": {"label": "NVIDIA GeForce RTX 3060 6GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 3050 Ti 4GB",
        "handle": "nvidia-geforce-rtx-3050-ti-4gb",
        "fields": {"label": "NVIDIA GeForce RTX 3050 Ti 4GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 3050 4GB",
        "handle": "nvidia-geforce-rtx-3050-4gb",
        "fields": {"label": "NVIDIA GeForce RTX 3050 4GB"}
    },

    # NVIDIA RTX 20 Series (2018-2021)
    {
        "display_name": "NVIDIA GeForce RTX 2080 Super 8GB",
        "handle": "nvidia-geforce-rtx-2080-super-8gb",
        "fields": {"label": "NVIDIA GeForce RTX 2080 Super 8GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 2080 8GB",
        "handle": "nvidia-geforce-rtx-2080-8gb",
        "fields": {"label": "NVIDIA GeForce RTX 2080 8GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 2070 Super 8GB",
        "handle": "nvidia-geforce-rtx-2070-super-8gb",
        "fields": {"label": "NVIDIA GeForce RTX 2070 Super 8GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 2070 8GB",
        "handle": "nvidia-geforce-rtx-2070-8gb",
        "fields": {"label": "NVIDIA GeForce RTX 2070 8GB"}
    },
    {
        "display_name": "NVIDIA GeForce RTX 2060 6GB",
        "handle": "nvidia-geforce-rtx-2060-6gb",
        "fields": {"label": "NVIDIA GeForce RTX 2060 6GB"}
    },

    # NVIDIA GTX 16 Series (2019-2022)
    {
        "display_name": "NVIDIA GeForce GTX 1660 Ti 6GB",
        "handle": "nvidia-geforce-gtx-1660-ti-6gb",
        "fields": {"label": "NVIDIA GeForce GTX 1660 Ti 6GB"}
    },
    {
        "display_name": "NVIDIA GeForce GTX 1650 Ti 4GB",
        "handle": "nvidia-geforce-gtx-1650-ti-4gb",
        "fields": {"label": "NVIDIA GeForce GTX 1650 Ti 4GB"}
    },
    {
        "display_name": "NVIDIA GeForce GTX 1650 4GB",
        "handle": "nvidia-geforce-gtx-1650-4gb",
        "fields": {"label": "NVIDIA GeForce GTX 1650 4GB"}
    },

    # AMD Radeon RX 6000 Series (2020-2023)
    {
        "display_name": "AMD Radeon RX 6800M 12GB",
        "handle": "amd-radeon-rx-6800m-12gb",
        "fields": {"label": "AMD Radeon RX 6800M 12GB"}
    },
    {
        "display_name": "AMD Radeon RX 6700M 10GB",
        "handle": "amd-radeon-rx-6700m-10gb",
        "fields": {"label": "AMD Radeon RX 6700M 10GB"}
    },
    {
        "display_name": "AMD Radeon RX 6600M 8GB",
        "handle": "amd-radeon-rx-6600m-8gb",
        "fields": {"label": "AMD Radeon RX 6600M 8GB"}
    },
    {
        "display_name": "AMD Radeon RX 6500M 4GB",
        "handle": "amd-radeon-rx-6500m-4gb",
        "fields": {"label": "AMD Radeon RX 6500M 4GB"}
    },

    # AMD Radeon RX 5000 Series (2019-2021)
    {
        "display_name": "AMD Radeon RX 5700M 8GB",
        "handle": "amd-radeon-rx-5700m-8gb",
        "fields": {"label": "AMD Radeon RX 5700M 8GB"}
    },
    {
        "display_name": "AMD Radeon RX 5600M 6GB",
        "handle": "amd-radeon-rx-5600m-6gb",
        "fields": {"label": "AMD Radeon RX 5600M 6GB"}
    },
    {
        "display_name": "AMD Radeon RX 5500M 4GB",
        "handle": "amd-radeon-rx-5500m-4gb",
        "fields": {"label": "AMD Radeon RX 5500M 4GB"}
    },
]

# =============================================================================
# DISPLAY DATA
# Laptop display specifications covering common resolutions and refresh rates
# Format: "Size-inch Resolution (RefreshHz)"
# =============================================================================

DISPLAY_DATA = [
    # 13.3-inch displays
    {
        "display_name": "13.3-inch FHD (60Hz)",
        "handle": "13-3-inch-fhd-60hz",
        "fields": {"label": "13.3-inch FHD (60Hz)"}
    },
    {
        "display_name": "13.3-inch QHD (60Hz)",
        "handle": "13-3-inch-qhd-60hz",
        "fields": {"label": "13.3-inch QHD (60Hz)"}
    },
    {
        "display_name": "13.3-inch 4K (60Hz)",
        "handle": "13-3-inch-4k-60hz",
        "fields": {"label": "13.3-inch 4K (60Hz)"}
    },

    # 14-inch displays
    {
        "display_name": "14-inch FHD (60Hz)",
        "handle": "14-inch-fhd-60hz",
        "fields": {"label": "14-inch FHD (60Hz)"}
    },
    {
        "display_name": "14-inch FHD (90Hz)",
        "handle": "14-inch-fhd-90hz",
        "fields": {"label": "14-inch FHD (90Hz)"}
    },
    {
        "display_name": "14-inch QHD (120Hz)",
        "handle": "14-inch-qhd-120hz",
        "fields": {"label": "14-inch QHD (120Hz)"}
    },
    {
        "display_name": "14-inch 4K (60Hz)",
        "handle": "14-inch-4k-60hz",
        "fields": {"label": "14-inch 4K (60Hz)"}
    },

    # 15.6-inch displays (most common)
    {
        "display_name": "15.6-inch HD (60Hz)",
        "handle": "15-6-inch-hd-60hz",
        "fields": {"label": "15.6-inch HD (60Hz)"}
    },
    {
        "display_name": "15.6-inch FHD (60Hz)",
        "handle": "15-6-inch-fhd-60hz",
        "fields": {"label": "15.6-inch FHD (60Hz)"}
    },
    {
        "display_name": "15.6-inch FHD (120Hz)",
        "handle": "15-6-inch-fhd-120hz",
        "fields": {"label": "15.6-inch FHD (120Hz)"}
    },
    {
        "display_name": "15.6-inch FHD (144Hz)",
        "handle": "15-6-inch-fhd-144hz",
        "fields": {"label": "15.6-inch FHD (144Hz)"}
    },
    {
        "display_name": "15.6-inch FHD (165Hz)",
        "handle": "15-6-inch-fhd-165hz",
        "fields": {"label": "15.6-inch FHD (165Hz)"}
    },
    {
        "display_name": "15.6-inch QHD (120Hz)",
        "handle": "15-6-inch-qhd-120hz",
        "fields": {"label": "15.6-inch QHD (120Hz)"}
    },
    {
        "display_name": "15.6-inch QHD (165Hz)",
        "handle": "15-6-inch-qhd-165hz",
        "fields": {"label": "15.6-inch QHD (165Hz)"}
    },
    {
        "display_name": "15.6-inch 4K (60Hz)",
        "handle": "15-6-inch-4k-60hz",
        "fields": {"label": "15.6-inch 4K (60Hz)"}
    },

    # 16-inch displays
    {
        "display_name": "16-inch FHD (60Hz)",
        "handle": "16-inch-fhd-60hz",
        "fields": {"label": "16-inch FHD (60Hz)"}
    },
    {
        "display_name": "16-inch QHD (120Hz)",
        "handle": "16-inch-qhd-120hz",
        "fields": {"label": "16-inch QHD (120Hz)"}
    },
    {
        "display_name": "16-inch QHD (165Hz)",
        "handle": "16-inch-qhd-165hz",
        "fields": {"label": "16-inch QHD (165Hz)"}
    },
    {
        "display_name": "16-inch 4K (60Hz)",
        "handle": "16-inch-4k-60hz",
        "fields": {"label": "16-inch 4K (60Hz)"}
    },

    # 17.3-inch displays (gaming laptops)
    {
        "display_name": "17.3-inch FHD (60Hz)",
        "handle": "17-3-inch-fhd-60hz",
        "fields": {"label": "17.3-inch FHD (60Hz)"}
    },
    {
        "display_name": "17.3-inch FHD (144Hz)",
        "handle": "17-3-inch-fhd-144hz",
        "fields": {"label": "17.3-inch FHD (144Hz)"}
    },
    {
        "display_name": "17.3-inch FHD (240Hz)",
        "handle": "17-3-inch-fhd-240hz",
        "fields": {"label": "17.3-inch FHD (240Hz)"}
    },
    {
        "display_name": "17.3-inch FHD (300Hz)",
        "handle": "17-3-inch-fhd-300hz",
        "fields": {"label": "17.3-inch FHD (300Hz)"}
    },
    {
        "display_name": "17.3-inch QHD (165Hz)",
        "handle": "17-3-inch-qhd-165hz",
        "fields": {"label": "17.3-inch QHD (165Hz)"}
    },
    {
        "display_name": "17.3-inch 4K (120Hz)",
        "handle": "17-3-inch-4k-120hz",
        "fields": {"label": "17.3-inch 4K (120Hz)"}
    },
]

# =============================================================================
# STORAGE DATA
# Common laptop storage configurations
# Format: "Capacity Type" or "Primary + Secondary"
# =============================================================================

STORAGE_DATA = [
    # Single SSD configurations
    {
        "display_name": "128GB SSD",
        "handle": "128gb-ssd",
        "fields": {"label": "128GB SSD"}
    },
    {
        "display_name": "256GB SSD",
        "handle": "256gb-ssd",
        "fields": {"label": "256GB SSD"}
    },
    {
        "display_name": "512GB SSD",
        "handle": "512gb-ssd",
        "fields": {"label": "512GB SSD"}
    },
    {
        "display_name": "1TB SSD",
        "handle": "1tb-ssd",
        "fields": {"label": "1TB SSD"}
    },
    {
        "display_name": "2TB SSD",
        "handle": "2tb-ssd",
        "fields": {"label": "2TB SSD"}
    },

    # Single HDD configurations (budget laptops)
    {
        "display_name": "500GB HDD",
        "handle": "500gb-hdd",
        "fields": {"label": "500GB HDD"}
    },
    {
        "display_name": "1TB HDD",
        "handle": "1tb-hdd",
        "fields": {"label": "1TB HDD"}
    },
    {
        "display_name": "2TB HDD",
        "handle": "2tb-hdd",
        "fields": {"label": "2TB HDD"}
    },

    # Dual storage configurations (SSD + HDD)
    {
        "display_name": "256GB SSD + 1TB HDD",
        "handle": "256gb-ssd-1tb-hdd",
        "fields": {"label": "256GB SSD + 1TB HDD"}
    },
    {
        "display_name": "512GB SSD + 1TB HDD",
        "handle": "512gb-ssd-1tb-hdd",
        "fields": {"label": "512GB SSD + 1TB HDD"}
    },
    {
        "display_name": "1TB SSD + 1TB HDD",
        "handle": "1tb-ssd-1tb-hdd",
        "fields": {"label": "1TB SSD + 1TB HDD"}
    },
    {
        "display_name": "256GB SSD + 2TB HDD",
        "handle": "256gb-ssd-2tb-hdd",
        "fields": {"label": "256GB SSD + 2TB HDD"}
    },
    {
        "display_name": "512GB SSD + 2TB HDD",
        "handle": "512gb-ssd-2tb-hdd",
        "fields": {"label": "512GB SSD + 2TB HDD"}
    },

    # High-capacity configurations
    {
        "display_name": "4TB SSD",
        "handle": "4tb-ssd",
        "fields": {"label": "4TB SSD"}
    },
    {
        "display_name": "8TB SSD",
        "handle": "8tb-ssd",
        "fields": {"label": "8TB SSD"}
    },
]

# =============================================================================
# OPERATING SYSTEM DATA
# Windows and macOS only (no Linux as specified in plan)
# Format: "Platform Version"
# =============================================================================

OS_DATA = [
    # Windows Operating Systems (2018-2025)
    {
        "display_name": "Windows 11",
        "handle": "windows-11",
        "fields": {"label": "Windows 11"}
    },
    {
        "display_name": "Windows 11 Pro",
        "handle": "windows-11-pro",
        "fields": {"label": "Windows 11 Pro"}
    },
    {
        "display_name": "Windows 10",
        "handle": "windows-10",
        "fields": {"label": "Windows 10"}
    },
    {
        "display_name": "Windows 10 Pro",
        "handle": "windows-10-pro",
        "fields": {"label": "Windows 10 Pro"}
    },

    # macOS Operating Systems (2013-2025)
    {
        "display_name": "macOS Sonoma",
        "handle": "macos-sonoma",
        "fields": {"label": "macOS Sonoma"}
    },
    {
        "display_name": "macOS Ventura",
        "handle": "macos-ventura",
        "fields": {"label": "macOS Ventura"}
    },
    {
        "display_name": "macOS Monterey",
        "handle": "macos-monterey",
        "fields": {"label": "macOS Monterey"}
    },
    {
        "display_name": "macOS Big Sur",
        "handle": "macos-big-sur",
        "fields": {"label": "macOS Big Sur"}
    },
    {
        "display_name": "macOS Catalina",
        "handle": "macos-catalina",
        "fields": {"label": "macOS Catalina"}
    },
    {
        "display_name": "macOS Mojave",
        "handle": "macos-mojave",
        "fields": {"label": "macOS Mojave"}
    },
    {
        "display_name": "macOS High Sierra",
        "handle": "macos-high-sierra",
        "fields": {"label": "macOS High Sierra"}
    },
    {
        "display_name": "macOS Sierra",
        "handle": "macos-sierra",
        "fields": {"label": "macOS Sierra"}
    },
]

# =============================================================================
# KEYBOARD LAYOUT DATA
# Common keyboard layouts for international laptop market
# Format: "Region - Layout Type"
# =============================================================================

KEYBOARD_LAYOUT_DATA = [
    {
        "display_name": "US - International Keyboard",
        "handle": "us-international-keyboard",
        "fields": {"label": "US - International Keyboard"}
    },
    {
        "display_name": "Japanese - JIS Keyboard",
        "handle": "japanese-jis-keyboard",
        "fields": {"label": "Japanese - JIS Keyboard"}
    },
    {
        "display_name": "UK - QWERTY Keyboard",
        "handle": "uk-qwerty-keyboard",
        "fields": {"label": "UK - QWERTY Keyboard"}
    },
    {
        "display_name": "German - QWERTZ Keyboard",
        "handle": "german-qwertz-keyboard",
        "fields": {"label": "German - QWERTZ Keyboard"}
    },
    {
        "display_name": "French - AZERTY Keyboard",
        "handle": "french-azerty-keyboard",
        "fields": {"label": "French - AZERTY Keyboard"}
    },
]

# =============================================================================
# DATA SUMMARY AND STATISTICS
# =============================================================================

def get_data_summary():
    """Get summary statistics of the metaobject data"""
    categories = {
        "Processors": len(PROCESSOR_DATA),
        "Graphics (Integrated)": len(GRAPHICS_DATA), 
        "VGA (Dedicated)": len(VGA_DATA),
        "Displays": len(DISPLAY_DATA),
        "Storage": len(STORAGE_DATA),
        "Operating Systems": len(OS_DATA),
        "Keyboard Layouts": len(KEYBOARD_LAYOUT_DATA),
    }
    
    total_entries = sum(categories.values())
    
    return {
        "categories": categories,
        "total_entries": total_entries,
        "coverage": {
            "windows_laptops": "2018-2025 (7-year span)",
            "macbooks": "2013-2025 (12-year span)",
            "os_support": "Windows & macOS only (no Linux)",
            "format": "Simplified label-only structure"
        },
        "metaobject_definitions": {
            "processor": "gid://shopify/MetaobjectDefinition/10078486677",
            "graphics": "gid://shopify/MetaobjectDefinition/10078617749", 
            "vga": "gid://shopify/MetaobjectDefinition/10078650517",
            "display": "gid://shopify/MetaobjectDefinition/10078388373",
            "storage": "gid://shopify/MetaobjectDefinition/10097983637",
            "os": "gid://shopify/MetaobjectDefinition/10827989141",
            "keyboard_layout": "gid://shopify/MetaobjectDefinition/10097819797",
        }
    }

def validate_data_structure():
    """Validate that all data follows the simplified label-only format"""
    all_datasets = [
        ("PROCESSOR_DATA", PROCESSOR_DATA),
        ("GRAPHICS_DATA", GRAPHICS_DATA),
        ("VGA_DATA", VGA_DATA), 
        ("DISPLAY_DATA", DISPLAY_DATA),
        ("STORAGE_DATA", STORAGE_DATA),
        ("OS_DATA", OS_DATA),
        ("KEYBOARD_LAYOUT_DATA", KEYBOARD_LAYOUT_DATA),
    ]
    
    validation_results = []
    
    for dataset_name, dataset in all_datasets:
        for i, entry in enumerate(dataset):
            # Check required fields
            if not all(key in entry for key in ["display_name", "handle", "fields"]):
                validation_results.append(f"❌ {dataset_name}[{i}]: Missing required fields")
                continue
                
            # Check simplified structure - only label field
            if "label" not in entry["fields"]:
                validation_results.append(f"❌ {dataset_name}[{i}]: Missing 'label' field")
                continue
                
            if len(entry["fields"]) != 1:
                validation_results.append(f"❌ {dataset_name}[{i}]: Should only have 'label' field")
                continue
                
            # Check label matches display_name
            if entry["fields"]["label"] != entry["display_name"]:
                validation_results.append(f"❌ {dataset_name}[{i}]: label != display_name")
                continue
                
            validation_results.append(f"✅ {dataset_name}[{i}]: Valid")
    
    return validation_results

if __name__ == "__main__":
    # Display summary when run directly
    summary = get_data_summary()
    print("🚀 Laptop Metaobject Data Summary")
    print("=" * 50)
    
    for category, count in summary["categories"].items():
        print(f"📋 {category}: {count} entries")
    
    print(f"\n📊 Total Entries: {summary['total_entries']}")
    print(f"🎯 Coverage: {summary['coverage']['windows_laptops']} Windows, {summary['coverage']['macbooks']} Mac")
    print(f"🖥️  OS Support: {summary['coverage']['os_support']}")
    print(f"📝 Format: {summary['coverage']['format']}")
    
    print("\n🔍 Data Validation:")
    validation = validate_data_structure()
    valid_count = sum(1 for result in validation if result.startswith("✅"))
    total_count = len(validation)
    print(f"✅ Valid entries: {valid_count}/{total_count}")
    
    # Show any validation errors
    errors = [result for result in validation if result.startswith("❌")]
    if errors:
        print("\n❌ Validation Errors:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"   {error}")
    else:
        print("🎉 All entries pass validation!")