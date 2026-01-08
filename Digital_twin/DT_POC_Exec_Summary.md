# Digital Twin POC - Executive Summary & Quick Reference

## PROJECT OVERVIEW

**Objective:** Design and validate a comprehensive Digital Twin proof-of-concept for tobacco manufacturing (cigarettes, vape devices, heated sticks) that enables OEE improvement, predictive maintenance, and GxP compliance.

**Scope:** Single production line (end-to-end: leaf intake → finished goods logistics)

**Duration:** 6–9 months POC | **Investment:** €800K–€1.2M | **Expected Payback:** 2.9–3.5 years

---

## EXECUTIVE HIGHLIGHTS

### Business Case
- **Current OEE:** 85.4% (availability 92%, performance 96%, quality 97%)
- **Target OEE:** 93.2% (+8% improvement via downtime reduction, speed optimization, defect control)
- **Annual Benefit (Single Line):** €475K (reduced downtime: €150–200K, scrap reduction: €80–120K, energy: €40–60K, maintenance: €60–100K, other: €145–155K)
- **3-Year Net Benefit:** €35K (conservative); **5-Year Net Benefit:** €725K
- **Payback Period:** 2.9 years

### Technology Stack
- **Cloud:** Azure IoT Hub + Digital Twins + Synapse Analytics + Power BI (or AWS IoT TwinMaker alternative)
- **Edge:** Industrial PC (Windows IoT/Linux) + OPC-UA client + MQTT subscriber + local historian buffer
- **Protocols:** OPC-UA (PLC), MQTT (sensors), REST (MES APIs), Kafka (event streaming)
- **Data Model:** Time-series (telemetry), transactional (batch/lot master), audit logs (GxP)

### Success Criteria (POC Phase 1)
- ✓ OEE measured within ±2% of manual baseline
- ✓ Downtime events captured with >95% accuracy
- ✓ Anomaly detection >85% precision, <10% false-positive rate
- ✓ Predictive maintenance model >70% accuracy (7-day failure forecast)
- ✓ 100% GxP compliance (audit trail, digital signatures, traceability)
- ✓ Operator adoption >70% (daily active users)

---

## SCOPE SNAPSHOT

| Category | Details |
|----------|---------|
| **Physical Assets** | Rolling machine, packing machine, printer, conveyor, filters, wrapper, adhesive, printers, cartonization, palletizers, robots, AGVs |
| **Sensors/Data Points** | 40+ telemetry streams: temperature, humidity, vibration, pressure, weight, current, flow, vision system (defect detection) |
| **Process Coverage** | Leaf preparation → blending → rolling → filter application → wrapping → packing → printing → cartonization → palletization → warehouse staging |
| **Parallel Products** | Cigarettes (regular, menthol), vape devices (liquid fill, battery assembly, device test), heated-tobacco sticks |
| **Utilities** | Compressed air, electrical supply, waste/scrap recovery |
| **Data Sources** | PLC (OPC-UA), SCADA, MES (production orders, scheduling), Historian, IoT sensors (MQTT), vision system, QA/LIMS, AGV fleet mgmt, maintenance system |

---

## INTEGRATION ARCHITECTURE (SIMPLIFIED)

```
Plant Floor (Real-time)
    │
    ├─ PLC (Siemens/Rockwell) ──OPC-UA──┐
    ├─ SCADA HMI ─────────────OPC-UA─────┤
    ├─ IoT Sensors (temp, vibration, weight) ──MQTT──┤
    └─ Historian DB (PI, Ignition) ──REST API──┘
                                        │
                                        ↓
                    ┌──────────────────────────────────┐
                    │     Edge Gateway                 │
                    │  (Industrial PC, Windows/Linux)  │
                    │  ├─ OPC-UA Client               │
                    │  ├─ MQTT Subscriber             │
                    │  ├─ Data Validation & Buffering │
                    │  ├─ Local Historian (offline)    │
                    │  └─ Encryption/TLS              │
                    └──────┬───────────────────────────┘
                           │ (MQTT over VPN, TLS 1.3)
                           ↓
            ┌──────────────────────────────────────────┐
            │   Cloud Platform (Azure Option)         │
            │  ├─ IoT Hub (D2C ingestion)            │
            │  ├─ Stream Analytics (real-time)       │
            │  ├─ Data Lake (raw + processed)        │
            │  ├─ Synapse (batch analytics, ML)      │
            │  ├─ Digital Twins (semantic model)     │
            │  └─ Power BI (dashboards)              │
            └──────┬───────────────────────────────────┘
                   │
        ┌──────────┴──────────┬──────────────┐
        ↓                     ↓              ↓
    Operator Dashboard   Management Report  Executive KPIs
    (Real-time alerts)   (Daily, Weekly)    (Monthly, Trend)
```

