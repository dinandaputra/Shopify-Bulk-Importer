"""
Laptop specifications database with complete model, configuration, and component information.
Used for template generation and validation.

Template Format: "Brand Model [CPU/RAM/GPU/Display/Storage] [Color]"
Example: "ASUS TUF F15 FX507ZV4 [i7-12700H/16GB/RTX 4060/144Hz/512GB] [Graphite Black]"
"""

from typing import Dict, List, NamedTuple, Optional
from dataclasses import dataclass

@dataclass
class LaptopConfiguration:
    """Single laptop configuration specification"""
    cpu: str
    ram: str
    gpu: str
    display: str
    storage: str
    vga: str = ""
    os: str = "Windows 11"
    keyboard_layout: str = "US"
    keyboard_backlight: str = "Yes"
    
    def get_spec_string(self) -> str:
        """Generate spec string for template: CPU/RAM/GPU/Display/Storage"""
        return f"{self.cpu}/{self.ram}/{self.gpu}/{self.display}/{self.storage}"

@dataclass
class LaptopSpec:
    """Complete laptop model specification"""
    brand: str
    model: str
    base_model: str  # e.g., "ASUS TUF F15 FX507ZV4"
    configurations: List[LaptopConfiguration]
    colors: List[str]
    series: str
    year: int
    category: str = "Gaming"

# Standardized component naming - abbreviated to detailed format mapping
STANDARDIZED_COMPONENTS = {
    "cpu": {
        # Intel processors (abbreviated -> detailed format matching Shopify metaobjects)
        "i7-12700H": "Intel Core i7-12700H (16 CPUs), ~2.3GHz",
        "i7-12650H": "Intel Core i7-12650H (16 CPUs), ~2.3GHz", 
        "i5-12500H": "Intel Core i5-12500H (12 CPUs), ~3.1GHz",
        "i5-11400H": "Intel Core i5-11400H (12 CPUs), ~2.7GHz",
        "i7-11800H": "Intel Core i7-11800H (16 CPUs), ~2.3GHz",
        "i9-12900H": "Intel Core i9-12900H (20 CPUs), ~2.5GHz",
        "i7-13700H": "Intel Core i7-13700H (20 CPUs), ~2.4GHz",
        "i9-13900H": "Intel Core i9-13900H (20 CPUs), ~2.6GHz",
        "i5-13500H": "Intel Core i5-13500H (16 CPUs), ~2.6GHz",
        "i7-14700HX": "Intel Core i7-14700HX (20 CPUs), ~2.1GHz",
        "i9-14900HX": "Intel Core i9-14900HX (24 CPUs), ~2.2GHz",
        "i7-9750H": "Intel Core i7-9750H (12 CPUs), ~2.6GHz",
        "i5-10300H": "Intel Core i5-10300H (8 CPUs), ~2.5GHz",
        "i7-10750H": "Intel Core i7-10750H (12 CPUs), ~2.6GHz",
        "i7-11370H": "Intel Core i7-11370H (8 CPUs), ~3.3GHz",
        "i9-11900H": "Intel Core i9-11900H (16 CPUs), ~2.5GHz",
        
        # AMD processors
        "Ryzen 7 5800H": "AMD Ryzen 7 5800H (16 CPUs), ~3.2GHz",
        "Ryzen 5 5600H": "AMD Ryzen 5 5600H (12 CPUs), ~3.3GHz",
        "Ryzen 7 6800H": "AMD Ryzen 7 6800H (16 CPUs), ~3.2GHz",
        "Ryzen 9 5900HX": "AMD Ryzen 9 5900HX (16 CPUs), ~3.3GHz",
        "Ryzen 7 4800H": "AMD Ryzen 7 4800H (16 CPUs), ~2.9GHz",
        "Ryzen 5 4600H": "AMD Ryzen 5 4600H (12 CPUs), ~3.0GHz",
        "Ryzen 9 6900HX": "AMD Ryzen 9 6900HX (16 CPUs), ~3.3GHz",
        "Ryzen 7 7735HS": "AMD Ryzen 7 7735HS (16 CPUs), ~3.2GHz",
        "Ryzen 9 7940HS": "AMD Ryzen 9 7940HS (16 CPUs), ~4.0GHz",
        "Ryzen 9 8945HS": "AMD Ryzen 9 8945HS (16 CPUs), ~4.0GHz",
        "Ryzen 7 7040": "AMD Ryzen 7 7040 (16 CPUs), ~3.8GHz",
    },
    
    "ram": {
        "8GB": "8GB DDR4",
        "16GB": "16GB DDR4", 
        "32GB": "32GB DDR4",
        "64GB": "64GB DDR4"
    },
    
    "gpu": {
        # NVIDIA RTX 40 series (abbreviated -> detailed format)
        "RTX 4090": "NVIDIA GeForce RTX 4090 16GB",
        "RTX 4080": "NVIDIA GeForce RTX 4080 16GB",
        "RTX 4070": "NVIDIA GeForce RTX 4070 12GB",
        "RTX 4060": "NVIDIA GeForce RTX 4060 8GB",
        "RTX 4050": "NVIDIA GeForce RTX 4050 6GB",
        
        # NVIDIA RTX 30 series
        "RTX 3080": "NVIDIA GeForce RTX 3080 10GB",
        "RTX 3070": "NVIDIA GeForce RTX 3070 8GB",
        "RTX 3060": "NVIDIA GeForce RTX 3060 6GB",
        "RTX 3050": "NVIDIA GeForce RTX 3050 4GB",
        "RTX 3080 Ti": "NVIDIA GeForce RTX 3080 Ti 12GB",
        "RTX 3070 Ti": "NVIDIA GeForce RTX 3070 Ti 8GB",
        
        # NVIDIA RTX 20 series
        "RTX 2070": "NVIDIA GeForce RTX 2070 8GB",
        "RTX 2080": "NVIDIA GeForce RTX 2080 8GB",
        "RTX 2060": "NVIDIA GeForce RTX 2060 6GB",
        
        # NVIDIA GTX series
        "GTX 1650": "NVIDIA GeForce GTX 1650 4GB",
        "GTX 1650 Ti": "NVIDIA GeForce GTX 1650 Ti 4GB",
        "GTX 1660 Ti": "NVIDIA GeForce GTX 1660 Ti 6GB",
        
        # AMD graphics
        "RX 6600M": "AMD Radeon RX 6600M 8GB",
        "RX 6700M": "AMD Radeon RX 6700M 10GB",
        
        # Integrated graphics (these will map to graphics field)
        "Integrated": "Intel Iris Xe Graphics",
        "Intel UHD": "Intel UHD Graphics",
        "Intel Iris Xe": "Intel Iris Xe Graphics",
        "AMD Radeon": "AMD Radeon Graphics",
        "Apple GPU": "Apple GPU (M1)",
    },
    
    "display": {
        # Abbreviated -> detailed format matching Shopify metaobjects
        "144Hz": "15-inch FHD (144Hz)",
        "120Hz": "15-inch FHD (120Hz)", 
        "60Hz": "15-inch FHD (60Hz)",
        "17.3 144Hz": "17.3-inch FHD (144Hz)",
        "14 60Hz": "14-inch FHD (60Hz)",
        "13.3 60Hz": "13.3-inch FHD (60Hz)",
        "4K": "15-inch 4K UHD (60Hz)",
        "QHD 165Hz": "15-inch QHD (165Hz)",
        "165Hz": "15-inch FHD (165Hz)",
        "17.3 165Hz": "17.3-inch FHD (165Hz)",
        "14 QHD 120Hz": "14-inch QHD (120Hz)",
        "240Hz": "15-inch FHD (240Hz)",
        "17.3 240Hz": "17.3-inch FHD (240Hz)",
        "QHD 240Hz": "15-inch QHD (240Hz)",
        "300Hz": "15-inch FHD (300Hz)",
        "14 OLED 120Hz": "14-inch OLED (120Hz)",
        "16 OLED 240Hz": "16-inch OLED (240Hz)",
    },
    
    "storage": {
        # Abbreviated -> detailed format matching Shopify metaobjects
        "256GB": "256GB SSD",
        "512GB": "512GB SSD", 
        "1TB": "1TB SSD",
        "2TB": "2TB SSD",
        "1TB+256GB": "1TB HDD + 256GB SSD",
    }
}

