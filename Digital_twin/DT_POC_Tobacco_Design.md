# Digital Twin Proof of Concept (POC) Design
## Tobacco Manufacturing End-to-End Production Flow

**Document Version:** 1.0 | **Date:** January 2026 | **Status:** POC Design Phase

---

## EXECUTIVE SUMMARY

This document outlines a comprehensive Digital Twin POC for a tobacco manufacturing facility (e.g., PMI-type operation) that virtualizes the complete production flow from raw material intake through finished-goods logistics hand-off. The POC will demonstrate OEE improvement (target: +8-12%), bottleneck detection, predictive maintenance readiness, and GxP compliance capabilities.

**Estimated POC Duration:** 6-9 months  
**Estimated POC Investment:** €800K–€1.2M (pilot line)  
**Expected ROI Payback:** 18-24 months post-deployment

---

## 1. SCOPE & BOUNDARIES

### 1.1 Physical Scope

**In Scope (Pilot Line):**
- **Manufacturing Line:** End-to-end cigarette/vape production (1 complete line)
- **Utilities Area:** Compressed air, utilities monitoring
- **Warehouse Zone:** Raw material intake buffer, finished goods staging
- **QC Lab:** Defect detection, moisture testing, lab integration
- **Maintenance Area:** Tool inventory, preventive maintenance records
- **Logistics Zone:** Cartonization, palletization, label verification, shipping

**Out of Scope (Post-POC Scaling):**
- Multiple production lines (Phase 2+)
- Regulatory affairs ERP integration (Phase 2)
- Supplier supply chain twins
- Customer/retailer tracking

### 1.2 Functional Scope

| Component | Included | Notes |
|-----------|----------|-------|
| Real-time telemetry ingestion | ✓ | SCADA, MES, sensors |
| Process state tracking | ✓ | Production phases, transitions |
| Asset lifecycle management | ✓ | Equipment health, maintenance |
| Quality tracking by batch/lot | ✓ | Defect rate, rework loops |
| Downtime root-cause analysis | ✓ | Automated anomaly detection |
| Predictive maintenance models | ✓ | MTBF/MTTR trending |
| Scenario simulation & what-if | ✓ | Limited to changeover optimization |
| Full-line 3D visualization | ✓ | Line model with equipment overlays |
| GxP compliance auditing | ✓ | Change records, audit trail |
| ESG & energy tracking | ✓ | Consumption by asset/product |

---

## 2. PHYSICAL ASSETS TO MODEL

### 2.1 Equipment Categories

#### **A. Leaf Preparation & Processing**
- **Cutting Machines** (e.g., Hauni, Molins cutters)
  - Input speed, blade wear, vibration
  - Output density, particle size consistency
- **Dryers & Conditioning Units**
  - Temperature, humidity, residence time
  - Moisture content verification
- **Blending Hoppers** (automated)
  - Fill level, blend uniformity sensors

#### **B. Cigarette Production Line (Primary Workflow)**
1. **Rolling/Forming Machines** (e.g., Hauni Protos)
   - Rod diameter, weight, density sensors
   - Wrapper tension, rod length consistency
   - Scrap rate, product yield
   
2. **Filter Application Units**
   - Filter insertion speed, adhesion pressure
   - Filter alignment cameras, dimensional checks
   - Plug/filter gap measurement
   
3. **Wrapping Machines** (outer wrap)
   - Wrapper glue pattern, seam strength
   - Circumference, weight consistency
   
4. **Packing Machines** (single-sticks → pack)
   - Stick orientation, stick count verification
   - Pack weight, firmness, uniformity
   - Reject gates (defective sticks)
   
5. **Printing & Coding**
   - Barcode/QR legibility (vision systems)
   - Health warning print clarity
   - Date code, batch lot printing
   - Color registration accuracy

6. **Cartonization**
   - Pack count/carton, carton weight
   - Label placement, alignment
   - Carton integrity, glue patterns
   
7. **Palletization**
   - Carton arrangement, pallet weight
   - Stretch wrap uniformity
   - Pallet ID generation, RFID encoding

#### **C. Conveyor System**
- **Main throughput conveyor**
  - Speed (m/min), product flow rate
  - Belt tension, product jam detection
  - Accumulation/buffer zones
  
- **Reject/rework loops**
  - Divert valve positions
  - Rework product traceability
  
- **Sortation gates**
  - Pneumatic valve response time
  - Sorting accuracy

#### **D. Alternative Product Lines (Vape/Heated Tobacco)**

**Vape Assembly Line:**
- **Liquid Filling Units**
  - Fill volume, pressure, temperature
  - Leakage detection sensors
  - Cartridge position verification
  
- **Cartridge/Battery Assembly**
  - Assembly press force, dwell time
  - Contact resistance measurements
  - Weight verification
  
- **Device Testing Station**
  - Electrical continuity tests
  - Puff-simulation pressure ramps
  - Battery capacity (mAh) verification
  - Leak rate (negative pressure test)
  
- **Packaging (Color, SKU verification)**
  - Vision confirmation: product variant
  - Label/packaging integrity checks

**Heated Tobacco Sticks:**
- Substrate forming (similar to cigarette rod)
- Flavor/additive coating
- Stick wrapping & integrity sealing
- Pack assembly & serialization

#### **E. Sensors & Instrumentation (Distributed)**

**Temperature & Humidity Sensors:**
- Leaf conditioning areas (setpoint monitoring)
- Rolling machine zones (wrapper malfunction prevention)
- Storage/warehouse (product stability)

**Vibration Sensors:**
- Motor bearing monitors (early fault detection)
- Conveyor drive shafts
- High-speed cutting machines (blade wear correlation)

**Pressure Sensors:**
- Compressed air distribution (supply pressure, leaks)
- Pneumatic divert gates (valve response)
- Filter attachment pressure (consistency)

**Weight & Dimensional Sensors:**
- Rod weight (in-line checks, 0.3% tolerance)
- Stick count (pack verification, ±1 unit)
- Carton weight (target ±10g)
- Barcode/QR vision system (legibility %)

**Flow Meters:**
- Adhesive/glue dispense rates (ml/min)
- Leaf material flow (kg/h)
- Waste product streams (scrap recovery)

**Electrical Sensors:**
- Motor current draws (trending for wear)
- Servo positioning feedback (consistency)
- Photoeyes (product detection, jam sensing)

#### **F. PLCs & Controllers**
- **Main Production PLC** (Siemens S7-1200/1500, Allen-Bradley CompactLogix)
  - Real-time program scanning (10–50ms cycle)
  - Networked I/O modules (analog, digital, safety-rated)
  
- **Decentralized I/O** (PROFINET, EtherCAT)
  - Line segment controllers
  - Motor drives (VFD) with communication
  
- **Batch & Track-and-Trace Controller**
  - Lot/batch ID generation
  - GxP timestamp logging
  - Serialization management

#### **G. Robots & Automated Guided Vehicles (AGVs)**
- **Palletizing Robot** (e.g., ABB, KUKA)
  - Position feedback, load cell
  - Uptime/downtime events
  - Maintenance schedule tracking
  
- **Automated Guided Vehicles (AGVs)**
  - Position tracking (warehouse mapping)
  - Battery state-of-charge (%)
  - Collision/safety sensor events
  - Delivery completion timestamps

#### **H. Supporting Systems Integration**
- **SCADA Front-end** (traditional HMI feeds real-time data)
- **Manufacturing Execution System (MES)**
  - Order tracking, lot master data
  - Production scheduling, changeovers
  - Downtime logging, maintenance work orders
- **Historian Database**
  - Trend data (OSIsoft PI, Ignition historian)
  - High-resolution time-series
- **Vision System**
  - Print quality inspection cameras
  - Defect detection (cracks, debris, label misalignment)
  - AI/ML defect classification

---

## 3. PROCESS STEPS & WORKFLOW

### 3.1 Cigarette Pack Production Flow

```
Raw Material Intake
    ↓
Leaf Cutting & Drying
    ↓
Blending & Conditioning
    ↓
Rolling (Rod Formation)
    ↓
Filter Application
    ↓
Wrapping (Outer Cover)
    ↓
Packing (Single Stick → Pack)
    ↓
Printing & Coding (Barcode/QR/Warnings)
    ↓
Quality Inspection (Vision + Lab Sampling)
    ↓
Cartonization (Pack → Carton, 10/20 packs)
    ↓
Labeling & Registration
    ↓
Palletization (Carton → Pallet)
    ↓
Stretch Wrap & Pallet ID
    ↓
Staging & Logistics Hand-Off
```

### 3.2 Process Step Details & Telemetry Points

| Step | Equipment | Key Sensors | GxP Checkpoints | Typical Cycle Time |
|------|-----------|------------|-----------------|------------------|
| **Leaf Intake** | Cutting machine | Weight, moisture, particle size | Batch ID logging, supplier traceability | 10–20 kg/min |
| **Conditioning** | Dryer/humidifier | Temperature, humidity, dwell time | Setpoint validation, deviation alerts | Variable (1–8 hrs) |
| **Rolling** | Hauni/Molins rod machine | Rod weight, diameter, density | ±0.3g tolerance, auto-reject, SPC | 7,500–8,500 cigs/min |
| **Filter Apply** | Filter feeder + adhesive dispense | Filter insertion speed, adhesive ml/min | Filter lot traceability, adhesive cure time | 7,500–8,500 cigs/min |
| **Wrapping** | Outer wrapper application | Wrapper tension, glue bead pattern | Wrapper lot tracking, seam strength tests | 7,500–8,500 cigs/min |
| **Packing (Sticks→Pack)** | Packing machine | Stick count, pack weight, firmness | Product count verification, net weight compliance | 600–1,200 packs/min |
| **Print & Code** | Rotogravure printer + digital coder | Print density, barcode legibility (%), date code | Barcode readability %, serialization continuity | 600–1,200 packs/min |
| **Quality Inspection** | Vision system + sampling | Defect type/count, moisture test (lab) | Reject reason logging, SPC charts | Sampling: 1/200–1/500 |
| **Cartonization** | Carton forming + packing | Pack count, carton weight, label placement | Carton integrity checks, serial carton numbering | 150–300 cartons/min |
| **Palletization** | Robotic palletizer | Pallet arrangement, pallet weight | Pallet ID generation, GS1-128 SSCC, pallet sealing | 40–80 pallets/shift |
| **Staging** | Warehouse buffer | Pallet position, dwell time, final QC sample | Quarantine if QC fail, release approval | Pre-shipment hold |

### 3.3 Rework & Reject Handling

**Inline Rejects:**
- Rod diameter out of tolerance → automated scrap divert valve
- Pack weight low/high → auto-reject gate
- Printing defect (barcode illegible) → vision-triggered divert to rework pack

**Rework Loops:**
- Rejected packs → buffer conveyor → re-packing station
- Rejects logged by serial pack ID and timestamp
- Rework traceability: original lot + rework stage tracked separately

**Scrap Disposal:**
- Accumulated scrap → waste cart → recycling/energy recovery
- Scrap weight monitored (KPI: target scrap <2%)

---

## 4. VAPE & HEATED-TOBACCO PRODUCT VARIANTS

### 4.1 Vape Device Production (Parallel Line)

**Workflow:**
```
Liquid Reservoir Preparation → Filling & Sealing → Cartridge Assembly
    ↓
Battery Module Assembly (cell + connectors) → Continuity Test
    ↓
Device Integration (cartridge + battery) → Functional Test (puff simulation)
    ↓
Leak Test (negative pressure) → Battery Capacity Test (mAh charging/discharging)
    ↓
Device Coding (IMEI/serial) → Packaging (variant-specific SKU)
    ↓
Quality Inspection (packaging integrity) → Case Assembly & Palletization
    ↓
Logistics Hand-Off
```