---

## KEY DELIVERABLES

### Phase 1 Outputs (6–9 months)

1. **Architecture & Design Documents**
   - System architecture (3-layer: plant, edge, cloud)
   - Component diagram (OPC-UA, MQTT, REST integration)
   - Data flow specification (telemetry → cloud → analytics → visualization)
   - Network architecture & security design
   - DQ (Design Qualification) document

2. **Data Models & Schemas**
   - Time-series schema (telemetry, metrics, anomalies)
   - Batch/Lot master data model
   - Equipment asset hierarchy
   - Audit trail & GxP compliance schema

3. **Implementation & Deployment**
   - Edge gateway software (OPC-UA client, MQTT, buffering)
   - Cloud infrastructure (Azure resource groups, Data Lake, storage)
   - ETL pipelines (raw → processed data)
   - Real-time dashboards (Power BI or Grafana)

4. **Analytics Models**
   - OEE calculation engine (Availability, Performance, Quality)
   - Anomaly detection (Isolation Forest unsupervised model)
   - Predictive maintenance (Gradient Boosted model, 7-day failure probability)
   - Process SPC (Statistical Process Control, control limits for rod weight, pack weight)

5. **Validation & Compliance**
   - IQ (Installation Qualification) report
   - OQ (Operational Qualification) test results
   - PQ (Performance Qualification) 4-week continuous run validation
   - GxP audit trail verification (21 CFR Part 11 readiness)

6. **Lessons Learned & Roadmap**
   - Change management insights (operator adoption, training effectiveness)
   - Performance metrics baseline (OEE, defect rate, downtime)
   - Scaling roadmap to Phase 2 (additional lines, advanced analytics)

---

## TECHNOLOGY SELECTION

### Recommended: **Azure Stack** (for GxP-regulated environments)

| Component | Technology | Why |
|-----------|-----------|-----|
| **Cloud** | Azure IoT Hub + Digital Twins + Synapse | Tight integration, GxP validation support, proven pharma case studies (J&J, AstraZeneca) |
| **Real-time Compute** | Stream Analytics or Apache Spark | SQL-like syntax, <5sec latency, auto-scaling |
| **Data Lake** | ADLS Gen 2 + Synapse SQL Pool | Cost-effective, native encryption, RBAC, audit logging |
| **Analytics** | Power BI + AML (AutoML) | Rapid dashboard development, anomaly detection, model governance |
| **Visualization** | Power BI + Azure Digital Twins (3D) | Integrated twin + 3D viewer, operator-friendly dashboards |
| **Security** | Azure Key Vault, Managed Identity, NSGs | Certificate rotation, secret management, network isolation |
| **Cost (1-year POC)** | €400–500K cloud + €250–350K services = **€650–850K total** | Transparent pricing, per-usage billing |

### Alternative: **AWS Stack** (if AWS-standardized organization)

- **Advantage:** AWS IoT TwinMaker purpose-built for manufacturing twins, lower cloud costs (€350–450K)
- **Same integration patterns** (MQTT, REST), similar analytics capabilities
- **Recommendation:** Choose based on organizational cloud standardization, not technical merits (both viable)

### Hybrid Multi-Cloud (Risk Mitigation)

- Edge: Apache NiFi or Siemens MindSphere Agent (cloud-agnostic)
- Data Lake: MinIO (on-prem) + S3 + ADLS (avoid vendor lock-in)
- Cost: €650–900K (similar to single-cloud, with flexibility)

---

## INTEGRATION PATTERNS

