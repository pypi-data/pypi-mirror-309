import os
import streamlit.components.v1 as components

_RELEASE = True  

if not _RELEASE:
    _cv_text_el = components.declare_component(
       
        "cv_text_element",
        
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _cv_text_el = components.declare_component("cv_text_el", path=build_dir)


def cv_text_el(
        data=None, 
        styles=None,
        key=None, 
        default=None):
    
    component_value = _cv_text_el(
        data=data, 
        styles=styles,
        key=key, 
        default=default 
        )

    return component_value