# CPU to Integrated Graphics mapping - maps CPU models to their actual integrated graphics
CPU_TO_INTEGRATED_GRAPHICS = {
    # Intel 14th gen (2024) - Iris Xe or UHD 770
    "i7-14700HX": "Intel UHD Graphics 770",
    "i9-14900HX": "Intel UHD Graphics 770",
    
    # Intel 13th gen (2023) - Iris Xe or UHD 770
    "i7-13700H": "Intel Iris Xe Graphics",
    "i9-13900H": "Intel Iris Xe Graphics",
    "i5-13500H": "Intel Iris Xe Graphics",
    
    # Intel 12th gen (2022) - Iris Xe or UHD 770
    "i7-12700H": "Intel Iris Xe Graphics",
    "i7-12650H": "Intel Iris Xe Graphics",
    "i5-12500H": "Intel Iris Xe Graphics",
    "i9-12900H": "Intel Iris Xe Graphics",
    
    # Intel 11th gen (2021) - Iris Xe or UHD
    "i5-11400H": "Intel UHD Graphics",
    "i7-11800H": "Intel UHD Graphics",
    "i7-11370H": "Intel Iris Xe Graphics",
    "i9-11900H": "Intel UHD Graphics",
    
    # Intel 10th gen (2020) - UHD 630
    "i5-10300H": "Intel UHD Graphics 630",
    "i5-10200H": "Intel UHD Graphics 630",
    "i7-10750H": "Intel UHD Graphics 630",
    "i7-10700H": "Intel UHD Graphics 630",
    
    # Intel 9th gen (2019) - UHD 630
    "i7-9750H": "Intel UHD Graphics 630",
    "i5-9300H": "Intel UHD Graphics 630",
    
    # Intel 8th gen (2018) - UHD 630
    "i7-8750H": "Intel UHD Graphics 630",
    "i5-8300H": "Intel UHD Graphics 630",
    
    # AMD Ryzen 8000 series (2024) - RDNA3
    "Ryzen 9 8945HS": "AMD Radeon 780M Graphics",
    
    # AMD Ryzen 8000/7000 series (2023-2024) - RDNA3
    "Ryzen 7 8845HS": "AMD Radeon 780M Graphics",
    "Ryzen 7 7840HS": "AMD Radeon 780M Graphics",
    "Ryzen 9 7945HX": "AMD Radeon 780M Graphics",
    
    # AMD Ryzen 7000 series (2022-2023) - RDNA2/RDNA3
    "Ryzen 7 7735HS": "AMD Radeon 680M Graphics",
    "Ryzen 9 7940HS": "AMD Radeon 780M Graphics",
    "Ryzen 7 7040": "AMD Radeon 780M Graphics",
    "Ryzen 5 7640HS": "AMD Radeon Graphics",
    
    # AMD Ryzen 6000 series (2022) - RDNA2
    "Ryzen 7 6800H": "AMD Radeon 680M Graphics",
    "Ryzen 9 6900HX": "AMD Radeon 680M Graphics",
    "Ryzen 5 6600H": "AMD Radeon Graphics",
    
    # AMD Ryzen 5000 series (2021) - Vega
    "Ryzen 7 5800H": "AMD Radeon Graphics",
    "Ryzen 5 5600H": "AMD Radeon Graphics",
    "Ryzen 9 5900HX": "AMD Radeon Graphics",
    
    # AMD Ryzen 4000 series (2020) - Vega
    "Ryzen 7 4800H": "AMD Radeon Graphics",
    "Ryzen 5 4600H": "AMD Radeon Graphics",
}