**Key Sensors & Telemetry:**
- **Liquid Filling:** Volume (ml ±0.5), temperature (viscosity monitoring), leakage sensors
- **Battery Assembly:** Cell voltage (nominal 3.7V), resistance (mOhm), weight (±0.5g)
- **Device Testing:**
  - Electrical continuity (pass/fail)
  - Puff simulation pressure ramp (bar vs. time graph)
  - Battery capacity (mAh recorded per device)
  - Leak rate: -50 to -100 mbar for 5 seconds (pass/fail)
- **Packaging:** Vision system (SKU variant verification), label placement, sealing quality

**GxP Checkpoints:**
- Component lot traceability (liquid supplier, battery cells)
- Test data logging (every device tested → production record)
- Deviation alerts (test failure reason, serial device ID)
- Temperature/humidity monitoring (liquid storage stability)
- Serialization: IMEI + QR code link to test data

### 4.2 Heated Tobacco Stick Production

**Workflow:**
```
Substrate Formation (similar to cigarette rod, but with additive coating)
    ↓
Flavor/Botanical Coating (spray/dispense application)
    ↓
Stick Wrapping (protective outer layer, heat-resistant paper)
    ↓
Integrity Sealing (end-caps or adhesive closure)
    ↓
Stick Serialization (batch + sequential number, printing)
    ↓
Pack Assembly (25 sticks/pack, custom box)
    ↓
Labeling & Compliance (warning labels, user instructions)
    ↓
Case Packing & Palletization
    ↓
Logistics Hand-Off
```

**Differentiation from Cigarettes:**
- **Coating step:** Botanical/flavor additive applied at controlled temperature & humidity
- **Heat-resistant wrapping:** Special paper grades, strength verification
- **Serialization:** Each stick coded (track individual stick if needed for recalls)
- **Regulatory labels:** Different graphics, compatibility with heating-device instructions
- **Packaging format:** Often premium/smaller cases (10–20 sticks/pack)

**Key Sensors:**
- Coating application: ml/min, spray pattern (vision), temperature
- Stick structural integrity: burst pressure test (bar) sampled per batch
- Pack assembly: stick count ±1, pack weight ±5g
- Serialization: barcode legibility, batch continuity

---

## 5. DATA SOURCES & INTEGRATION

### 5.1 Primary Data Sources

| Source | Protocol | Data Type | Frequency | Integration Method |
|--------|----------|-----------|-----------|-------------------|
| **PLC (Production Line)** | Modbus/TCP, PROFINET, EtherCAT | DI/DO, AI/AO, counters | 10–50ms (native), 1s (gateway) | OPC-UA server or MQTT agent |
| **SCADA/HMI** | OPC-UA, HTTP REST | Real-time process variables, alarms | 1–5s | OPC-UA client pull, or webhook push |
| **MES** | REST API, SFTP, database replication | Production orders, lot master data, changeover schedules | Transactional (event-driven) | API polling or message queue |
| **Historian (PI, Ignition)** | REST, OPC-UA, direct query | Time-series trend data (retrospective analysis) | Query on-demand, 5–15min batch | Batch export or streaming topic |
| **IoT Sensors** | MQTT, CoAP, HTTP | Temperature, humidity, vibration, pressure, weight | 5–30s per sensor | MQTT broker subscription |
| **Vision Systems** | HTTP POST (webhook), SFTP, database insert | Defect classification, print quality score, image metadata | Per-pack or per-carton (near real-time) | Webhook or message queue |
| **QA/Lab Systems** | LIMS (Laboratory Information Management System) API, database replication | Moisture content, chemical analysis, batch test results | Sampling basis (e.g., 1/500 packs) | Daily batch export or API sync |
| **AGV Fleet Management** | REST API, MQTT | Position (GPS/RFID), battery %, task status, collision events | 10–30s | MQTT pub/sub or REST polling |
| **Maintenance Management System** | REST API, SFTP | Work orders, equipment history, spare parts, MTBF/MTTR | Event-driven (work order created/closed) | API webhook or batch sync |
| **Energy Management** | Modbus, M-Bus, IEC 61850 | Power consumption (kWh), reactive power (kVAr) | 15–60min per meter | Edge gateway aggregation → cloud |

### 5.2 Integration Architecture

#### **Option A: Hybrid OPC-UA + MQTT Gateway (Recommended for GxP)**

```
Plant Floor
  ├─ PLC (OPC-UA server built-in)
  ├─ SCADA (OPC-UA server)
  ├─ Historian (OPC-UA server)
  └─ IoT Devices (MQTT clients)
       ↓
  Edge Gateway (Windows/Linux Industrial PC)
    ├─ OPC-UA Client (subscribes to PLC/SCADA/Historian)
    ├─ MQTT Client (subscribes to sensor topics)
    ├─ Local Data Buffering (disk buffer for offline resilience)
    ├─ Timestamp Synchronization (NTP)
    ├─ Encryption/TLS (data in transit)
    └─ Device Certificate Management (X.509, rotated annually)
       ↓
  Cloud Ingestion Layer
    ├─ Azure Event Hubs (MQTT → Event Hub bridge)
    ├─ Azure IoT Hub (device identity, D2C telemetry)
    ├─ MQTT Broker (Mosquitto or cloud-native, e.g., Azure IoT Hub native MQTT)
    └─ Validation & Enrichment (derive OEE metrics, add context)
       ↓
  Cloud Data Lake & Analytics
    ├─ Azure Data Lake Storage (Gen 2) - raw ingestion
    ├─ Azure Synapse Analytics (SQL warehouse, transformation)
    ├─ Power BI / Grafana (real-time dashboards)
    └─ Azure Digital Twins (semantic model, simulation engine)
```

#### **Option B: Pure Azure Digital Twins + IoT Hub (Cloud-Native)**

```
Edge → Azure IoT Hub (MQTT/AMQP) → Stream Analytics → Digital Twins instance
                                                    ↓
                                              Telemetry Models
                                              (Component telemetry → DT properties)
                                                    ↓
                                       Event Routing (anomalies → alerts)
                                                    ↓
                                       Power BI visualization
```

**Recommendation:** Option A (hybrid) for brownfield facilities with legacy OPC-UA; Option B for greenfield with modern IoT stack.

---

## 6. TELEMETRY & KPI REQUIREMENTS

### 6.1 Core Telemetry

#### **Process Variables (Continuous)**
- **Throughput (packs/min):**
  - Target: 600–1,200 packs/min (line speed)
  - Calculated from: conveyor speed (m/min) × pack spacing (m) ÷ 60
  - Frequency: 1 Hz (real-time line monitoring)

- **Temperature & Humidity:**
  - Leaf conditioning: 20–25°C, 65–75% RH (set points ±2°C, ±3%)
  - Wrapping area: 18–25°C, 50–65% RH
  - Frequency: 30–60s per zone

- **Vibration (Acceleration, g):**
  - High-speed motor/bearing: peak, RMS, frequency spectrum (FFT)
  - Thresholds: alert >3.5g RMS, warning >2.5g RMS
  - Frequency: 10 Hz sampled, aggregated 1-min bins

- **Pressure (bar):**
  - Compressed air supply: target 6.5–7.0 bar, alert <6.3 bar (efficiency loss)
  - Pneumatic gates: pulse pressure feedback
  - Frequency: 5–10s

- **Weight (grams, ±0.1g precision):**
  - Rod weight: target 0.85–0.95g per stick, reject if ±0.3g
  - Pack weight: target 19.0–21.0g (20 sticks), reject if ±0.5g
  - Carton weight: target 410–430g, alert if ±10g
  - Frequency: per-unit (7,500+ Hz effective sampling)

- **Motor Current Draw (Amps):**
  - Main drive motor: trending baseline (early wear detection)
  - Frequency: 1–5s sampling, flagged if >10% above 30-day moving average

#### **Line State Variables (Discrete)**
- **Production Mode:** Running | Stopped | Changeover | Maintenance | Error
- **Product Type:** Cigarette-Regular | Cigarette-Menthol | Vape-Device | Heated-Stick
- **Pack Count (integer):** Cumulative production counter
- **Reject Count (integer):** Cumulative reject counter (with reason codes)
- **Lot/Batch ID (string):** Current batch being produced
- **Line Speed (%):** Actual speed as % of nominal (0–110%)

#### **Downtime Events (Event Log)**
- **Timestamp, Duration, Reason Code:**
  - Mechanical jam → conveyor stop sensor triggered
  - Motor fault → VFD error code captured
  - Scheduled changeover → MES changeover event
  - Preventive maintenance → PM work order ID
  - Operator intervention → human stop event
  - Quality hold → QC failure, product quarantine

### 6.2 Quality Tracking

#### **Per-Pack Tracking:**
- Pack Serial ID: (Lot_ID-YYYYMMDDHHmmss-Seq_number)
- Unit Weight: 19.5 ± 0.5g
- Barcode/QR Legibility Score: 0–100% (vision system)
- Stick Count: 20 ± 1
- Pass/Fail Status: Green | Yellow (warning) | Red (reject)
- Defect Category: Printing | Weight | Stick-break | Other
- Timestamp (log created, not production time)

#### **Per-Carton Tracking:**
- Carton Serial ID: (Lot_ID-Carton_Seq, or SSCC for pallets)
- Pack Count: 10 or 20 packs (configurable)
- Carton Weight: 410 ± 10g
- Label Placement (vision score): 95–100% required
- Seal Integrity: Pressure test pass/fail
- Lot Consolidation: all packs in carton from same lot (GxP requirement)

#### **Per-Batch/Lot Tracking:**
- **Batch Master Data:**
  - Lot ID, product code, packaging variant
  - Start timestamp, end timestamp, planned duration
  - Raw material lot traceability (leaf supplier, date, blend formula)
  - Batch-level QA summary: total packs, rejects, defect breakdown
  - Compliance status: GxP validated, audit trail complete

### 6.3 Equipment & Asset Health

#### **Predictive Maintenance Indicators (per equipment):**
| Equipment | Telemetry | Alert Threshold | MTBF Target | MTTR Target |
|-----------|-----------|-----------------|-------------|------------|
| **Rolling Machine** | Vibration (g RMS), motor current (A) | 3.5g, +10% I | 2,000 hrs | 8 hrs |
| **Packing Machine** | Servo error (mm), cycle time variance | ±5mm, >5% var | 1,500 hrs | 6 hrs |
| **Printing Unit** | Ink viscosity, nozzle pressure, printhead temp | Setpoint ±5%, 45–55°C | 1,800 hrs | 4 hrs |
| **Conveyor Drive** | Belt tension, motor current, vibration | Tension <80%, +8% I | 3,000 hrs | 6 hrs |
| **Filter Feeder** | Feeder bin level (%), jam counter | <10% level, jam >3/hr | 2,500 hrs | 5 hrs |

#### **Maintenance Schedule Visibility:**
- Preventive Maintenance (PM) calendar: due dates, estimated downtime
- Work Order History: completed PMs, actual downtime, parts replaced, labor hours
- Spare Parts Availability: on-hand inventory, reorder points, supplier lead times
- Equipment Age: installation date, hours-of-operation counter, depreciation schedule

---

## 7. QUALITY TRACKING & COMPLIANCE

### 7.1 Defect Rate Monitoring

