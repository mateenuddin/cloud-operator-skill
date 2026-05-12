# Reference Catalog

Three deep references for the broader cloud-operator surface area, beyond the skill itself.

## Pages

- **[Service catalog](service-catalog.md)** — ~245 cloud services across AWS, GCP, and Azure, organized by capability (Pricing, Compute, Storage, Database, Networking, Identity, Management, Observability, Analytics, ML, Integration). One-line "what it does" per entry. Use this when you need the menu.
- **[Operations catalog](operations-catalog.md)** — Drill from service to actual API operation, with MCP-availability annotation per row. Five priority areas covered in depth: Pricing/Billing, Compute/Storage, Identity/Security, Management/Observability, AI/GPU.
- **[Mindmap (interactive)](mindmap.md)** — Same hierarchy as the service catalog rendered as a Mermaid mindmap. Pannable, zoomable, searchable.

## How to use these

When the skill says "consult `references/aws-pillars.md` for family conventions," that file lives in the skill folder ([`docs/skill/references/aws-pillars.md`](../skill/references/aws-pillars.md)). The Reference Catalog here is the *broader* docs — service breadth and operation depth.

Rough rule of thumb:

- **Designing a new agent skill?** Browse the service catalog to scope what's in / out.
- **Wiring an MCP for action calls?** Check the operations catalog for available API ops + MCP status.
- **Onboarding to multi-cloud?** Use the mindmap to compare equivalents at a glance.