# Complete laptop specifications database
LAPTOP_SPECS: Dict[str, LaptopSpec] = {
    # ASUS TUF Gaming Series
    "ASUS TUF F15 FX507ZV4": LaptopSpec(
        brand="ASUS",
        model="TUF Gaming F15",
        base_model="ASUS TUF F15 FX507ZV4",
        configurations=[
            LaptopConfiguration(
                cpu="i7-12700H",
                ram="16GB", 
                gpu="RTX 4060",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-12700H",
                ram="32GB",
                gpu="RTX 4060",
                display="144Hz", 
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Graphite Black", "Eclipse Gray"],
        series="TUF Gaming",
        year=2023,
        category="Gaming"
    ),
    
    "ASUS TUF F15 FX507ZC4": LaptopSpec(
        brand="ASUS",
        model="TUF Gaming F15", 
        base_model="ASUS TUF F15 FX507ZC4",
        configurations=[
            LaptopConfiguration(
                cpu="i5-12500H",
                ram="8GB",
                gpu="RTX 4050",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US", 
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i5-12500H",
                ram="16GB",
                gpu="RTX 4050", 
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Graphite Black", "Eclipse Gray"],
        series="TUF Gaming",
        year=2023,
        category="Gaming"
    ),
    
    # ASUS TUF Gaming F15 Series - Missing Models
    "ASUS TUF Gaming F15 FX506": LaptopSpec(
        brand="ASUS",
        model="TUF Gaming F15",
        base_model="ASUS TUF Gaming F15 FX506",
        configurations=[
            LaptopConfiguration(
                cpu="i5-10300H",
                ram="8GB",
                gpu="GTX 1650",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-10750H",
                ram="16GB",
                gpu="GTX 1650 Ti",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-11800H",
                ram="16GB",
                gpu="RTX 3060",
                display="240Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Fortress Gray", "Bonfire Black"],
        series="TUF Gaming",
        year=2020,
        category="Gaming"
    ),
    
    "ASUS TUF Dash F15 FX516": LaptopSpec(
        brand="ASUS",
        model="TUF Dash F15",
        base_model="ASUS TUF Dash F15 FX516",
        configurations=[
            LaptopConfiguration(
                cpu="i7-11370H",
                ram="8GB",
                gpu="RTX 3050",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-11370H",
                ram="16GB",
                gpu="RTX 3060",
                display="240Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-11370H",
                ram="32GB",
                gpu="RTX 3070",
                display="240Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray", "Moonlight White"],
        series="TUF Gaming",
        year=2021,
        category="Gaming"
    ),
    
    "ASUS TUF Gaming F15 FX507ZM": LaptopSpec(
        brand="ASUS",
        model="TUF Gaming F15",
        base_model="ASUS TUF Gaming F15 FX507ZM",
        configurations=[
            LaptopConfiguration(
                cpu="i7-12700H",
                ram="16GB",
                gpu="RTX 3060",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-12700H",
                ram="32GB",
                gpu="RTX 3070",
                display="165Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Mecha Gray", "Jaeger Gray"],
        series="TUF Gaming",
        year=2022,
        category="Gaming"
    ),
    
    "ASUS TUF Gaming F15 FX507VI": LaptopSpec(
        brand="ASUS",
        model="TUF Gaming F15",
        base_model="ASUS TUF Gaming F15 FX507VI",
        configurations=[
            LaptopConfiguration(
                cpu="i7-13700H",
                ram="16GB",
                gpu="RTX 4060",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i9-13900H",
                ram="32GB",
                gpu="RTX 4070",
                display="165Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Mecha Gray", "Jaeger Gray"],
        series="TUF Gaming",
        year=2023,
        category="Gaming"
    ),
    
    # ASUS TUF Gaming A15 Series
    "ASUS TUF Gaming A15 FA506": LaptopSpec(
        brand="ASUS",
        model="TUF Gaming A15",
        base_model="ASUS TUF Gaming A15 FA506",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 5 4600H",
                ram="8GB",
                gpu="GTX 1650",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="Ryzen 7 4800H",
                ram="16GB",
                gpu="RTX 3060",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="Ryzen 7 5800H",
                ram="16GB",
                gpu="RTX 3070",
                display="144Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Fortress Gray", "Bonfire Black"],
        series="TUF Gaming",
        year=2020,
        category="Gaming"
    ),
    
    "ASUS TUF Gaming A15 FA507": LaptopSpec(
        brand="ASUS",
        model="TUF Gaming A15",
        base_model="ASUS TUF Gaming A15 FA507",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 5 5600H",
                ram="8GB",
                gpu="RTX 3050",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="Ryzen 7 5800H",
                ram="16GB",
                gpu="RTX 3060",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="Ryzen 7 5800H",
                ram="32GB",
                gpu="RTX 3070",
                display="144Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray", "Graphite Black"],
        series="TUF Gaming",
        year=2021,
        category="Gaming"
    ),
    
    "ASUS TUF Gaming A17 FA706": LaptopSpec(
        brand="ASUS",
        model="TUF Gaming A17",
        base_model="ASUS TUF Gaming A17 FA706",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 5 4600H",
                ram="8GB",
                gpu="GTX 1650",
                display="17.3 144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="Ryzen 7 4800H",
                ram="16GB",
                gpu="RTX 3060",
                display="17.3 144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="Ryzen 7 5800H",
                ram="16GB",
                gpu="RTX 3070",
                display="17.3 144Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Fortress Gray", "Bonfire Black"],
        series="TUF Gaming",
        year=2020,
        category="Gaming"
    ),
    
    # ASUS TUF Gaming A17 and F17 Series - Additional Models
    "ASUS TUF Gaming A17 FA707": LaptopSpec(
        brand="ASUS",
        model="TUF Gaming A17",
        base_model="ASUS TUF Gaming A17 FA707",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 5 5600H",
                ram="8GB",
                gpu="RTX 3050",
                display="17.3 144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="Ryzen 7 5800H",
                ram="16GB",
                gpu="RTX 3060",
                display="17.3 144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="Ryzen 7 5800H",
                ram="32GB",
                gpu="RTX 3070",
                display="17.3 165Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray", "Fortress Gray"],
        series="TUF Gaming",
        year=2021,
        category="Gaming"
    ),
    
    "ASUS TUF Gaming F17 FX706": LaptopSpec(
        brand="ASUS",
        model="TUF Gaming F17",
        base_model="ASUS TUF Gaming F17 FX706",
        configurations=[
            LaptopConfiguration(
                cpu="i5-10300H",
                ram="8GB",
                gpu="GTX 1650",
                display="17.3 144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-10750H",
                ram="16GB",
                gpu="RTX 3060",
                display="17.3 144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Fortress Gray", "Bonfire Black"],
        series="TUF Gaming",
        year=2020,
        category="Gaming"
    ),
    
    "ASUS TUF Gaming F17 FX707": LaptopSpec(
        brand="ASUS",
        model="TUF Gaming F17",
        base_model="ASUS TUF Gaming F17 FX707",
        configurations=[
            LaptopConfiguration(
                cpu="i7-12700H",
                ram="16GB",
                gpu="RTX 3060",
                display="17.3 144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-12700H",
                ram="32GB",
                gpu="RTX 4060",
                display="17.3 165Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Mecha Gray", "Jaeger Gray"],
        series="TUF Gaming",
        year=2022,
        category="Gaming"
    ),
    
    # ASUS ROG Strix Series
    "ASUS ROG Strix G15 G513": LaptopSpec(
        brand="ASUS",
        model="ROG Strix G15",
        base_model="ASUS ROG Strix G15 G513",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 7 5800H",
                ram="16GB",
                gpu="RTX 3060",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="Ryzen 7 5800H",
                ram="32GB",
                gpu="RTX 3070",
                display="144Hz",
                storage="1TB",
                vga="HDMI, USB-C", 
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray", "Electro Punk"],
        series="ROG Strix",
        year=2022,
        category="Gaming"
    ),
    
    "ASUS ROG Strix G15 G512": LaptopSpec(
        brand="ASUS",
        model="ROG Strix G15",
        base_model="ASUS ROG Strix G15 G512",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 7 4800H",
                ram="16GB",
                gpu="RTX 3060",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="Ryzen 9 5900HX",
                ram="32GB",
                gpu="RTX 3070",
                display="144Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray", "Original Black"],
        series="ROG Strix",
        year=2020,
        category="Gaming"
    ),
    
    "ASUS ROG Strix G17 G713": LaptopSpec(
        brand="ASUS",
        model="ROG Strix G17",
        base_model="ASUS ROG Strix G17 G713",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 7 5800H",
                ram="16GB",
                gpu="RTX 3060",
                display="17.3 144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="Ryzen 9 5900HX",
                ram="32GB",
                gpu="RTX 3080",
                display="17.3 165Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray", "Electro Punk"],
        series="ROG Strix",
        year=2021,
        category="Gaming"
    ),
    
    "ASUS ROG Strix SCAR 15 G533": LaptopSpec(
        brand="ASUS",
        model="ROG Strix SCAR 15",
        base_model="ASUS ROG Strix SCAR 15 G533",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 9 5900HX",
                ram="16GB",
                gpu="RTX 3070",
                display="165Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="Ryzen 9 5900HX",
                ram="32GB",
                gpu="RTX 3080",
                display="165Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray", "Electro Punk"],
        series="ROG Strix",
        year=2021,
        category="Gaming"
    ),
    
    # ASUS ROG Strix Additional Models - Missing from Original
    "ASUS ROG Strix G15 G531": LaptopSpec(
        brand="ASUS",
        model="ROG Strix G15",
        base_model="ASUS ROG Strix G15 G531",
        configurations=[
            LaptopConfiguration(
                cpu="i7-9750H",
                ram="16GB",
                gpu="GTX 1660 Ti",
                display="120Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-9750H",
                ram="32GB",
                gpu="RTX 2060",
                display="144Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Stealth Black", "Glacier Blue"],
        series="ROG Strix",
        year=2019,
        category="Gaming"
    ),
    
    "ASUS ROG Strix G15 G532": LaptopSpec(
        brand="ASUS",
        model="ROG Strix G15",
        base_model="ASUS ROG Strix G15 G532",
        configurations=[
            LaptopConfiguration(
                cpu="i7-10750H",
                ram="16GB",
                gpu="RTX 2060",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-10750H",
                ram="32GB",
                gpu="RTX 2070",
                display="240Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray", "Original Black"],
        series="ROG Strix",
        year=2020,
        category="Gaming"
    ),
    
    "ASUS ROG Strix G17 G731": LaptopSpec(
        brand="ASUS",
        model="ROG Strix G17",
        base_model="ASUS ROG Strix G17 G731",
        configurations=[
            LaptopConfiguration(
                cpu="i7-9750H",
                ram="16GB",
                gpu="GTX 1660 Ti",
                display="17.3 120Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-9750H",
                ram="32GB",
                gpu="RTX 2060",
                display="17.3 144Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Stealth Black", "Glacier Blue"],
        series="ROG Strix",
        year=2019,
        category="Gaming"
    ),
    
    "ASUS ROG Strix G17 G732": LaptopSpec(
        brand="ASUS",
        model="ROG Strix G17",
        base_model="ASUS ROG Strix G17 G732",
        configurations=[
            LaptopConfiguration(
                cpu="i7-10750H",
                ram="16GB",
                gpu="RTX 2060",
                display="17.3 144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-10750H",
                ram="32GB",
                gpu="RTX 2070",
                display="17.3 240Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray", "Original Black"],
        series="ROG Strix",
        year=2020,
        category="Gaming"
    ),
    
    "ASUS ROG Strix SCAR 17 G733": LaptopSpec(
        brand="ASUS",
        model="ROG Strix SCAR 17",
        base_model="ASUS ROG Strix SCAR 17 G733",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 9 5900HX",
                ram="32GB",
                gpu="RTX 3070",
                display="17.3 165Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="Ryzen 9 5900HX",
                ram="32GB",
                gpu="RTX 3080",
                display="17.3 300Hz",
                storage="2TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray", "Electro Punk"],
        series="ROG Strix",
        year=2021,
        category="Gaming"
    ),
    
    "ASUS ROG Strix G16 G614": LaptopSpec(
        brand="ASUS",
        model="ROG Strix G16",
        base_model="ASUS ROG Strix G16 G614",
        configurations=[
            LaptopConfiguration(
                cpu="i7-14700HX",
                ram="16GB",
                gpu="RTX 4060",
                display="16 OLED 240Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i9-14900HX",
                ram="32GB",
                gpu="RTX 4070",
                display="16 OLED 240Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i9-14900HX",
                ram="32GB",
                gpu="RTX 4080",
                display="16 OLED 240Hz",
                storage="2TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray", "Volt Green"],
        series="ROG Strix",
        year=2024,
        category="Gaming"
    ),
    
    # ASUS ROG Zephyrus Series
    "ASUS ROG Zephyrus G14 GA401": LaptopSpec(
        brand="ASUS",
        model="ROG Zephyrus G14",
        base_model="ASUS ROG Zephyrus G14 GA401",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 7 4800H",
                ram="16GB",
                gpu="RTX 3060",
                display="14 QHD 120Hz",
                storage="512GB",
                vga="USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="White"
            ),
            LaptopConfiguration(
                cpu="Ryzen 9 5900HX",
                ram="32GB",
                gpu="RTX 3070",
                display="14 QHD 120Hz",
                storage="1TB",
                vga="USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="White"
            )
        ],
        colors=["Eclipse Gray", "Moonlight White"],
        series="ROG Zephyrus",
        year=2020,
        category="Gaming"
    ),
    
    "ASUS ROG Zephyrus G15 GA503": LaptopSpec(
        brand="ASUS",
        model="ROG Zephyrus G15",
        base_model="ASUS ROG Zephyrus G15 GA503",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 7 5800H",
                ram="16GB",
                gpu="RTX 3070",
                display="QHD 165Hz",
                storage="1TB",
                vga="USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="White"
            ),
            LaptopConfiguration(
                cpu="Ryzen 9 5900HX",
                ram="32GB",
                gpu="RTX 3080",
                display="QHD 165Hz",
                storage="1TB",
                vga="USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="White"
            )
        ],
        colors=["Eclipse Gray", "Moonlight White"],
        series="ROG Zephyrus",
        year=2021,
        category="Gaming"
    ),
    
    "ASUS ROG Zephyrus M16 GU603": LaptopSpec(
        brand="ASUS",
        model="ROG Zephyrus M16",
        base_model="ASUS ROG Zephyrus M16 GU603",
        configurations=[
            LaptopConfiguration(
                cpu="i7-11800H",
                ram="16GB",
                gpu="RTX 3060",
                display="QHD 165Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i9-12900H",
                ram="32GB",
                gpu="RTX 3070 Ti",
                display="QHD 165Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray", "Off Black"],
        series="ROG Zephyrus",
        year=2021,
        category="Gaming"
    ),
    
    "ASUS ROG Zephyrus S17 GX703": LaptopSpec(
        brand="ASUS",
        model="ROG Zephyrus S17",
        base_model="ASUS ROG Zephyrus S17 GX703",
        configurations=[
            LaptopConfiguration(
                cpu="i7-11800H",
                ram="32GB",
                gpu="RTX 3080",
                display="17.3 165Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i9-12900H",
                ram="32GB",
                gpu="RTX 3080 Ti",
                display="17.3 165Hz",
                storage="2TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray"],
        series="ROG Zephyrus",
        year=2021,
        category="Gaming"
    ),
    
    # ASUS ROG Zephyrus Additional Models - Missing from Original
    "ASUS ROG Zephyrus S GX502": LaptopSpec(
        brand="ASUS",
        model="ROG Zephyrus S",
        base_model="ASUS ROG Zephyrus S GX502",
        configurations=[
            LaptopConfiguration(
                cpu="i7-9750H",
                ram="16GB",
                gpu="RTX 2070",
                display="240Hz",
                storage="512GB",
                vga="USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-9750H",
                ram="32GB",
                gpu="RTX 2080",
                display="240Hz",
                storage="1TB",
                vga="USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Asus Blue", "Gun Metal"],
        series="ROG Zephyrus",
        year=2019,
        category="Gaming"
    ),
    
    "ASUS ROG Zephyrus S17 GX701": LaptopSpec(
        brand="ASUS",
        model="ROG Zephyrus S17",
        base_model="ASUS ROG Zephyrus S17 GX701",
        configurations=[
            LaptopConfiguration(
                cpu="i7-9750H",
                ram="32GB",
                gpu="RTX 2070",
                display="17.3 300Hz",
                storage="1TB",
                vga="USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-9750H",
                ram="32GB",
                gpu="RTX 2080",
                display="17.3 300Hz",
                storage="1TB",
                vga="USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Asus Blue"],
        series="ROG Zephyrus",
        year=2019,
        category="Gaming"
    ),
    
    "ASUS ROG Zephyrus M GU502": LaptopSpec(
        brand="ASUS",
        model="ROG Zephyrus M",
        base_model="ASUS ROG Zephyrus M GU502",
        configurations=[
            LaptopConfiguration(
                cpu="i7-9750H",
                ram="16GB",
                gpu="RTX 2060",
                display="240Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i7-9750H",
                ram="32GB",
                gpu="RTX 2070",
                display="240Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Stealth Black", "Brushed Metal"],
        series="ROG Zephyrus",
        year=2019,
        category="Gaming"
    ),
    
    "ASUS ROG Zephyrus G GA502": LaptopSpec(
        brand="ASUS",
        model="ROG Zephyrus G",
        base_model="ASUS ROG Zephyrus G GA502",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 7 4800H",
                ram="16GB",
                gpu="GTX 1660 Ti",
                display="120Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="White"
            ),
            LaptopConfiguration(
                cpu="Ryzen 7 4800H",
                ram="32GB",
                gpu="RTX 2060",
                display="144Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="White"
            )
        ],
        colors=["Glacier Blue", "Metallic Hairline"],
        series="ROG Zephyrus",
        year=2019,
        category="Gaming"
    ),
    
    "ASUS ROG Zephyrus G14 GA402": LaptopSpec(
        brand="ASUS",
        model="ROG Zephyrus G14",
        base_model="ASUS ROG Zephyrus G14 GA402",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 7 6800H",
                ram="16GB",
                gpu="RTX 3060",
                display="14 QHD 120Hz",
                storage="512GB",
                vga="USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="White"
            ),
            LaptopConfiguration(
                cpu="Ryzen 9 6900HX",
                ram="32GB",
                gpu="RTX 3070 Ti",
                display="14 QHD 120Hz",
                storage="1TB",
                vga="USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="White"
            )
        ],
        colors=["Eclipse Gray", "Moonlight White"],
        series="ROG Zephyrus",
        year=2022,
        category="Gaming"
    ),
    
    "ASUS ROG Zephyrus G16 GU605": LaptopSpec(
        brand="ASUS",
        model="ROG Zephyrus G16",
        base_model="ASUS ROG Zephyrus G16 GU605",
        configurations=[
            LaptopConfiguration(
                cpu="i7-14700HX",
                ram="16GB",
                gpu="RTX 4070",
                display="16 OLED 240Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i9-14900HX",
                ram="32GB",
                gpu="RTX 4080",
                display="16 OLED 240Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            ),
            LaptopConfiguration(
                cpu="i9-14900HX",
                ram="32GB",
                gpu="RTX 4090",
                display="16 OLED 240Hz",
                storage="2TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Eclipse Gray", "Platinum White"],
        series="ROG Zephyrus",
        year=2024,
        category="Gaming"
    ),
    
    # ASUS Vivobook Pro Gaming Series
    "ASUS Vivobook Pro 15 K3500": LaptopSpec(
        brand="ASUS",
        model="Vivobook Pro 15",
        base_model="ASUS Vivobook Pro 15 K3500",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 7 5800H",
                ram="16GB",
                gpu="RTX 3050",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="White"
            ),
            LaptopConfiguration(
                cpu="Ryzen 9 5900HX",
                ram="32GB",
                gpu="RTX 3060",
                display="144Hz",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="White"
            )
        ],
        colors=["Quiet Blue", "Cool Silver"],
        series="Vivobook Pro",
        year=2021,
        category="Gaming"
    ),
    
    "ASUS Vivobook Pro 16X N7600": LaptopSpec(
        brand="ASUS",
        model="Vivobook Pro 16X",
        base_model="ASUS Vivobook Pro 16X N7600",
        configurations=[
            LaptopConfiguration(
                cpu="i7-11370H",
                ram="16GB",
                gpu="RTX 3050 Ti",
                display="4K",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="White"
            ),
            LaptopConfiguration(
                cpu="i9-11900H",
                ram="32GB",
                gpu="RTX 3060",
                display="4K",
                storage="1TB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="White"
            )
        ],
        colors=["Starry Black", "Glacier Blue"],
        series="Vivobook Pro",
        year=2021,
        category="Gaming"
    ),
    
    # Dell G15 Gaming Series
    "Dell G15 5520": LaptopSpec(
        brand="Dell",
        model="G15 Gaming",
        base_model="Dell G15 5520",
        configurations=[
            LaptopConfiguration(
                cpu="i5-12500H",
                ram="8GB",
                gpu="RTX 3050",
                display="120Hz",
                storage="256GB",
                vga="HDMI",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="Blue"
            ),
            LaptopConfiguration(
                cpu="i7-12700H",
                ram="16GB",
                gpu="RTX 3060",
                display="120Hz",
                storage="512GB",
                vga="HDMI",
                os="Windows 11", 
                keyboard_layout="US",
                keyboard_backlight="Blue"
            )
        ],
        colors=["Dark Shadow Gray", "Specter Green"],
        series="G Series",
        year=2022,
        category="Gaming"
    ),
    
    # HP Pavilion Gaming Series
    "HP Pavilion Gaming 15-dk": LaptopSpec(
        brand="HP",
        model="Pavilion Gaming 15",
        base_model="HP Pavilion Gaming 15-dk",
        configurations=[
            LaptopConfiguration(
                cpu="i5-11400H",
                ram="8GB",
                gpu="GTX 1650",
                display="60Hz",
                storage="512GB",
                vga="HDMI",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="Green"
            ),
            LaptopConfiguration(
                cpu="i7-11800H",
                ram="16GB",
                gpu="RTX 3050",
                display="144Hz",
                storage="512GB",
                vga="HDMI",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="Green"
            )
        ],
        colors=["Shadow Black", "Acid Green"],
        series="Pavilion Gaming",
        year=2021,
        category="Gaming"
    ),
    
    # Lenovo Legion Series
    "Lenovo Legion 5 15ACH6H": LaptopSpec(
        brand="Lenovo",
        model="Legion 5",
        base_model="Lenovo Legion 5 15ACH6H",
        configurations=[
            LaptopConfiguration(
                cpu="Ryzen 5 5600H",
                ram="8GB",
                gpu="RTX 3050",
                display="120Hz",
                storage="256GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="White"
            ),
            LaptopConfiguration(
                cpu="Ryzen 7 5800H",
                ram="16GB",
                gpu="RTX 3060",
                display="144Hz",
                storage="512GB",
                vga="HDMI, USB-C",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="RGB"
            )
        ],
        colors=["Phantom Blue", "Shadow Black"],
        series="Legion",
        year=2021,
        category="Gaming"
    ),
    
    # MSI GF Series
    "MSI GF63 Thin 11SC": LaptopSpec(
        brand="MSI",
        model="GF63 Thin",
        base_model="MSI GF63 Thin 11SC",
        configurations=[
            LaptopConfiguration(
                cpu="i5-11400H",
                ram="8GB",
                gpu="GTX 1650",
                display="60Hz",
                storage="256GB",
                vga="HDMI",
                os="Windows 11",
                keyboard_layout="US",
                keyboard_backlight="Red"
            ),
            LaptopConfiguration(
                cpu="i7-11800H",
                ram="16GB",
                gpu="RTX 3050",
                display="144Hz",
                storage="512GB",
                vga="HDMI",
                os="Windows 11",
                keyboard_layout="US", 
                keyboard_backlight="Red"
            )
        ],
        colors=["Black"],
        series="GF",
        year=2021,
        category="Gaming"
    )
}

def get_all_laptop_models() -> List[str]:
    """Get list of all laptop model names"""
    return list(LAPTOP_SPECS.keys())

def get_laptop_spec(model: str) -> Optional[LaptopSpec]:
    """Get laptop specification by model name"""
    return LAPTOP_SPECS.get(model)

def get_models_by_brand(brand: str) -> List[str]:
    """Get laptop models by brand"""
    return [model for model, spec in LAPTOP_SPECS.items() if spec.brand.lower() == brand.lower()]

def get_models_by_series(series: str) -> List[str]:
    """Get laptop models by series"""
    return [model for model, spec in LAPTOP_SPECS.items() if spec.series.lower() == series.lower()]

def generate_all_laptop_templates() -> List[str]:
    """Generate all possible laptop templates with configurations and colors"""
    templates = []
    
    for model, spec in LAPTOP_SPECS.items():
        for config in spec.configurations:
            spec_string = config.get_spec_string()
            for color in spec.colors:
                template = f"{model} [{spec_string}] [{color}]"
                templates.append(template)
    
    return sorted(templates)

def search_laptop_templates(search_term: str) -> List[str]:
    """Search laptop templates with fuzzy matching"""
    if not search_term:
        return generate_all_laptop_templates()
    
    all_templates = generate_all_laptop_templates()
    search_lower = search_term.lower()
    
    # Split search term into keywords for multi-component matching
    keywords = search_lower.split()
    
    scored_templates = []
    for template in all_templates:
        template_lower = template.lower()
        score = 0
        
        # Exact phrase match gets highest score
        if search_lower in template_lower:
            score += 100
        
        # Individual keyword matching
        for keyword in keywords:
            if keyword in template_lower:
                score += 50
                
                # Bonus for spec component matches
                if any(keyword in comp.lower() for comp in ['rtx', 'gtx', 'i7', 'i5', 'ryzen', 'gb', 'hz']):
                    score += 25
        
        # Bonus for brand matches
        if any(brand.lower() in search_lower for brand in ['asus', 'dell', 'hp', 'lenovo', 'msi']):
            if any(brand.lower() in template_lower for brand in ['asus', 'dell', 'hp', 'lenovo', 'msi']):
                score += 30
        
        if score > 0:
            scored_templates.append((score, template))
    
    # Sort by score descending, then alphabetically
    scored_templates.sort(key=lambda x: (-x[0], x[1]))
    
    return [template for score, template in scored_templates]

def parse_laptop_template(template: str) -> Optional[Dict[str, str]]:
    """Parse laptop template to extract model, configuration, and color
    
    Args:
        template: Laptop template like "ASUS TUF F15 FX507ZV4 [i7-12700H/16GB/RTX 4060/144Hz/512GB] [Graphite Black]"
        
    Returns:
        Dict with model, cpu, ram, gpu, display, storage, color, and other extracted info
    """
    try:
        # Split template into parts
        if '[' not in template or ']' not in template:
            return None
            
        # Extract base model (everything before first bracket)
        model_part = template.split('[')[0].strip()
        
        # Extract spec string (between first pair of brackets)
        spec_start = template.find('[') + 1
        spec_end = template.find(']', spec_start)
        spec_string = template[spec_start:spec_end]
        
        # Extract color (between second pair of brackets)
        color_start = template.find('[', spec_end) + 1
        color_end = template.find(']', color_start)
        color = template[color_start:color_end] if color_start > 0 and color_end > 0 else ""
        
        # Parse spec string: CPU/RAM/GPU/Display/Storage
        spec_parts = spec_string.split('/')
        if len(spec_parts) != 5:
            return None
            
        cpu, ram, gpu, display, storage = spec_parts
        
        # Find matching laptop spec
        laptop_spec = get_laptop_spec(model_part)
        if not laptop_spec:
            return None
            
        # Find matching configuration
        matching_config = None
        for config in laptop_spec.configurations:
            if (config.cpu == cpu and config.ram == ram and 
                config.gpu == gpu and config.display == display and config.storage == storage):
                matching_config = config
                break
        
        if not matching_config:
            return None
            
        result = {
            'model': model_part,
            'brand': laptop_spec.brand,
            'cpu': cpu,
            'ram': ram,
            'gpu': gpu,
            'display': display,
            'storage': storage,
            'color': color,
            'vga': matching_config.vga,
            'os': matching_config.os,
            'keyboard_layout': matching_config.keyboard_layout,
            'keyboard_backlight': matching_config.keyboard_backlight,
            'series': laptop_spec.series,
            'category': laptop_spec.category,
            'template': template
        }
        
        return result
        
    except (IndexError, ValueError):
        return None

def generate_product_title(model: str, cpu: str, ram: str, sim_carrier: str = "SIM Free") -> str:
    """Generate product title for laptop
    
    Args:
        model: Laptop model like "ASUS TUF F15 FX507ZV4"
        cpu: CPU like "i7-12700H"  
        ram: RAM like "16GB"
        sim_carrier: Not applicable for laptops, included for consistency
        
    Returns:
        Product title like "ASUS TUF F15 FX507ZV4 i7-12700H 16GB"
    """
    return f"{model} {cpu} {ram}"

def validate_laptop_combination(model: str, cpu: str, ram: str, gpu: str, display: str, storage: str) -> bool:
    """Validate if laptop specification combination exists"""
    laptop_spec = get_laptop_spec(model)
    if not laptop_spec:
        return False
        
    for config in laptop_spec.configurations:
        if (config.cpu == cpu and config.ram == ram and 
            config.gpu == gpu and config.display == display and config.storage == storage):
            return True
            
    return False

def get_laptop_colors(model: str) -> List[str]:
    """Get available colors for laptop model"""
    laptop_spec = get_laptop_spec(model)
    return laptop_spec.colors if laptop_spec else []

def get_laptop_configurations(model: str) -> List[LaptopConfiguration]:
    """Get all configurations for laptop model"""
    laptop_spec = get_laptop_spec(model)
    return laptop_spec.configurations if laptop_spec else []

def get_full_component_name(component_type: str, abbreviated_name: str) -> str:
    """Convert abbreviated component name to detailed component name
    
    Args:
        component_type: Type of component ('cpu', 'gpu', 'display', 'storage', 'ram')
        abbreviated_name: Abbreviated name like 'i7-11370H', 'RTX 3070', '240Hz'
        
    Returns:
        Detailed component name like 'Intel Core i7-11370H (8 CPUs), ~3.3GHz', 'NVIDIA GeForce RTX 3070 8GB', '15.6-inch FHD (240Hz)'
    """
    if component_type not in STANDARDIZED_COMPONENTS:
        return abbreviated_name
    
    # Direct mapping from abbreviated to detailed format
    return STANDARDIZED_COMPONENTS[component_type].get(abbreviated_name, abbreviated_name)

def get_abbreviated_component_name(component_type: str, detailed_name: str) -> str:
    """Convert detailed component name back to abbreviated name for metafield processing
    
    Args:
        component_type: Type of component ('cpu', 'gpu', 'display', 'storage', 'ram')
        detailed_name: Detailed name like 'Intel Core i7-11370H (8 CPUs), ~3.3GHz'
        
    Returns:
        Abbreviated name like 'i7-11370H' for metafield lookup
    """
    if component_type not in STANDARDIZED_COMPONENTS:
        return detailed_name
    
    # Reverse lookup: find abbreviated name from detailed name
    for abbreviated, detailed in STANDARDIZED_COMPONENTS[component_type].items():
        if detailed == detailed_name:
            return abbreviated
    
    return detailed_name

def expand_laptop_template_specs(template_info: Dict[str, str]) -> Dict[str, str]:
    """Expand abbreviated component specifications to full names for display
    
    Args:
        template_info: Dict containing abbreviated specs from parse_laptop_template
        
    Returns:
        Dict with both abbreviated (for internal use) and full (for display) specs
    """
    expanded = template_info.copy()
    
    # Add full format versions for display
    if 'cpu' in template_info and template_info['cpu']:
        expanded['cpu_full'] = get_full_component_name('cpu', template_info['cpu'])
    
    if 'gpu' in template_info and template_info['gpu']:
        gpu_full = get_full_component_name('gpu', template_info['gpu'])
        expanded['gpu_full'] = gpu_full
        
        # Determine if GPU is integrated or dedicated
        integrated_keywords = ['Intel Iris', 'Intel UHD', 'Intel HD', 'AMD Radeon Graphics', 'Apple GPU', 'Integrated']
        is_integrated = any(keyword in gpu_full for keyword in integrated_keywords)
        
        if is_integrated:
            # Put integrated graphics in the graphics field, don't use the vga field from config
            expanded['integrated_graphics'] = gpu_full
            expanded['vga'] = ''  # Clear VGA for integrated-only systems
            expanded['gpu_full'] = ''  # Clear GPU full since it's integrated
        else:
            # Put dedicated graphics in gpu_full (which maps to VGA in UI), set integrated graphics based on CPU
            expanded['gpu_full'] = gpu_full  # This will be used for VGA field
            
            # Auto-detect integrated graphics based on CPU using accurate mapping
            cpu = template_info.get('cpu', '')
            
            # Use the CPU_TO_INTEGRATED_GRAPHICS mapping for accurate integrated graphics
            if cpu in CPU_TO_INTEGRATED_GRAPHICS:
                expanded['integrated_graphics'] = CPU_TO_INTEGRATED_GRAPHICS[cpu]
            elif 'Apple' in cpu or cpu.startswith('M'):
                expanded['integrated_graphics'] = f'Apple GPU ({cpu})'
            else:
                # Fallback for CPUs not in the mapping
                if 'Intel' in cpu or cpu.startswith('i'):
                    expanded['integrated_graphics'] = 'Intel UHD Graphics'
                elif 'Ryzen' in cpu or 'AMD' in cpu:
                    expanded['integrated_graphics'] = 'AMD Radeon Graphics'
                else:
                    expanded['integrated_graphics'] = ''
        
        # Don't copy the vga field from template - it contains port info, not graphics card info
        if 'vga' in expanded:
            del expanded['vga']
        
    if 'display' in template_info and template_info['display']:
        expanded['display_full'] = get_full_component_name('display', template_info['display'])
        
    if 'storage' in template_info and template_info['storage']:
        expanded['storage_full'] = get_full_component_name('storage', template_info['storage'])
        
    if 'ram' in template_info and template_info['ram']:
        expanded['ram_full'] = get_full_component_name('ram', template_info['ram'])
    
    return expanded