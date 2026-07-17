# 🌐 AetherNet-Core-Cloud: Multi-Agent AI Telecom Switch & Spoofing Guard

AetherNet-Core-Cloud is an enterprise-grade, cloud-optimized autonomous voice-phishing (vishing) mitigation system. It scans incoming call transcripts in real time, intercepts sophisticated corporate line-spoofing scams, deflates adversarial prompt injections, and applies dynamic network routing adjustments. 

This production build is engineered to run seamlessly on low-overhead, free cloud hosting tiers (like Render, Railway, or Fly.io) by utilizing an adaptive in-memory checkpointer layer and an ultra-low-cost cloud inference mesh powered by **GPT-4o-Mini**.

---

## 💎 Cloud Architecture Matrix Core

### 1. Zero-Database Adaptive Checkpoint Gating (Pillar 5)
Eliminates the baseline operational requirement for a dedicated managed database cluster during live demonstrations. The graph gateway dynamically analyzes system environment variables. If no `DATABASE_URL` is detected, it automatically spins up a localized, stateful `MemorySaver` instance, allowing the complete multi-agent graph mesh to function smoothly on zero-cost, stateless hosting environments.

### 2. Zero-Trust Programmatic Safety Airlock Node (Pillar 2)
Protects operational budgets from malicious activity. The graph enforces a deterministic programmatic airlock shield (`native_telecom_airlock_node`) right at the ingestion boundary. If a transcript contains an injection attack or code exploit (e.g., a SQL injection attempt), the graph instantly fires a conditional routing bridge straight to a secure termination block—hanging up the line with **0ms model latency** and saving 100% of your cloud token budget.

### 3. Context-Aware Priority Overrides & Spoofing Defense (Pillar 1)
Addresses cognitive bias limitations common in lightweight standard AI configurations. When a malicious actor spoofs a high-trust caller ID (such as an internal `VIP_ENTERPRISE` line) to harvest corporate credentials, the agent's custom system-prompt configuration instructs the model that conversational threat markers always override database trust statuses, ensuring a clean network deflection.

### 4. Real-Time Telemetry & Token Cost Accounting (Pillar 3)
Provides full system transparency. The application features a dynamic React/Tailwind frontend tracking array that records prompt execution node traces and evaluates token consumption micro-billing in real time ($ USD metric scaling), giving developers and operators clear insight into graph processing costs.

---

## 🗺️ System Topology Routing Architecture

```text
               [ Raw Ingest Stream: Caller ID & Transcript ]
                                    │
                                    ▼
                    ┌────────────────────────────────┐
                    │ Pillar 2: Safety Airlock Node  │
                    └───────────────┬────────────────┘
                                    │
              (Adversarial System Overrides / Exploits)
                                    ├──► [ Hard Deflection Exit Path ]
                                    │     (Token Cost: $0.000000)
                       (If Cleared Safety Bounds)
                                    └──► [ Initialize State Checkpointer ]
                                              │
                                              ▼
                            ┌────────────────────────────────┐
                            │ Pillar 4: OpenAI Extractor     │
                            │   (Threat Index & Category)    │
                            └───────────────┬────────────────┘
                                              │
                                              ▼
                            ┌────────────────────────────────┐
                            │ Pillar 5: Mock Registry Lookup │
                            │ (Hydrates Subscriber Profile)  │
                            └───────────────┬────────────────┘
                                              │
                                              ▼
                            ┌────────────────────────────────┐
                            │ Pillar 1: OpenAI Orchestrator  │
                            │   (Resolves Safe Route Path)   │
                            └───────────────┬────────────────┘
                                              │
                                              ▼
                            ┌────────────────────────────────┐
                            │ Pillar 5: Active State Pruner  │
                            │ (Scrubs Bulk Text from Memory) │
                            └───────────────┬────────────────┘
                                              │
                                              ▼
                                           [ END ]