**Real-time SPC (Statistical Process Control):**
- **Control Limits:**
  - Rod weight: ±0.3g (6σ = 0.15g); alert if 2 of 3 points >1σ outside setpoint
  - Pack weight: ±0.5g (6σ = 0.25g)
  - Stick count: ±1 (discrete)
  
- **Trending KPIs:**
  - Defect rate (%) = (Rejected Units / Total Units Produced) × 100
  - Target: <2% for standard line
  - Goal: <0.5% after optimization
  
- **Defect Categorization:**
  - 20% Weight variations (mechanical wear → maintenance alert)
  - 15% Printing defects (vision system → ink quality check)
  - 25% Stick count errors (packing machine → jam detection)
  - 15% Filter adhesion (temperature → process parameter review)
  - 25% Other (operator error, contamination, etc.)

### 7.2 Rework & Traceability

**Rework Logic:**
1. Pack rejected at primary inspection
2. Divert to rework buffer, append "RW" tag to lot ID
3. Re-pack station: remove faulty sticks, replenish from same lot
4. Re-inspect (same criteria)
5. Log: original serial, rework reason, rework timestamp, re-inspection result
6. **Limit:** max 1 rework per pack; if fails 2nd time → scrap

**Traceability Chain (GxP Requirement):**
- Raw material (leaf lot) → Blending lot → Cutting machine → Rolling machine → Filter lot → Packing lot → Carton lot → Pallet lot
- Each lot change triggers MES event, timestamped
- Audit trail: 7-year retention (regulatory requirement)

### 7.3 Batch & Lot Compliance Checks

| Check | Frequency | Pass Criteria | GxP Control |
|-------|-----------|---------------|------------|
| **Lot Closure** | Per batch completion | All packs assigned to lot, QA sample result available | Prevent consumption until QA approved |
| **Cross-Lot Contamination** | Per carton | All packs in carton from same lot ID | Carton-level lot consolidation rule |
| **Shelf-Life Segregation** | At warehouse receipt | Product lot age <80% of shelf-life | Quarantine if >shelf-life |
| **Component Lot Expiry** | Per production shift | All consumed components (filter, wrapper, glue) within expiry | MES automatic expiry check |
| **GxP Deviation Logging** | On occurrence | Documented, investigated, approved by QA | Digital signature required |

---

## 8. SIMULATION GOALS & USE CASES

### 8.1 Primary Simulation Scenarios

#### **Scenario 1: Throughput Bottleneck Detection**
- **Goal:** Identify which equipment (rolling machine vs. packing machine vs. printing) constrains overall line throughput
- **Simulation Input:** Run each machine at 100%, 95%, 90% nominal speed independently
- **Output:** 
  - Pack production rate vs. each machine speed (sensitivity curve)
  - Identify bottleneck: if rolling machine to 90% → line rate drops 15%, it's a bottleneck
  - Recommendation: invest in rolling machine upgrade first
- **Expected Impact:** +5–8% throughput gain by removing bottleneck

#### **Scenario 2: Changeover Time Optimization**
- **Goal:** Reduce product changeover downtime (e.g., Cigarette-Regular → Cigarette-Menthol)
- **Current State:** 45–60 min (clean hoppers, reprogram PLC, verify first packs)
- **Simulation Inputs:**
  - Parallel cleaning (hopper A while line runs on hopper B)
  - Quick-change filter cartridges (vs. full teardown)
  - Pre-staged PMC parameters (load from recipe library)
- **Output:** 
  - Predicted changeover time: 25–30 min
  - Steps to parallelize, sequences to reorder
- **Expected Impact:** 30–40% reduction in changeover time

#### **Scenario 3: Predictive Maintenance Scheduling**
- **Goal:** Determine optimal PM intervals to balance uptime vs. risk of failure
- **Simulation Inputs:**
  - Vibration trend (exponential wear model fitted to historical data)
  - Failure history (rolling machine blade failure every 1,800 hrs, ±200 hrs variance)
  - PM duration: 4 hours (includes parts + labor)
  - Production value: €500/hour
- **Output:**
  - Optimal PM interval: 1,600 hours (schedule before predicted failure)
  - Risk of unexpected failure at 1,600-hr window: <2%
  - Annual cost saved (avoided downtime): €12,000
- **Expected Impact:** Improved MTTR from 8→6 hrs (planned vs. emergency response)

#### **Scenario 4: Energy Consumption Optimization**
- **Goal:** Reduce energy per unit produced (€ /pack)
- **Simulation Inputs:**
  - Current energy consumption: 12 kWh per 1,000 packs
  - Cost: €1.20 per 1,000 packs
  - Drive motors run at constant speed; idle consumption: 60% of running load
  - Opportunity: install VFD on main drive, reduce speed to match demand peaks
- **Simulation Runs:**
  - Scenario A: Flat speed (baseline) → 12 kWh/1,000 packs
  - Scenario B: VFD with dynamic speed → 10.2 kWh/1,000 packs (15% reduction)
- **Output:**
  - Annual energy savings: 400,000 packs × (12–10.2) kWh / 1,000 = 720 kWh → €86/year (small, but validates model)
  - Payback for VFD installation (€15,000) in 5–6 years
- **Expected Impact:** ESG reporting: reduced carbon footprint, energy efficiency certification candidate

#### **Scenario 5: OEE Improvement Roadmap**
- **Goal:** Identify levers to improve Overall Equipment Effectiveness (target: +8%)
- **Current OEE Breakdown:**
  - Availability: 92% (downtime: 8%)
  - Performance: 96% (speed losses: 4%)
  - Quality: 97% (defects: 3%)
  - **Overall OEE: 92% × 96% × 97% = 85.4%**
- **Improvement Initiatives & Simulation:**
  1. **Reduce unplanned downtime** (jam prevention via vision) → Availability 92% → 95% (+3%)
  2. **Optimize changeover** (parallel cleaning, quick-change filters) → Availability 95% → 97% (+2%)
  3. **VFD for speed consistency** → Performance 96% → 98% (+2%)
  4. **Predictive maintenance** → fewer speed reductions during wear → Performance 98% → 98.5% (+0.5%)
  5. **Defect rate improvement** (SPC + corrective actions) → Quality 97% → 98.5% (+1.5%)
- **Simulated New OEE: 97% × 98.5% × 98.5% = 94.2% (+8.8%)**
- **Business Impact:** +8.8% more packs produced (same equipment, same labor) → €500k–€1M additional annual revenue (depending on line rate)

---

## 9. VISUALIZATION & DASHBOARD ARCHITECTURE

### 9.1 3D Line Model

**Technology Stack:**
- **3D Engine:** Three.js (web-based) or Cesium.js (geo-aware)
- **CAD Source:** Autodesk Fusion 360 export → glTF/GLTF format
- **Real-time Updates:** WebSocket connection to Digital Twins instance

**Content:**
- **Equipment Geometry:**
  - Rolling machine (cylindrical drum, visible wear simulation)
  - Packing machine (box with animated tapes)
  - Conveyor (belt with animated product flow)
  - Color-coded by status: Green (running), Yellow (warning), Red (fault)

- **Sensor Overlays:**
  - Temperature gauge at leaf dryer (numeric + visual)
  - Vibration icon at motor bearing (pulsing if >threshold)
  - Product count ticker (packs/min)

- **Event Annotations:**
  - Jam detected → red highlight on conveyor section
  - Changeover in progress → blue overlay on packing machine
  - PM due → yellow exclamation at equipment

### 9.2 Real-time Dashboards

#### **Operator Dashboard (Plant Floor, Control Room)**
- **KPI Cards:**
  - Current throughput: 850 packs/min (97% of nominal)
  - Defect rate: 1.2% (yellow, within tolerance but trending up)
  - Downtime today: 45 min (4.5% availability loss)
  - Energy: 11.8 kWh per 1,000 packs
  
- **Line State Panel:**
  - Current lot: LOT-20250108-001
  - Product: Cigarette-Regular-20pc
  - Estimated completion: 14:30 (45 min remaining)
  - Status: Running at 95% speed (post-changeover ramp-up)

- **Active Alerts:**
  - Vibration warning on rolling motor: 3.2g RMS (3.5g alert limit)
  - Recommendation: Schedule PM for rolling machine within 3 shifts
  - Compressed air pressure: 6.4 bar (low, check compressor output)

#### **Management Dashboard (Excel/Power BI, Daily Review)**
- **Shift Summary:**
  - Total packs produced: 285,000
  - Defect rate: 1.8% (trending down from 2.1% last week)
  - Downtime: 72 min (OEE impact: -1.2%)
  - Main downtime cause: Filter jam (35 min), Changeover (25 min), PM (12 min)

- **Trend Charts:**
  - Defect rate by category (printing, weight, count) - last 7 days
  - Downtime duration vs. cause - last 30 days
  - OEE breakdown (availability, performance, quality) - last 12 weeks

- **Predictive Alerts:**
  - Rolling machine vibration trending up → PM recommended within 168 hours
  - Filter supplier performance: 2 lots rejected in last 10 days → review with supplier

#### **Executive Dashboard (C-Suite, Weekly Scorecard)**
- **KPI Highlights:**
  - OEE: 85.4% (target: 85%, ✓ on track)
  - Production rate: 92% of plan (slight underrun due to changeover optimization test)
  - Quality: 1.8% defect rate (target: <2%, ✓ passing)
  - Unplanned downtime: 2.4 hours (18% reduction vs. prior month)

- **ROI Tracking:**
  - Digital Twin adoption: Week 4 of POC
  - Bottleneck identified: rolling machine confirmed
  - Projected annual benefit: €180k (downtime reduction) + €45k (energy) = €225k
  - Payback period: 4.5 years (based on €1M POC + full-scale deployment cost)

- **Compliance Status:**
  - GxP audit: 0 open findings (full audit trail logged)
  - Traceability: 100% of lots linked to raw material
  - Serialization: 99.8% barcode legibility (target: >99%)

### 9.3 Alert & Notification System

**Severity Levels:**
- **Critical:** Equipment failure, safety hazard, GxP violation → SMS + email to manager + plant engineer
- **Warning:** Threshold exceeded, PM due soon → email to operator + supervisor
- **Info:** Status changes, routine events → log entry, visible in dashboard only

**Example Alert Configuration:**
```
Alert: "Rolling Motor Vibration"
Condition: RMS vibration > 3.5g for 60 seconds
Severity: Warning
Notify: Operator (mobile), Plant Manager (email)
Auto-Action: Reduce line speed to 75%, schedule PM work order
Escalate: If vibration > 4.5g → Critical, call maintenance ASAP
```

---

## 10. STANDARDS, CONSTRAINTS & COMPLIANCE

### 10.1 GxP Compliance (Good Manufacturing Practice)

**FDA 21 CFR Part 11 (Electronic Records):**
- All production records maintained in validated system (digital twin + MES)
- Audit trail: WHO changed WHAT, WHEN, WHY (non-repudiable, timestamped)
- Digital signatures: required for lot release, deviation approvals
- Data integrity: secure hashing, tamper detection

**Data Retention:**
- Production records: 7 years minimum (longer in some markets)
- Deviation logs: lifetime + 10 years
- Calibration records (sensors): 2 years post-retirement
- Validation protocols: 7 years

### 10.2 ISO & International Standards

| Standard | Application | Requirement |
|----------|-------------|------------|
| **ISO 13849-1** | Safety-related control systems | Risk assessment, FMEA, proof test intervals |
| **ISO 50001** | Energy management | Energy baseline, improvement targets, audit trail |
| **ISO 22000** | Food Safety Mgmt (applies to tobacco) | Hazard analysis, critical control points, traceability |
| **IEC 62304** | Medical device software (if vape claims medicinal) | V&V, risk mgmt, change control |
| **NIST Cybersecurity Framework** | Data protection | ID, Protect, Detect, Respond, Recover |

