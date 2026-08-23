---
permalink: /
title: "Fan Yuan"
author_profile: true
---

# About Me

I am Fan Yuan, an Artificial Intelligence student at Zhejiang University (2026–2029). My research interests center on intelligent agents, large language models, and reinforcement learning.

I am especially interested in reasoning with multimodal language models, including visual mathematical reasoning and the design of capable learning systems.

## Research Interests

<ul class="research-interests" aria-label="Research interests">
  <li>AI Agents</li>
  <li>OPD</li>
  <li>Large Language Models</li>
  <li>Reinforcement Learning</li>
</ul>

## Selected Publications

{% assign sorted_publications = site.publications | sort: "date" | reverse %}
<div class="publication-list">
  {% for publication in sorted_publications %}
    {% include publication-card.html publication=publication %}
  {% endfor %}
</div>
