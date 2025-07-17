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


if __name__=="__main__":
    with open("assets/original.svg",'r') as f:
        svg = f.read()

    outline = extract_outline_svg(svg)

    with open("assets/outlines.svg",'w') as f:
        f.write(outline)