### 10.3 ESG & Sustainability Constraints

**Environmental Reporting:**
- Energy consumption tracked per unit (kWh/pack)
- Water usage (if wet scrubbers for air quality) tracked (l/pack)
- Waste & scrap (kg/pack) monitored for circular economy reporting
- Carbon footprint calculation: direct emissions (site) + indirect (supply chain)

**Social Compliance:**
- Worker safety: no anomalies in air quality, noise, ergonomics during shifts
- Data privacy: operator names logged only for audit trail (privacy-by-design)

**Governance:**
- Compliance status visible in executive dashboards
- Automated deviation alerts for ESG thresholds
- Annual certification readiness (ISO 50001, sustainability reporting)

### 10.4 Cybersecurity Controls

**Network Segmentation:**
- **DMZ (Demilitarized Zone):** Edge gateway
- **Manufacturing Network:** PLCs, SCADA, sensors (isolated VLAN, no direct internet)
- **Cloud Connection:** VPN tunnel (IPSec or AWS Direct Connect for Azure)
- **IT Network:** Office PCs, email (separate from plant floor)

**Access Control (RBAC):**
- **Operator Role:** View real-time dashboards, acknowledge alarms, manual speed adjustment (read-most, write-limited)
- **Supervisor Role:** Lot release, deviation approvals, trend analysis
- **Engineer Role:** Configure alerts, change SPC limits, schedule PM
- **Admin Role:** System configuration, user management, backup/restore
- **Audit Role:** Read-only access to all records for compliance review

**Device Identity & Authentication:**
- Each IoT sensor, edge gateway, cloud connection uses X.509 certificate (not shared passwords)
- Certificate rotation every 12 months
- Revocation process: blacklist certificate within 24 hours of compromise

**Data Encryption:**
- **In Transit:** TLS 1.3 (MQTT over port 8883, REST over HTTPS)
- **At Rest:** AES-256 encryption for historian data in cloud storage
- **Keys:** Azure Key Vault or AWS Secrets Manager (centralized, audited rotation)

---

## 11. INTEGRATION ARCHITECTURE

### 11.1 Edge Gateway Configuration (Detailed)

**Hardware:**
- Industrial PC (e.g., Beckhoff CX-series, or standard hardened x86)
- Processor: Intel i7 or equivalent (multi-core for real-time buffering)
- RAM: 16 GB
- Storage: 256 GB SSD + 2TB external drive (local historian buffer, offline resilience)
- Network: Dual Ethernet (one for plant, one for cloud/VPN)

**Operating System:**
- Windows 10 IoT Enterprise OR Linux (Ubuntu 22.04 LTS hardened)
- Real-time kernel optional (if deterministic buffering required)

**Software Stack:**
```
Layer 1: Protocol Handlers
├─ OPC-UA Client (Python: pyopc, or C#: OPC Foundation SDK)
├─ MQTT Client (Python: paho-mqtt, or C#: MQTTnet)
├─ Modbus TCP Client (Python: pymodbus)
├─ REST Client (Python: requests)
└─ Database Client (ODBC/JDBC for historian queries)

Layer 2: Data Processing & Buffering
├─ Time-series aggregation (1-min rolling averages)
├─ Anomaly detection (Z-score, isolation forest for outliers)
├─ Unit conversion (raw sensor → engineering units)
├─ Data validation (range checks, delta validation)
└─ Local disk buffer (queue if cloud connection lost)

Layer 3: Cloud Connectivity
├─ MQTT Publisher (edge → Azure IoT Hub or event stream)
├─ REST API Client (batch telemetry upload)
├─ VPN Client (IPSec tunnel establishment)
└─ Connection health monitor (reconnect logic)

Layer 4: Logging & Audit
├─ Event logger (INFO, WARN, ERROR to local file)
├─ Audit trail (who/what/when/why for config changes)
└─ Certificate rotation agent (check expiry monthly, rotate 30 days prior)
```

**Configuration Example (YAML):**
```yaml
data_sources:
  - name: "Rolling_Machine_PLC"
    protocol: "opc-ua"
    endpoint: "opc.tcp://192.168.1.10:4840"
    poll_interval_ms: 1000
    tags:
      - name: "rod_weight"
        node_id: "ns=2;i=1001"
        unit: "grams"
        min: 0.5
        max: 2.0

  - name: "IoT_Sensors_MQTT"
    protocol: "mqtt"
    broker: "192.168.1.20"
    port: 8883
    tls_ca: "/etc/certs/mqtt-ca.crt"
    topics:
      - "sensors/temperature/leaf_dryer"
      - "sensors/humidity/leaf_dryer"
      - "sensors/vibration/rolling_motor"

cloud_export:
  protocol: "mqtt"
  endpoint: "my-iot-hub.azure-devices.net"
  connection_string: "${AZURE_IOT_HUB_KEY}"
  buffer_path: "/var/data/buffer"
  buffer_max_gb: 100
  batch_size: 1000
  flush_interval_sec: 60

validation_rules:
  - tag: "rod_weight"
    check: "delta_max_10pct"  # fail if change >10% in 1 interval
    severity: "warning"
```

### 11.2 Cloud Platform Stack (Azure Option)

#### **Data Ingestion Tier:**
- **Azure IoT Hub** (or Event Hubs)
  - MQTT endpoint: `{hub-name}.azure-devices.net:8883`
  - Authentication: X.509 cert or shared key (cert preferred)
  - Message format: JSON payload with metadata

#### **Real-time Processing:**
- **Azure Stream Analytics** (or Azure Functions)
  - Input: IoT Hub stream
  - Transformation: enrich with GPS, add OEE calculations
  - Output: Power BI dataset (real-time), Azure Data Lake (batch)

#### **Data Storage:**
- **Azure Data Lake Storage Gen 2** (ADLS)
  - Raw ingestion: `/raw/telemetry/{device}/{YYYY}/{MM}/{DD}/{HH}/`
  - Processed layer: `/processed/kpis/{line}/{YYYY-MM-DD}`
  - Historian: `/historian/timeseries/{tag}/{YYYY}/{MM}/{DD}`

#### **Digital Twins & Simulation:**
- **Azure Digital Twins** (optional, for advanced scenarios)
  - Model: DTDL (Digital Twins Definition Language) for equipment/process
  - Twin graph: relationships between rolling machine → packing machine → line
  - Telemetry endpoints: ingest time-series, query state
  - Routes: model changes → Event Hub → notifications

#### **Analytics & Visualization:**
- **Azure Synapse Analytics** (formerly SQL Data Warehouse)
  - SQL pool: historical queries (slow, cost-effective for batch)
  - Spark pool: ML model training (defect prediction, maintenance scheduling)
  
- **Power BI**
  - Real-time dashboards (connected to Stream Analytics dataset)
  - Paginated reports (daily PDF for GxP records)
  - Q&A (executive natural-language queries: "What was OEE last Tuesday?")

#### **Machine Learning:**
- **Azure Machine Learning (AML)**
  - Training data: 6-month historian of vibration + maintenance labels
  - Model: time-series anomaly detection (Isolation Forest, Autoencoders)
  - Deployment: real-time scoring in Stream Analytics
  - Retraining: monthly (scheduled pipeline)

#### **Security & Compliance:**
- **Azure Key Vault**
  - Secrets: IoT Hub connection strings, API keys
  - Certificates: auto-rotation, audit logging
  
- **Azure Policy**
  - Enforce encryption at rest, network isolation, RBAC rules
  
- **Azure Audit & Compliance**
  - Activity logs: all API calls, deletions, modifications
  - Compliance dashboard: GxP readiness, SOC 2 Type II status

### 11.3 Data Flow Diagram

```
Plant Floor (Real-time)
    ↓
┌─────────────────────────────────────┐
│ Edge Gateway (Local Processing)     │
│ ├─ OPC-UA Client (PLC, SCADA)      │
│ ├─ MQTT Subscription (sensors)      │
│ ├─ Buffering & Validation           │
│ └─ Offline Resilience               │
└─────────────────────────────────────┘
    ↓ (MQTT over VPN/TLS)
┌─────────────────────────────────────┐
│ Azure IoT Hub (Cloud Gateway)       │
│ ├─ Device identity & auth           │
│ ├─ Message deduplication            │
│ └─ Device-to-Cloud (D2C) routing    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Stream Analytics (Real-time Compute)│
│ ├─ OEE calculation (Availability,   │
│ │   Performance, Quality aggregates) │
│ ├─ Anomaly detection triggers       │
│ └─ Data enrichment (context added)  │
└─────────────────────────────────────┘
    ↓ (split output)
    ├─ Power BI (Real-time dataset)
    ├─ Event Hub (alert notifications)
    ├─ Azure Digital Twins (state update)
    └─ ADLS (raw data lake)
    
    (Batch Processing - Daily)
    ↓
┌─────────────────────────────────────┐
│ Azure Synapse (SQL + Spark)         │
│ ├─ Data transformation (wide table) │
│ ├─ ML model scoring                 │
│ └─ Report generation                │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Power BI / Grafana (Visualization)  │
│ ├─ Dashboards (operator, mgmt, exec)│
│ ├─ Reports (compliance, trend)      │
│ └─ Alerts (notifications)           │
└─────────────────────────────────────┘

(Feedback Loop)
    ←─────────────────────────────────
        Simulation parameters
        SPC limit updates
        Maintenance scheduling
```

---

## 12. ANALYTICS LAYER & KPI CALCULATIONS

### 12.1 Overall Equipment Effectiveness (OEE)

**Formula:**
```
OEE = Availability × Performance × Quality

Availability = Actual Runtime / Planned Production Time
            = (Planned Time - Downtime) / Planned Time

Performance = (Ideal Cycle Time × Total Count) / Actual Runtime
            = (7500 packs/hr / Actual Rate) × 100%

Quality = Good Count / Total Count
        = (Total - Defects) / Total × 100%
```

**Calculation Example (1-hour shift):**
- Planned time: 60 min
- Downtime: 4 min (jam), 2 min (changeover) = 6 min → **Availability = 54/60 = 90%**
- Ideal rate: 7,500 packs/hr (125 packs/min)
- Actual: 108 packs/min → **Performance = (125/108) × 100 = 115.7%** (overspeed, unlikely but possible in simulation)
- Actual: 7,000 total packs, 100 defects → **Quality = (7,000 - 100) / 7,000 = 98.6%**
- **OEE = 90% × 99% × 98.6% = 87.4%**

**Trend Reporting:**
- Real-time: Updated every 1 minute (rolling aggregate)
- Hourly summary: Aggregated to hour (published at :00)
- Daily summary: Average of all hourly OEE values
- Weekly summary: Average of all daily OEE values

### 12.2 Anomaly Detection Algorithm

**Method: Isolation Forest (unsupervised, no training labels needed)**

**Input Features (per 5-min window):**
1. Vibration RMS (rolling motor)
2. Motor current (amps)
3. Temperature (leaf dryer)
4. Defect rate (%) - 5-min rolling
5. Downtime events (count)

**Model Training:**
- Use 6 months of historical data (clean operation, no anomalies labeled)
- Isolation Forest learns normal operating envelope (no classes required)
- Anomaly score: 0.0–1.0 (0 = normal, 1 = extreme outlier)

