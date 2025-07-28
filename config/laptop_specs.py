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

# Standardized component naming for consistent templates
STANDARDIZED_COMPONENTS = {
    "cpu": {
        # Intel processors
        "Intel Core i7-12700H": "i7-12700H",
        "Intel Core i7-12650H": "i7-12650H", 
        "Intel Core i5-12500H": "i5-12500H",
        "Intel Core i5-11400H": "i5-11400H",
        "Intel Core i7-11800H": "i7-11800H",
        "Intel Core i9-12900H": "i9-12900H",
        "Intel Core i7-13700H": "i7-13700H",
        "Intel Core i9-13900H": "i9-13900H",
        "Intel Core i5-13500H": "i5-13500H",
        "Intel Core i7-14700HX": "i7-14700HX",
        "Intel Core i9-14900HX": "i9-14900HX",
        "Intel Core i7-9750H": "i7-9750H",
        "Intel Core i5-10300H": "i5-10300H",
        "Intel Core i7-10750H": "i7-10750H",
        "Intel Core i7-11370H": "i7-11370H",
        "Intel Core i9-11900H": "i9-11900H",
        
        # AMD processors
        "AMD Ryzen 7 5800H": "Ryzen 7 5800H",
        "AMD Ryzen 5 5600H": "Ryzen 5 5600H",
        "AMD Ryzen 7 6800H": "Ryzen 7 6800H",
        "AMD Ryzen 9 5900HX": "Ryzen 9 5900HX",
        "AMD Ryzen 7 4800H": "Ryzen 7 4800H",
        "AMD Ryzen 5 4600H": "Ryzen 5 4600H",
        "AMD Ryzen 9 6900HX": "Ryzen 9 6900HX",
        "AMD Ryzen 7 7735HS": "Ryzen 7 7735HS",
        "AMD Ryzen 9 7940HS": "Ryzen 9 7940HS",
        "AMD Ryzen 9 8945HS": "Ryzen 9 8945HS",
        "AMD Ryzen 7 7040": "Ryzen 7 7040",
    },
    
    "ram": {
        "8GB": "8GB",
        "16GB": "16GB", 
        "32GB": "32GB",
        "64GB": "64GB"
    },
    
    "gpu": {
        # NVIDIA RTX 40 series
        "NVIDIA GeForce RTX 4090": "RTX 4090",
        "NVIDIA GeForce RTX 4080": "RTX 4080",
        "NVIDIA GeForce RTX 4070": "RTX 4070",
        "NVIDIA GeForce RTX 4060": "RTX 4060",
        "NVIDIA GeForce RTX 4050": "RTX 4050",
        
        # NVIDIA RTX 30 series
        "NVIDIA GeForce RTX 3080": "RTX 3080",
        "NVIDIA GeForce RTX 3070": "RTX 3070",
        "NVIDIA GeForce RTX 3060": "RTX 3060",
        "NVIDIA GeForce RTX 3050": "RTX 3050",
        "NVIDIA GeForce RTX 3080 Ti": "RTX 3080 Ti",
        "NVIDIA GeForce RTX 3070 Ti": "RTX 3070 Ti",
        
        # NVIDIA GTX series
        "NVIDIA GeForce GTX 1650": "GTX 1650",
        "NVIDIA GeForce GTX 1650 Ti": "GTX 1650 Ti",
        "NVIDIA GeForce GTX 1660 Ti": "GTX 1660 Ti",
        "NVIDIA GeForce GTX 2070": "RTX 2070",
        "NVIDIA GeForce GTX 2080": "RTX 2080",
        
        # AMD graphics
        "AMD Radeon RX 6600M": "RX 6600M",
        "AMD Radeon RX 6700M": "RX 6700M",
        
        # Integrated graphics
        "Intel Iris Xe Graphics": "Integrated",
        "AMD Radeon Graphics": "Integrated",
    },
    
    "display": {
        "15.6 inch FHD 144Hz": "144Hz",
        "15.6 inch FHD 120Hz": "120Hz", 
        "15.6 inch FHD 60Hz": "60Hz",
        "17.3 inch FHD 144Hz": "17.3 144Hz",
        "14 inch FHD 60Hz": "14 60Hz",
        "13.3 inch FHD 60Hz": "13.3 60Hz",
        "15.6 inch 4K 60Hz": "4K",
        "16 inch QHD 165Hz": "QHD 165Hz",
        "15.6 inch FHD 165Hz": "165Hz",
        "17.3 inch FHD 165Hz": "17.3 165Hz",
        "15.6 inch QHD 165Hz": "QHD 165Hz",
        "14 inch QHD 120Hz": "14 QHD 120Hz",
        "15.6 inch FHD 240Hz": "240Hz",
        "17.3 inch FHD 240Hz": "17.3 240Hz",
        "15.6 inch QHD 240Hz": "QHD 240Hz",
        "15.6 inch FHD 300Hz": "300Hz",
        "14 inch OLED 120Hz": "14 OLED 120Hz",
        "16 inch OLED 240Hz": "16 OLED 240Hz",
    },
    
    "storage": {
        "256GB SSD": "256GB",
        "512GB SSD": "512GB", 
        "1TB SSD": "1TB",
        "2TB SSD": "2TB",
        "1TB HDD + 256GB SSD": "1TB+256GB",
    }
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