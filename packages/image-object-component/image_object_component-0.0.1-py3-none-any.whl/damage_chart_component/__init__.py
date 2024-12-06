import os
import streamlit.components.v1 as components

_RELEASE = True 

if not _RELEASE:
    _image_chart_damage = components.declare_component(
       
        "image_chart_damage",
        
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _image_chart_damage = components.declare_component("image_chart_damage", path=build_dir)


def image_chart_damage(
        data=None, 
        damageStat=None, 
        playerLevelStage="playerLvlData", 
        img_main_height_width={"height":100, "width":100}, 
        chartType="pie", 
        styles=None,
        outerChartLayout=None,
        proportionData=None,
        barChartScale=8,
        innerImgScale=4,
        key=None, 
        default=None):
    
    component_value = _image_chart_damage(
        data=data, 
        damageStat=damageStat, 
        playerLevelStage=playerLevelStage, 
        img_main_height_width=img_main_height_width,
        chartType=chartType, 
        styles=styles,
        outerChartLayout=outerChartLayout,
        proportionData=proportionData,
        barChartScale=barChartScale,
        innerImgScale=innerImgScale, 
        key=key, 
        default=default 
        )

    return component_value
