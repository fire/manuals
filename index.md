# V-Sekai — Multiplayer Fabric

Documentation for the multiplayer fabric stack: a WebTransport game server platform built on Godot, Elixir, and CockroachDB. The runtime is moving from Fly.io onto a self-hosted Harvester HCI cluster, where each service runs as a VM image driven by podman quadlets.

The project spans two GitHub organizations that are both in active use:

- [`v-sekai-multiplayer-fabric`](https://github.com/v-sekai-multiplayer-fabric) holds the engine, the Harvester VM images, the rendering and USD research, and this documentation. It is the home for new work.
- [`V-Sekai-fire`](https://github.com/V-Sekai-fire) holds the runtime services and game systems that have not yet migrated (gateway, planner, storage, avatars, and the `multiplayer-fabric` submodule umbrella).

The migration is partial. Many repos have moved; several have not. The split below records where each one lives today. See the org-migration decision for how the two orgs relate and why.

## Where things live

| Resource                                                             | Contents                             |
| -------------------------------------------------------------------- | ------------------------------------ |
| [Decisions](decisions.qmd)                                           | Architecture decision records (MADR) |
| [Changelog](changelog.qmd)                                           | Daily deck logs                      |
| [References](references.qmd)                                         | Bibliography of cited sources        |
| Compiling the engine                                                 | Local build SOP for Godot            |

## Capabilities and where they live

Each capability maps to the engine feature branch in [godot](https://github.com/v-sekai-multiplayer-fabric/godot) that implements it, plus the supporting repos. The Tier column follows the [feature classification](decisions/20260606-feature-classification-poc-baseline-stretch.md): proof of concept, baseline, or stretch.

| Capability                                                                                         | Tier             | Engine branch                                                                        | Supporting repos                                                                                                                                                                                                             | Status                                                                                |
| -------------------------------------------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Native video playback                                                                              | Baseline         | `feat/native-media` (MediaFoundation, GStreamer)                                     | [native-media-test](https://github.com/v-sekai-multiplayer-fabric/native-media-test), [vulkan-video-godot](https://github.com/v-sekai-multiplayer-fabric/vulkan-video-godot)                                                 | Working; builds on Windows and Linux.                                                 |
| Networking transport (WebTransport / HTTP/3) | Baseline         | `feat/module-http3` (picoquic + web/wasm backends)                                   | [zone-server](https://github.com/v-sekai-multiplayer-fabric/zone-server)                                                                                                                                                     | Working; `WebTransportPeer`/`QUICClient`/`QUICServer`, demos, Lean termination proof. |
| Scene baking via OpenUSD                                                                           | Baseline         | —                                                                                    | [openusd-fabric](https://github.com/v-sekai-multiplayer-fabric/openusd-fabric), [zone-baker](https://github.com/v-sekai-multiplayer-fabric/zone-baker), [idtx-flow](https://github.com/v-sekai-multiplayer-fabric/idtx-flow) | Working; USD schema, Blender export hooks, scene validation, headless export.         |
| Spatial audio (HRTF + audio probes) | Baseline         | `feat/spatial-audio-server`, `feat/module-resonance-audio` (patched Resonance Audio) | [sponza-godot-audio](https://github.com/v-sekai-multiplayer-fabric/sponza-godot-audio)                                                                                                                                       | Working; demo and benchmark scene.                                                    |
| Speech                                                                                             | Baseline         | `feat/module-speech`                                                                 | —                                                                                                                                                                                                                            | Working.                                                                              |
| Pen stroke creation (codename cassie)                                                              | Proof of concept | `feat/module-cassie`                                                                 | [vsekai-materialx](https://github.com/v-sekai-multiplayer-fabric/vsekai-materialx), [materialx-shaders-lean](https://github.com/v-sekai-multiplayer-fabric/materialx-shaders-lean)                                           | Pen stroke creation is solid; patch surface creation is buggy (loses about 90%).      |
| Multiplayer presence (tracker orbs) | Proof of concept | `feat/module-xr-grid`                                                                | [xr-grid](https://github.com/v-sekai-multiplayer-fabric/xr-grid)                                                                                                                                                             | Proposed; head and hand pose orbs sent over low-level WebTransport.                   |

## Repositories — `v-sekai-multiplayer-fabric`

### Engine

| Repo                                                                                                             | Purpose                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [godot](https://github.com/v-sekai-multiplayer-fabric/godot)                                                     | V-Sekai fork of the Godot engine. Feature branches per topic.                                                  |
| [merge](https://github.com/v-sekai-multiplayer-fabric/merge)                                                     | `gitassembly` recipe and `update_godot_v_sekai.exs` driver that composes the engine from its feature branches. |
| [godot-images](https://github.com/v-sekai-multiplayer-fabric/godot-images)                                       | Single-source-of-truth engine builds: editor (baker) and template_release (zone server). Publishes to GHCR.    |
| [godot-sandbox-gdscript-compiler](https://github.com/v-sekai-multiplayer-fabric/godot-sandbox-gdscript-compiler) | GDScript-to-sandbox compiler for the engine's `module_sandbox`.                                                |
| [godot-sandbox-programs](https://github.com/v-sekai-multiplayer-fabric/godot-sandbox-programs)                   | RISC-V programs run inside `module_sandbox` (fork).                                                            |
| [native-media-test](https://github.com/v-sekai-multiplayer-fabric/native-media-test)                             | Godot project exercising the engine's native media (audio/video) backend.                                      |
| [vulkan-video-godot](https://github.com/v-sekai-multiplayer-fabric/vulkan-video-godot)                           | Vulkan Video decode integration for Godot (placeholder).                                                       |

### Runtime services

| Repo                                                                         | Purpose                                                                        |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [zone-server](https://github.com/v-sekai-multiplayer-fabric/zone-server)     | Headless Godot zone server (template_release, double precision).               |
| [zone-backend](https://github.com/v-sekai-multiplayer-fabric/zone-backend)   | URO: Phoenix/Elixir backend for identity, the zone directory, and the planner. |
| [zone-baker](https://github.com/v-sekai-multiplayer-fabric/zone-baker)       | Minimal headless Godot project that validates and exports VSK assets.          |
| [observability](https://github.com/v-sekai-multiplayer-fabric/observability) | VictoriaMetrics, VictoriaLogs, Tempo, and the OTEL Collector.                  |

### Harvester VM images

Each service ships as a qcow2 image layered on a shared base and run via podman quadlets.

| Repo                                                                                       | Purpose                                                                                      |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| [linux-base-image](https://github.com/v-sekai-multiplayer-fabric/linux-base-image)         | AlmaLinux 9 GenericCloud with podman, chrony, and qemu-guest-agent. Base for every VM image. |
| [zone-server-image](https://github.com/v-sekai-multiplayer-fabric/zone-server-image)       | Headless Godot zone server runtime VM.                                                       |
| [zone-baker-image](https://github.com/v-sekai-multiplayer-fabric/zone-baker-image)         | Headless Godot asset validator and exporter VM.                                              |
| [zone-backend-image](https://github.com/v-sekai-multiplayer-fabric/zone-backend-image)     | URO Phoenix backend VM.                                                                      |
| [cockroach-crdb-image](https://github.com/v-sekai-multiplayer-fabric/cockroach-crdb-image) | CockroachDB server VM (v-sekai fork).                                                        |
| [restic-backup-image](https://github.com/v-sekai-multiplayer-fabric/restic-backup-image)   | versitygw, restic, and a cockroach client for the backup VM.                                 |
| [gha-runner-image](https://github.com/v-sekai-multiplayer-fabric/gha-runner-image)         | Org-wide GitHub Actions self-hosted runner as a podman quadlet.                              |
| [sccache-cache-image](https://github.com/v-sekai-multiplayer-fabric/sccache-cache-image)   | versitygw S3 endpoint dedicated to sccache for fast C++ rebuilds.                            |

### Rendering, shaders, and USD

| Repo                                                                                           | Purpose                                                                                                      |
| ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [godot-toon-shaders](https://github.com/v-sekai-multiplayer-fabric/godot-toon-shaders)         | Godot toon shader ports and a shared parameter map (MToon 0.x / MToon10, planned SCSS and lilToon).          |
| [vsekai-materialx](https://github.com/v-sekai-multiplayer-fabric/vsekai-materialx)             | PBR/NPR/Slug as MaterialX nodes compiled to Slang; ThorVG-to-Slug vectorization, differentiable via SlangPy. |
| [materialx-shaders-lean](https://github.com/v-sekai-multiplayer-fabric/materialx-shaders-lean) | Lean 4 formalization of PBR, NPR, and vector shaders under MaterialX.                                        |
| [MaterialX](https://github.com/v-sekai-multiplayer-fabric/MaterialX)                           | The MaterialX material-exchange standard (fork).                                                             |
| [idtx-flow](https://github.com/v-sekai-multiplayer-fabric/idtx-flow)                           | Godot plugin importing USD via openUSD (fork).                                                               |
| [openusd-fabric](https://github.com/v-sekai-multiplayer-fabric/openusd-fabric)                 | OpenUSD pipeline spanning Blender, Godot, Hydra, Unity, and a Lean schema.                                   |
| [sponza-godot-audio](https://github.com/v-sekai-multiplayer-fabric/sponza-godot-audio)         | Sponza demo and audio benchmark for Godot 4.                                                                 |

### Spatial and verification

| Repo                                                                                     | Purpose                                                                       |
| ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [lean-predictive-bvh](https://github.com/v-sekai-multiplayer-fabric/lean-predictive-bvh) | Lean 4 formal verification and codegen for the Predictive BVH spatial oracle. |

### Tooling and integration

| Repo                                                                                                       | Purpose                                                                               |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [vsekai-godot-mcp](https://github.com/v-sekai-multiplayer-fabric/vsekai-godot-mcp)                         | In-editor MCP server addon for Godot (Streamable-HTTP, constant-work command buffer). |
| [viser](https://github.com/v-sekai-multiplayer-fabric/viser)                                               | Web-based 3D visualization in Python (fork).                                          |
| [xr-grid](https://github.com/v-sekai-multiplayer-fabric/xr-grid)                                           | VR interaction tool (fork).                                                           |
| [terraform-provider-harvester](https://github.com/v-sekai-multiplayer-fabric/terraform-provider-harvester) | Terraform provider for Harvester (fork).                                              |

### Infrastructure and docs

| Repo                                                             | Purpose                                                                          |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [infra](https://github.com/v-sekai-multiplayer-fabric/infra)     | OpenTofu config that deploys the stack onto Harvester HCI as podman-quadlet VMs. |
| [manuals](https://github.com/v-sekai-multiplayer-fabric/manuals) | This Quarto site.                                                                |

### Archived

| Repo                                                                                                 | Purpose                                 |
| ---------------------------------------------------------------------------------------------------- | --------------------------------------- |
| [friends-art-game-loop](https://github.com/v-sekai-multiplayer-fabric/friends-art-game-loop)         | Local-first art-game loop experiment.   |
| [sandbox-gdextension-godot](https://github.com/v-sekai-multiplayer-fabric/sandbox-gdextension-godot) | Earlier GDExtension sandbox approach.   |
| [usd-converter-for-vrchat](https://github.com/v-sekai-multiplayer-fabric/usd-converter-for-vrchat)   | VRChat-to-VRM 1.0 converter UPM (fork). |

## Still on `V-Sekai-fire` (not yet migrated)

These repos remain the source of truth under the older org. Links in the [decisions](decisions.qmd) and [changelog](changelog.qmd) that point at them are correct and still resolve.

| Repo                                                                                                       | Purpose                                                             |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| [multiplayer-fabric](https://github.com/V-Sekai-fire/multiplayer-fabric)                                   | Umbrella monorepo registering the V-Sekai-fire repos as submodules. |
| [multiplayer-fabric-gateway](https://github.com/V-Sekai-fire/multiplayer-fabric-gateway)                   | Elixir WebTransport gateway on UDP 443.                             |
| [multiplayer-fabric-zone-console](https://github.com/V-Sekai-fire/multiplayer-fabric-zone-console)         | Operator console for zone health and shard rotations.               |
| [multiplayer-fabric-webtransport](https://github.com/V-Sekai-fire/multiplayer-fabric-webtransport)         | Elixir bindings for the Rust wtransport library.                    |
| [multiplayer-fabric-taskweft](https://github.com/V-Sekai-fire/multiplayer-fabric-taskweft)                 | Re-entrant temporal HTN planner and ReBAC engine.                   |
| [multiplayer-fabric-humanoid-project](https://github.com/V-Sekai-fire/multiplayer-fabric-humanoid-project) | Humanoid avatars and animations (`mire.vrm` test avatar).           |
| [aria-storage](https://github.com/V-Sekai-fire/aria-storage)                                               | casync/desync chunked content-addressable storage.                  |
| [elixir-turboquant-llm](https://github.com/V-Sekai-fire/elixir-turboquant-llm)                             | Quantized LLM inference NIF (Elixir / llama.cpp).                   |
| [multiplayer-fabric-cycle-tests](https://github.com/V-Sekai-fire/multiplayer-fabric-cycle-tests)           | Maglev cycle smoke tests, one per cycle.                            |

## Quick start

The local workflow is bash-first (POSIX shebangs, `/tmp` paths, symlinks, `lsof`, the UNIX docker socket). On Windows, use WSL2 (Ubuntu).

```sh
git clone https://github.com/v-sekai-multiplayer-fabric/godot
```

The engine assembles from feature branches via `merge` and builds through `godot-images`. To build the engine locally, follow the Compiling the Godot engine SOP.