**Scoring Logic (per 5-min window):**
```
anomaly_score = isolation_forest.score(feature_vector)

if anomaly_score > 0.7:
  severity = "Critical"
  alert_message = "Equipment behavior outside normal range"
  notify = [operator, plant_manager]
elif anomaly_score > 0.5:
  severity = "Warning"
  alert_message = "Subtle change in equipment behavior"
  notify = [operator]
else:
  severity = "None"
  action = "Log only, no alert"
```

**Example Alert Generated:**
```
Alert Timestamp: 2026-01-08 14:23:45
Alert ID: ANOMALY-20250108-142345
Equipment: Rolling Motor
Anomaly Score: 0.81 (Critical threshold: 0.70)
Deviation Description:
  - Vibration RMS: 3.8g (normal: 2.1g, +81%)
  - Motor Current: 45A (normal: 38A, +18%)
  - Combined pattern: unusual, suggests blade wear + bearing friction
Recommended Action: Schedule immediate inspection of rolling machine motor
Priority: High
Action Items:
  - [Operator] Visually inspect motor bearing for overheating
  - [Maintenance] Check vibration trend for next 2 hours
  - [Engineer] If trend continues upward, PM work order to replace bearing
```

### 12.3 Predictive Maintenance Score

**Goal:** Predict equipment failure probability in next 7 days.

**Method: Gradient Boosted Model (trained on failure history)**

**Training Data Preparation:**
```
Historical Input:
- Date, vibration (daily avg, daily max, trend slope)
- Motor current (daily avg, daily max)
- Temperature (daily avg)
- Product type (impacts wear rate)
- Time since last PM

Label:
- Days until failure (if failed within 30 days)
- Censored (if no failure observed, mark as >30 days)
```

**Model Output:**
```
PM_Score = Probability(failure within 7 days) × 100%
         (0–100%, with confidence interval)

Score Ranges:
- PM_Score < 5%: Normal operation, routine PM only
- PM_Score 5–20%: Increased wear, monitor daily, schedule PM in 2–3 weeks
- PM_Score 20–50%: High wear, PM within 1 week
- PM_Score > 50%: Imminent failure, PM within 48 hours or reduce operating speed
```

**Example Report (rolling machine):**
```
Asset: Rolling Machine Motor
Today's PM Score: 34%
7-Day Failure Probability: 34% (confidence: 92%)
Recommendation: Schedule PM within 7 days

Trend (last 30 days):
Day 1:  PM_Score = 8%
Day 5:  PM_Score = 12%
Day 10: PM_Score = 18%
Day 15: PM_Score = 23%
Day 20: PM_Score = 29%
Day 25: PM_Score = 34%  ← Current

Slope: +0.52% per day (trend: increasing risk)

Key Drivers of High Score:
1. Vibration RMS up 45% vs. 30-day baseline
2. Motor current up 22% vs. baseline
3. Temperature elevated by 8°C vs. normal
4. Days since last PM: 127 days (PM interval: 180 days, but wear accelerating)

Action: Order replacement bearing (2-day lead time), schedule PM for 2026-01-11
```

### 12.4 What-If Simulation Queries

**Example 1: "What if we run the line 10% faster?"**

**Inputs:**
- Base speed: 125 packs/min → Target speed: 137.5 packs/min (+10%)
- Increased throughput: +2,500 packs/8hr shift → +€1,250 revenue/shift
- Risk: Higher vibration, faster wear, increased defect rate

**Simulation:**
```
Assume: Wear accelerates with speed^1.5 (empirical model)
Current vibration (125 packs/min): 2.1g RMS
Predicted vibration (137.5 packs/min): 2.1 × (1.10)^1.5 = 2.35g RMS (+12%)

Current defect rate (125 packs/min): 1.2%
Predicted defect rate (137.5 packs/min): 1.2 × 1.08 = 1.3% (+0.1pp, slight)

Current MTBF rolling motor: 1,800 hours
Predicted MTBF: 1,800 / (1.10)^0.5 = 1,714 hours (−5% life)

ROI Calculation (annualized):
Revenue gain: 2,500 packs/shift × 5 shifts/week × 50 weeks/year × €0.50/pack = €312.5k
Cost of earlier bearing replacement: 1 bearing/year @€1,500 = €1,500
Defect loss (scrap): 300 extra scrap packs/year × €0.50 = €150
Net annual benefit: €312,500 − €1,500 − €150 = €310,850

Recommendation: Increase speed; benefit outweighs wear cost (98% ROI confidence).
```

**Example 2: "What if we reduce changeover time from 45 to 30 min?"**

**Inputs:**
- Current changeover time: 45 min per changeover (8 changeovers/day)
- Proposed process: parallel hopper cleaning, quick-change filters, pre-staged parameters
- Lost production during changeover: 125 packs/min × 45 min = 5,625 packs
- New lost production: 125 × 30 min = 3,750 packs
- Gain per changeover: 1,875 packs × €0.50 = €937.50

**Annual Benefit:**
- 5 days/week × 50 weeks/year × 8 changeovers/day = 2,000 changeovers/year
- Gain per changeover: €937.50
- Total annual benefit: €1,875,000
- Investment: Process redesign + staff training: €50,000
- Payback: <2 weeks

**Recommendation:** Invest in changeover optimization; immediate high-ROI project.

---

## 13. DIGITAL TWIN TYPE CLASSIFICATION

| Type | Definition | POC Scope | Value |
|------|-----------|-----------|-------|
| **Descriptive Twin** | Mirrors current physical state in real-time (dashboards, alerts) | ✓ Primary focus | Enable situational awareness, anomaly detection |
| **Predictive Twin** | Forecasts future state (wear, failure, quality) based on ML models | ✓ Phase 1 | Maintenance scheduling, process optimization |
| **Prescriptive Twin** | Recommends actions and optimizes control parameters (auto-tune line speed, suggest changeover sequence) | Partial (Phase 2) | Autonomous production planning, recipe optimization |

**POC Delivers:** Descriptive + early Predictive capabilities. Prescriptive moves to Phase 2+ with regulatory validation.

---

## 14. PLATFORM & TECHNOLOGY SELECTION

### 14.1 Recommended Stack for POC

#### **Option A: Azure-Centric (Microsoft Stack)**

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Cloud Platform** | Azure (IoT Hub, Digital Twins, Synapse) | GxP validation support, HIPAA/compliance certified, strong pharma/tobacco case studies |
| **Edge Gateway** | Windows IoT Enterprise + Node-RED or Python | Proven OPC-UA support, familiar to Siemens/Rockwell users |
| **Real-time Compute** | Stream Analytics or Spark Streaming | SQL-like syntax, low ops overhead |
| **Data Lake** | ADLS Gen 2 + Synapse SQL | Native Azure, cost-effective, RBAC integrated |
| **Analytics** | Power BI + AML (AutoML for anomaly detection) | Tight integration, rapid dashboard development |
| **3D Visualization** | Azure Digital Twins + Three.js (web) | Semantic model + interactive rendering |
| **Messaging** | Azure Service Bus (AMQP) or Event Hub (MQTT) | Guaranteed delivery, dead-letter queues (GxP requirement) |

**Estimated Cost (1-year pilot):**
- Azure resources: €400–500k (compute, storage, analytics)
- Implementation services: €250–350k
- **Total: €650–850k**

#### **Option B: AWS IoT-Centric (AWS Stack)**

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Cloud Platform** | AWS (IoT Core, IoT SiteWise, TwinMaker) | AWS IoT TwinMaker specifically designed for manufacturing twins; cost-competitive |
| **Edge Gateway** | AWS IoT Greengrass + local Lambda functions | Offline capability, MQTT native, auto-sync to cloud |
| **Real-time Compute** | Kinesis Data Streams + Lambda | Low latency, serverless scaling |
| **Data Lake** | S3 + Glue (ETL) + Athena (SQL queries) | S3 cost-effective, Glue catalog simplifies schema management |
| **Analytics** | QuickSight + SageMaker (ML models) | QuickSight less feature-rich than Power BI but sufficient; SageMaker strong for defect detection |
| **3D Visualization** | AWS IoT TwinMaker (native 3D viewer) + custom web app | Integrated twin and visualization; faster time-to-value |
| **Messaging** | MQTT native (AWS IoT Core) | MQTT broker built-in, no separate service needed |

**Estimated Cost (1-year pilot):**
- AWS resources: €350–450k (IoT Core, TwinMaker, Kinesis, Sagemaker, storage)
- Implementation services: €200–300k
- **Total: €550–750k**

#### **Option C: Hybrid Multi-Cloud (Recommended for Risk Mitigation)**

**Rationale:** Avoid single-vendor lock-in; leverage best-of-breed tools.

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Edge Gateway** | Siemens MindSphere Agent OR Apache NiFi | OPC-UA native (MindSphere), cloud-agnostic (NiFi) |
| **Cloud Platform** | Azure + AWS (both fed from edge) | Multi-cloud hedge; failover capability |
| **Data Lake** | MinIO (on-prem) + S3 + ADLS (cloud) | Open-source, cost-controlled, avoids vendor lock-in |
| **Real-time Compute** | Apache Kafka + Spark (on-prem edge) + cloud analytics | Kafka proven in tobacco/pharma, Spark portable |
| **Visualization** | Grafana (open-source) + Power BI (enterprise) | Grafana agile, Power BI for exec reports; dual-stack |
| **ML/Analytics** | MLflow (model registry) + open-source libraries (scikit-learn, XGBoost) | Reproducible, vendor-neutral |

**Estimated Cost (1-year pilot):**
- On-premises infrastructure (edge, historian): €100–150k (capex)
- Cloud resources (shared between Azure/AWS): €250–350k (opex)
- Implementation services: €300–400k
- **Total: €650–900k** (similar to single-cloud, but with risk mitigation)

**POC Recommendation:** **Option A (Azure) for speed-to-market**, OR **Option C (Hybrid) for long-term flexibility**. Option B (AWS) equally viable if organization has AWS standardization.

---

## 15. DATA MODEL & ASSET HIERARCHY

### 15.1 Entity Relationship Diagram (Simplified)

```
Manufacturing Facility
├─ Production Line (1 digital twin for POC)
│  ├─ Equipment (Rolling Machine, Packing Machine, etc.)
│  │  ├─ Sensors (temperature, vibration, weight, etc.)
│  │  ├─ Maintenance History (PM records, failures, replacements)
│  │  └─ Configuration (setpoints, alert thresholds, recipes)
│  ├─ Downtime Events (recorded per shift)
│  │  ├─ Event Type (jam, motor fault, changeover, PM)
│  │  ├─ Duration (minutes)
│  │  ├─ Root Cause (if known)
│  │  └─ Resolution (action taken)
│  └─ Production Batches (lots tracked)
│     ├─ Raw Material (leaf lot, filter lot, wrapper lot)
│     ├─ Product Output (pack count, defect count, scrap)
│     ├─ Quality Results (lab test, vision inspection)
│     └─ Traceability (serialized packs → cartons → pallets)
├─ Warehouse / Logistics
│  ├─ Raw Material Inventory (incoming QC, storage)
│  ├─ WIP Buffer (packs awaiting cartonization)
│  └─ Finished Goods Staging (pallets awaiting shipment)
└─ Utilities
   ├─ Compressed Air System (main supply, pressure, flow)
   ├─ Electrical Distribution (main feed, sub-panels)
   └─ Waste / Scrap Management (scrap accumulation, disposal)
```

### 15.2 Time-Series Data Schema (ADLS/Data Lake)