### **Pattern 1: OPC-UA Subscribe (Deterministic, Real-time)**
- PLC/SCADA implements OPC-UA server
- Edge gateway OPC-UA client subscribes to key variables (rod weight, pack count, downtime events)
- Frequency: 1–5s (native, 10–50ms if needed)
- **Use for:** Critical production KPIs, safety signals, immediate alerts

### **Pattern 2: MQTT Pub/Sub (Lightweight, Distributed Sensors)**
- IoT devices (temperature sensor, vibration meter, pressure transducer) publish to MQTT broker
- Edge/cloud MQTT subscribers ingest and process
- Frequency: 5–30s per sensor
- **Use for:** Non-critical monitoring, redundant measurements, legacy device integration

### **Pattern 3: REST Batch APIs (Transactional, Event-driven)**
- MES system exposes REST API for production orders, lot master data, changeover events
- Edge/cloud queries API on-demand or subscribes to webhooks
- Frequency: Transactional (event-triggered), not continuous
- **Use for:** Batch context (which lot is currently running), historical queries

### **Pattern 4: Message Bus / Event Streaming (Decoupled Analytics)**
- Apache Kafka or Azure Event Hubs sits between telemetry sources and analytics consumers
- Producers: edge gateway, sensors, MES, vision system
- Consumers: anomaly detection, data lake writer, dashboards, alerts
- **Benefit:** New analytics jobs can subscribe without modifying producers

---

## DATA SECURITY & GxP COMPLIANCE

### Network Segmentation
- **DMZ:** Edge gateway (VPN tunnel only to cloud)
- **Manufacturing Network:** PLC, SCADA, sensors (isolated VLAN, no direct internet)
- **IT Network:** Office PCs (separate, no access to manufacturing)

### Device Identity & Authentication
- All devices (edge gateway, sensors, cloud services) authenticated via **X.509 certificates**
- **NO shared passwords** used for production systems
- Certificate rotation: annually, with 30-day pre-expiry rollover
- Revocation: within 24 hours if compromised

### Encryption
- **In Transit:** TLS 1.3 (MQTT: port 8883, REST: HTTPS)
- **At Rest:** AES-256 (Azure Storage, SQL database)
- **Keys:** Azure Key Vault (centralized, audited)

### Audit Trail (21 CFR Part 11)
- **Every production event logged:** lot ID, timestamp, user/system, action (start/stop/change/release)
- **Non-repudiable:** digital signatures on lot release (via Azure Key Vault)
- **Retention:** 7 years (production records), lifetime + 10 years (deviations)
- **Access Control (RBAC):**
  - **Operator:** Read dashboards, acknowledge alarms
  - **Supervisor:** Approve lot release, view trends
  - **Engineer:** Configure alerts, adjust SPC limits
  - **Admin:** System configuration, user management
  - **Auditor:** Read-only access to all records

---

## SIMULATION & WHAT-IF ANALYSIS

### Example 1: Throughput Bottleneck Detection
**Goal:** Identify which equipment limits line speed

**Simulation:**
- Increase rolling machine speed 10% → monitor downstream (packing machine utilization)
- If packing machine can't keep up → rolling machine is bottleneck
- **Output:** Prioritize packing machine upgrade for +8% throughput gain

### Example 2: Changeover Optimization
**Current:** 45 min changeover time (8 changeovers/day)
**Proposed:** Parallel hopper cleaning, quick-change filters → 30 min

**Benefit Calculation:**
- Lost production per changeover: 125 packs/min × 45 min = 5,625 packs
- After optimization: 125 × 30 min = 3,750 packs
- Gain: 1,875 packs × €0.50 = €937.50 per changeover
- Annual: 2,000 changeovers × €937.50 = **€1,875,000 annual benefit**
- **ROI:** 2-week payback on changeover optimization investment

### Example 3: Predictive Maintenance Scheduling
**Goal:** Reduce unexpected bearing failures (currently every 1,800 hours)

**Approach:**
- Monitor vibration trend (exponential wear model)
- At 1,600 hours, vibration reaches threshold → schedule PM before failure
- Planned PM: 4 hours downtime (scheduled, no production loss)
- Unplanned failure: 8 hours emergency response + safety risk

**Benefit:** Reduce MTTR 8→6 hours, eliminate safety incidents, improve MTBF predictability
**Annual savings:** €12,000 (avoided downtime)

