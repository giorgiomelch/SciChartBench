AREA_LINE_BAR_HISTOGRAM_SCHEMA = {
    "name": "area_line_bar_histogram_schema",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "chart_title": {"type": ["string", "null"]},
            "x_axis_label": {"type": ["string", "null"]},
            "y_axis_label": {"type": ["string", "null"]},
            "categorical_axis": {
                "type": ["string", "null"],
                "enum": ["x", "y", None]
            },
            "data_points": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "series_name": {"type": "string"},
                        "x_value": {"type": ["string", "number"]},
                        "y_value": {"type": ["string", "number"]}
                    },
                    "required": ["series_name", "x_value", "y_value"]
                }
            }
        },
        "required": ["chart_title", "data_points"]
    }
}
SCATTER_SCHEMA = {
    "name": "scatter_schema",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "chart_title": {"type": ["string", "null"]},
            "x_axis_label": {"type": ["string", "null"]},
            "y_axis_label": {"type": ["string", "null"]},
            "data_points": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "series_name": {"type": "string"},
                        "x_value": {"type": ["number", "string"]},
                        "y_value": {"type": "number"}
                    },
                    "required": ["series_name", "x_value", "y_value"]
                }
            }
        },
        "required": ["chart_title", "data_points"]
    }
}
RADAR_SCHEMA = {
    "name": "radar_schema",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "chart_title": {"type": ["string", "null"]},
            "data_points": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "series_name": {"type": "string"},
                        "x_value": {"type": "string"},
                        "y_value": {"type": "number"}
                    },
                    "required": ["series_name", "x_value", "y_value"]
                }
            }
        },
        "required": ["chart_title", "data_points"]
    }
}
PIE_SCHEMA = {
    "name": "pie_schema",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "chart_title": {"type": ["string", "null"]},
            "data_points": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "series_name": {"type": "string"},
                        "x_value": {"type": "string"},
                        "y_value": {"type": "number"}
                    },
                    "required": ["series_name", "x_value", "y_value"]
                }
            }
        },
        "required": ["chart_title", "data_points"]
    }
}
BOX_SCHEMA = {
    "name": "box_schema",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "chart_title": {"type": ["string", "null"]},
            "x_axis_label": {"type": ["string", "null"]},
            "y_axis_label": {"type": ["string", "null"]},
            "categorical_axis": {
                "type": ["string", "null"],
                "enum": ["x", "y", None]
            },
            "data_points": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "series_name": {"type": "string"},
                        "x_value": {"type": ["string", "number"]},
                        "y_value": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "min": {"type": "number"},
                                "q1": {"type": ["number", "null"]},
                                "median": {"type": "number"},
                                "q3": {"type": ["number", "null"]},
                                "max": {"type": "number"}
                            },
                            "required": ["min", "median", "max"]
                        }
                    },
                    "required": ["series_name", "x_value", "y_value"]
                }
            }
        },
        "required": ["chart_title", "data_points"]
    }
}
ERRORPOINT_SCHEMA = {
    "name": "errorpoint_schema",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "chart_title": {"type": ["string", "null"]},
            "x_axis_label": {"type": ["string", "null"]},
            "y_axis_label": {"type": ["string", "null"]},
            "categorical_axis": {
                "type": ["string", "null"],
                "enum": ["x", "y", None]
            },
            "data_points": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "series_name": {"type": "string"},
                        "x_value": {"type": ["string", "number"]},
                        "y_value": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "min": {"type": "number"},
                                "median": {"type": "number"},
                                "max": {"type": "number"}
                            },
                            "required": ["min", "median", "max"]
                        }
                    },
                    "required": ["series_name", "x_value", "y_value"]
                }
            }
        },
        "required": ["chart_title", "data_points"]
    }
}
BUBBLE_SCHEMA = {
    "name": "bubble_schema",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "chart_title": {"type": ["string", "null"]},
            "x_axis_label": {"type": ["string", "null"]},
            "y_axis_label": {"type": ["string", "null"]},
            "categorical_axis": {
                "type": ["string", "null"],
                "enum": ["x", "y", None]
            },
            "data_points": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "series_name": {"type": "string"},
                        "x_value": {"type": ["number", "string"]},
                        "y_value": {"type": ["number", "string"]},
                        "z_value": {"type": "number"},
                        "w_value": {"type": ["number", "null"]}
                    },
                    "required": ["series_name", "x_value", "y_value", "z_value"]
                }
            }
        },
        "required": ["chart_title", "data_points"]
    }
}
HEATMAP_SCHEMA = {
    "name": "heatmap_schema",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "chart_title": {"type": ["string", "null"]},
            "x_axis_label": {"type": ["string", "null"]},
            "y_axis_label": {"type": ["string", "null"]},
            "data_points": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "x_value": {"type": ["string", "number"]},
                        "y_value": {"type": ["string", "number"]},
                        "intensity_value": {"type": "number"}
                    },
                    "required": ["x_value", "y_value", "intensity_value"]
                }
            }
        },
        "required": ["chart_title", "data_points"]
    }
}
SCHEMA2CHARTCLASS = {
    "area": AREA_LINE_BAR_HISTOGRAM_SCHEMA,
    "line": AREA_LINE_BAR_HISTOGRAM_SCHEMA,
    "bar": AREA_LINE_BAR_HISTOGRAM_SCHEMA,
    "histogram": AREA_LINE_BAR_HISTOGRAM_SCHEMA,
    "scatter": SCATTER_SCHEMA,
    "radar": RADAR_SCHEMA,
    "pie": PIE_SCHEMA,
    "box": BOX_SCHEMA,
    "errorpoint": ERRORPOINT_SCHEMA,
    "bubble": BUBBLE_SCHEMA,
    "heatmap": HEATMAP_SCHEMA
}