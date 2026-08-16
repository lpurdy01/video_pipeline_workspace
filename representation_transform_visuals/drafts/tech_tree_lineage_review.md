# Tech Tree Lineage Review

Use this file to comment on what belongs in the public-facing tree. The goal is not to prove every historical influence. The goal is to decide which relationships are useful, defensible, and visually worth showing.

Suggested comment tags:

- `KEEP`: belongs in the diagram.
- `CUT`: too detailed, distracting, or not part of this argument.
- `RENAME`: good idea, wrong label.
- `MOVE`: node belongs, but the parent/edge is wrong.
- `TOO-DEEP`: true enough, but too technical for this video.
- `NEEDS-SOURCE`: keep only if we can support it cleanly.

## Visual Premise

This version treats the tech tree like a radial skill tree. The center is only a visual origin, not a technology or claim. Each category becomes a wedge whose size can change with its contents. The frontier is an outer layer or fog-of-war region, not a normal category wedge.

The current wedges are:

- Classical signal and media transforms.
- Dynamics, stability, and control.
- Learned representation spaces.
- Language, code, and verification.
- Outer frontier / unrevealed research region.

## Review Diagram

```mermaid
flowchart TB
  origin((" "))

  subgraph signal_wedge["wedge: classical signal and media transforms"]
    fourier["Fourier transform"]
    frequency_domain["frequency-domain view"]
    signal_processing["signal processing"]
    wireless["wireless communication"]
    compressed_audio["compressed audio: MP3 / AAC"]
    spectral_imaging["spectral imaging / MRI"]

    dct["discrete cosine transform"]
    block_frequency["block frequency bases"]
    jpeg["JPEG image compression"]
    video_codecs["video codecs: MPEG / H.26x / AV1"]

    fourier --> frequency_domain --> signal_processing
    signal_processing --> wireless
    signal_processing --> compressed_audio
    signal_processing --> spectral_imaging
    dct --> block_frequency
    block_frequency --> jpeg
    block_frequency --> video_codecs
  end

  subgraph dynamics_wedge["wedge: dynamics, stability, and control"]
    laplace["Laplace transform"]
    transfer_functions["transfer functions"]
    stability_control["stability and control"]
    feedback_control["feedback controllers"]
    motor_control["brushless motor control"]
    flight_robotics["flight / robotics stability"]
    state_space["state-space models"]
    neural_ssm["neural SSMs: S4 / Mamba"]

    laplace --> transfer_functions --> stability_control
    stability_control --> feedback_control
    feedback_control --> motor_control
    feedback_control --> flight_robotics
    stability_control --> state_space
    state_space -. convergence .-> neural_ssm
  end

  subgraph learned_wedge["wedge: learned representation spaces"]
    neural_networks["neural networks"]
    embeddings["embeddings"]
    transformers["transformer sequence models"]
    llms["large language models"]
    contrastive_space["contrastive multimodal spaces"]
    autoencoders["autoencoders / GANs"]
    neural_codecs["neural codecs: EnCodec"]
    audio_tokens["discrete audio tokens"]
    speech_agents["speech / audio agents"]
    multimodal_tools["multimodal tools"]

    neural_networks --> embeddings --> transformers --> llms
    neural_networks --> contrastive_space --> multimodal_tools
    neural_networks --> autoencoders --> neural_codecs --> audio_tokens
    audio_tokens --> speech_agents
    audio_tokens --> multimodal_tools
    transformers -. convergence .-> neural_ssm
    neural_ssm --> llms
  end

  subgraph software_wedge["wedge: language, code, and verification"]
    software_formalisms["software as formal representation"]
    expert_systems["classical expert systems"]
    blackboard["blackboard architectures"]
    formal_verifiers["SMT / Dafny / proof tools"]
    code_agents["autonomous code agents"]
    research_agents["research assistants"]
    vv_systems["V&V / evidence systems"]
    reliable_agents["reliable agent workflows"]

    software_formalisms --> code_agents
    llms --> code_agents
    llms --> research_agents
    expert_systems -. historical precedent .-> blackboard
    code_agents --> blackboard
    blackboard --> vv_systems
    formal_verifiers -. convergence .-> vv_systems
    code_agents --> vv_systems
    vv_systems --> reliable_agents
  end

  subgraph frontier_layer["outer layer: frontier / unrevealed research region"]
    orgs["transform-native organizations"]
    self_compute["self-inhabiting compute"]
    experiment_loops["autonomous experiment loops"]
    devs["discrete-event world models"]
    closed_loop_rd["closed-loop R&D"]

    reliable_agents --> orgs
    code_agents --> orgs
    research_agents --> orgs
    reliable_agents --> self_compute
    research_agents --> experiment_loops
    multimodal_tools --> experiment_loops
    reliable_agents --> experiment_loops
    experiment_loops --> devs
    devs --> closed_loop_rd
    orgs --> closed_loop_rd
    self_compute --> closed_loop_rd
  end

  origin --- fourier
  origin --- dct
  origin --- laplace
  origin --- neural_networks
  origin --- software_formalisms
  origin --- expert_systems
  origin --- formal_verifiers
```

