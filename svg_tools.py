# from svg.path import parse_path, Path, Line, Arc, CubicBezier, QuadraticBezier
from xml.etree import ElementTree as ET
from xml.dom import minidom

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

from xml.etree import ElementTree as ET
from xml.dom import minidom

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

def shape_to_path(element):
    tag = element.tag.split("}")[-1]
    
    if tag == 'path':
        d = element.get('d')
    
    elif tag == 'rect':
        x = float(element.get('x', 0))
        y = float(element.get('y', 0))
        w = float(element.get('width', 0))
        h = float(element.get('height', 0))
        d = f"M{x},{y} h{w} v{h} h{-w} Z"
    
    elif tag == 'circle':
        cx = float(element.get('cx', 0))
        cy = float(element.get('cy', 0))
        r = float(element.get('r', 0))
        d = f"M{cx - r},{cy} a{r},{r} 0 1,0 {2*r},0 a{r},{r} 0 1,0 {-2*r},0"
    
    elif tag == 'ellipse':
        cx = float(element.get('cx', 0))
        cy = float(element.get('cy', 0))
        rx = float(element.get('rx', 0))
        ry = float(element.get('ry', 0))
        d = f"M{cx - rx},{cy} a{rx},{ry} 0 1,0 {2*rx},0 a{rx},{ry} 0 1,0 {-2*rx},0"
    
    elif tag == 'line':
        x1 = float(element.get('x1', 0))
        y1 = float(element.get('y1', 0))
        x2 = float(element.get('x2', 0))
        y2 = float(element.get('y2', 0))
        d = f"M{x1},{y1} L{x2},{y2}"
    
    elif tag == 'polyline':
        points = element.get('points', '').strip()
        if not points:
            return None
        pts = points.split()
        d = f"M{pts[0]} " + " ".join(f"L{pt}" for pt in pts[1:])
    
    elif tag == 'polygon':
        points = element.get('points', '').strip()
        if not points:
            return None
        pts = points.split()
        d = f"M{pts[0]} " + " ".join(f"L{pt}" for pt in pts[1:]) + " Z"
    
    else:
        return None

    # Create new <path> element with outline style
    path_el = ET.Element(f"{{{SVG_NS}}}path")
    path_el.set("d", d)
    path_el.set("stroke", "black")
    path_el.set("stroke-width", "1")
    path_el.set("fill", "none")
    return path_el

def extract_outline_svg(svg_string):
    root = ET.fromstring(svg_string)
    new_svg = ET.Element(f"{{{SVG_NS}}}svg", root.attrib)

    # Copy dimensions
    for attr in ['viewBox', 'width', 'height']:
        if attr in root.attrib:
            new_svg.set(attr, root.attrib[attr])
    
    new_svg.set('width','210')
    new_svg.set('height','210')

    tag_names = ['path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon']

    for elem in root.iter():
        tag = elem.tag.split("}")[-1]
        if tag in tag_names:
            path_elem = shape_to_path(elem)
            if path_elem is not None:
                new_svg.append(path_elem)

    rough_string = ET.tostring(new_svg, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

import os
import hashlib
import functools
from pathlib import Path
import re
from typing import Callable, Optional

def svg_cache(cache_dir: str = "assets", pth: str = "orig", width: int = 250, height: int = 250):
    """
    Decorator that caches SVG output based on string input.
    
    Args:
        cache_dir: Directory to store cached SVG files (default: "assets")
        name_suffix: String to append to the filename (default: "")
        width: Width to set for SVG if not present (default: 250)
        height: Height to set for SVG if not present (default: 250)
    
    Returns:
        Decorator function
    """
    def decorator(func: Callable[[str,str], str]) -> Callable[[str], str]:
        @functools.wraps(func)
        def wrapper(input_string: str,league:str="EPL") -> str:
            # Create cache directory if it doesn't exist
            cache_path = Path(os.path.join(cache_dir,league),pth)
            cache_path.mkdir(parents=True, exist_ok=True)
            
            
            # Create filename with optional suffix
            filename = f"{input_string}.svg"
            file_path = cache_path / filename
            
            # Check if cached file exists
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        cached_svg = f.read()
                    print(f"Loaded cached SVG: {file_path}")
                    return cached_svg
                except (IOError, OSError) as e:
                    print(f"Error reading cached file {file_path}: {e}")
                    # Continue to regenerate if cache read fails
            
            # Generate new SVG
            print(f"Generating new SVG for input: {input_string[:50]}...")
            svg_content = func(input_string,league)
            
            # Ensure SVG has proper dimensions
            processed_svg = _ensure_svg_dimensions(svg_content, width, height)
            
            # Save to cache
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(processed_svg)
                print(f"Cached SVG saved: {file_path}")
            except (IOError, OSError) as e:
                print(f"Error saving cache file {file_path}: {e}")
            
            return processed_svg
        
        return wrapper
    return decorator

def _ensure_svg_dimensions(svg_content: str, width: int, height: int) -> str:
    """
    Ensures SVG has proper width and height attributes.
    
    Args:
        svg_content: The SVG content as string
        width: Desired width
        height: Desired height
    
    Returns:
        SVG content with proper dimensions
    """
    # Check if SVG tag exists
    if not svg_content.strip().startswith('<svg'):
        # If it's not a complete SVG, wrap it
        svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">{svg_content}</svg>'
    else:
        # Check if width and height are already set
        has_width = re.search(r'width\s*=\s*["\'][^"\']*["\']', svg_content)
        has_height = re.search(r'height\s*=\s*["\'][^"\']*["\']', svg_content)
        
        if not has_width or not has_height:
            # Find the opening SVG tag
            svg_tag_match = re.search(r'<svg([^>]*)>', svg_content)
            if svg_tag_match:
                svg_attributes = svg_tag_match.group(1)
                
                # Add width if not present
                if not has_width:
                    svg_attributes += f' width="{width}"'
                
                # Add height if not present
                if not has_height:
                    svg_attributes += f' height="{height}"'
                
                # Replace the SVG tag
                new_svg_tag = f'<svg{svg_attributes}>'
                svg_content = svg_content.replace(svg_tag_match.group(0), new_svg_tag)
    
    return svg_content

if __name__=="__main__":
    with open("assets/original.svg",'r') as f:
        svg = f.read()

    outline = extract_outline_svg(svg)

    with open("assets/outlines.svg",'w') as f:
        f.write(outline)

  # Test the cached functions
    print("Testing SVG cache decorator:")
    print("-" * 40)
    
    # First call - should generate and cache
