
# Create a Mermaid diagram for tobacco manufacturing digital twin architecture

diagram_code = """
graph TB
    subgraph Cloud["Cloud Platform Layer"]
        ADT["Azure Digital Twins Service"]
        EH["Event Hub"]
        DL["Data Lake (Synapse)"]
        PBI["Power BI/Analytics"]
    end
    
    subgraph Edge["Edge & Integration Layer"]
        OPC["OPC-UA Gateway"]
        MQTT["MQTT Broker"]
        ER["Edge Runtime"]
        LH["Local Historian"]
    end
    
    subgraph Plant["Plant Floor Layer"]
        MA["Manufacturing Assets<br/>(Cutting, Rolling, Packing, Printing)"]
        FC["Fillers, Conveyors<br/>Robots, AGVs"]
        SP["Sensors & PLCs"]
        VS["Vision Systems"]
        QC["QC Systems"]
    end
    
    SP -->|"Real-time telemetry<br/>(MQTT/OPC-UA)"| MQTT
    MA -->|"Real-time telemetry<br/>(MQTT/OPC-UA)"| OPC
    FC -->|"Real-time telemetry<br/>(MQTT/OPC-UA)"| MQTT
    VS -->|"Real-time telemetry<br/>(MQTT/OPC-UA)"| OPC
    QC -->|"Real-time telemetry<br/>(MQTT/OPC-UA)"| MQTT
    
    MQTT --> ER
    OPC --> ER
    
    ER -->|"Alert/event streams"| EH
    ER --> LH
    
    LH -->|"Historian queries"| DL
    EH --> ADT
    EH --> DL
    
    ADT --> PBI
    DL --> PBI
    
    PBI -->|"Analytics feedback"| ER
    ADT -->|"Command & control"| ER
    
    ER -->|"Command & control"| OPC
    ER -->|"Command & control"| MQTT
    
    OPC -->|"Command & control"| MA
    MQTT -->|"Command & control"| SP
    MQTT -->|"Command & control"| FC
    
    classDef cloudStyle fill:#B3E5EC,stroke:#1FB8CD,stroke-width:2px,color:#000
    classDef edgeStyle fill:#FFEB8A,stroke:#D2BA4C,stroke-width:2px,color:#000
    classDef plantStyle fill:#A5D6A7,stroke:#2E8B57,stroke-width:2px,color:#000
    
    class ADT,EH,DL,PBI cloudStyle
    class OPC,MQTT,ER,LH edgeStyle
    class MA,FC,SP,VS,QC plantStyle
"""

# Create the diagram using the helper function
create_mermaid_diagram(diagram_code, 'architecture.png', 'architecture.svg', width=1400, height=1000)