## Main Questions

- Should Fourier, Laplace, and DCT each get their own visible branch, or should one or more collapse into a shared "classical transforms" wedge for the video?
- Is "brushless motor control" vivid enough as the Laplace/control payoff, or should this become flight control, robotics, or power electronics more broadly?
- Should `neural SSMs: S4 / Mamba` be a visible cross-category convergence, or a brief article-only side note?
- Should the software wedge include V&V/evidence systems, or does that pull too hard toward the verifiability compiler project?
- Should `classical expert systems` and `blackboard architectures` remain as historical precedent for agent workflows?
- Should the frontier layer be shown as an outer fog-of-war ring, a higher 3D shell, or a final zoom-out beyond the main tree?

## Node Review

| Node | Tag | Comment |
| --- | --- | --- |
| Fourier transform |  |  |
| frequency-domain view |  |  |
| signal processing |  |  |
| wireless communication |  |  |
| compressed audio: MP3 / AAC |  |  |
| spectral imaging / MRI |  |  |
| discrete cosine transform |  |  |
| block frequency bases |  |  |
| JPEG image compression |  |  |
| video codecs: MPEG / H.26x / AV1 |  |  |
| Laplace transform |  |  |
| transfer functions |  |  |
| stability and control |  |  |
| feedback controllers |  |  |
| brushless motor control |  |  |
| flight / robotics stability |  |  |
| state-space models |  |  |
| neural SSMs: S4 / Mamba |  |  |
| neural networks |  |  |
| embeddings |  |  |
| transformer sequence models |  |  |
| large language models |  |  |
| contrastive multimodal spaces |  |  |
| autoencoders / GANs |  |  |
| neural codecs: EnCodec |  |  |
| discrete audio tokens |  |  |
| speech / audio agents |  |  |
| multimodal tools |  |  |
| software as formal representation |  |  |
| autonomous code agents |  |  |
| research assistants |  |  |
| classical expert systems |  |  |
| blackboard architectures |  |  |
| SMT / Dafny / proof tools |  |  |
| V&V / evidence systems |  |  |
| reliable agent workflows |  |  |
| transform-native organizations |  |  |
| self-inhabiting compute |  |  |
| autonomous experiment loops |  |  |
| discrete-event world models |  |  |
| closed-loop R&D |  |  |

## Edge Review

| Edge | Tag | Comment |
| --- | --- | --- |
| Fourier -> frequency-domain view -> signal processing |  |  |
| signal processing -> wireless communication |  |  |
| signal processing -> compressed audio |  |  |
| signal processing -> spectral imaging / MRI |  |  |
| DCT -> block frequency bases -> JPEG / video codecs |  |  |
| Laplace -> transfer functions -> stability and control |  |  |
| stability/control -> feedback controllers -> motor control / flight robotics |  |  |
| stability/control -> state-space models -> neural SSMs |  |  |
| neural networks -> embeddings -> transformers -> LLMs |  |  |
| neural networks -> contrastive multimodal spaces -> multimodal tools |  |  |
| neural networks -> autoencoders/GANs -> neural codecs -> audio tokens -> speech agents |  |  |
| transformer sequence models -> neural SSMs |  |  |
| neural SSMs -> LLMs |  |  |
| LLMs -> code agents / research assistants |  |  |
| code agents + formal verifiers + blackboard architectures -> V&V systems |  |  |
| V&V systems -> reliable agent workflows |  |  |
| reliable workflows / code agents / research assistants -> frontier layer |  |  |
| reliable workflows + multimodal tools + research assistants -> autonomous experiment loops |  |  |
| autonomous experiment loops -> discrete-event world models -> closed-loop R&D |  |  |