### Example 4: Energy Optimization
**Current:** 12 kWh per 1,000 packs (€1.20/1,000 packs)
**Proposed:** VFD on main drive, dynamic speed matching demand → 10.2 kWh/1,000 packs

**Energy Savings:** 400,000 packs/year × 1.8 kWh/1,000 = 720 kWh → **€86/year** (modest, but validates model)
**ESG Impact:** Reduced carbon footprint, energy efficiency certification eligible

---

## ANALYTICS & KPI CALCULATIONS

### OEE Formula & Current Baseline

```
OEE = Availability × Performance × Quality

Availability = (Planned Time - Downtime) / Planned Time
             = 54 min / 60 min = 90%

Performance = (Ideal Cycle Time × Total Count) / Actual Runtime
            = (125 packs/min / 108 actual) × 100 = 115.7% (can exceed 100% if overspeed)

Quality = Good Count / Total Count
        = 6,900 good / 7,000 total = 98.6%

Current OEE = 90% × 99% × 98.6% = 87.4%
Target OEE = 93.2% (improvement levers below)
```

### Improvement Levers to Reach 93.2% OEE

| Lever | Current → Target | Method | Impact |
|-------|---|---|---|
| **Reduce jam downtime** | Avail 92% → 95% | Vision system, improved conveyor design | +€150K/year |
| **Optimize changeover** | Avail 95% → 97% | Parallel cleaning, quick-change parts | +€30K/year (labor) |
| **Improve speed consistency** | Perf 96% → 98% | VFD + dynamic setpoint | +€20K/year (energy) |
| **Reduce defect rate** | Quality 97% → 98.5% | SPC + corrective actions | +€80K/year (scrap reduction) |
| **Expected Net Result** | OEE 85.4% → 93.2% | Sustained effort | **+€280K/year** |

---

## VALIDATION APPROACH (GxP Compliance)

### Four-Stage Validation

1. **DQ (Design Qualification)** — Weeks 1–2
   - Requirements traceability matrix (RTM)
   - Risk assessment (FMEA)
   - System architecture review
   - **Output:** DQ report signed by QA/IT/Engineering

2. **IQ (Installation Qualification)** — Weeks 5–8
   - Hardware configurations verified
   - Software versions & patch levels documented
   - Network connectivity tested
   - Backup/recovery systems functional
   - **Output:** IQ report with detailed asset inventory

3. **OQ (Operational Qualification)** — Weeks 9–12
   - Real-time telemetry flowing end-to-end
   - Alerts trigger correctly
   - Historical queries return expected data
   - Dashboard responsiveness <3 sec
   - **Output:** OQ test results (all PASS/FAIL documented)

4. **PQ (Performance Qualification)** — Weeks 13–20
   - 4-week continuous operation at production throughput
   - >99% data completeness
   - Anomaly detection accuracy measured
   - System uptime 99.5% (excluding scheduled maintenance)
   - **Output:** PQ final report + validation sign-off by executive sponsor

### Monthly Reconciliation (Post-POC)
- Extract monthly summary from MES (ground truth): total packs, defects, downtime
- Extract same metrics from Digital Twin data lake
- Compare variance (<1% target on production count)
- Investigate discrepancies, update validation log

---

## ROADMAP: POC → PRODUCTION

### **Phase 1: POC (Months 0–9, €1.0M)**
- Single production line digital twin
- Real-time dashboards + basic predictive maintenance
- GxP validation (DQ, IQ, OQ, PQ)
- **Success Gate:** OEE measured accurately, user adoption >70%, zero GxP findings

### **Phase 2: Scale to Plant (Months 10–18, €1.5–2.5M)**
- Deploy to remaining 3 lines in same facility
- Advanced analytics (predictive quality, prescriptive recommendations)
- Full validation for all 4 lines
- **Deliverable:** Validated multi-line platform, standardized equipment models

### **Phase 3: Multi-Site Deployment (Months 19–36, €5M+)**
- Roll out to 3–5 additional PMI manufacturing facilities
- Centralized global data lake with federated analytics
- Cross-facility benchmarking, demand planning
- **Vision:** Digital shadow of entire tobacco supply chain (manufacturing → retail)

---