```json
{
  "timestamp": "2026-01-08T14:23:45.123Z",
  "device_id": "rolling-motor-01",
  "device_type": "electric_motor",
  "equipment_name": "Rolling Machine Primary Motor",
  "facility_id": "PMI-SOFIA-01",
  "line_id": "LINE-001",
  "telemetry": {
    "vibration_rms_g": 2.15,
    "vibration_peak_g": 4.32,
    "vibration_frequency_hz": 47.8,
    "motor_current_amps": 38.5,
    "motor_voltage_volts": 460.0,
    "motor_temp_celsius": 65.2,
    "bearing_temp_celsius": 62.1
  },
  "metadata": {
    "batch_id": "LOT-20250108-001",
    "product_type": "cigarette_regular",
    "line_speed_pct": 98,
    "hours_since_last_pm": 127
  },
  "calculated_kpis": {
    "power_kw": 13.8,
    "anomaly_score": 0.23,
    "failure_prob_7day_pct": 12
  },
  "data_quality": {
    "completeness": 1.0,
    "validity": "pass",
    "timeliness_ms": 245
  }
}
```

### 15.3 Batch/Lot Master Data (Transactional)

```json
{
  "lot_id": "LOT-20250108-001",
  "facility": "PMI-SOFIA-01",
  "line": "LINE-001",
  "product_code": "CIG-REG-20PC",
  "product_description": "Cigarette Regular 20pc Pack",
  "planned_start": "2026-01-08T06:00:00Z",
  "actual_start": "2026-01-08T06:05:00Z",
  "actual_end": "2026-01-08T14:35:00Z",
  "planned_duration_hours": 8.5,
  "actual_duration_hours": 8.5,
  "raw_materials": {
    "leaf_lot": "LEAF-20250107-003",
    "filter_lot": "FILTER-20250106-102",
    "wrapper_lot": "WRAPPER-20250107-048"
  },
  "production_summary": {
    "total_packs_produced": 128000,
    "total_packs_defective": 2048,
    "defect_rate_pct": 1.6,
    "scrap_weight_kg": 125.4,
    "energy_kwh": 1152
  },
  "quality_results": {
    "qa_sample_size": 300,
    "qa_failed_count": 5,
    "lab_moisture_pct": 12.1,
    "lab_result_status": "PASS",
    "qa_approved_by": "QA-SUSP-0012",
    "qa_approval_timestamp": "2026-01-08T15:30:00Z"
  },
  "compliance": {
    "gxp_audit_trail_complete": true,
    "serialization_complete": true,
    "traceability_verified": true,
    "deviation_count": 0
  }
}
```

---

## 16. POC SUCCESS CRITERIA & VALIDATION

### 16.1 Acceptance Criteria

| Criterion | Target | Threshold | Measurement |
|-----------|--------|-----------|-------------|
| **Data Completeness** | >99% of expected telemetry points received hourly | >98% | Missing data ratio per device per hour |
| **Data Latency** | <5 seconds (edge to cloud) | <10 sec | Timestamp delta analysis |
| **System Uptime** | 99.5% (pilot line only) | >99% | Monitored by cloud health checks |
| **Anomaly Detection Precision** | >80% of alerts are actionable | >70% | Manual review of alert logs |
| **Model Accuracy (Predictive)** | RMSE < 2 hours for maintenance prediction | < 4 hours | Backtest against 6-month historical |
| **OEE Baseline Established** | Measure existing OEE accurately (within ±2%) | ±3% | Compare manual counts vs. system |
| **GxP Audit Trail** | 100% of lots traceable, audit trail complete | 100% | Audit of 50 random lots |
| **3D Visualization Load Time** | <3 seconds to render full line | <5 sec | Browser-based latency test |
| **Dashboard Responsiveness** | <2 sec to update KPI cards after telemetry ingestion | <3 sec | Waterfall timing in Power BI |
| **User Adoption** | >80% of operators use system daily for alerts | >70% | Login analytics, feature usage |

### 16.2 Model Fidelity Thresholds

**Descriptive Twin Accuracy:**
- Current line state (running/stopped, product type, speed) → **100% match** vs. physical line
- Equipment health indicators (vibration, temperature) → **±5%** vs. calibrated instruments
- Downtime events → **100% detection** of events >2 minutes duration

**Predictive Model Validation:**
- Anomaly detection: **>85% sensitivity** (catch true anomalies), **<10% false positive rate** (avoid nuisance alerts)
- Failure prediction: **>70% of predicted failures** occur within 7 days (not perfect, acceptable for maintenance scheduling)
- Quality prediction: **±2% accuracy** on defect rate forecast (1-hour ahead)

### 16.3 Comparison vs. Real Production Data

**Monthly Reconciliation Process:**
1. **Export monthly production summary** from MES (ground truth):
   - Total packs produced, defects, downtime hours
2. **Extract same metrics from Digital Twin** (from data lake)
3. **Compare & calculate variance:**
   - Target: <1% variance on production count
   - Target: <5% variance on downtime hours (time classification may differ slightly)
4. **Investigate discrepancies:**
   - Data quality issues (missing sensors)
   - Model calculation errors
   - Edge case handling (rapid changeovers)
5. **Document findings** in validation log (GxP requirement)

**Example Reconciliation (January 2026):**
```
Metric                  MES Actual    DT Calculated   Variance    Status
─────────────────────────────────────────────────────────────────────────
Total Packs            1,280,000      1,279,500      −0.04%      ✓ PASS
Defective Packs           19,200        19,300      +0.52%      ✓ PASS
Downtime Hours (Total)       20.5         20.8      +1.5%       ✓ PASS
  - Jam Events                 8.2          8.1      −1.2%       ✓ PASS
  - Changeover Events         10.2         10.5      +2.9%       ✓ PASS (expected variance)
  - PM Events                  2.1          2.2      +4.8%       ✓ PASS
OEE %                       85.2%        84.9%      −0.3pp      ✓ PASS (±2% target)

Conclusion: All metrics within tolerance. Model fidelity validated.
```

---

## 17. INTEGRATION PATTERNS & PROTOCOLS

### 17.1 Protocol Deep-Dive

#### **OPC-UA (OLE for Process Control – Unified Architecture)**

**Use Case:** Legacy PLC communication, deterministic real-time requirements

**Characteristics:**
- Client-server model (edge gateway = client, PLC = server)
- Subscribe/publish model (reduces polling overhead)
- Structured data types (security credentials, timestamp, status code per value)
- Binary encoding (compact, efficient)
- TLS security built-in

**Example OPC-UA Read/Subscribe (pseudo-code):**
```python
client = OPC_Client("opc.tcp://192.168.1.10:4840")
client.connect()

# Subscribe to rod weight (real-time)
sub = client.subscribe()
node = client.get_node("ns=2;i=1001")  # Rod weight node ID
sub.subscribe_data_change(node, callback=on_rod_weight_change)

def on_rod_weight_change(node, val):
    print(f"Rod weight: {val.value} grams @ {val.timestamp}")
    # Store to buffer, validate, send to cloud

client.disconnect()
```

#### **MQTT (Message Queuing Telemetry Transport)**

**Use Case:** IoT sensors, lightweight, publish-subscribe

**Characteristics:**
- Publish-subscribe decouples sensors from subscribers
- QoS 0 (fire-forget), QoS 1 (at-least-once delivery)
- Topic hierarchy (e.g., `sensors/rolling-motor/vibration`)
- Small message size (ideal for battery-powered sensors)
- TLS security, client certificate authentication

**Example MQTT Publish (pseudo-code):**
```python
import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.tls_set(ca_certs="mqtt-ca.crt",
               certfile="device.crt",
               keyfile="device.key",
               tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)

client.connect("192.168.1.20", 8883)

payload = {
    "timestamp": "2026-01-08T14:23:45Z",
    "device_id": "vibration-01",
    "vibration_g": 2.15,
    "temperature_c": 65.2
}

client.publish(
    topic="manufacturing/rolling-motor/telemetry",
    payload=json.dumps(payload),
    qos=1
)
```

#### **REST APIs (RESTful Web Services)**

**Use Case:** Batch data export from MES, historian queries, async operations

**Characteristics:**
- HTTP/HTTPS, stateless
- JSON payloads (human-readable, schema-flexible)
- Standard verbs (GET, POST, PUT, DELETE)
- Slower than OPC-UA for real-time (polling-based typically)

**Example REST Batch Export:**
```bash
# MES query: Get all production orders for line 001 on 2026-01-08
curl -X POST https://mes-api.company.local/api/v1/orders/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "line_id": "LINE-001",
    "date": "2026-01-08",
    "limit": 100
  }'

# Response:
{
  "data": [
    {
      "order_id": "ORD-20250108-001",
      "lot_id": "LOT-20250108-001",
      "product_code": "CIG-REG-20PC",
      "scheduled_start": "2026-01-08T06:00:00Z",
      "scheduled_end": "2026-01-08T14:30:00Z"
    }
  ],
  "total": 8,
  "status": "success"
}
```

### 17.2 Message Bus / Event Streaming

**Recommended:** Apache Kafka (on-prem) or Azure Event Hubs / AWS Kinesis (cloud)

**Why:** Decouple producers (edge, sensors) from consumers (analytics, alerts, visualization)

**Example Kafka Architecture (Hybrid Option):**
```
Sensors → MQTT Broker → Edge App (MQTT consumer) → Kafka Producer
                                                        ↓
                                     Kafka Topics (partitioned by equipment)
                                        ├─ topic: rolling-motor-telemetry
                                        ├─ topic: packing-machine-telemetry
                                        └─ topic: quality-events
                                        ↓
                                   Kafka Consumers
                                        ├─ Stream Processor (anomaly detection)
                                        ├─ Data Lake Writer (ADLS sink connector)
                                        ├─ Alert Notifier
                                        └─ Historian (time-series DB)
```

**Benefits:**
- **Decoupling:** New consumers (e.g., ML model) can subscribe without modifying producers
- **Replay:** Reprocess historical data for model retraining
- **Scalability:** Partitions allow parallel consumption
- **Durability:** Broker persists messages (configurable retention)

---

## 18. SECURITY ARCHITECTURE

### 18.1 Network Segmentation

```
┌────────────────────────────────────────────────────────────┐
│ Internet (Public)                                          │
└─────────────────────────┬──────────────────────────────────┘
                          │ (VPN Tunnel - IPSec or TLS)
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ DMZ (Demilitarized Zone)                                    │
│ ├─ VPN Gateway / Bastion Host                             │
│ └─ Edge Gateway (cloud connectivity only)                 │
└──┬────────────────────────────────────────────────────────┘
   │ (Firewall: Port 4840 OPC-UA, 8883 MQTT)
   ↓
┌─────────────────────────────────────────────────────────────┐
│ Manufacturing Network (Isolated VLAN)                       │
│ ├─ PLC / SCADA                                             │
│ ├─ Historian Server                                        │
│ ├─ MES Application Server                                  │
│ └─ Local Historian / Buffering                             │
│                                                             │
│ Access Control:                                             │
│ - No direct internet access (outbound via VPN only)       │
│ - No SSH/RDP from manufacturing to office IT             │
│ - Firewall rules: whitelist only required ports            │
└─────────────────────────────────────────────────────────────┘
```

### 18.2 Device Identity & X.509 Certificates

**Certificate Lifecycle:**
1. **Generation:** Manufacturer issues certificate to edge gateway + each IoT device
   - Common Name (CN): device-id (e.g., "rolling-motor-01")
   - Issuer: Company CA (internal or public)
   - Validity: 1 year
   - Key usage: Digital signature, TLS client auth

