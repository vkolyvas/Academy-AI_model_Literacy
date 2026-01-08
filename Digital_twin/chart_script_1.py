
diagram_code = """
flowchart LR
    subgraph PF["PLANT FLOOR LAYER"]
        direction TB
        PLC["PLC<br/>Siemens/Rockwell"]
        SCADA["SCADA HMI"]
        Sensors["Sensors<br/>temp/vibration/weight"]
        Equipment["Equipment<br/>rolling/packing/printing"]
        HistDB[("Historian DB<br/>time-series")]
    end
    
    subgraph EDGE["EDGE & INTEGRATION LAYER"]
        direction TB
        OPC["OPC-UA Client"]
        MQTT["MQTT Broker/Client<br/>JSON payload"]
        Valid["Data Validation"]
        Buffer["Local Buffer Cache"]
        VPN["VPN Tunnel"]
    end
    
    subgraph CLOUD["CLOUD LAYER - AZURE"]
        direction TB
        IoTHub{{"IoT Hub"}}
        StreamA{{"Stream Analytics<br/>REAL-TIME PATH"}}
        Lake[("Data Lake<br/>BATCH/HISTORICAL PATH")]
        DT{{"Digital Twins"}}
        PowerBI["Power BI Dashboard"]
    end
    
    Sensors --> PLC
    Equipment --> PLC
    PLC -->|"OPC-UA subscribe"| OPC
    SCADA -->|"OPC-UA subscribe"| OPC
    PLC --> HistDB
    
    OPC -->|"MQTT publish JSON"| MQTT
    MQTT --> Valid
    Valid --> Buffer
    Buffer --> VPN
    
    VPN -->|"Telemetry upload"| IoTHub
    IoTHub -->|"real-time compute"| StreamA
    IoTHub -->|"batch store"| Lake
    StreamA -->|"update"| DT
    DT -->|"dashboard update"| PowerBI
    Lake -->|"historical query"| PowerBI
    HistDB -.->|"historical query"| Lake
"""

# Create the diagram using the helper function with simpler styling
png_path, svg_path = create_mermaid_diagram(
    diagram_code, 
    'digital_twin_arch.png', 
    'digital_twin_arch.svg', 
    width=1400, 
    height=900
)

print(f"Diagram created successfully")
print(f"PNG: {png_path}")
print(f"SVG: {svg_path}")