## RISK MITIGATION

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Legacy PLC incompatible with OPC-UA** | Data ingestion blocked | Early compatibility testing (Week 1), backup REST API integration |
| **Cloud latency spike (>10 sec)** | Alerts delayed | Hybrid edge buffering (local historian), VPN QoS, failover to AWS |
| **Operator adoption low** | System unused, no ROI | Change management, operator training, gamification |
| **GxP non-compliance** | Regulatory audit failure | Validation from inception, audit trail non-negotiable, legal review |
| **Data quality issues** | Inaccurate models | Data quality monitoring dashboard, redundant sensors for critical KPIs |
| **Cybersecurity breach** | Production disruption | Network segmentation, certificate-based auth, penetration testing |

---

## INVESTMENT SUMMARY

### POC Cost Breakdown
| Item | Cost (€K) | Notes |
|------|---|---|
| Cloud platform (1-year) | 400–500 | Azure IoT Hub, Digital Twins, Synapse, Power BI |
| Edge gateway & sensors | 80–120 | Industrial PC, OPC-UA licenses, MQTT equipment |
| Integration & development | 250–350 | Systems integrator labor, APIs, custom scripts |
| Training & validation | 50–80 | Operator training, GxP validation, testing |
| Contingency (10%) | 80–105 | Risk buffer |
| **Total POC** | **860–1,155** | **Central: €1,000K** |

### Annual Operating Cost (Single Line)
- Cloud SaaS: €50–80K
- Connectivity: €10–15K
- Monitoring & maintenance: €30–50K
- Backup & DR: €10–15K
- **Total OpEx:** €100–160K/year (central: €130K)

### Expected Annual Benefits (Year 1)
- Downtime reduction: €150–200K
- Scrap reduction: €80–120K
- Energy efficiency: €40–60K
- Maintenance optimization: €60–100K
- Compliance/labor: €50–90K
- **Total Annual Benefit:** €380–570K (central: €475K)

### ROI & Payback
- **Net Year 1:** €475K benefit − €130K OpEx − €1,000K POC = −€655K
- **Payback Period:** 2.9 years
- **5-Year Cumulative Benefit:** €2,375K − €650K OpEx − €1,000K POC = **€725K profit**
- **5-Year ROI:** 72.5%

---

## SUCCESS METRICS & SIGN-OFF

### POC Acceptance Criteria

| Criterion | Target | Threshold |
|-----------|--------|-----------|
| **Data Completeness** | >99% hourly | >98% |
| **System Latency** | <5 sec edge→cloud | <10 sec |
| **System Uptime** | 99.5% | >99% |
| **Anomaly Detection Precision** | >80% actionable alerts | >70% |
| **Predictive Model Accuracy** | RMSE <2 hrs (MTBF) | <4 hrs |
| **OEE Baseline Accuracy** | ±2% vs. manual | ±3% |
| **GxP Audit Trail** | 100% traceability | 100% |
| **User Adoption** | >80% daily usage | >70% |
| **Business Benefit Identified** | >€250K annual | Documented |

### Approval Sign-Off
- [ ] Operations Director
- [ ] Quality Assurance Manager
- [ ] IT/Cybersecurity Officer
- [ ] Finance/CFO (ROI validation)
- [ ] Executive Sponsor (overall go-ahead)

---

## NEXT STEPS

1. **Week 1:** Stakeholder kickoff, finalize technology selection (Azure vs. AWS vs. Hybrid)
2. **Week 2:** RFQ for edge gateway & systems integrator
3. **Week 3–4:** DQ document, requirements finalization
4. **Week 5–8:** Hardware procurement, cloud provisioning, software development
5. **Week 9–12:** OQ testing on production line (read-only pilot)
6. **Week 13–20:** PQ (4-week continuous run) + hardening
7. **Week 21–24:** Final validation, sign-off, Phase 2 planning

---

**Document Prepared By:** Cloud Solutions Architect  
**Date:** January 8, 2026  
**Status:** POC Design Phase – Ready for Stakeholder Approval

---

*For detailed technical specifications, architecture diagrams, data models, integration patterns, GxP validation procedures, cost-benefit analysis, and multi-phase roadmap, refer to the comprehensive design document: "DT_POC_Tobacco_Design.md"*