2. **Distribution:** Secure provisioning
   - Pre-load into device firmware (factory)
   - OR hardware security module (HSM) with secure boot
   - Never transmitted in plaintext

3. **Validation:** Cloud-side certificate pinning
   - Azure IoT Hub / AWS IoT Core maintains device CA cert
   - Validates each device certificate against CA
   - Revokes if tampered/compromised

4. **Rotation:** 12 months or on compromise
   - Automated reminder 30 days before expiry
   - Generate new cert, deploy via secure channel
   - Retire old cert (30-day grace period)

**Example Certificate (openssl output):**
```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 1001 (0x3e9)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=GR, ST=Attica, L=Kifisia, O=PMI, CN=PMI-Root-CA
        Subject: C=GR, O=PMI, CN=rolling-motor-01
        Not Before: Jan 1 00:00:00 2026 GMT
        Not After : Jan 1 00:00:00 2027 GMT
        X509v3 Key Usage:
            Digital Signature, TLS Web Client Authentication
        X509v3 Extended Key Usage:
            TLS Web Client Auth
    Signature Algorithm: sha256WithRSAEncryption
```

### 18.3 Role-Based Access Control (RBAC)

**Azure RBAC Example (Power BI, SQL, Storage):**

```
Role                  Permissions
────────────────────────────────────────────────────────────
Operator              - View real-time dashboard (read-only)
                      - Acknowledge alerts, mark resolved
                      - No configuration changes

Supervisor            - All operator permissions
                      - View production history (trends)
                      - Approve lot release (digitally sign)
                      - Schedule PM work orders

Engineer              - All supervisor permissions
                      - Modify alert thresholds
                      - Adjust SPC control limits
                      - Configure new equipment

Admin                 - All permissions
                      - User management
                      - System configuration
                      - Backup/restore operations

Auditor               - Read-only across all data
                      - Audit trail visibility
                      - No write access
                      - 24/7 access

Azure Implementation:
- Operator: "Manufacturing Reader" built-in role
- Supervisor: "Manufacturing Supervisor" custom role (limited write)
- Engineer: "Manufacturing Engineer" custom role
- Admin: "Owner" or "Contributor" role
- Auditor: "Reader" role + "Storage Account Blob Data Reader"
```

---

## 19. VALIDATION PLAN (GxP Required)

### 19.1 Design Qualification (DQ)

**Objective:** Verify system design meets requirements.

**Scope:**
- Requirements traceability matrix (RTM): every requirement → design document → test case
- Risk assessment (FMEA): identify failure modes, mitigation
- Security architecture review: penetration test scoping

**Deliverables:**
- DQ report (signed by QA/IT/Engineering)
- RTM spreadsheet
- FMEA table
- Security audit checklist

**Example DQ Test Case:**

| ID | Requirement | Design Element | DQ Test | Expected Result | Status |
|----|-----------|----|-----|------|--------|
| DQ-001 | OPC-UA connection to PLC shall be encrypted (TLS 1.3) | Edge gateway OpenSSL config, TLS server config on PLC | Capture network traffic, verify encryption, certificate validation | TLS 1.3 cipher suite detected, certificate chain valid | ✓ PASS |
| DQ-002 | Telemetry latency shall be <5 seconds | Stream Analytics processing time, blob storage write latency | Inject test message, measure end-to-end timestamp delta | Latency 2.3 sec (within threshold) | ✓ PASS |
| DQ-003 | Audit trail shall be non-repudiable | Digital signature on lot release using Azure Key Vault | Release a test lot, verify signature, attempt tampering | Tamper detected, signature invalid | ✓ PASS |

### 19.2 Installation Qualification (IQ)

**Objective:** Verify system components installed per specifications.

**Scope:**
- Hardware configurations (CPU, RAM, storage, network)
- Software versions (OS, firmware, library versions)
- Network connectivity & security baselines
- Backup/recovery systems functional

**Deliverables:**
- IQ report with detailed configurations
- Network diagram with IP addressing
- Hardware inventory list
- Backup test results

### 19.3 Operational Qualification (OQ)

**Objective:** Verify system performs intended operations under normal conditions.

**Scope:**
- OPC-UA client connects and subscribes to live PLC data
- MQTT sensors publish telemetry, edge gateway receives
- Cloud ingestion pipeline processes messages within latency SLA
- Dashboards update in real-time
- Alerts trigger and notify operators
- Historical queries execute and return correct data

**Example OQ Test:**

| Test Case | Steps | Expected Result | Actual Result | Status |
|-----------|-------|-----------------|--------|--------|
| **OQ-RT-001: Real-time Telemetry** | 1. Start edge gateway <br> 2. PLC outputs rod weight 0.90g <br> 3. Wait 5 sec <br> 4. Check Power BI dashboard | Rod weight displayed in real-time dashboard within 5 sec, ±0.01g accuracy | Rod weight displayed as 0.90g @ 4.3 sec latency | ✓ PASS |
| **OQ-ALR-001: Anomaly Alert** | 1. Inject vibration value 4.2g (above 3.5g threshold) <br> 2. Wait 10 sec <br> 3. Check alert notifications | Alert "Rolling Motor Vibration High" appears in operator console and email notification sent within 10 sec | Alert appeared @ 7.2 sec, email delivered @ 8.5 sec | ✓ PASS |
| **OQ-HST-001: Historical Query** | 1. Query data lake for rod weight data from yesterday <br> 2. Request 1-hour aggregates | Return 24 rows (1 per hour), each with min/max/avg rod weight | Returned 24 rows, avg weight 0.876g ±0.02g variance from manual checks | ✓ PASS |

### 19.4 Performance Qualification (PQ)

**Objective:** Verify system performs under expected production load (full line throughput, continuous operation).

**Scope:**
- Sustained telemetry ingestion (7,500 packs/min, all sensors)
- Dashboard responsiveness under load
- Data quality metrics maintained
- Anomaly detection accuracy over 4-week continuous run

**Duration:** Minimum 4 weeks continuous operation (capture seasonal/product-mix variations)

**Success Criteria:**
- Data completeness: >99% of expected telemetry received
- System uptime: 99.5% (excluding planned maintenance)
- Dashboard load time: <3 sec 95th percentile
- Anomaly detection false-positive rate: <5%
- Data lake query latency: <2 sec (90th percentile)

---

## 20. RISK MANAGEMENT

### 20.1 Key Risks & Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-----------|
| **Legacy PLC incompatibility with OPC-UA** | POC blocked, unable to ingest plant data | Medium | Early compatibility testing (Week 1), OPC gateway vendor support |
| **Network latency spike (cloud VPN)** | Telemetry delay >10 sec, alerts delayed | Low | Hybrid edge buffer (local historian), VPN traffic QoS prioritization |
| **Data quality issues (missing sensors, noise)** | Model inaccuracy, false alerts | Medium | Data quality monitoring, anomaly detection on sensor values, redundant sensors for critical KPIs |
| **Operator adoption low** | System unused, no ROI realization | Medium | Change management, operator training, gamification (leaderboards), integration into daily workflow |
| **Vendor lock-in (Azure)** | High switching cost if dissatisfied | Medium | Hybrid architecture option, consider multi-cloud from start |
| **GxP non-compliance** | Regulatory audit failure, line shutdown | Low | Validation plan from inception, audit trail non-negotiable, legal review of requirements |
| **Production disruption during deployment** | Line downtime, lost revenue | Low | Pilot line only (not main production), off-shift integration, rollback plan |
| **Cybersecurity breach** | Data theft, operational disruption | Low | Network segmentation, certificate-based auth, regular penetration tests, incident response plan |

### 20.2 Change Management Strategy

**Timeline:**
1. **Month 1:** Requirements workshop with operators, supervisors, engineering
2. **Month 2–4:** System build & validation (minimal plant floor presence)
3. **Month 5:** Soft launch (read-only dashboards, observers)
4. **Month 6:** Operator training, gradual alert activation
5. **Month 6+:** Full deployment, continuous feedback

**Training Plan:**
- **Operators:** 4-hour workshop on dashboard navigation, alert response
- **Supervisors:** 6-hour session on lot release, deviation handling, trend analysis
- **Engineers:** 2-day deep-dive on configuration, troubleshooting, model tuning
- **IT/Security:** 1-day on certificate rotation, backup procedures, incident response

---

## 21. POC SUCCESS CRITERIA SUMMARY

| Deliverable | Success Metric | Target | Status |
|-------------|---|---|------|
| **Data Ingestion** | % uptime, latency | >99% uptime, <5 sec | Baseline: TBD |
| **Real-time Dashboard** | Load time, refresh rate | <3 sec load, 1 Hz refresh | Baseline: TBD |
| **Anomaly Detection** | Precision, recall | >85% precision, <10% false pos rate | Baseline: TBD |
| **Predictive Model** | 7-day failure forecast accuracy | >70% correct predictions | Baseline: TBD |
| **OEE Measurement** | Variance vs. manual counts | <1% on production count | Baseline: 85.2% |
| **GxP Compliance** | Audit trail completeness | 100% of lots traceable | Baseline: TBD |
| **Operator Adoption** | Daily active users | >80% of operators | Baseline: TBD |
| **Business Impact** | Cost savings identified | >€250k annualized benefit | Baseline: TBD |

---

## 22. ROADMAP: POC → PRODUCTION SCALING

### 22.1 Phase 1: POC (Months 1–9, €800k–€1.2M)

**Deliverables:**
- Single production line digital twin (pilot)
- Real-time dashboards (operator, management, executive)
- Anomaly detection + basic predictive maintenance
- GxP validation (DQ, IQ, OQ, PQ)
- Lesson learned document

**Success Gates:**
- OEE measured within ±2% of manual baseline
- Downtime events captured with >95% accuracy
- User adoption >70% (operators engaging daily)
- Regulatory audit finds zero GxP findings

### 22.2 Phase 2: Scale to Plant (Months 10–18, €1.5M–€2.5M)

**Additional Lines:**
- Deploy twin to remaining 3 lines in same facility
- Standardize equipment models, reuse designs
- Consolidate cloud infrastructure (multi-tenant data lake)

**Advanced Analytics:**
- Predictive quality (defect rate forecasting)
- Prescriptive recommendations (auto-tune line speed, suggest changeover sequence)
- Energy optimization AI
- Supply chain integration (link to MES lot master → quality)

**Regulatory Path:**
- Full validation package (DQ, IQ, OQ, PQ) for all 4 lines
- FDA 21 CFR Part 11 certification readiness
- Compliance audit by external auditor

### 22.3 Phase 3: Multi-Site Deployment (Months 19–36, €5M+)

**Scope:**
- Roll out to 3–5 additional tobacco manufacturing facilities (other PMI plants)
- Centralized data lake with federated analytics (global benchmarking)
- Corporate-level dashboards (OEE by plant, by product, by region)

**Advanced Use Cases:**
- Cross-facility demand planning (pull inventory from lowest-cost plant)
- Shared supplier quality insights (filter defects across all plants → supplier feedback)
- Environmental impact reporting (energy, water, scrap by facility)
- Global digital twin (connect production → logistics → retail)

---

## 23. COST-BENEFIT ANALYSIS

### 23.1 POC Investment

| Category | Est. Cost (€K) | Notes |
|----------|---|---|
| **Cloud Platform (1 year)** | 400–500 | Azure IoT Hub, Digital Twins, Synapse, Power BI licenses |
| **Edge Gateway & Sensors** | 80–120 | Industrial PC, OPC-UA licenses, MQTT equipment |
| **Integration & Development** | 250–350 | Systems integrator labor, custom scripts, API development |
| **Training & Validation** | 50–80 | Operator training, GxP validation (DQ, IQ, OQ, PQ) |
| **Contingency (10%)** | 80–105 | Risk buffer |
| **Total POC** | **860–1,155** | **Central estimate: €1,000k** |

### 23.2 Annual Operating Cost (Post-POC, Single Line)

| Item | Cost (€K) | Notes |
|------|---|---|
| Cloud SaaS subscriptions | 50–80 | Power BI, Azure Data Lake, IoT Hub usage |
| Internet/VPN connectivity | 10–15 | Dedicated cloud link, redundancy |
| Monitoring & Maintenance | 30–50 | Cloud ops, model retraining (data scientist), platform patching |
| Backup & Disaster Recovery | 10–15 | Extra storage, replication |
| **Total OpEx (Annual)** | **100–160** | **Central: €130k/year** |

### 23.3 Benefits (First Year, Single Line)

| Benefit | Annual Impact (€K) | Confidence | Calculation |
|---------|---|---|---|
| **Downtime Reduction** | 150–200 | High | 10–15% less unplanned downtime × €500/hr × 1,440 operational hrs/year |
| **Defect Rate Improvement** | 80–120 | Medium | 0.5% reduction in scrap → fewer packs discarded → €40–60k revenue saved |
| **Energy Efficiency** | 40–60 | Medium | 10% energy reduction via VFD + optimization → €50k savings |
| **Maintenance Optimization** | 60–100 | Medium | Reduce PM downtime 20%, extend MTBF → spare parts + labor savings |
| **Quality Compliance** | 20–40 | Medium | Fewer deviations → less regulatory risk, faster lot release |
| **Labor Productivity** | 30–50 | Low | Operators spend less time troubleshooting, more on value-add tasks |
| **Total Annual Benefit** | **380–570** | | **Central: €475k/year** |

### 23.4 ROI Calculation

```
POC Cost: €1,000k
Annual Benefit (Year 1+): €475k
OpEx (Year 1+): €130k
Net Benefit (Year 1): €475k − €130k = €345k

Payback Period:
€1,000k ÷ €345k/year = 2.9 years (≈ 35 months)

3-Year Cumulative ROI:
Gross benefit (3 years): €475k × 3 = €1,425k
OpEx (3 years): €130k × 3 = €390k
POC cost: €1,000k
Net profit (3 years): €1,425k − €390k − €1,000k = €35k
ROI % (3 years): €35k ÷ €1,000k = 3.5%

5-Year Cumulative ROI:
Gross benefit: €475k × 5 = €2,375k
OpEx: €130k × 5 = €650k
POC cost: €1,000k
Net profit: €2,375k − €650k − €1,000k = €725k
ROI %: €725k ÷ €1,000k = 72.5%
Payback: ~2.9 years
```

**Conclusion:** POC pays for itself in 3–4 years through downtime/scrap reduction alone. Additional upside from capacity gains (higher throughput) not yet quantified.

---

## 24. NEXT STEPS: DETAILED ROADMAP

### Week 1–2: Initiation
- [ ] Stakeholder kickoff (operations, engineering, IT, QA)
- [ ] Requirements workshop (finalize KPIs, data points, alert thresholds)
- [ ] Technology selection decision (Azure vs. AWS vs. Hybrid)
- [ ] Vendor RFQ for edge gateway & integration partner
- [ ] Security & GxP compliance pre-assessment

### Week 3–4: Design & Procurement
- [ ] Detailed system architecture (data flows, component diagram)
- [ ] Data model design (entities, time-series schema)
- [ ] Equipment mapping (PLC tags, sensor IDs, naming convention)
- [ ] Network design & firewall rules
- [ ] Procurement of edge gateway, sensors, cloud resources
- [ ] DQ document preparation

### Week 5–8: Development
- [ ] Edge gateway setup (OPC-UA client, MQTT subscriber, buffering logic)
- [ ] Cloud infrastructure provisioning (IoT Hub, Data Lake, Analytics)
- [ ] Dashboard development (Power BI or Grafana)
- [ ] Integration testing (end-to-end data flow)
- [ ] Model development (anomaly detection, predictive maintenance baseline)
- [ ] IQ execution (hardware configs verified)

### Week 9–12: Pilot & OQ
- [ ] Go-live on production line (read-only, monitoring only)
- [ ] OQ test execution (real-time telemetry, alerts, historical queries)
- [ ] Data quality monitoring (missing data detection, outlier analysis)
- [ ] Model accuracy validation (compare predictions vs. actual)
- [ ] User feedback collection (operators, supervisors, engineers)
- [ ] Minor tuning based on feedback

### Week 13–20: PQ & Hardening
- [ ] 4-week continuous operation with all telemetry flowing
- [ ] PQ test execution (sustained load, anomaly detection accuracy, dashboard latency)
- [ ] GxP compliance gap closure (audit trail verification, digital signatures)
- [ ] Security hardening (penetration test, certificate validation, access control)
- [ ] Documentation finalization (runbooks, troubleshooting guides)
- [ ] Change management & operator training

### Week 21–24: Validation & Sign-Off
- [ ] Final validation report (DQ, IQ, OQ, PQ all PASS)
- [ ] Regulatory readiness review (GxP compliance audit)
- [ ] Business case review (expected ROI, risk assessment)
- [ ] Executive sign-off (approval to proceed to Phase 2)
- [ ] Lessons learned workshop
- [ ] Sustainment planning (monthly KPI reviews, model retraining schedule)

---

## APPENDIX A: GLOSSARY OF TERMS

| Term | Definition |
|------|-----------|
| **OEE** | Overall Equipment Effectiveness = Availability × Performance × Quality |
| **MTBF** | Mean Time Between Failures (average operational hours until failure) |
| **MTTR** | Mean Time To Repair (average time to restore equipment to service) |
| **GxP** | Good Manufacturing Practice (21 CFR Part 11, FDA requirement for pharma/tobacco) |
| **DQ** | Design Qualification (verification that design meets requirements) |
| **IQ** | Installation Qualification (verification of component installation) |
| **OQ** | Operational Qualification (verification of operational performance) |
| **PQ** | Performance Qualification (verification under expected production load) |
| **OPC-UA** | OLE for Process Control – Unified Architecture (industrial protocol) |
| **MQTT** | Message Queuing Telemetry Transport (lightweight IoT protocol) |
| **SCADA** | Supervisory Control and Data Acquisition (traditional manufacturing control system) |
| **MES** | Manufacturing Execution System (production order tracking, scheduling) |
| **PLCProgrammable Logic Controller (real-time equipment controller) |
| **VFD** | Variable Frequency Drive (motor speed controller) |
| **SPC** | Statistical Process Control (quality monitoring via control charts) |
| **Historian** | Time-series database (stores equipment telemetry over time) |
| **Digital Twin** | Virtual replica of physical asset/process synchronized with real-time data |
| **Telemetry** | Real-time sensor data streamed from equipment |
| **KPI** | Key Performance Indicator (metric tracked for business insight) |

---

## APPENDIX B: SAMPLE POWER BI DASHBOARD WIREFRAME

```
┌─────────────────────────────────────────────────────────────────┐
│ OPERATOR DASHBOARD - Production Line 001                   [Refresh] │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  [KPI Cards]                                                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────────┐
│  │ Throughput  │ │ Defect Rate │ │  Downtime   │ │ Current Prod │
│  │  850/min    │ │    1.2%     │ │  45 min     │ │  CIG-REG-20  │
│  │  (97% nom)  │ │  (alert ⚠)  │ │  (4.5% OEE) │ │   LOT-001    │
│  └─────────────┘ └─────────────┘ └─────────────┘ └──────────────┘
│                                                                   │
│  [Real-time Line State]                                           │
│  Equipment Status:                                                │
│  Rolling Motor ●[Running] 2.1g RMS   Temperature 65°C            │
│  Packing Mach ●[Running] 380W        Cycle Time 3.5s             │
│  Conveyor     ●[Running] 87% speed   Product Jam Detect [NO]    │
│  Printer      ●[Running] Ink 65°C    Barcode ✓ 99%              │
│                                                                   │
│  [Defects (Last 10 min)]               [Alerts]                  │
│  Printing 3 ▊▊▊                        ⚠ Vibration High          │
│  Weight 1 ▊                            ⚠ Compressed Air Low       │
│  Count 2 ▊▊                            ⚫ Rolling Motor PM Due    │
│                                                                   │
│  [Downtime Log (This Shift)]                                      │
│  14:15 → 14:20 Jam (conveyor) [Resolved]                        │
│  13:45 → 13:48 Changeover (Menu→Reg) [Resolved]                 │
│                                                                   │
│  [Trend Charts]                                                   │
│  OEE (24h)  ▄▅▆█▇▆▅▄▃▂▁  [Current: 87%]                        │
│  Scrap (%)  ▁▁▁▂▂▁▁▂▂▂▁  [Current: 1.2%]                        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ MANAGEMENT DASHBOARD - Weekly Summary                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Shift      OEE     Packs Prod  Defect Rate  Downtime  Energy   │
│  ────────────────────────────────────────────────────────────── │
│  Mon(A)    85.2%     412,000       1.8%      52 min   3,200kWh  │
│  Mon(B)    86.1%     425,000       1.5%      48 min   3,150kWh  │
│  Tue(A)    84.9%     408,000       1.9%      58 min   3,220kWh  │
│  ...                                                              │
│  Weekly Avg 85.4%    2,912,000      1.7%     352 min  22,360kWh │
│  Target     85.0%    2,800,000      2.0%    <400 min  23,000kWh │
│  Variance   +0.4pp   +4.0%         −0.3pp    −12%     −2.8%     │
│                      ✓ PASS        ✓ PASS    ✓ PASS   ⚠ WARN   │
│                                                                   │
│  [Top Issues This Week]                    [Predictive Alerts]   │
│  1. Filter feeder jam (4 events) → Clean  • Rolling motor PM in  │
│  2. Changeover time avg 38 min → Review   120 hrs (Score: 34%)   │
│  3. Wrap tension variance (5%) → Adjust   • Filter supplier lot  │
│                                            quality issue detected │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## APPENDIX C: REFERENCES & STANDARDS

**Regulatory:**
- FDA 21 CFR Part 11 (Electronic Records, Electronic Signatures)
- ICH Q7 (Good Manufacturing Practice for Active Pharmaceutical Ingredients)
- ISO 13849-1 (Safety of machinery – Safety-related control systems)
- ISO 50001 (Energy management systems)

**Technical Standards:**
- OPC UA Part 1–14 (IEC 62541 series)
- MQTT Version 5.0 (OASIS standard)
- IEC 62304 (Medical device software lifecycle processes)
- NIST Cybersecurity Framework

**Industry Guidance:**
- ISPE GAMP5 (Guide to Good Practice in Validation)
- PDA Technical Report 60 (Automation for Pharma and Biotech)
- Tobacco Master File requirements (if applicable)

---

**END OF DOCUMENT**

---

### Document Control

| Version | Author | Date | Status | Changes |
|---------|--------|------|--------|---------|
| 1.0 | Cloud Solutions Architect | Jan 8, 2026 | Draft - POC Design Phase | Initial comprehensive design document |

### Approval Sign-Off

- [ ] Operations Director
- [ ] Quality Assurance Manager
- [ ] IT/Cybersecurity Officer
- [ ] Executive Sponsor (CFO/COO)

---

**This document is confidential and for internal use only. Unauthorized distribution is prohibited.**
